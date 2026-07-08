Overview





import React, { useState, useEffect } from 'react';
function App() {
  // Global States matching Short-Term Memory Requirements
  const [status, setStatus] = useState('Kiosk System Active');
  const [activeAgent, setActiveAgent] = useState('GET_PROCESS_AGENT');
  const [sessionUser, setSessionUser] = useState({
    name: 'John Doe',
    role: 'Staff Account Verified',
    id: 'JD'
  });
  const [uptime, setUptime] = useState(98); // Uptime counter simulation
  const [logs, setLogs] = useState([
    '[WAKEWORD] Listening for "Maggie"...',
    '[LDAP] Connecting to Windows Active Directory...',
    '[SYSTEM] Maggie Kiosk Framework Online.'
  ]);
  // Simulate Uptime Incrementer
  useEffect(() => {
    const timer = setInterval(() => setUptime(prev => prev + 1), 1000);
    return () => clearInterval(timer);
  }, []);
  const formatUptime = (secs) => {
    const h = String(Math.floor(secs / 3600)).padStart(2, '0');
    const m = String(Math.floor((secs % 3600) / 60)).padStart(2, '0');
    const s = String(secs % 60).padStart(2, '0');
    return `${h}:${m}:${s}`;
  };
  const handleConnect = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/robot/connect', { method: 'POST' });
      const data = await res.json();
      if (data.status === 'success') {
        alert("Success! Connected to Maggie.");
      } else {
        alert("Connection Failed: " + data.message + "\n\nDid you run reachy-mini-daemon?");
      }
    } catch (err) {
      alert("Error: Backend is not running.");
    }
  };
  const handleDisconnect = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/robot/disconnect', { method: 'POST' });
      const data = await res.json();
      if (data.status === 'success') {
        alert("Maggie is turned off and resting.");
      } else {
        alert("Error: " + data.message);
      }
    } catch (err) {
      alert("Error: Backend is not running.");
    }
  };
  return (
    <div style={{
      backgroundColor: '#0a0f1d',
            </div>
          </div>
          
          {/* BOTTOM LEFT CONNECT BUTTONS */}
          <div style={{ marginTop: 'auto', textAlign: 'left' }}>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button 
                onClick={handleConnect}
                style={{ 
                  background: '#10b981', 
                  color: 'white', 
                  padding: '0.75rem 1.5rem', 
                  border: 'none', 
                  borderRadius: '8px', 
                  fontWeight: 'bold', 
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  fontSize: '1rem'
                }}>
                🔌 Connect to Maggie
              </button>
              <button 
                onClick={handleDisconnect}
                style={{ 
                  background: '#ef4444', 
                  color: 'white', 
                  padding: '0.75rem 1.5rem', 
                  border: 'none', 
                  borderRadius: '8px', 
                  fontWeight: 'bold', 
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  fontSize: '1rem'
                }}>
                💤 Turn Off
              </button>
            </div>
            <p style={{ fontSize: '0.75rem', color: '#f87171', marginTop: '0.5rem' }}>
              ⚠️ You must start <code>reachy-mini-daemon</code> in your terminal before connecting.
            </p>
          </div>
          
        </main>
        {/* RIGHT-SIDE PANE: SYSTEM TELEMETRY BUS */}
        <aside style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          
          {/* 1. AGENTS WORKING */}
          <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px', padding: '1.25rem' }}>
            <h3 style={{ margin: '0 0 1rem', fontSize: '0.85rem', color: '#64748b', letterSpacing: '1px' }}>1. AGENTS WORKING</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {['GET_PROCESS_AGENT', 'WIKI_LOOKUP_AGENT', 'SMTP_TICKET_AGENT', 'CAMERA_CAPTURE_AGENT', 'CAMPUS_SCRAPER_AGENT'].map((agent) => (
                <div key={agent} style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '0.6rem 1rem',
                  background: activeAgent === agent ? 'rgba(14, 165, 233, 0.15)' : '#1e293b',
                  border: activeAgent === agent ? '1px solid #0ea5e9' : '1px solid transparent',
                  borderRadius: '6px',
                  fontSize: '0.85rem',
                  fontWeight: 'bold',
                  fontFamily: 'monospace',
                  color: activeAgent === agent ? '#38bdf8' : '#94a3b8'
                }}>
                  <span>• {agent}</span>
                  {activeAgent === agent && <span style={{ fontSize: '0.7rem', color: '#38bdf8', background: 'rgba(56, 189, 248, 0.2)', padding: '0.1rem 0.4rem', borderRadius: '4px' }}>RUNNING</span>}
                </div>
              ))}
            </div>
          </div>
          {/* 2. SHORT-TERM MEMORY */}
          <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px', padding: '1.25rem' }}>
            <h3 style={{ margin: '0 0 0.75rem', fontSize: '0.85rem', color: '#64748b', letterSpacing: '1px' }}>2. SHORT-TERM MEMORY</h3>
            <div style={{ background: '#020617', padding: '0.75rem', borderRadius: '6px', fontSize: '0.8rem', fontFamily: 'monospace', color: '#38bdf8', borderLeft: '3px solid #38bdf8' }}>
              <strong>ACTIVE_TRANSCRIPTION:</strong> "Where is the main campus IT service desk located?"
            </div>
          </div>
          {/* 4. EXECUTION CONSOLE */}
          <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px', padding: '1.25rem', flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
            <h3 style={{ margin: '0 0 0.75rem', fontSize: '0.85rem', color: '#64748b', letterSpacing: '1px' }}>4. RUNNING PROCESSES LOG</h3>
            <div style={{
              flexGrow: 1,
              background: '#020617',
              padding: '0.75rem',
              borderRadius: '6px',
              fontFamily: 'monospace',
              fontSize: '0.8rem',
              color: '#a7f3d0',
              overflowY: 'auto',
              lineHeight: '1.5'
            }}>
              {logs.map((log, i) => (
                <div key={i} style={{ marginBottom: '0.25rem' }}>{log}</div>
              ))}
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}
export default App;
