from census import Census
from us_counties import us
from flask import Flask, request, send_from_directory, abort
import os
import threading
from numpy import random

# start this server from the root '\Covid-Tracker' directory
os.chdir(os.path.dirname(os.path.realpath(__file__)).replace("\src\middleend", ""))
dir_path = os.getcwd() + '\\src\\frontend\\covid-interface\\build' # path to react build dir

###
#import sys
#sys.path.append('.\\src\\backend\\')
#import regression
###


app = Flask(__name__)
key = "dd5ee110bc1dbb9e53eab3790d804f59014e006d"
c = Census(key)

userState = None
userCounty = None
userLevel = None
userPopulation = -1
userArea = -1




## census utilities ##
def get_population(state, county):
    q = c.acs5.state_county(('NAME', 'B01003_001E'), state.fips, county.fips) # total population for county
    return int(q[0]['B01003_001E'])

def set_population(state, county):
    global userPopulation, userCounty, userState
    userCounty = county
    userState = state
    userPopulation = get_population(userState, userCounty)
    return

def get_area(state, county):
    q = c.sf3.state_county(('AREALAND'), state.fips, county.fips)
    return (int(q[0]['AREALAND']) / 2589988)

def set_area(state, county):
    global userArea
    userArea = get_area(state, county)
    return

def set_density():
    return userPopulation / userArea


## routing
@app.route('/')
def connect():
    return send_from_directory('{}\\'.format(dir_path), 'index.html')

@app.route('/static/css/<path:filename>')
def serveCSS(filename):
    return send_from_directory('{}\\static\\css\\'.format(dir_path), filename)

@app.route('/static/js/<path:filename>')
def serveJS(filename):
    return send_from_directory('{}\\static\\js\\'.format(dir_path), filename)

@app.route('/submit/<string:state>/<string:county>', methods=['POST'])
def getUserData(state, county):
    # lookup county data on different threads
    try:
        userState = us.states.lookup(state)
        userCounty = [x for x in us.counties.lookup(county) if x.state == userState][0]

        nt = threading.Thread(target=set_population, args=(userState, userCounty))
        nt.start()

        nt = threading.Thread(target=set_area, args=(userState, userCounty))
        nt.start()
        return "recieved"
    except:
        abort(404)


@app.route('/fetch/<string:level>', methods=['GET'])
def sendJSON(level):
    global userLevel, userPopulation
    userPopulation = set_density()
    userLevel = level

    if userLevel != '' and userPopulation != -1:
        userLevel = level

        # generate dummy y-vals
        infection_data = random.randint(1,101, 100)

        o = {
            'type': 'line',
            'series': [{'values': infection_data.tolist()}]
            }
    else:
        abort(404)
    return o



def main():
    global userCounty, userState, userLevel, userArea
    '''
    user_state = 'IL'
    user_county = 'Cook'
    st = us.states.lookup(user_state)
    co = [x for x in us.counties.lookup(user_county) if x.state == st][0]
    combined = str('{}{}'.format(st.fips, co.fips))
    print(get_population(st, co))
    '''

    app.run()
    
main()