from datetime import datetime

from core.database import Database
from core.detector import DetectionResult, EventType


class IncidentManager:
    def __init__(self, database: Database):
        self.database = database

        self.active_outage_id: int | None = None
        self.active_outage_started: datetime | None = None

    def process(
        self,
        detection: DetectionResult,
        latency_ms: float | None,
        timestamp: datetime,
    ):
        event = detection.event_type

        # -----------------------------------------------
        # CONNECTION LOST
        # -----------------------------------------------
        if event == EventType.CONNECTION_LOST:
            self._start_outage(
                detection=detection,
                timestamp=timestamp,
            )

            return

        # -----------------------------------------------
        # CONNECTION RESTORED
        # -----------------------------------------------
        if event == EventType.CONNECTION_RESTORED:
            self._end_outage(
                timestamp=timestamp,
            )

            return

        # -----------------------------------------------
        # PING SPIKE / HIGH PING
        # -----------------------------------------------
        if event in (
            EventType.PING_SPIKE,
            EventType.HIGH_PING,
        ):
            self.database.create_incident(
                incident_type=event.value,
                severity=detection.severity.value,
                started_at=timestamp.isoformat(),
                latency_ms=latency_ms,
                peak_latency_ms=latency_ms,
                baseline_ms=detection.baseline_ms,
                message=detection.message,
            )

    def _start_outage(
        self,
        detection: DetectionResult,
        timestamp: datetime,
    ):
        # Prevent duplicate outage incidents.
        if self.active_outage_id is not None:
            return

        incident_id = self.database.create_incident(
            incident_type="CONNECTION_LOSS",
            severity=detection.severity.value,
            started_at=timestamp.isoformat(),
            baseline_ms=detection.baseline_ms,
            message=detection.message,
        )

        self.active_outage_id = incident_id
        self.active_outage_started = timestamp

    def _end_outage(
        self,
        timestamp: datetime,
    ):
        if (
            self.active_outage_id is None
            or self.active_outage_started is None
        ):
            return

        duration = (
            timestamp - self.active_outage_started
        ).total_seconds()

        self.database.close_incident(
            incident_id=self.active_outage_id,
            ended_at=timestamp.isoformat(),
            duration_seconds=duration,
        )

        self.active_outage_id = None
        self.active_outage_started = None