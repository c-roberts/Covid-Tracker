import React from 'react';
import CovidForm from './form';
import './App.css';

function App() {
  return (
  <div>
    <div >
      <CovidForm/>
    </div>
    <div id="pre">
      <p>Levels of <b>social distancing</b>, labeled on our graphs as low, medium, and high, are determined by average mobility 
        scores for the given country over a three-month period.  A county’s mobility score is based on average distances 
        traveled by people living in the given region. Our model’s metric of social distancing is determined by a 
        country’s change in mobility score from the pre-covid average.</p>
      <p>A <b>low</b> level of social distancing refers to behavior where a country’s mobility score exhibits a low amount
        of change between the pre-covid and covid time periods.  This behavior is common in countries that consistently 
        experience low average mobility scores (rural countries), where people may already be socially distant by virtue of
        living in sparsely populated areas. A <b>high</b> level of social distancing refers to behavior where a country’s 
        mobility score exhibits a high amount of change 
        when covid begins affecting the given country.  This behavior is common in countries that consistently experience high 
        average mobility scores, where people have not been socially distant before covid due to living in densely populated urban 
        areas.</p>
      <p>Changes in average mobility scores are partially a consequence of policies instituted by many governments that limit 
        social gatherings and suggest that people remain six feet away from each other.  For example, a country like the United 
        States with many urban centers consistently exhibits high mobility scores before covid, but due in part to social distancing 
        policies created by the U.S. government, average mobility scores have dropped. This behavior indicates a high level of 
        social distancing.</p>
      </div>
  <div>
    
  </div>
  </div>
  );
}

export default App;
