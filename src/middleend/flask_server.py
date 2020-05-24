from census import Census
from us_counties import us
from flask import Flask, request, send_from_directory
import os
import threading

app = Flask(__name__)
key = "dd5ee110bc1dbb9e53eab3790d804f59014e006d"
c = Census(key)

userState = None
userCounty = None
userLevel = None

dir_path = os.path.dirname(os.path.realpath(__file__))


## utilities
def get_population(state, county):
    q = c.acs5.state_county(('NAME', 'B01003_001E'), state.fips, county.fips) # total population for county
    return int(q[0]['B01003_001E'])


## routing
@app.route('/')
def connect():
    return send_from_directory('{}\src\\'.format(dir_path), 'index.html')


@app.route('/static/css/<path:filename>')
def serveCSS(filename):
    return send_from_directory('{}\src\\static\\css\\'.format(dir_path), filename)

@app.route('/static/js/<path:filename>')
def serveJS(filename):
    return send_from_directory('{}\src\\static\\js\\'.format(dir_path), filename)


@app.route('/submit/<string:state>/<string:county>/<string:level>', methods=['POST'])
def getUserData(state, county, level):
    global userCounty, userState, userLevel
    
    userState = us.states.lookup(state)
    userCounty = [x for x in us.counties.lookup(county) if x.state == userState][0]
    userLevel = level

    #                                        #
    # look up population on different thread #
    #                                        #

    return 'recieved'



##
def main():
    global userCounty, userState, userLevel
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