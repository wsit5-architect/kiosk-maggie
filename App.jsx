import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import React, { useState, useEffect } from 'react';
import KioskPane from './components/KioskPane';
import TelemetryPane from './components/TelemetryPane';
import './index.css';
function App() {
  const [count, setCount] = useState(0)
  const [logs, setLogs] = useState([]);
  return (
    <>
      <section id="center">
        <div className="hero">
          <img src={heroImg} className="base" width="170" height="179" alt="" />
          <img src={reactLogo} className="framework" alt="React logo" />
          <img src={viteLogo} className="vite" alt="Vite logo" />
        </div>
        <div>
          <h1>Get started</h1>
          <p>
            Edit <code>src/App.jsx</code> and save to test <code>HMR</code>
          </p>
        </div>
        <button
          type="button"
          className="counter"
          onClick={() => setCount((count) => count + 1)}
        >
          Count is {count}
        </button>
      </section>
  useEffect(() => {
    // Connect to WebSocket on the backend
    const ws = new WebSocket('ws://localhost:8000/ws/telemetry');
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setLogs((prev) => [...prev, data].slice(-20)); // Keep last 20 logs
    };
      <div className="ticks"></div>
    return () => ws.close();
  }, []);
      <section id="next-steps">
        <div id="docs">
          <svg className="icon" role="presentation" aria-hidden="true">
            <use href="/icons.svg#documentation-icon"></use>
          </svg>
          <h2>Documentation</h2>
          <p>Your questions, answered</p>
          <ul>
            <li>
              <a href="https://vite.dev/" target="_blank">
                <img className="logo" src={viteLogo} alt="" />
                Explore Vite
              </a>
            </li>
            <li>
              <a href="https://react.dev/" target="_blank">
                <img className="button-icon" src={reactLogo} alt="" />
                Learn more
              </a>
            </li>
          </ul>
  const handleSimulateTrigger = async (text) => {
    try {
      await fetch('http://localhost:8000/trigger_intent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });
    } catch (err) {
      console.error("Error triggering intent", err);
    }
  };
  const handleConnectRobot = async () => {
    try {
      const res = await fetch('http://localhost:8001/connect_robot', { method: 'POST' });
      const data = await res.json();
      if (data.status === 'success') {
        alert("Success: Connected to Maggie!");
      } else {
        alert("Error: " + data.message + "\n\nDid you run 'reachy-mini-daemon' in the terminal?");
      }
    } catch (err) {
      alert("Error: Backend not running.");
    }
  };
  const handleDisconnectRobot = async () => {
    try {
      const res = await fetch('http://localhost:8001/disconnect_robot', { method: 'POST' });
      const data = await res.json();
      if (data.status === 'success') {
        alert("Maggie is turned off and resting.");
      } else {
        alert("Error: " + data.message);
      }
    } catch (err) {
      alert("Error: Backend not running.");
    }
  };
  return (
    <div className="app-container">
      <div className="split-pane">
        <div className="pane-left">
          <KioskPane onTrigger={handleSimulateTrigger} onConnect={handleConnectRobot} onDisconnect={handleDisconnectRobot} />
        </div>
        <div id="social">
          <svg className="icon" role="presentation" aria-hidden="true">
            <use href="/icons.svg#social-icon"></use>
          </svg>
          <h2>Connect with us</h2>
          <p>Join the Vite community</p>
          <ul>
            <li>
              <a href="https://github.com/vitejs/vite" target="_blank">
                <svg
                  className="button-icon"
                  role="presentation"
                  aria-hidden="true"
                >
                  <use href="/icons.svg#github-icon"></use>
                </svg>
                GitHub
              </a>
            </li>
            <li>
              <a href="https://chat.vite.dev/" target="_blank">
                <svg
                  className="button-icon"
                  role="presentation"
                  aria-hidden="true"
                >
                  <use href="/icons.svg#discord-icon"></use>
                </svg>
                Discord
              </a>
            </li>
            <li>
              <a href="https://x.com/vite_js" target="_blank">
                <svg
                  className="button-icon"
                  role="presentation"
                  aria-hidden="true"
                >
                  <use href="/icons.svg#x-icon"></use>
                </svg>
                X.com
              </a>
            </li>
            <li>
              <a href="https://bsky.app/profile/vite.dev" target="_blank">
                <svg
                  className="button-icon"
                  role="presentation"
                  aria-hidden="true"
                >
                  <use href="/icons.svg#bluesky-icon"></use>
                </svg>
                Bluesky
              </a>
            </li>
          </ul>
        <div className="pane-right">
          <TelemetryPane logs={logs} />
        </div>
      </section>
      <div className="ticks"></div>
      <section id="spacer"></section>
    </>
  )
      </div>
    </div>
  );
}
export default App
export default App;
