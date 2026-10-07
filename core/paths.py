import os
import sys
from pathlib import Path


APP_FOLDER_NAME = "NetWatch"


def get_app_data_dir() -> Path:
    """
    Return the directory used for persistent
    NetWatch runtime data.
    """

    if sys.platform == "win32":
        local_app_data = os.getenv(
            "LOCALAPPDATA"
        )

        if local_app_data:
            app_data_dir = (
                Path(local_app_data)
                / APP_FOLDER_NAME
            )

        else:
            app_data_dir = (
                Path.home()
                / "AppData"
                / "Local"
                / APP_FOLDER_NAME
            )

    else:
        app_data_dir = (
            Path.home()
            / ".netwatch"
        )

    app_data_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    return app_data_dir


def get_settings_path() -> Path:
    return (
        get_app_data_dir()
        / "settings.json"
    )


def get_database_path() -> Path:
    return (
        get_app_data_dir()
        / "netwatch.db"
    )