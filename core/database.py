import sqlite3
from core.paths import get_database_path
from pathlib import Path


class Database:
    def __init__(
        self,
        db_path=None,
    ):
        if db_path is None:
            self.db_path = (
                get_database_path()
            )
        else:
            self.db_path = Path(
                db_path
            )

            self.db_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

        self._create_tables()

    # =========================================================
    # CONNECTION
    # =========================================================

    def _connect(self):
        return sqlite3.connect(
            self.db_path
        )

    # =========================================================
    # CREATE TABLES
    # =========================================================

    def _create_tables(self):
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS incidents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    severity TEXT NOT NULL,

                    started_at TEXT NOT NULL,
                    ended_at TEXT,

                    duration_seconds REAL,

                    latency_ms REAL,
                    peak_latency_ms REAL,
                    baseline_ms REAL,

                    message TEXT
                )
                """
            )

            connection.commit()

    # =========================================================
    # CREATE INCIDENT
    # =========================================================

    def create_incident(
        self,
        incident_type: str,
        severity: str,
        started_at: str,
        latency_ms: float | None = None,
        peak_latency_ms: float | None = None,
        baseline_ms: float | None = None,
        message: str | None = None,
    ) -> int:

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO incidents (
                    type,
                    severity,
                    started_at,
                    latency_ms,
                    peak_latency_ms,
                    baseline_ms,
                    message
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    incident_type,
                    severity,
                    started_at,
                    latency_ms,
                    peak_latency_ms,
                    baseline_ms,
                    message,
                ),
            )

            connection.commit()

            return cursor.lastrowid

    # =========================================================
    # CLOSE INCIDENT
    # =========================================================

    def close_incident(
        self,
        incident_id: int,
        ended_at: str,
        duration_seconds: float,
    ):
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE incidents
                SET
                    ended_at = ?,
                    duration_seconds = ?
                WHERE id = ?
                """,
                (
                    ended_at,
                    duration_seconds,
                    incident_id,
                ),
            )

            connection.commit()

    # =========================================================
    # GET INCIDENTS
    # =========================================================

    def get_incidents(
        self,
        limit: int = 100,
    ):
        with self._connect() as connection:
            connection.row_factory = sqlite3.Row

            cursor = connection.execute(
                """
                SELECT *
                FROM incidents
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            )

            return cursor.fetchall()

    # =========================================================
    # GENERAL STATISTICS
    # =========================================================

    def get_statistics(self) -> dict:
        with self._connect() as connection:
            connection.row_factory = sqlite3.Row

            # Total incidents
            total_incidents = connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM incidents
                """
            ).fetchone()["count"]

            # Connection losses
            connection_losses = connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM incidents
                WHERE type = 'CONNECTION_LOSS'
                """
            ).fetchone()["count"]

            # Ping spikes
            ping_spikes = connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM incidents
                WHERE type = 'PING_SPIKE'
                """
            ).fetchone()["count"]

            # High ping incidents
            high_ping = connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM incidents
                WHERE type = 'HIGH_PING'
                """
            ).fetchone()["count"]

            # Total downtime
            total_downtime = connection.execute(
                """
                SELECT
                    COALESCE(
                        SUM(duration_seconds),
                        0
                    ) AS total
                FROM incidents
                WHERE type = 'CONNECTION_LOSS'
                """
            ).fetchone()["total"]

            # Highest recorded incident ping
            highest_ping = connection.execute(
                """
                SELECT
                    MAX(
                        COALESCE(
                            peak_latency_ms,
                            latency_ms
                        )
                    ) AS highest
                FROM incidents
                """
            ).fetchone()["highest"]

            # Average incident ping
            average_ping = connection.execute(
                """
                SELECT
                    AVG(
                        COALESCE(
                            peak_latency_ms,
                            latency_ms
                        )
                    ) AS average
                FROM incidents
                WHERE
                    peak_latency_ms IS NOT NULL
                    OR latency_ms IS NOT NULL
                """
            ).fetchone()["average"]

            # Last incident
            last_incident = connection.execute(
                """
                SELECT
                    type,
                    severity,
                    started_at
                FROM incidents
                ORDER BY id DESC
                LIMIT 1
                """
            ).fetchone()

            return {
                "total_incidents": total_incidents,
                "connection_losses": connection_losses,
                "ping_spikes": ping_spikes,
                "high_ping": high_ping,
                "total_downtime": total_downtime,
                "highest_ping": highest_ping,
                "average_ping": average_ping,
                "last_incident": last_incident,
            }

    # =========================================================
    # SEVERITY STATISTICS
    # =========================================================

    def get_severity_statistics(self) -> dict:
        severity_counts = {
            "NORMAL": 0,
            "WARNING": 0,
            "HIGH": 0,
            "CRITICAL": 0,
        }

        with self._connect() as connection:
            connection.row_factory = sqlite3.Row

            rows = connection.execute(
                """
                SELECT
                    severity,
                    COUNT(*) AS count
                FROM incidents
                GROUP BY severity
                """
            ).fetchall()

            for row in rows:
                severity_counts[
                    row["severity"]
                ] = row["count"]

        return severity_counts