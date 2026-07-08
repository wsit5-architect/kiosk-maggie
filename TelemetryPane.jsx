Overview





import React from 'react';
import '../index.css';
function TelemetryPane({ logs }) {
  return (
    <div className="telemetry-pane">
      <div className="telemetry-header">
        <h2>Agent Telemetry Dashboard</h2>
        <div className="live-badge">LIVE</div>
      </div>
      
      <div className="dashboard-grid">
        <div className="dashboard-module glass-panel" style={{ gridColumn: '1 / -1' }}>
          <h3>📸 Live Camera Feed</h3>
          <div style={{ background: '#000', borderRadius: '8px', overflow: 'hidden', display: 'flex', justifyContent: 'center' }}>
            <img 
              src="http://localhost:8001/video_feed" 
              alt="Maggie Live Feed" 
              style={{ width: '100%', maxHeight: '300px', objectFit: 'contain' }}
              onError={(e) => { e.target.style.display = 'none'; }}
            />
          </div>
        </div>
        
        <div className="dashboard-module glass-panel">
          <h3>1. Agents Working</h3>
          <ul className="agent-list">
            <li className="active-agent"><span className="dot pulse"></span> MAGGIE_LISTEN_AGENT</li>
            <li><span className="dot"></span> GET_PROCESS_AGENT</li>
            <li><span className="dot"></span> ORCHESTRATOR_AGENT</li>
          </ul>
        </div>
        
        <div className="dashboard-module glass-panel">
          <h3>2. Short-Term Memory</h3>
          <div className="memory-log">
            {logs.filter(l => l.category === 'Short-Term Memory').map((log, i) => (
              <div key={i} className="log-entry">{log.message}</div>
            ))}
          </div>
        </div>
        
        <div className="dashboard-module glass-panel">
          <h3>3. Long-Term Memory</h3>
          <div className="memory-log">
            <div className="log-entry">[SYSTEM] Kiosk Uptime: 24h</div>
            <div className="log-entry">[CACHE] Loaded 2 fallback profiles.</div>
          </div>
        </div>
        
        <div className="dashboard-module glass-panel">
          <h3>4. Running Processes</h3>
          <div className="process-console">
            {logs.filter(l => l.category === 'Running Processes').map((log, i) => (
              <div key={i} className="console-line">&gt; {log.message}</div>
            ))}
            <div className="console-line">&gt; [SYSTEM] Waiting for input...</div>
          </div>
        </div>
      </div>
    </div>
  );
}
export default TelemetryPane;
