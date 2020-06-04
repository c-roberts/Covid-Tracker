import ZingChart from 'zingchart-react';
import React from 'react';

class Chart extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        levelDistancing: '',
        display: props.display,
        config: {
          type: 'line',
          series: [{
            values: [0,0,0,0,0,0,0,0]
          }]
        }
      }
      this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event) {
        const target = event.target;
        const value = target.value;
    
        this.setState({
            levelDistancing: value
        });
        if (value !== '') {
            fetch(`fetch/${value}`, {
                method: "GET",
                cache: "no-cache",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json",
                },
                redirect: "follow", 
                referrer: "no-referrer",
            }).then(response => response.json()).then(
            (result) => {
                    this.setState({
                        config: result,
                });
            })
          }
      }

      componentDidUpdate(prevProps){
        if(this.state.display !== this.props.display){
            this.setState({
                display: (this.props.display)
            })
        }
    }


    render() {
        if (!this.state.display) { 
            return (<div/>);
        }
        else { 
            return (
                <div id='output-container'>
                    <form>
                        <label>
                        <b>Level of Social Distancing:&nbsp;</b>
                        <select name="levelDistancing" value={this.state.levelDistancing} onChange={this.handleChange}>
                        <option value=""></option>
                        <option value="none">None</option>
                        <option value="low">Low</option>
                        <option value="moderate">Moderate</option>
                        <option value="high">High</option>
                        <option value="lockdown">Lockdown</option>
                    </select>
                    </label>
                  </form>
                  <br/>
                  <br/>
                  <ZingChart data={this.state.config}/>
                </div>
              );
    }

    }
  }

  export default Chart;