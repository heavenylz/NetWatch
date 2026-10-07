# Changelog

All notable changes to **NetWatch** will be documented in this file.

---

## [1.0.0] - 2026-10-07

### Initial Release

The first public release of NetWatch.

### Added

#### Network Monitoring

* Real-time network latency monitoring.
* Configurable ping target.
* Configurable monitoring interval.
* Online and offline connection detection.
* Automatic connection restoration detection.
* Live latency history tracking.

#### Anomaly Detection

* Dynamic latency baseline calculation.
* Automatic ping spike detection.
* High-latency detection.
* Configurable spike multiplier.
* Configurable minimum spike threshold.
* Configurable disconnect threshold.
* Multiple event severity levels:

  * Normal
  * Warning
  * High
  * Critical

#### Incident Management

* Automatic incident creation when network problems are detected.
* Connection-loss incident tracking.
* Automatic incident closure after connectivity is restored.
* Ping spike and high-latency incident recording.
* Incident duration tracking.
* Peak latency recording.
* Baseline latency recording.
* Persistent incident storage using SQLite.

#### Dashboard

* Real-time connection status.
* Current ping display.
* Baseline latency display.
* Network health indicator.
* Live latency history graph.
* Dynamic status colors.
* Animated connection-status indicator.
* Ping status animations.

#### Incidents

* Dedicated incident history page.
* Severity-based incident indicators.
* Incident type and message display.
* Latency and baseline information.
* Incident duration.
* Event timestamps.
* Manual incident list refresh.
* Empty and error states.

#### Statistics

* Total incident count.
* Connection-loss count.
* Total recorded downtime.
* Highest recorded latency.
* Average incident latency.
* Incident type breakdown.
* Severity distribution.
* Most recent incident information.

#### Settings

* Configurable ping target.
* Configurable check interval.
* Configurable history length.
* Configurable anomaly-detection sensitivity.
* Input validation.
* Persistent configuration.
* Runtime setting changes without requiring an application restart.
* Reset-to-default functionality.

#### User Interface

* Custom dark interface built with CustomTkinter.
* Sidebar navigation.
* Animated navigation states.
* Page transition animations.
* Responsive window layout.
* Custom NetWatch branding.
* NetWatch application logo.
* Windows window and taskbar icon support.
* Author and copyright information.

#### Reliability

* Graceful application shutdown.
* Background monitoring thread.
* Safe UI updates from the monitoring system.
* Ping process timeout handling.
* Invalid ping-response handling.
* Hostname and IP address validation.
* Persistent local SQLite database.
* Persistent local settings.

### Tested

NetWatch v1.0.0 was tested for:

* Settings persistence across application restarts.
* Runtime ping-target changes.
* Connection loss detection.
* Connection restoration.
* Incident creation and closure.
* Statistics updates.
* High-ping anomaly detection.
* Invalid settings and validation behavior.
* Rapid page navigation.
* Window resizing.
* Repeated page refreshes.
* Application shutdown during active monitoring.

---

## Project

**NetWatch**
Version 1.0.0
Developed by **heavenylz**

© 2026 heavenylz. All rights reserved.
