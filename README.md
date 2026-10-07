# NetWatch

**NetWatch** is a lightweight desktop network monitoring application for Windows, built with Python and CustomTkinter.

It continuously monitors your internet connection, measures latency, detects connection losses and abnormal ping increases, records incidents, and provides a clean interface for reviewing network stability.

**Version:** 1.0.0
**Author:** heavenylz
**Platform:** Windows

---

## Features

### Real-Time Network Monitoring

NetWatch continuously pings a configurable target and displays the current state of your connection.

* Live latency monitoring
* Online/offline detection
* Configurable monitoring interval
* Configurable ping target
* Real-time network status
* Ping history graph

### Anomaly Detection

NetWatch analyzes latency measurements and automatically detects abnormal network behavior.

It can identify:

* Ping spikes
* High latency
* Connection loss
* Connection restoration

Detection sensitivity can be adjusted from the Settings page.

### Incident Tracking

Detected network problems are automatically stored as incidents.

Each incident can contain information such as:

* Incident type
* Severity
* Start time
* End time
* Duration
* Latency
* Peak latency
* Baseline latency
* Event message

Connection-loss incidents remain active until connectivity is restored.

### Statistics

The Statistics page provides an overview of recorded network events, including:

* Total incidents
* Connection losses
* Total downtime
* Highest recorded ping
* Average incident latency
* Incident type distribution
* Severity distribution
* Most recent incident

### Customizable Settings

NetWatch allows monitoring behavior to be configured directly from the application.

Available settings include:

* Ping target
* Check interval
* History length
* Spike multiplier
* Minimum spike latency
* Disconnect threshold

Settings are validated before being saved and remain persistent between application sessions.

---

## Interface

NetWatch uses a custom dark desktop interface with four main sections:

### Dashboard

Displays the current connection status, latency, network health, baseline latency, and live ping history.

### Incidents

Shows previously detected network incidents with severity, timing, latency, and duration information.

### Statistics

Provides aggregated statistics and incident distribution information.

### Settings

Allows monitoring and anomaly-detection parameters to be configured without restarting the application.

---

## Installation

### Download

For normal Windows users, download the latest `NetWatch.exe` from the project's GitHub Releases page.

No Python installation is required when using the packaged executable.

### Run from Source

To run NetWatch directly from the source code, Python is required.

Clone the repository:

```bash
git clone https://github.com/heavenylz/NetWatch.git
cd NetWatch
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Start NetWatch:

```bash
python main.py
```

---

## Requirements

NetWatch currently uses:

* Python
* CustomTkinter
* Matplotlib
* Pillow
* SQLite

SQLite is provided by Python's standard library and does not require a separate installation.

---

## Project Structure

```text
NetWatch/
├── assets/
│   ├── netwatch_logo.png
│   └── netwatch.ico
│
├── core/
│   ├── database.py
│   ├── detector.py
│   ├── incident_manager.py
│   ├── monitor.py
│   ├── settings_manager.py
│   └── validation.py
│
├── data/
│   ├── netwatch.db
│   └── settings.json
│
├── ui/
│   ├── pages/
│   │   ├── dashboard.py
│   │   ├── incidents.py
│   │   ├── settings.py
│   │   └── statistics.py
│   │
│   ├── animations.py
│   ├── app.py
│   ├── sidebar.py
│   └── theme.py
│
├── config.py
├── main.py
├── README.md
├── requirements.txt
└── settings.example.json
```

Runtime database and personal settings files are not intended to be included in source releases.

---

## How It Works

NetWatch periodically sends ping requests to the configured target.

Successful measurements are passed to the anomaly detector, which maintains a latency baseline and evaluates new measurements for abnormal behavior.

When a significant network event is detected, the incident manager records it in the local SQLite database.

The interface then presents this information through the Dashboard, Incidents, and Statistics pages.

All monitoring data remains local to the application.

---

## Default Configuration

The default configuration is:

```json
{
    "ping_target": "1.1.1.1",
    "check_interval": 2.0,
    "history_length": 60,
    "spike_multiplier": 2.5,
    "minimum_spike_ms": 60.0,
    "disconnect_threshold": 3
}
```

These values can be changed from the Settings page.

---

## Data Storage

NetWatch stores its runtime information locally.

The application uses:

```text
data/settings.json
```

for user configuration and:

```text
data/netwatch.db
```

for recorded network incidents.

These files may contain machine-specific monitoring data and should generally not be committed to the repository.

---

## Privacy

NetWatch does not require an account and does not upload monitoring information to an external NetWatch service.

Network monitoring and incident storage are performed locally on the user's computer.

---

## Version

Current release:

**NetWatch v1.0.0**

This is the first public release of NetWatch.

---

## Author

Developed by **heavenylz**.

© 2026 heavenylz. All rights reserved.
