import React from 'react';
import * as APIKEYS from './apiKeys';
import firebase from 'firebase'
import { Image, Button, Form, Col, Navbar } from 'react-bootstrap';
import './App.css';
import uuidv4 from 'uuid/v4';

const config = {
  apiKey: APIKEYS.apiKey,
  authDomain: APIKEYS.authDomain,
  databaseURL: APIKEYS.databaseURL,
  projectId: APIKEYS.projectId,
  storageBucket: APIKEYS.storageBucket,
  messagingSenderId: APIKEYS.messagingSenderId,
}

class App extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      file: null,
      intruder: true,
    }
    this.handleChange = this.handleChange.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
    this.setAuthorized = this.setAuthorized.bind(this)
    this.setIntruder = this.setIntruder.bind(this)
    this.onChange = this.onChange.bind(this)
    this.uploadIntruderImageToStorage = this.uploadIntruderImageToStorage.bind(this)
    this.uploadAuthorizedImageToStorage = this.uploadAuthorizedImageToStorage.bind(this)
    firebase.initializeApp(config);
    this.db = firebase.database();
    this.storageRef = firebase.storage().ref();
  }

  uploadIntruderImageToStorage = (image) => {
    let id = uuidv4();
    let fileType = image.type.toString().replace("image/", ".").replace("jpeg", "jpg");
    return this.storageRef.child(id + fileType).put(image)
      .then(() => {
        this.db.ref('/intruders/').push({
          imageId: id + fileType
        });
        console.log(`"${id} Uploaded Successfully`);
      })
  }

  uploadAuthorizedImageToStorage = (image) => {
    let id = uuidv4();
    let fileType = image.type.toString().replace("image/", ".").replace("jpeg", "jpg");
    return this.storageRef.child(id + fileType).put(image)
      .then(() => {
        this.db.ref('/authorized/').push({
          imageId: id + fileType,
          name: this.state.name
        });
        console.log(`"${id} Uploaded Successfully`);
      })
  }

  onChange(event) {
    this.setState({
      ...this.state,
      [event.target.name]: event.target.value
    });
  }

  setIntruder() {
    this.setState({
      ...this.state,
      intruder: true,
      name: undefined
    });
  }

  setAuthorized() {
    this.setState({
      ...this.state,
      intruder: false
    });
  }

  handleChange(event) {
    try {
      this.setState({
        ...this.state,
        file: URL.createObjectURL(event.target.files[0]),
        rawFile: event.target.files[0]
      })
    } catch (error) {
      console.log(error)
    }
  }

  handleSubmit() {
    if (this.state.intruder) {
      this.uploadIntruderImageToStorage(this.state.rawFile);
    } else {
      this.uploadAuthorizedImageToStorage(this.state.rawFile);
    }
    alert("File Uploaded Successfully");
    this.setState({
      ...this.state,
      complete: true
    });
  }

  handleRefresh = () => {
    window.location.reload();
  }

  render() {
    return (
      <div className="App">
        <Navbar bg="dark" variant="dark">
          <Navbar.Brand>
            <img
              alt=""
              src="https://lh3.googleusercontent.com/proxy/ylJBSBoT_JuxQiIYNL2APbpiyYMYyyTx_oC7BPLRG2XOkIcEFqwElR_evK61A17zUN0dbbIZidkYgQ6WYiZtUKcMLzfwdvqRx-UXpI-_-iW6A-1CmA"
              width="25"
              height="30"
              className="d-inline-block align-top"
            />{' '}Secure Spaces
              </Navbar.Brand>
        </Navbar>
        <Image src={this.state.file} thumbnail />
        <Form>
          <Col>
            <br />
            <Image className='upload' src={"https://image.freepik.com/free-icon/upload-document_318-8461.jpg"} />
            <br />
            <Button disabled={this.state.complete} variant="dark">
              <input type="file" onChange={this.handleChange} name="file" id="file" class="inputfile" />
              <label for="file">Upload Image</label>
            </Button>
            <hr />
            <Button disabled={this.state.complete} onClick={this.setIntruder} variant={this.state.intruder ? "danger" : "outline-danger"}>Intruder</Button>
            <Button disabled={this.state.complete} onClick={this.setAuthorized} variant={this.state.intruder ? "outline-success" : "success"}>Authorized</Button>
            <Form.Group>
              {!this.state.intruder ? <div>
                <br />
                <Form.Control onChange={this.onChange} name="name" placeholder="Name" value={this.state.name} />
              </div> : null}
            </Form.Group>
            <hr />
            {!this.state.complete ?
              <Button onClick={this.handleSubmit} variant="dark" size="lg" disabled={!this.state.file || (!this.state.name && !this.state.intruder) ? true : false}>Submit</Button>
              :
              <Button onClick={this.handleRefresh} variant="dark" size="lg">Reload</Button>
            }
          </Col>
        </Form>
      </div >
    );
  }
}

export default App;
