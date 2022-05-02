import { Buffer } from 'buffer';
import React from 'react';
import ReactHtmlParser from 'react-html-parser';
import './Form.css';

export default class Form extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      lang: 'java',
      code: '',
      result: '',
      error: '',
    };

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleInputChange(event) {
    this.setState({
      [event.target.name]: event.target.value,
    });
  }

  handleSubmit(event) {
    event.preventDefault();

    this.setState({ result: '' });
    this.setState({ error: '' });

    var formdata = new FormData();
    formdata.append('lang', this.state.lang);
    formdata.append('code', Buffer.from(this.state.code).toString('base64'));
    formdata.append('secret', "hsdiwu8&%$$");

    var requestOptions = {
      method: 'POST',
      body: formdata,
      redirect: 'follow',
    };

    let url_highlight = '';
    let url = window.location.href;
    if (url.indexOf('localhost') !== -1 || url.indexOf('127.0.0.1') !== -1) {
      url_highlight = 'http://localhost:8089/api/v1/highlight';
    } else {
      url_highlight =
        'https://ase-service-1.iugkfeabdb168.eu-central-1.cs.amazonlightsail.com/api/v1/highlight';
    }

    fetch(url_highlight, requestOptions)
      .then((response) => {
        if (response.ok) return response.json();
        return response.text().then((text) => {
          throw new Error(text);
        });
      })
      .then((response) => Buffer.from(response.resp, 'base64').toString())
      .then((result) => this.setState({ result: result }))
      .catch((error) =>
        this.setState({
          error: error.message.replace(/"|{|}/g, '').split('msg:')[1],
        })
      );
  }

  render() {
    return (
      <div className="form-box">
        <h5>Code Syntax Highlighter</h5>
        <div>
          {' '}
          {this.state.error && (
            <h3 data-testid="error" className="error">
              {ReactHtmlParser(this.state.error)}
            </h3>
          )}
        </div>
        <form onSubmit={this.handleSubmit}>
          <label>
            Language:
            <select
              name="lang"
              value={this.state.lang}
              onChange={this.handleInputChange}
            >
              <option value="java">Java</option>
              <option value="kotlin">Kotlin</option>
              <option value="python">Python</option>
            </select>
          </label>
          <br />
          <label>
            Code:
            <textarea
              name="code"
              value={this.state.code}
              onChange={this.handleInputChange}
            />
          </label>
          <input className="submit" type="submit" value="Submit" />
        </form>
        <div>
          {this.state.result && (
            <label>
              Result:
              <div className="result">{ReactHtmlParser(this.state.result)}</div>
              <textarea
                readOnly
                data-testid="result"
                value={this.state.result}
              />
            </label>
          )}
        </div>
      </div>
    );
  }
}
