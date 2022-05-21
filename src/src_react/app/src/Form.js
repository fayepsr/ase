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
      mode: 'html',
      result: '',
      error: '',
    };

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.sendRequest = this.sendRequest.bind(this);
  }

  handleInputChange(event) {
    let name = event.target.name;
    let value = event.target.value;
    this.setState({ [name]: value });
  }

  handleSubmit(event) {
    event.preventDefault();

    this.setState({ result: '', error: '' }, () => {
      var formdata = new FormData();
      formdata.append('lang', this.state.lang);
      formdata.append('code', Buffer.from(this.state.code).toString('base64'));
      formdata.append('secret', process.env.REACT_APP_API_KEY);
      formdata.append('mode', this.state.mode);
      this.sendRequest(formdata);
    });
  }

  sendRequest(formdata) {
    var requestOptions = {
      method: 'POST',
      body: formdata,
      redirect: 'follow',
    };

    fetch(process.env.REACT_APP_API_URL, requestOptions)
      .then((response) => {
        if (response.ok) return response.json();
        return response.text().then((text) => {
          throw new Error(text);
        });
      })
      .then((response) => {
        if (this.state.mode === 'json') return JSON.stringify(response);
        return Buffer.from(response.resp, 'base64').toString();
      })
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
          <div>
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
          </div>
          <div>
            <label>
              Code:
              <textarea
                name="code"
                value={this.state.code}
                onChange={this.handleInputChange}
              />
            </label>
          </div>
          <div>
            <label>
              Result format:
              <label>
                <input
                  type="radio"
                  name="mode"
                  value="html"
                  checked={this.state.mode === 'html'}
                  onClick={this.handleInputChange}
                />
                HTML
              </label>
              <label>
                <input
                  type="radio"
                  name="mode"
                  value="json"
                  checked={this.state.mode === 'json'}
                  onClick={this.handleInputChange}
                />
                JSON
              </label>
            </label>
          </div>
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
