from collections import deque
from dataclasses import dataclass
from enum import Enum
from statistics import mean


class Severity(Enum):
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class EventType(Enum):
    NORMAL = "NORMAL"
    PING_SPIKE = "PING_SPIKE"
    HIGH_PING = "HIGH_PING"
    TIMEOUT = "TIMEOUT"
    CONNECTION_LOST = "CONNECTION_LOST"
    CONNECTION_RESTORED = "CONNECTION_RESTORED"


@dataclass
class DetectionResult:
    event_type: EventType
    severity: Severity
    message: str
    baseline_ms: float | None = None


class AnomalyDetector:
    def __init__(
        self,
        history_size: int = 15,
        spike_multiplier: float = 2.5,
        minimum_spike_ms: float = 60,
        disconnect_threshold: int = 3,
    ):
        self.history_size = history_size
        self.spike_multiplier = spike_multiplier
        self.minimum_spike_ms = minimum_spike_ms
        self.disconnect_threshold = disconnect_threshold

        self.history = deque(
            maxlen=history_size
        )

        self.consecutive_timeouts = 0
        self.connection_lost = False

    # =========================================================
    # UPDATE SETTINGS
    # =========================================================

    def update_settings(
        self,
        spike_multiplier: float,
        minimum_spike_ms: float,
        disconnect_threshold: int,
    ):
        self.spike_multiplier = spike_multiplier
        self.minimum_spike_ms = minimum_spike_ms
        self.disconnect_threshold = disconnect_threshold

    # =========================================================
    # ANALYZE
    # =========================================================

    def analyze(
        self,
        latency_ms: float | None,
    ) -> DetectionResult:

        # -----------------------------------------------------
        # TIMEOUT
        # -----------------------------------------------------

        if latency_ms is None:
            self.consecutive_timeouts += 1

            if (
                self.consecutive_timeouts
                >= self.disconnect_threshold
                and not self.connection_lost
            ):
                self.connection_lost = True

                return DetectionResult(
                    event_type=EventType.CONNECTION_LOST,
                    severity=Severity.CRITICAL,
                    message=(
                        "Connection lost after "
                        f"{self.consecutive_timeouts} "
                        "consecutive timeouts."
                    ),
                    baseline_ms=self._baseline(),
                )

            if self.connection_lost:
                return DetectionResult(
                    event_type=EventType.TIMEOUT,
                    severity=Severity.CRITICAL,
                    message=(
                        "Connection is still unavailable."
                    ),
                    baseline_ms=self._baseline(),
                )

            return DetectionResult(
                event_type=EventType.TIMEOUT,
                severity=Severity.WARNING,
                message=(
                    f"Ping timeout "
                    f"({self.consecutive_timeouts}/"
                    f"{self.disconnect_threshold})"
                ),
                baseline_ms=self._baseline(),
            )

        # -----------------------------------------------------
        # CONNECTION RESTORED
        # -----------------------------------------------------

        if self.connection_lost:
            self.connection_lost = False
            self.consecutive_timeouts = 0

            previous_baseline = self._baseline()

            self.history.append(
                latency_ms
            )

            return DetectionResult(
                event_type=EventType.CONNECTION_RESTORED,
                severity=Severity.NORMAL,
                message=(
                    "Connection restored at "
                    f"{latency_ms:.0f} ms."
                ),
                baseline_ms=previous_baseline,
            )

        self.consecutive_timeouts = 0

        baseline = self._baseline()

        # -----------------------------------------------------
        # LEARNING PHASE
        # -----------------------------------------------------

        if (
            baseline is None
            or len(self.history) < 5
        ):
            self.history.append(
                latency_ms
            )

            return DetectionResult(
                event_type=EventType.NORMAL,
                severity=Severity.NORMAL,
                message=(
                    f"Ping: {latency_ms:.0f} ms"
                ),
                baseline_ms=baseline,
            )

        # -----------------------------------------------------
        # SPIKE LIMIT
        # -----------------------------------------------------

        spike_limit = max(
            baseline * self.spike_multiplier,
            self.minimum_spike_ms,
        )

        # -----------------------------------------------------
        # CLASSIFICATION
        # -----------------------------------------------------

        if latency_ms >= 200:
            result = DetectionResult(
                event_type=EventType.HIGH_PING,
                severity=Severity.CRITICAL,
                message=(
                    "Critical latency detected: "
                    f"{latency_ms:.0f} ms."
                ),
                baseline_ms=baseline,
            )

        elif latency_ms >= 100:
            result = DetectionResult(
                event_type=EventType.HIGH_PING,
                severity=Severity.HIGH,
                message=(
                    "High latency detected: "
                    f"{latency_ms:.0f} ms."
                ),
                baseline_ms=baseline,
            )

        elif latency_ms >= spike_limit:
            result = DetectionResult(
                event_type=EventType.PING_SPIKE,
                severity=Severity.WARNING,
                message=(
                    "Ping spike detected: "
                    f"{latency_ms:.0f} ms "
                    f"(baseline {baseline:.1f} ms)."
                ),
                baseline_ms=baseline,
            )

        else:
            result = DetectionResult(
                event_type=EventType.NORMAL,
                severity=Severity.NORMAL,
                message=(
                    f"Ping: {latency_ms:.0f} ms"
                ),
                baseline_ms=baseline,
            )

        # Normal measurements are used to improve
        # the baseline. Anomalies are not.
        if result.event_type == EventType.NORMAL:
            self.history.append(
                latency_ms
            )

        return result

    # =========================================================
    # BASELINE
    # =========================================================

    def _baseline(
        self,
    ) -> float | None:

        if not self.history:
            return None

        return mean(
            self.history
        )