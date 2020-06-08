import React from 'react';
import ReactDOM from 'react-dom';
import Chart from './chart';

class CovidForm extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        levelDistancing: '',
        countyName: '',
        stateName: '',
        area: '',
        isLoaded : false
      };
  
      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }
  
    handleChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;
    
        this.setState({
          [name]: value
        });
      }
    
    handleSubmit(event) {
        event.preventDefault();
        if (this.state.countyName !== '' && this.state.countyName !== ''){
          console.log('Submitted');
          fetch(`submit/${this.state.stateName}/${this.state.countyName}`, {
              method: "POST", // *GET, POST, PUT, DELETE, etc.
              mode: "cors", // no-cors, cors, *same-origin
              cache: "no-cache",
              credentials: "same-origin",
              headers: {
                  "Content-Type": "text/plain",
              },
              redirect: "follow", 
              referrer: "no-referrer",
              body: '', 
          }).then(
            (result) => 
              {
                if (result.status === 200) { this.setState({isLoaded : true, area: this.state.countyName}) }
                else { alert("Input not recognized") }
              }
            )
          }
        }
      
  
    render() {
      return (
        <div>
        <div id='input-container'>
        <form onSubmit={this.handleSubmit}>
          <label>
            <b>County:&nbsp;</b>
            <input
              name="countyName"
              type="text"
              value={this.state.countyName}
              onChange={this.handleChange} />
          </label>
          <br/>
          <label>
            <b>State:&nbsp;</b>
                <select name="stateName" value={this.state.stateName} onChange={this.handleChange}>
                    <option value=""></option>
                    <option value="AL">Alabama</option>
                    <option value="AK">Alaska</option>
                    <option value="AZ">Arizona</option>
                    <option value="AR">Arkansas</option>
                    <option value="CA">California</option>
                    <option value="CO">Colorado</option>
                    <option value="CT">Connecticut</option>
                    <option value="DE">Delaware</option>
                    <option value="DC">District Of Columbia</option>
                    <option value="FL">Florida</option>
                    <option value="GA">Georgia</option>
                    <option value="HI">Hawaii</option>
                    <option value="ID">Idaho</option>
                    <option value="IL">Illinois</option>
                    <option value="IN">Indiana</option>
                    <option value="IA">Iowa</option>
                    <option value="KS">Kansas</option>
                    <option value="KY">Kentucky</option>
                    <option value="LA">Louisiana</option>
                    <option value="ME">Maine</option>
                    <option value="MD">Maryland</option>
                    <option value="MA">Massachusetts</option>
                    <option value="MI">Michigan</option>
                    <option value="MN">Minnesota</option>
                    <option value="MS">Mississippi</option>
                    <option value="MO">Missouri</option>
                    <option value="MT">Montana</option>
                    <option value="NE">Nebraska</option>
                    <option value="NV">Nevada</option>
                    <option value="NH">New Hampshire</option>
                    <option value="NJ">New Jersey</option>
                    <option value="NM">New Mexico</option>
                    <option value="NY">New York</option>
                    <option value="NC">North Carolina</option>
                    <option value="ND">North Dakota</option>
                    <option value="OH">Ohio</option>
                    <option value="OK">Oklahoma</option>
                    <option value="OR">Oregon</option>
                    <option value="PA">Pennsylvania</option>
                    <option value="RI">Rhode Island</option>
                    <option value="SC">South Carolina</option>
                    <option value="SD">South Dakota</option>
                    <option value="TN">Tennessee</option>
                    <option value="TX">Texas</option>
                    <option value="UT">Utah</option>
                    <option value="VT">Vermont</option>
                    <option value="VA">Virginia</option>
                    <option value="WA">Washington</option>
                    <option value="WV">West Virginia</option>
                    <option value="WI">Wisconsin</option>
                    <option value="WY">Wyoming</option>
                </select>
          </label>
          <br/>
          <input id='submit' type="submit" value="Submit" />
        </form>
        </div>
        <Chart display={this.state.isLoaded} area={this.state.area}/>
        </div>
        
      );
    }
  }
  
  ReactDOM.render(
    <CovidForm />,
    document.getElementById('root')
  );

  export default CovidForm;
  