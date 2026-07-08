Overview





import React from 'react';
import '../index.css';
function KioskPane({ onTrigger, onConnect, onDisconnect }) {
  return (
    <div className="kiosk-pane glass-panel" style={{ position: 'relative' }}>
      <div className="kiosk-header">
        <h1>Hello, I'm Maggie</h1>
        <p>Your IT Service Desk Assistant at George Fox University</p>
      </div>
      
      <div className="kiosk-content">
        <div className="status-indicator">
          <div className="pulse-ring"></div>
          <p>Listening for "Maggie"...</p>
        </div>
        
        <div className="instructions">
          <h3>How I can help:</h3>
          <ul>
            <li>File an IT ticket</li>
            <li>Look up internal wiki info</li>
            <li>Answer campus questions</li>
            <li>Capture your ID photo</li>
          </ul>
        </div>
        
        <button className="simulate-btn" onClick={() => onTrigger('I need a new ID card photo.')}>
          Simulate: "I need a new ID card"
        </button>
      </div>
      {/* Floating Bottom Left Connect Button */}
      <div style={{ position: 'absolute', bottom: '20px', left: '20px', textAlign: 'left', zIndex: 100 }}>
        <div style={{ display: 'flex', gap: '10px', marginBottom: '5px' }}>
          <button className="simulate-btn" style={{ background: '#10b981', margin: 0, padding: '10px 15px' }} onClick={onConnect}>
            🔌 Connect to Maggie
          </button>
          <button className="simulate-btn" style={{ background: '#ef4444', margin: 0, padding: '10px 15px' }} onClick={onDisconnect}>
            💤 Turn Off
          </button>
        </div>
        <p style={{ fontSize: '0.75rem', color: '#f87171', margin: 0, maxWidth: '250px', background: 'rgba(0,0,0,0.5)', padding: '5px', borderRadius: '4px' }}>
          ⚠️ Start <code>reachy-mini-daemon</code> before connect!
        </p>
      </div>
    </div>
  );
}
export default KioskPane;
