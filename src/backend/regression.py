import utils
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import scale
from sklearn.linear_model import LinearRegression

from pprint import pprint

# set working directory to be current
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)


class CovidRegression:
    def __init__(self):
        self.query = "SELECT cases_date, county_state, county_name, cases FROM covid_county_cases"
        self.data = utils.query_data(self.query)
        self.values = {'low': {}, 'medium': {}, 'high': {}}
        self.cases = None
        self.mobility = None
        self.k = 10

    def sanitize(self):
        for i in range(0, len(self.data), 1):
            d = self.data[i]
            self.data[i] = (d[0], d[1].replace(" ", "_"), d[2].replace(" ", "_"))

    def process_cases_over_time(self):
        data_dict = {}

        for d in self.data:
            if 'county' in self.query:
                name = d[1] + '-' + d[2]

            # elif 'state' in self.query:
            #     name = d[1]
            else:
                raise Exception("invalid query")
            name = name.replace(" ", "_")
            if name in data_dict:
                start = data_dict[name]['start_date']
                end = d[0]
                delta = end - start
                data_dict[name]['days'].append(delta.days + 1)
                data_dict[name]['cases'].append(d[-1])
            else:
                data_dict[name] = {'days': [1], 'cases': [d[-1]], 'start_date': d[0]}

        self.cases = data_dict

    # process k nearest neighbors and their corresponding mobility scores into self.mobility
    def process_mobility_scores(self, pop, den):
        self.cases = self.cases

        if 'county' in self.query:
            population_data = utils.query_data("SELECT state, county, area_km2, population FROM counties_area_pop")

            densities = np.array([pop[3] for pop in population_data]) / np.array([pop[2] for pop in population_data])
            populations = [pop[3] for pop in population_data]

            z_scores = (scale(np.array(densities)) + scale(np.array(populations))) / 2.0
            standardized = list(zip([pop[0] + '-' + pop[1] for pop in population_data], z_scores))
        # elif 'state' in self.query:
        #     population_data = pd.read_csv('nst-est2019-alldata.csv')
        #     # 5th column contains state names, 17th column contains population count
        #     populations = list(zip(population_data.iloc[:, 4].values, population_data.iloc[:, 16].values))
        else:
            raise Exception("invalid query")

        sorted_populations = sorted(standardized, key=lambda x: x[1])

        # standardize
        std_pop = (pop - np.mean(np.array(populations))) / np.std(np.array(populations))
        std_den = (den - np.mean(np.array(densities))) / np.std(np.array(densities))
        std_score = (std_pop + std_den) / 2
        # print("STANDARD SCORES:", std_pop, std_den, std_score)

        # knn
        county = utils.binary_search_tuples(sorted_populations, std_score)[0]
        ind = [p[0] for p in sorted_populations].index(county)
        nearest_neighbor_tuples = sorted_populations[ind - int(self.k/2) : ind + int(self.k/2)]
        nearest_neighbors = [tup[0] for tup in nearest_neighbor_tuples]

        start_date = '3/1/20'
        end_date = '6/1/20'
        mobility_scores = utils.get_mobility_data(start_date, end_date)
        mobility_scores_nn = [(n, mobility_scores[n]) for n in nearest_neighbors if n in mobility_scores]

        self.mobility = sorted(mobility_scores_nn, key=lambda x: x[1])

    def process_plot_values(self, num, x, y):
        sd_lvls = ['low', 'medium', 'high']

        #t = 'Number of Cases Over Time - {} Social Distancing'
        #t = t.format(sd_lvls[num - 1].capitalize())

        self.values[sd_lvls[num - 1]]['x'] = x
        self.values[sd_lvls[num - 1]]['y'] = y

        #plt.title(t)

    def create_plot(self, lvl, plt_num):
        days = np.array(self.cases[lvl]['days'])
        x = days.reshape(-1, 1)
        y = np.array(self.cases[lvl]['cases'])

        poly_reg = PolynomialFeatures(degree=3)
        x_poly = poly_reg.fit_transform(x)
        pol_reg = LinearRegression()
        pol_reg.fit(x_poly, y)

        plot = plt.figure(plt_num)
        plt.scatter(x, y, color='red')
        plt.plot(x, pol_reg.predict(poly_reg.fit_transform(x)), color='blue')

        self.process_plot_values(plt_num, days, y)

        plt.xlabel('Time (days)')
        plt.ylabel('Number of Cases')

        print("\nThe spread of COVID-19 in your region will be similar to that of", lvl)

        print("Regression function coefficients for figure", plt_num)
        return pol_reg.coef_

    def visualize(self):
        # counties representing each lvl of social distancing
        low = self.mobility[-1][0]
        med = self.mobility[int(self.k/2)-1][0]
        high = self.mobility[0][0]

        self.create_plot(low, 1)
        self.create_plot(med, 2)
        self.create_plot(high, 3)

        plt.show()

    def get_values(self, level):
        # counties representing each lvl of social distancing
        if level == 'low':
            kn = self.mobility[-1][0]
            n = 1
        elif level == 'medium':
            kn = self.mobility[int(self.k/2)-1][0]
            n = 2
        elif level == 'high':
            kn = self.mobility[0][0]
            n = 3

        kn = kn.replace(" ", "_")
        if kn == 'New_York-New_York':
            kn = 'New_York-New_York_City'

        days = np.array(self.cases[kn]['days'])
        x = days.reshape(-1, 1)
        y = np.array(self.cases[kn]['cases'])

        poly_reg = PolynomialFeatures(degree=3)
        x_poly = poly_reg.fit_transform(x)
        pol_reg = LinearRegression()
        pol_reg.fit(x_poly, y)

        self.process_plot_values(n, days, y)

        return

'''
model = CovidRegression()
model.process_cases_over_time()

population = 200000
density = 500

model = CovidRegression()
model.process_cases_over_time()
model.process_mobility_scores(population, density)
#input(model.get_values("low"))
model.visualize()

x_low = model.values['low']['x']
y_low = model.values['low']['y']
x_medium = model.values['medium']['x']
y_medium = model.values['medium']['y']
x_high = model.values['high']['x']
y_high = model.values['high']['y']
'''

