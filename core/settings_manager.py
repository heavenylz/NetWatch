import json
from core.paths import get_settings_path

from core.validation import (
    TargetValidationError,
    validate_ping_target,
)


class SettingsManager:
    DEFAULT_SETTINGS = {
        "ping_target": "1.1.1.1",
        "check_interval": 2.0,
        "history_length": 60,
        "spike_multiplier": 2.5,
        "minimum_spike_ms": 60.0,
        "disconnect_threshold": 3,
    }

    def __init__(
        self,
        settings_path=None,
    ):
        if settings_path is None:
            self.settings_path = (
                get_settings_path()
            )
        else:
            from pathlib import Path

            self.settings_path = Path(
                settings_path
            )

            self.settings_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

    def load(self) -> dict:
        if not self.settings_path.exists():
            settings = self.DEFAULT_SETTINGS.copy()
            self.save(settings)
            return settings

        try:
            with self.settings_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                loaded_settings = json.load(file)

            # This also makes old settings files compatible
            # if new settings are added in future versions.
            settings = self.DEFAULT_SETTINGS.copy()
            settings.update(loaded_settings)

            return self.validate(settings)

        except (
            json.JSONDecodeError,
            OSError,
            TypeError,
            ValueError,
        ):
            settings = self.DEFAULT_SETTINGS.copy()
            self.save(settings)
            return settings

    def save(
        self,
        settings: dict,
    ):
        validated_settings = self.validate(
            settings
        )

        with self.settings_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                validated_settings,
                file,
                indent=4,
            )

    def reset(self) -> dict:
        settings = self.DEFAULT_SETTINGS.copy()

        self.save(settings)

        return settings

    @classmethod
    def validate(
        cls,
        settings: dict,
    ) -> dict:
        validated = cls.DEFAULT_SETTINGS.copy()

        ping_target = str(
            settings.get(
                "ping_target",
                validated["ping_target"],
            )
        ).strip()

        try:
            validated["ping_target"] = (
                validate_ping_target(
                    ping_target
                )
            )

        except TargetValidationError:
            validated["ping_target"] = (
                cls.DEFAULT_SETTINGS[
                    "ping_target"
                ]
            )

        try:
            check_interval = float(
                settings.get(
                    "check_interval",
                    validated["check_interval"],
                )
            )

            if 0.5 <= check_interval <= 60:
                validated["check_interval"] = (
                    check_interval
                )
        except (TypeError, ValueError):
            pass

        try:
            history_length = int(
                settings.get(
                    "history_length",
                    validated["history_length"],
                )
            )

            if 10 <= history_length <= 1000:
                validated["history_length"] = (
                    history_length
                )
        except (TypeError, ValueError):
            pass

        try:
            spike_multiplier = float(
                settings.get(
                    "spike_multiplier",
                    validated["spike_multiplier"],
                )
            )

            if 1.1 <= spike_multiplier <= 20:
                validated["spike_multiplier"] = (
                    spike_multiplier
                )
        except (TypeError, ValueError):
            pass

        try:
            minimum_spike_ms = float(
                settings.get(
                    "minimum_spike_ms",
                    validated["minimum_spike_ms"],
                )
            )

            if 1 <= minimum_spike_ms <= 5000:
                validated["minimum_spike_ms"] = (
                    minimum_spike_ms
                )
        except (TypeError, ValueError):
            pass

        try:
            disconnect_threshold = int(
                settings.get(
                    "disconnect_threshold",
                    validated[
                        "disconnect_threshold"
                    ],
                )
            )

            if 1 <= disconnect_threshold <= 100:
                validated["disconnect_threshold"] = (
                    disconnect_threshold
                )
        except (TypeError, ValueError):
            pass

        return validated