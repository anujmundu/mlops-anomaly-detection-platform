"""Embedded Real-Time Industrial Telemetry Dashboard for FastAPI.

Provides an executive-grade, dark-mode operations console for live anomaly
simulation, sensor telemetry charts, latency benchmarking, and recruiter showcase.
"""


def get_dashboard_html() -> str:
    """Return the complete standalone HTML/CSS/JS dashboard string."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IT-ADS | Real-Time Industrial Anomaly Detection Operations Console</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220%22%20%220%22%20%22100%22%20%22100%22><text y=%22.9em%22 font-size=%2290%22>⚡</text></svg>">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {
      --bg-base: #0a0e17;
      --bg-surface: #111827;
      --bg-card: #162032;
      --border-subtle: #1f2d42;
      --border-accent: #2d4263;
      --primary: #38bdf8;
      --primary-glow: rgba(56, 189, 248, 0.25);
      --success: #10b981;
      --success-glow: rgba(16, 185, 129, 0.25);
      --danger: #ef4444;
      --danger-glow: rgba(239, 68, 68, 0.35);
      --warning: #f59e0b;
      --text-main: #f3f4f6;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg-base);
      color: var(--text-main);
      font-family: var(--font-sans);
      line-height: 1.5;
      padding-bottom: 60px;
      overflow-x: hidden;
    }

    /* Ambient Background Glow */
    .ambient-glow {
      position: fixed;
      top: -150px;
      left: 50%;
      transform: translateX(-50%);
      width: 800px;
      height: 400px;
      background: radial-gradient(circle, rgba(56, 189, 248, 0.12) 0%, rgba(16, 185, 129, 0.05) 50%, transparent 70%);
      filter: blur(80px);
      z-index: -1;
      pointer-events: none;
    }

    .container {
      max-width: 1360px;
      margin: 0 auto;
      padding: 24px 20px;
    }

    /* Header Nav */
    header {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--border-subtle);
      margin-bottom: 28px;
    }
    .brand-group {
      display: flex;
      align-items: center;
      gap: 14px;
    }
    .logo-badge {
      width: 44px;
      height: 44px;
      border-radius: 10px;
      background: linear-gradient(135deg, #0284c7, #10b981);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      box-shadow: 0 0 20px rgba(56, 189, 248, 0.35);
    }
    .brand-title {
      font-size: 20px;
      font-weight: 800;
      letter-spacing: -0.5px;
      color: #fff;
    }
    .brand-subtitle {
      font-size: 13px;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }
    .nav-actions {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
    }
    .btn-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: var(--bg-surface);
      color: var(--text-main);
      border: 1px solid var(--border-subtle);
      padding: 8px 16px;
      border-radius: 9999px;
      font-size: 13px;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.2s ease;
    }
    .btn-pill:hover {
      background: var(--bg-card);
      border-color: var(--primary);
      color: var(--primary);
      transform: translateY(-1px);
    }
    .btn-pill.primary {
      background: linear-gradient(135deg, #0284c7, #0369a1);
      border-color: #38bdf8;
      color: #fff;
    }
    .btn-pill.primary:hover {
      box-shadow: 0 0 15px var(--primary-glow);
    }
    .status-indicator {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      border-radius: 9999px;
      background: rgba(16, 185, 129, 0.1);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: #34d399;
      font-size: 12px;
      font-weight: 700;
      font-family: var(--font-mono);
    }
    .pulse-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 8px #10b981;
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
      70% { transform: scale(1.1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
      100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* KPI Grid */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-bottom: 28px;
    }
    .kpi-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 18px 20px;
      position: relative;
      overflow: hidden;
    }
    .kpi-card::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--primary), transparent);
    }
    .kpi-title {
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--text-muted);
      font-weight: 700;
      margin-bottom: 6px;
    }
    .kpi-value {
      font-size: 26px;
      font-weight: 800;
      color: #fff;
      font-family: var(--font-mono);
      display: flex;
      align-items: baseline;
      gap: 6px;
    }
    .kpi-subtitle {
      font-size: 12px;
      color: var(--text-dim);
      margin-top: 4px;
    }

    /* Main Grid */
    .main-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin-bottom: 28px;
    }
    @media (max-width: 992px) {
      .main-grid { grid-template-columns: 1fr; }
    }

    .card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 24px;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
    }
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      padding-bottom: 14px;
      border-bottom: 1px solid var(--border-subtle);
    }
    .card-title {
      font-size: 17px;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    /* Preset Scenarios */
    .preset-group {
      margin-bottom: 20px;
    }
    .preset-label {
      font-size: 12px;
      text-transform: uppercase;
      font-weight: 700;
      color: var(--text-dim);
      margin-bottom: 10px;
      letter-spacing: 0.5px;
    }
    .preset-buttons {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
    }
    @media (max-width: 500px) {
      .preset-buttons { grid-template-columns: 1fr; }
    }
    .btn-preset {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      padding: 10px 14px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      text-align: left;
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .btn-preset:hover {
      background: #1c293f;
      border-color: var(--primary);
      transform: translateY(-1px);
    }
    .btn-preset span.desc {
      font-size: 11px;
      font-weight: 400;
      color: var(--text-muted);
    }

    /* Sliders */
    .slider-row {
      margin-bottom: 14px;
    }
    .slider-labels {
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      margin-bottom: 4px;
    }
    .slider-name {
      font-weight: 600;
      color: var(--text-main);
    }
    .slider-val {
      font-family: var(--font-mono);
      font-weight: 700;
      color: var(--primary);
    }
    input[type=range] {
      width: 100%;
      height: 6px;
      border-radius: 4px;
      background: var(--bg-card);
      outline: none;
      -webkit-appearance: none;
    }
    input[type=range]::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: var(--primary);
      cursor: pointer;
      box-shadow: 0 0 10px var(--primary-glow);
    }

    .btn-infer {
      width: 100%;
      background: linear-gradient(135deg, #0284c7, #0ea5e9);
      color: #fff;
      border: none;
      padding: 14px 20px;
      border-radius: 12px;
      font-size: 15px;
      font-weight: 700;
      cursor: pointer;
      margin-top: 10px;
      box-shadow: 0 4px 15px rgba(14, 165, 233, 0.35);
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
    }
    .btn-infer:hover {
      filter: brightness(1.1);
      transform: translateY(-1px);
    }

    /* Output Console */
    .verdict-banner {
      padding: 20px;
      border-radius: 14px;
      margin-bottom: 20px;
      text-align: center;
      transition: all 0.3s ease;
      position: relative;
    }
    .verdict-banner.normal {
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .verdict-banner.anomaly {
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.5);
      box-shadow: 0 0 25px var(--danger-glow);
    }
    .verdict-banner.quarantine {
      background: rgba(245, 158, 11, 0.12);
      border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .verdict-status {
      font-size: 22px;
      font-weight: 800;
      letter-spacing: -0.5px;
      margin-bottom: 6px;
    }
    .verdict-banner.normal .verdict-status { color: #34d399; }
    .verdict-banner.anomaly .verdict-status { color: #f87171; }
    .verdict-banner.quarantine .verdict-status { color: #fbbf24; }
    .verdict-sub {
      font-size: 13px;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }

    .output-stats {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 20px;
    }
    .output-stat-box {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 12px 14px;
    }
    .output-stat-label {
      font-size: 11px;
      text-transform: uppercase;
      font-weight: 700;
      color: var(--text-dim);
    }
    .output-stat-val {
      font-size: 18px;
      font-weight: 800;
      font-family: var(--font-mono);
      color: #fff;
      margin-top: 2px;
    }

    /* Attribution Bars */
    .attribution-title {
      font-size: 12px;
      text-transform: uppercase;
      font-weight: 700;
      color: var(--text-dim);
      margin-bottom: 10px;
    }
    .attr-row {
      margin-bottom: 10px;
    }
    .attr-meta {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      font-family: var(--font-mono);
      margin-bottom: 4px;
    }
    .attr-bar-bg {
      height: 8px;
      background: var(--bg-card);
      border-radius: 4px;
      overflow: hidden;
    }
    .attr-bar-fill {
      height: 100%;
      border-radius: 4px;
      background: linear-gradient(90deg, #38bdf8, #ef4444);
      transition: width 0.4s ease;
    }

    /* JSON Box */
    .json-preview {
      background: #080c14;
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 14px;
      font-family: var(--font-mono);
      font-size: 11.5px;
      color: #cbd5e1;
      max-height: 180px;
      overflow-y: auto;
      white-space: pre-wrap;
    }

    /* Charts Row */
    .charts-grid {
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 24px;
      margin-bottom: 28px;
    }
    @media (max-width: 992px) {
      .charts-grid { grid-template-columns: 1fr; }
    }
    .chart-container {
      position: relative;
      height: 250px;
      width: 100%;
    }

    /* Architecture Footer Card */
    .arch-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 24px;
    }
    .arch-steps {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-top: 16px;
    }
    .arch-step-box {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 16px;
      position: relative;
    }
    .arch-step-num {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 6px;
    }
    .arch-step-name {
      font-size: 14px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 4px;
    }
    .arch-step-desc {
      font-size: 12px;
      color: var(--text-muted);
    }
  </style>
</head>
<body>
  <div class="ambient-glow"></div>
  <div class="container">

    <!-- Header Navigation -->
    <header>
      <div class="brand-group">
        <div class="logo-badge">⚡</div>
        <div>
          <div class="brand-title">IT-ADS Anomaly Operations Center</div>
          <div class="brand-subtitle">Production Inference Microservice • Isolation Forest • Sub-15ms SLA</div>
        </div>
      </div>
      <div class="nav-actions">
        <div class="status-indicator">
          <div class="pulse-dot"></div>
          <span>API 200 OK • CLOUD SERVING</span>
        </div>
        <a href="/docs" target="_blank" class="btn-pill primary">📖 Swagger UI Docs</a>
        <a href="/metrics" target="_blank" class="btn-pill">📈 Prometheus Metrics</a>
        <a href="/v1/health" target="_blank" class="btn-pill">🩺 Health Probe</a>
        <a href="https://github.com/anujmundu/mlops-anomaly-detection-platform" target="_blank" class="btn-pill">🐙 GitHub</a>
      </div>
    </header>

    <!-- Top KPI Grid -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-title">Active Champion Model</div>
        <div class="kpi-value">Isolation Forest</div>
        <div class="kpi-subtitle">100 Trees • Contamination 0.03</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Inference Latency SLA</div>
        <div class="kpi-value" id="kpi-latency">~8.5 <span style="font-size:14px; color:var(--text-muted)">ms</span></div>
        <div class="kpi-subtitle">Production Target: p99 &lt; 15.0ms</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Quality Gate Precision</div>
        <div class="kpi-value" style="color:#34d399">92.4%</div>
        <div class="kpi-subtitle">False Positive Rate: &le; 2.5%</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Data Firewall Gate</div>
        <div class="kpi-value" style="color:#38bdf8">Strict DLQ</div>
        <div class="kpi-subtitle">Great Expectations Range Audit</div>
      </div>
    </div>

    <!-- Main Anomaly Simulation & Output Console -->
    <div class="main-grid">

      <!-- Left Column: Interactive Simulation Controls -->
      <div class="card">
        <div class="card-header">
          <div class="card-title">🎛️ Real-Time Telemetry Sandbox</div>
          <span style="font-size:12px; color:var(--text-muted); font-family:var(--font-mono)" id="device-label">Device: TURBINE_NORMAL_01</span>
        </div>

        <!-- Preset Demonstration Buttons -->
        <div class="preset-group">
          <div class="preset-label">One-Click Demonstration Scenarios (Click to Test)</div>
          <div class="preset-buttons">
            <button class="btn-preset" onclick="loadPreset('normal')">
              🟢 Normal Operating State
              <span class="desc">Standard pump operating baseline</span>
            </button>
            <button class="btn-preset" onclick="loadPreset('thermal')">
              🔥 Thermal Shock Anomaly
              <span class="desc">Temp spike to 135°C (overheating)</span>
            </button>
            <button class="btn-preset" onclick="loadPreset('bearing')">
              ⚙️ Bearing Wear Degradation
              <span class="desc">Vibration surge to 24.5 mm/s</span>
            </button>
            <button class="btn-preset" onclick="loadPreset('corrupt')">
              🛡️ Test Quarantine (DLQ)
              <span class="desc">Negative pressure (-40 psi) rejected</span>
            </button>
          </div>
        </div>

        <!-- Telemetry Sliders -->
        <div class="slider-row">
          <div class="slider-labels">
            <span class="slider-name">Temperature (°C)</span>
            <span class="slider-val" id="val-temp">82.5 °C</span>
          </div>
          <input type="range" id="input-temp" min="40" max="150" step="0.5" value="82.5" oninput="updateVal('temp', '°C')">
        </div>

        <div class="slider-row">
          <div class="slider-labels">
            <span class="slider-name">Pressure (psi)</span>
            <span class="slider-val" id="val-press">105.0 psi</span>
          </div>
          <input type="range" id="input-press" min="-50" max="250" step="1" value="105.0" oninput="updateVal('press', 'psi')">
        </div>

        <div class="slider-row">
          <div class="slider-labels">
            <span class="slider-name">Vibration (mm/s)</span>
            <span class="slider-val" id="val-vib">4.5 mm/s</span>
          </div>
          <input type="range" id="input-vib" min="0" max="35" step="0.1" value="4.5" oninput="updateVal('vib', 'mm/s')">
        </div>

        <div class="slider-row">
          <div class="slider-labels">
            <span class="slider-name">Shaft Velocity (RPM)</span>
            <span class="slider-val" id="val-rpm">3200 RPM</span>
          </div>
          <input type="range" id="input-rpm" min="1000" max="6000" step="50" value="3200" oninput="updateVal('rpm', 'RPM')">
        </div>

        <div class="slider-row">
          <div class="slider-labels">
            <span class="slider-name">AC Supply Voltage (V)</span>
            <span class="slider-val" id="val-volt">230.0 V</span>
          </div>
          <input type="range" id="input-volt" min="180" max="280" step="0.5" value="230.0" oninput="updateVal('volt', 'V')">
        </div>

        <button class="btn-infer" onclick="triggerInference()">
          <span>⚡ Execute Real-Time Inference (/v1/predict)</span>
        </button>
      </div>

      <!-- Right Column: Real-Time Model Decision & Feature Attribution -->
      <div class="card">
        <div class="card-header">
          <div class="card-title">🔬 Model Decision & Feature Attribution</div>
          <span style="font-size:12px; color:var(--text-muted); font-family:var(--font-mono)">Isolation Forest</span>
        </div>

        <!-- Decision Banner -->
        <div class="verdict-banner normal" id="verdict-box">
          <div class="verdict-status" id="verdict-text">🟢 NORMAL OPERATION</div>
          <div class="verdict-sub" id="verdict-sub">Anomaly Score: 0.452 • Telemetry within healthy distribution</div>
        </div>

        <!-- Latency and Score Stats -->
        <div class="output-stats">
          <div class="output-stat-box">
            <div class="output-stat-label">Inference Latency</div>
            <div class="output-stat-val" id="stat-latency" style="color:#34d399">7.82 ms</div>
          </div>
          <div class="output-stat-box">
            <div class="output-stat-label">Calculated Anomaly Score</div>
            <div class="output-stat-val" id="stat-score">0.452 / 1.0</div>
          </div>
        </div>

        <!-- Root Cause Attribution Breakdown -->
        <div class="attribution-title">Root-Cause Feature Deviations (&sigma;-Sigma Norm)</div>
        <div id="attribution-container">
          <div class="attr-row">
            <div class="attr-meta">
              <span id="attr-name-1">rolling_mean_30m_temp</span>
              <span id="attr-val-1">+1.05 &sigma;</span>
            </div>
            <div class="attr-bar-bg"><div class="attr-bar-fill" id="attr-bar-1" style="width: 25%"></div></div>
          </div>
          <div class="attr-row">
            <div class="attr-meta">
              <span id="attr-name-2">sensor_velocity_norm</span>
              <span id="attr-val-2">+0.68 &sigma;</span>
            </div>
            <div class="attr-bar-bg"><div class="attr-bar-fill" id="attr-bar-2" style="width: 15%"></div></div>
          </div>
        </div>

        <!-- Raw JSON Contract -->
        <div style="margin-top: 18px">
          <div class="attribution-title">Live API Response Contract (/v1/predict)</div>
          <div class="json-preview" id="json-output">// Click 'Execute Real-Time Inference' to view live response payload...</div>
        </div>
      </div>
    </div>

    <!-- Live Telemetry Stream Charts -->
    <div class="charts-grid">
      <div class="card">
        <div class="card-header">
          <div class="card-title">📈 Streaming Telemetry & Trend Windows</div>
          <span style="font-size:12px; color:var(--text-muted); font-family:var(--font-mono)">Rolling 10-Event Buffer</span>
        </div>
        <div class="chart-container">
          <canvas id="telemetryChart"></canvas>
        </div>
      </div>
      <div class="card">
        <div class="card-header">
          <div class="card-title">🎯 Anomaly Probability Gauge</div>
          <span style="font-size:12px; color:var(--text-muted); font-family:var(--font-mono)">Isolation Forest</span>
        </div>
        <div class="chart-container">
          <canvas id="scoreGaugeChart"></canvas>
        </div>
      </div>
    </div>

    <!-- MLOps Architecture Lifecycle -->
    <div class="arch-card">
      <div class="card-title">🏛️ End-to-End MLOps System Lifecycle Architecture</div>
      <div class="arch-steps">
        <div class="arch-step-box">
          <div class="arch-step-num">STAGE 01</div>
          <div class="arch-step-name">Streaming Ingestion</div>
          <div class="arch-step-desc">Distributed Kafka broker (`sensor.telemetry.raw`) consuming real-time high-velocity IoT machinery telemetry.</div>
        </div>
        <div class="arch-step-box">
          <div class="arch-step-num">STAGE 02</div>
          <div class="arch-step-name">Data Quality Firewall</div>
          <div class="arch-step-desc">Great Expectations contract validation isolating corrupted or out-of-range sensor payloads directly to DLQ.</div>
        </div>
        <div class="arch-step-box">
          <div class="arch-step-num">STAGE 03</div>
          <div class="arch-step-name">17-D Feature Engine</div>
          <div class="arch-step-desc">Stateful 5m/30m rolling stats, delta changes, z-scores, and Euclidean velocity norms.</div>
        </div>
        <div class="arch-step-box">
          <div class="arch-step-num">STAGE 04</div>
          <div class="arch-step-name">Low-Latency Serving</div>
          <div class="arch-step-desc">FastAPI microservice executing Isolation Forest champion inference under a strict sub-15ms p99 SLA.</div>
        </div>
        <div class="arch-step-box">
          <div class="arch-step-num">STAGE 05</div>
          <div class="arch-step-name">Self-Healing Retraining</div>
          <div class="arch-step-desc">Continuous PSI and KS drift monitoring triggering automated retraining and zero-downtime hot-swapping.</div>
        </div>
      </div>
    </div>

  </div>

  <script>
    // State Tracking
    const historyLabels = ['T-9', 'T-8', 'T-7', 'T-6', 'T-5', 'T-4', 'T-3', 'T-2', 'T-1', 'Now'];
    const tempData = [81.2, 82.0, 81.5, 83.1, 82.4, 82.8, 83.0, 82.5, 82.7, 82.5];
    const vibData = [4.1, 4.3, 4.0, 4.2, 4.5, 4.3, 4.4, 4.2, 4.3, 4.5];

    // Chart.js Setup
    const ctxTelemetry = document.getElementById('telemetryChart').getContext('2d');
    const telemetryChart = new Chart(ctxTelemetry, {
      type: 'line',
      data: {
        labels: historyLabels,
        datasets: [
          {
            label: 'Temperature (°C)',
            data: tempData,
            borderColor: '#38bdf8',
            backgroundColor: 'rgba(56, 189, 248, 0.1)',
            tension: 0.35,
            fill: true,
            yAxisID: 'y'
          },
          {
            label: 'Vibration (mm/s)',
            data: vibData,
            borderColor: '#f59e0b',
            backgroundColor: 'transparent',
            tension: 0.35,
            borderDash: [4, 4],
            yAxisID: 'y1'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b' } },
          y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#38bdf8' }, position: 'left' },
          y1: { grid: { drawOnChartArea: false }, ticks: { color: '#f59e0b' }, position: 'right' }
        },
        plugins: {
          legend: { labels: { color: '#cbd5e1', font: { family: 'Plus Jakarta Sans' } } }
        }
      }
    });

    const ctxGauge = document.getElementById('scoreGaugeChart').getContext('2d');
    const scoreGaugeChart = new Chart(ctxGauge, {
      type: 'doughnut',
      data: {
        labels: ['Anomaly Score', 'Remaining Headroom'],
        datasets: [{
          data: [45, 55],
          backgroundColor: ['#10b981', '#1f293d'],
          borderWidth: 0,
          circumference: 180,
          rotation: 270
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        }
      }
    });

    function updateVal(key, unit) {
      const val = document.getElementById('input-' + key).value;
      document.getElementById('val-' + key).innerText = val + ' ' + unit;
    }

    let currentDeviceId = "TURBINE_NORMAL_01";
    function loadPreset(type) {
      if (type === 'normal') {
        currentDeviceId = "TURBINE_NORMAL_01";
        setValues(82.5, 105.0, 4.2, 3200, 230.0);
      } else if (type === 'thermal') {
        currentDeviceId = "TURBINE_THERMAL_02";
        setValues(135.0, 155.0, 7.8, 4100, 245.0);
      } else if (type === 'bearing') {
        currentDeviceId = "TURBINE_BEARING_03";
        setValues(95.0, 140.0, 30.0, 5800, 245.0);
      } else if (type === 'corrupt') {
        currentDeviceId = "TURBINE_QUARANTINE_04";
        setValues(82.5, -45.0, 4.5, 3200, 230.0);
      }
      const devEl = document.getElementById('device-label');
      if (devEl) devEl.innerText = 'Device: ' + currentDeviceId;
      triggerInference();
    }

    function setValues(t, p, v, r, volt) {
      document.getElementById('input-temp').value = t;
      document.getElementById('input-press').value = p;
      document.getElementById('input-vib').value = v;
      document.getElementById('input-rpm').value = r;
      document.getElementById('input-volt').value = volt;
      updateVal('temp', '°C');
      updateVal('press', 'psi');
      updateVal('vib', 'mm/s');
      updateVal('rpm', 'RPM');
      updateVal('volt', 'V');
    }

    async function triggerInference() {
      const payload = {
        device_id: currentDeviceId,
        timestamp: new Date().toISOString(),
        temperature: parseFloat(document.getElementById('input-temp').value),
        pressure: parseFloat(document.getElementById('input-press').value),
        vibration: parseFloat(document.getElementById('input-vib').value),
        rpm: parseFloat(document.getElementById('input-rpm').value),
        voltage: parseFloat(document.getElementById('input-volt').value)
      };

      const t0 = performance.now();
      try {
        const resp = await fetch('/v1/predict', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const t1 = performance.now();
        const latency = (t1 - t0).toFixed(2);

        if (resp.status === 422) {
          const errData = await resp.json();
          renderQuarantine(errData, latency);
          return;
        }

        const data = await resp.json();
        renderResult(data, latency, payload);
      } catch (err) {
        console.error("Inference call failed:", err);
      }
    }

    function renderResult(data, latency, payload) {
      const isAnomaly = data.is_anomaly;
      const score = data.anomaly_score.toFixed(4);
      const box = document.getElementById('verdict-box');
      const text = document.getElementById('verdict-text');
      const sub = document.getElementById('verdict-sub');

      box.className = 'verdict-banner ' + (isAnomaly ? 'anomaly' : 'normal');
      text.innerText = isAnomaly ? '🚨 CRITICAL INDUSTRIAL ANOMALY DETECTED' : '🟢 NORMAL OPERATION APPROVED';
      sub.innerText = 'Anomaly Score: ' + score + ' • Model Version: ' + data.model_version;

      document.getElementById('stat-latency').innerText = data.inference_latency_ms + ' ms';
      document.getElementById('kpi-latency').innerHTML = data.inference_latency_ms + ' <span style="font-size:14px; color:var(--text-muted)">ms</span>';
      document.getElementById('stat-score').innerText = score + ' / 1.0';

      // Update Gauge
      const scorePct = Math.round(data.anomaly_score * 100);
      scoreGaugeChart.data.datasets[0].data = [scorePct, 100 - scorePct];
      scoreGaugeChart.data.datasets[0].backgroundColor = isAnomaly ? ['#ef4444', '#1f293d'] : ['#10b981', '#1f293d'];
      scoreGaugeChart.update();

      // Update Chart Stream
      tempData.shift();
      tempData.push(payload.temperature);
      vibData.shift();
      vibData.push(payload.vibration);
      telemetryChart.update();

      // Feature Attribution
      if (data.contributing_features && data.contributing_features.length >= 2) {
        document.getElementById('attr-name-1').innerText = data.contributing_features[0].feature;
        document.getElementById('attr-val-1').innerText = '+' + data.contributing_features[0].deviation_sigma.toFixed(2) + ' σ';
        document.getElementById('attr-bar-1').style.width = Math.min(100, data.contributing_features[0].deviation_sigma * 6) + '%';

        document.getElementById('attr-name-2').innerText = data.contributing_features[1].feature;
        document.getElementById('attr-val-2').innerText = '+' + data.contributing_features[1].deviation_sigma.toFixed(2) + ' σ';
        document.getElementById('attr-bar-2').style.width = Math.min(100, data.contributing_features[1].deviation_sigma * 6) + '%';
      }

      document.getElementById('json-output').innerText = JSON.stringify(data, null, 2);
    }

    function renderQuarantine(errData, latency) {
      const box = document.getElementById('verdict-box');
      const text = document.getElementById('verdict-text');
      const sub = document.getElementById('verdict-sub');

      box.className = 'verdict-banner quarantine';
      text.innerText = '🛡️ DATA QUALITY FIREWALL QUARANTINE (DLQ)';
      sub.innerText = 'HTTP 422 Intercepted: Sensor value physically impossible. Diverted to quarantine.';

      document.getElementById('stat-latency').innerText = latency + ' ms';
      document.getElementById('stat-score').innerText = 'REJECTED (422)';
      document.getElementById('json-output').innerText = JSON.stringify(errData, null, 2);

      scoreGaugeChart.data.datasets[0].data = [100, 0];
      scoreGaugeChart.data.datasets[0].backgroundColor = ['#f59e0b', '#1f293d'];
      scoreGaugeChart.update();
    }

    // Auto-trigger scenario on load
    window.addEventListener('DOMContentLoaded', () => {
      const urlParams = new URLSearchParams(window.location.search);
      const scenario = urlParams.get('scenario') || 'normal';
      loadPreset(scenario);
    });
  </script>
</body>
</html>
"""
