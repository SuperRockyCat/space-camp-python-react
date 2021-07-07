import React, { useState, useRef, useEffect } from 'react';
import io from "socket.io-client";
import toggle from './toggle.png';
import './App.css';

let endpoint = 'http://localhost:5000/';
let socket = io.connect(endpoint);

const App = () => {
  const [messages, setMessages] = useState(["-"]);
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

  const AlwaysScrollToBottom = () => {
    const elementRef = useRef();
    useEffect(() => elementRef.current.scrollIntoView());
    return <div ref={elementRef} />;
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>
          Welcome to Space Camp!
        </h1>
        <div className={messages[messages.length - 1].split("-")[1].toLowerCase()}>
          <div className="App-logo">
            <img src={toggle} alt="logo" />
          </div>
        </div>
      <div className="messages">
        {messages.map(msg => (msg.split("-")[0] === "" ? "" : <p key={new Date().getTime() * Math.random()}>This is <span className="uniqueKey">{msg.split("-")[0]}</span>, and they're flying to <span className={msg.split("-")[1].toLowerCase() +"-text"}>{msg.split("-")[1]}</span></p>))}
        <AlwaysScrollToBottom />
      </div>
      <p>
        <input type="text" placeholder="Enter Key" onChange={onChange} value={message} />
        <input type="button" onClick={onClick} value="Send"/>
      </p>
      </header>
    </div>
  );
};

export default App;