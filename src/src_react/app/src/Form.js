import {Buffer} from 'buffer';
import React from 'react';
import ReactHtmlParser from 'react-html-parser'; 
import './Form.css';

export default class Form extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        lang: "java",
        code: "",
        result: "",
        error: ""
      };
  
      this.handleInputChange = this.handleInputChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }
  
    handleInputChange(event) {
      this.setState({
        [event.target.name]: event.target.value
      });
    }

    handleSubmit(event) {
      event.preventDefault();

      var formdata = new FormData();
      formdata.append("lang", this.state.lang);

      let buff = new Buffer(this.state.code);
      let base64datacode = buff.toString('base64');
      formdata.append("code", base64datacode);

      var requestOptions = {
        method: 'POST',
        body: formdata,
        redirect: 'follow'
      };

      let url = '';
      if( url.indexOf('localhost') !== -1 || url.indexOf('127.0.0.1') !== -1){
        url = "http://localhost:8089/api/v1/highlight";
      }
      else{
        url = "https://ase-service-1.iugkfeabdb168.eu-central-1.cs.amazonlightsail.com/api/v1/highlight";
      }

      fetch(
        url,
        requestOptions)
        .then(response => response.json())
        .then(response => Buffer.from(response.resp, "base64").toString())
        .then(result => this.setState({result: result}))
        .catch(error => this.setState({error: error.message}));
    }
  
    render() {
      return (
        <div className = "form-box">
          <h5>Code Syntax Highlighter</h5>
          <div> {this.state.error && <h3 className = "error">{this.state.error}</h3>} </div>
          <form onSubmit = {this.handleSubmit}>
            <label>
              Language:
              <select name = "lang" value = {this.state.lang} onChange = {this.handleInputChange}>
                <option value = "java">Java</option>
                <option value = "kotlin">Kotlin</option>
                <option value = "python">Python</option>
              </select>
            </label>
            <br />
            <label>
              Code:
              <textarea
                name = "code"
                value = {this.state.code}
                onChange = {this.handleInputChange} />
            </label>
            <input className = "submit" type = "submit" value = "Submit" />
          </form>
          <div>
          <label>
            Result:
            <div className = "result">
              { ReactHtmlParser (this.state.result) }
            </div>
            <textarea readOnly value = { this.state.result } />
          </label>
        </div>
        </div>
      );
    }
  }