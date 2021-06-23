import React, { useState } from 'react';
import io from "socket.io-client";
import toggle from './toggle.png';
import './App.css';

let endpoint = 'http://localhost:5000/';
let socket = io.connect(endpoint);

const App = () => {
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState("");

  socket.on("message", msg => {
    if(typeof msg === "number" || typeof msg === "string"){
      setMessages([...messages, msg])
    }; 
    
    if(typeof msg === "boolean") {
      setMessages([...messages, msg.toString()]);
    };

    if(typeof msg === "object") {
      setMessages([...messages, JSON.stringify(msg)]);
    };
  });  

  const onChange = (event) => {
    setMessage(event.target.value);
  };

  const onClick = () => {
    socket.emit("message", message);
    setMessage("");
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>
          Welcome to Space Camp!
        </h1>
        <img src={toggle} className="App-logo" alt="logo" />
      <div className="messages">
        {messages.map(msg => (<p>User ID: <span className="userId">{msg.split("-")[0]}</span> <br /> Variation: <span className="variation">{msg.split("-")[1]}</span></p>))}
      </div>
      <p>
        <input type="text" placeholder="Enter User ID" onChange={onChange} value={message} />
        <input type="button" onClick={onClick} value="Send"/>
      </p>
      </header>
    </div>
  );
};

export default App;