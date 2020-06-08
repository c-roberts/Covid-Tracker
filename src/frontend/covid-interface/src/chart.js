import ZingChart from 'zingchart-react';
import React from 'react';

class Chart extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        levelDistancing: '',
        area: props.area,
        display: props.display,
        config: {
          type: 'line',
          nearest: null,
          'scale-x': { format: "Day %v" },
          series: [{values: [0,0,0,0,0,0,0,0]}]
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
        if(this.state.area !== this.props.area){
          this.setState({
              area: (this.props.area),
              levelDistancing: '',
              config: {
                type: 'line',
                nearest: null,
                'scale-x': { format: "Day %v" },
                series: [{values: [0,0,0,0,0,0,0,0]}]
              }
            }
          )
      }
    }


    render() {
        let n;
        let pair;
        let f_string;
        if (this.state.config.nearest) { 
          pair = this.state.config.nearest.split("-")
          f_string = `${pair[1]}, ${pair[0]}`
          n = <div>This county is most similar to <b>{f_string}</b></div>
        }
        else { n = <div><br/></div>}
        if (!this.state.display) { return (<div/>);}

        else { 
            return (
                <div id='output-container'>
                    <form>
                      <label>
                        <b>Level of Social Distancing:&nbsp;</b>
                        <select name="levelDistancing" value={this.state.levelDistancing} onChange={this.handleChange}>
                          <option value=""></option>
                          <option value="low">Low</option>
                          <option value="medium">Moderate</option>
                          <option value="high">High</option>
                          <option value="compare">Compare</option>
                      </select>
                    </label>
                  </form>
                  {n}
                  <br/>
                  <ZingChart data={this.state.config}/>
                </div>
              );
    }

    }
  }

  export default Chart;