import utils
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression


class CovidRegression:
    def __init__(self):
        self.data = utils.query_data("SELECT cases_date, state_name, cases FROM covid_state_cases")

    def get_all_cases_over_time(self):
        data_dict = {}

        for d in self.data:
            state = d[1]
            if state in data_dict:
                start = data_dict[state]['start_date']
                end = d[0]
                delta = end - start
                data_dict[state]['days'].append(delta.days + 1)
                data_dict[state]['cases'].append(d[2])
            else:
                data_dict[state] = {'days': [1], 'cases': [d[2]], 'start_date': d[0]}

        return data_dict


    def plot_cases_over_time(self, pop):
        dictionary = self.get_all_cases_over_time()

        population_data = pd.read_csv('nst-est2019-alldata.csv')
        state_populations = tuple(zip(population_data.iloc[:, 4].values, population_data.iloc[:, 16].values))
        sorted_populations = sorted(state_populations, key=lambda x: x[1])

        state = utils.binary_search_tuples(sorted_populations, pop)[0]

        X = np.array(dictionary[state]['days']).reshape(-1, 1)
        y = np.array(dictionary[state]['cases'])

        poly_reg = PolynomialFeatures(degree=3)
        X_poly = poly_reg.fit_transform(X)
        pol_reg = LinearRegression()
        pol_reg.fit(X_poly, y)

        plt.scatter(X, y, color='red')
        plt.plot(X, pol_reg.predict(poly_reg.fit_transform(X)), color='blue')
        plt.title('Number of Cases Over Time')
        plt.xlabel('Time (days)')
        plt.ylabel('Number of Cases')

        t = 'Given the population parameter of {}, the spread of COVID-19 for your region would be most similar to that of {}.'
        print(t.format(pop, state))

        plt.show()

        return state

population = 2000000
model = CovidRegression()
model.plot_cases_over_time(population)
