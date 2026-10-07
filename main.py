import sys
import traceback

from config import APP_NAME, APP_VERSION
from ui.app import NetWatchApp


def main():
    app = None

    try:
        app = NetWatchApp()
        app.mainloop()

    except KeyboardInterrupt:
        print(
            f"\n{APP_NAME} v{APP_VERSION} stopped."
        )

    except Exception:
        print(
            f"\n{APP_NAME} encountered "
            "an unexpected error.\n",
            file=sys.stderr,
        )

        traceback.print_exc()

        input(
            "\nPress Enter to close..."
        )

    finally:
        if app is not None:
            try:
                app.shutdown()
            except Exception:
                pass


if __name__ == "__main__":
    main()