import platform
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PingResult:
    timestamp: datetime
    host: str
    latency_ms: float | None
    online: bool
    error: str | None = None


class NetworkMonitor:
    def __init__(
        self,
        host: str = "1.1.1.1",
    ):
        self.host = host

    def ping(self) -> PingResult:
        timestamp = datetime.now()
        system = platform.system().lower()

        if system == "windows":
            command = [
                "ping",
                "-n",
                "1",
                "-w",
                "1500",
                self.host,
            ]

        else:
            command = [
                "ping",
                "-c",
                "1",
                "-W",
                "2",
                self.host,
            ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                errors="ignore",
                creationflags=(
                    subprocess.CREATE_NO_WINDOW
                    if system == "windows"
                    else 0
                ),
                timeout=3,
            )

        except subprocess.TimeoutExpired:
            return PingResult(
                timestamp=timestamp,
                host=self.host,
                latency_ms=None,
                online=False,
                error="PING_PROCESS_TIMEOUT",
            )

        except FileNotFoundError:
            return PingResult(
                timestamp=timestamp,
                host=self.host,
                latency_ms=None,
                online=False,
                error="PING_COMMAND_NOT_FOUND",
            )

        except OSError:
            return PingResult(
                timestamp=timestamp,
                host=self.host,
                latency_ms=None,
                online=False,
                error="SYSTEM_ERROR",
            )

        if result.returncode != 0:
            return PingResult(
                timestamp=timestamp,
                host=self.host,
                latency_ms=None,
                online=False,
                error="PING_FAILED",
            )

        latency = self._extract_latency(
            result.stdout
        )

        if latency is None:
            return PingResult(
                timestamp=timestamp,
                host=self.host,
                latency_ms=None,
                online=False,
                error="INVALID_PING_RESPONSE",
            )

        return PingResult(
            timestamp=timestamp,
            host=self.host,
            latency_ms=latency,
            online=True,
            error=None,
        )

    @staticmethod
    def _extract_latency(
        output: str,
    ) -> float | None:

        patterns = [
            r"time[=<]\s*(\d+(?:[.,]\d+)?)\s*ms",
            r"süre[=<]\s*(\d+(?:[.,]\d+)?)\s*ms",
            r"temps[=<]\s*(\d+(?:[.,]\d+)?)\s*ms",
            r"zeit[=<]\s*(\d+(?:[.,]\d+)?)\s*ms",
        ]

        output = output.lower()

        for pattern in patterns:
            match = re.search(
                pattern,
                output,
                flags=re.IGNORECASE,
            )

            if match:
                try:
                    return float(
                        match.group(1).replace(
                            ",",
                            ".",
                        )
                    )

                except ValueError:
                    continue

        return None