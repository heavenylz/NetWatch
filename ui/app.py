import threading
import time
import os
import sys
import ctypes

import customtkinter as ctk

from config import (
    APP_NAME,
    APP_VERSION,
    DEFAULT_WINDOW_WIDTH,
    DEFAULT_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
    MIN_WINDOW_HEIGHT,
)

from core.database import Database
from core.detector import AnomalyDetector
from core.incident_manager import IncidentManager
from core.monitor import NetworkMonitor
from core.settings_manager import SettingsManager

from ui.sidebar import Sidebar
from ui.pages.dashboard import DashboardPage
from ui.pages.incidents import IncidentsPage
from ui.pages.statistics import StatisticsPage
from ui.pages.settings import SettingsPage

from ui.theme import BACKGROUND


class NetWatchApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._setup_app_identity()

        # =====================================================
        # WINDOW
        # =====================================================

        self.title(
            f"{APP_NAME} v{APP_VERSION}"
        )

        self.geometry(
            f"{DEFAULT_WINDOW_WIDTH}x"
            f"{DEFAULT_WINDOW_HEIGHT}"
        )

        self.minsize(
            MIN_WINDOW_WIDTH,
            MIN_WINDOW_HEIGHT,
        )

        self.configure(
            fg_color=BACKGROUND
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close,
        )

        ctk.set_appearance_mode(
            "dark"
        )

        ctk.set_default_color_theme(
            "blue"
        )

        # =====================================================
        # APPLICATION STATE
        # =====================================================

        self.monitoring = True
        self.closing = False

        self.current_page = None

        self.transitioning = False
        self.transition_after_ids = []

        # =====================================================
        # SETTINGS
        # =====================================================

        self.settings_manager = (
            SettingsManager()
        )

        self.settings = (
            self.settings_manager.load()
        )

        # =====================================================
        # BACKEND
        # =====================================================

        self.monitor = NetworkMonitor(
            self.settings[
                "ping_target"
            ]
        )

        self.detector = AnomalyDetector(
            spike_multiplier=self.settings[
                "spike_multiplier"
            ],
            minimum_spike_ms=self.settings[
                "minimum_spike_ms"
            ],
            disconnect_threshold=self.settings[
                "disconnect_threshold"
            ],
        )

        self.database = Database()

        self.incident_manager = (
            IncidentManager(
                self.database
            )
        )

        # =====================================================
        # WINDOW LAYOUT
        # =====================================================

        self.grid_columnconfigure(
            0,
            weight=0,
        )

        self.grid_columnconfigure(
            1,
            weight=1,
        )

        self.grid_rowconfigure(
            0,
            weight=1,
        )

        # =====================================================
        # SIDEBAR
        # =====================================================

        self.sidebar = Sidebar(
            self,

            on_dashboard=lambda: (
                self.show_page(
                    "dashboard"
                )
            ),

            on_incidents=lambda: (
                self.show_page(
                    "incidents"
                )
            ),

            on_statistics=lambda: (
                self.show_page(
                    "statistics"
                )
            ),

            on_settings=lambda: (
                self.show_page(
                    "settings"
                )
            ),
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        # =====================================================
        # PAGE AREA
        # =====================================================

        self.page_area = ctk.CTkFrame(
            self,
            fg_color=BACKGROUND,
            corner_radius=0,
        )

        self.page_area.grid(
            row=0,
            column=1,
            sticky="nsew",
        )

        self.page_area.grid_rowconfigure(
            0,
            weight=1,
        )

        self.page_area.grid_columnconfigure(
            0,
            weight=1,
        )

        # =====================================================
        # PAGE CONTAINER
        # =====================================================

        self.page_container = (
            ctk.CTkFrame(
                self.page_area,
                fg_color="transparent",
                corner_radius=0,
            )
        )

        self.page_container.grid(
            row=0,
            column=0,
            padx=35,
            pady=30,
            sticky="nsew",
        )

        self.page_container.grid_rowconfigure(
            0,
            weight=1,
        )

        self.page_container.grid_columnconfigure(
            0,
            weight=1,
        )

        # =====================================================
        # PAGES
        # =====================================================

        self.dashboard_page = (
            DashboardPage(
                self.page_container,
                monitor=self.monitor,
                history_length=(
                    self.settings[
                        "history_length"
                    ]
                ),
            )
        )

                # Apply the persisted target to the dashboard
        # during application startup.
        self.dashboard_page.update_target(
            self.monitor.host
        )

        self.incidents_page = (
            IncidentsPage(
                self.page_container,
                database=self.database,
            )
        )

        self.statistics_page = (
            StatisticsPage(
                self.page_container,
                database=self.database,
            )
        )

        self.settings_page = (
            SettingsPage(
                self.page_container,
                settings_manager=(
                    self.settings_manager
                ),
                settings=self.settings,
                on_settings_applied=(
                    self.apply_settings
                ),
            )
        )

        self.pages = {
            "dashboard":
                self.dashboard_page,

            "incidents":
                self.incidents_page,

            "statistics":
                self.statistics_page,

            "settings":
                self.settings_page,
        }

        for page in (
            self.pages.values()
        ):
            page.grid(
                row=0,
                column=0,
                sticky="nsew",
            )

            page.grid_remove()

        # =====================================================
        # INITIAL PAGE
        # =====================================================

        self.show_page(
            "dashboard",
            animate=False,
        )

        # =====================================================
        # MONITOR THREAD
        # =====================================================

        self.monitor_thread = (
            threading.Thread(
                target=self.monitor_loop,
                daemon=True,
                name="NetWatchMonitor",
            )
        )

        self.monitor_thread.start()


        # =========================================================
    # APP IDENTITY / ICON
    # =========================================================

    def _resource_path(
        self,
        relative_path,
    ):
        if hasattr(
            sys,
            "_MEIPASS",
        ):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                )
            )

        return os.path.join(
            base_path,
            relative_path,
        )

    def _setup_app_identity(self):
        # -----------------------------------------------------
        # Windows AppUserModelID
        #
        # This helps Windows identify NetWatch as its own app
        # instead of grouping it under python.exe.
        # -----------------------------------------------------

        if sys.platform == "win32":
            try:
                app_id = (
                    "heavenylz.NetWatch."
                    f"{APP_VERSION}"
                )

                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                    app_id
                )

            except Exception:
                pass

        # -----------------------------------------------------
        # Window / taskbar icon
        # -----------------------------------------------------

        try:
            icon_path = self._resource_path(
                os.path.join(
                    "assets",
                    "netwatch.ico",
                )
            )

            self.iconbitmap(
                icon_path
            )

        except Exception as error:
            print(
                "[NetWatch Icon Warning] "
                f"{type(error).__name__}: "
                f"{error}"
            )

    # =========================================================
    # NAVIGATION
    # =========================================================

    def show_page(
        self,
        page_name,
        animate=True,
    ):
        if self.closing:
            return

        if page_name not in self.pages:
            return

        # Do not redraw the page if it is already active.
        if (
            page_name == self.current_page
            and not self.transitioning
        ):
            self.sidebar.set_active(
                page_name
            )

            self._refresh_page(
                page_name
            )

            return

        # Ignore navigation spam while a transition
        # is already running.
        if self.transitioning:
            return

        if not animate:
            self._show_page_immediately(
                page_name
            )
            return

        self._start_page_transition(
            page_name
        )

    def _show_page_immediately(
        self,
        page_name,
    ):
        if self.closing:
            return

        self._hide_all_pages()

        page = self.pages[
            page_name
        ]

        page.grid()

        self.current_page = (
            page_name
        )

        self.sidebar.set_active(
            page_name
        )

        self._refresh_page(
            page_name
        )

    def _start_page_transition(
        self,
        page_name,
    ):
        self.transitioning = True

        self._cancel_transition_callbacks()

        # -----------------------------------------------------
        # Stage 1:
        # Slightly move the current container to the left.
        # -----------------------------------------------------

        self._animate_container_out(
            target_page=page_name,
            step=0,
        )

    def _animate_container_out(
        self,
        target_page,
        step,
    ):
        if self.closing:
            self.transitioning = False
            return

        # Short controlled transition.
        # 5 frames keeps Tkinter responsive.
        total_steps = 5

        if step >= total_steps:
            self._switch_transition_page(
                target_page
            )
            return

        progress = (
            step / total_steps
        )

        # Move from 35px to 48px.
        left_padding = int(
            35 + (13 * progress)
        )

        right_padding = max(
            22,
            35 - int(
                13 * progress
            ),
        )

        try:
            self.page_container.grid_configure(
                padx=(
                    left_padding,
                    right_padding,
                )
            )
        except Exception:
            self.transitioning = False
            return

        self._schedule_transition(
            18,
            lambda: (
                self._animate_container_out(
                    target_page,
                    step + 1,
                )
            ),
        )

    def _switch_transition_page(
        self,
        page_name,
    ):
        if self.closing:
            self.transitioning = False
            return

        self._hide_all_pages()

        self._refresh_page(
            page_name
        )

        page = self.pages[
            page_name
        ]

        try:
            page.grid()
        except Exception:
            self.transitioning = False
            return

        self.current_page = (
            page_name
        )

        self.sidebar.set_active(
            page_name
        )

        # Start slightly on the opposite side
        # before settling into place.
        try:
            self.page_container.grid_configure(
                padx=(22, 48)
            )
        except Exception:
            self.transitioning = False
            return

        self._animate_container_in(
            step=0
        )

    def _animate_container_in(
        self,
        step,
    ):
        if self.closing:
            self.transitioning = False
            return

        total_steps = 7

        if step >= total_steps:
            try:
                self.page_container.grid_configure(
                    padx=35
                )
            except Exception:
                pass

            self.transitioning = False
            self.transition_after_ids.clear()
            return

        progress = (
            step / total_steps
        )

        # Cubic ease-out.
        eased = (
            1
            - pow(
                1 - progress,
                3,
            )
        )

        left_padding = int(
            22 + (
                13 * eased
            )
        )

        right_padding = int(
            48 - (
                13 * eased
            )
        )

        try:
            self.page_container.grid_configure(
                padx=(
                    left_padding,
                    right_padding,
                )
            )
        except Exception:
            self.transitioning = False
            return

        self._schedule_transition(
            18,
            lambda: (
                self._animate_container_in(
                    step + 1
                )
            ),
        )

    def _hide_all_pages(self):
        for page in (
            self.pages.values()
        ):
            try:
                page.grid_remove()
            except Exception:
                pass

    def _refresh_page(
        self,
        page_name,
    ):
        if self.closing:
            return

        try:
            if page_name == "incidents":
                self.incidents_page.refresh()

            elif page_name == "statistics":
                self.statistics_page.refresh()

            elif page_name == "settings":
                self.settings_page.load_values(
                    self.settings
                )

        except Exception as error:
            if self.closing:
                return

            print(
                "[NetWatch Page Refresh Error] "
                f"{type(error).__name__}: "
                f"{error}"
            )

    # =========================================================
    # TRANSITION CALLBACKS
    # =========================================================

    def _schedule_transition(
        self,
        delay,
        callback,
    ):
        if self.closing:
            return

        try:
            after_id = self.after(
                delay,
                callback,
            )

            self.transition_after_ids.append(
                after_id
            )

        except Exception:
            pass

    def _cancel_transition_callbacks(self):
        for after_id in (
            self.transition_after_ids
        ):
            try:
                self.after_cancel(
                    after_id
                )
            except Exception:
                pass

        self.transition_after_ids.clear()

    # =========================================================
    # SETTINGS
    # =========================================================

    def apply_settings(
        self,
        new_settings,
    ):
        if self.closing:
            return

        self.settings = (
            new_settings.copy()
        )

        # -----------------------------------------------------
        # MONITOR
        # -----------------------------------------------------

        self.monitor.host = (
            self.settings[
                "ping_target"
            ]
        )

        # -----------------------------------------------------
        # DETECTOR
        # -----------------------------------------------------

        self.detector.update_settings(
            spike_multiplier=self.settings[
                "spike_multiplier"
            ],
            minimum_spike_ms=self.settings[
                "minimum_spike_ms"
            ],
            disconnect_threshold=self.settings[
                "disconnect_threshold"
            ],
        )

        # -----------------------------------------------------
        # DASHBOARD
        # -----------------------------------------------------

        self.dashboard_page.update_target(
            self.monitor.host
        )

        self.dashboard_page.resize_history(
            self.settings[
                "history_length"
            ]
        )

    # =========================================================
    # MONITORING
    # =========================================================

    def monitor_loop(self):
        while self.monitoring:
            try:
                ping_result = (
                    self.monitor.ping()
                )

                if not self.monitoring:
                    break

                detection = (
                    self.detector.analyze(
                        ping_result.latency_ms
                    )
                )

                self.incident_manager.process(
                    detection=detection,
                    latency_ms=(
                        ping_result.latency_ms
                    ),
                    timestamp=(
                        ping_result.timestamp
                    ),
                )

                if not self.monitoring:
                    break

                try:
                    self.after(
                        0,
                        self.update_dashboard,
                        ping_result,
                        detection,
                    )

                except RuntimeError:
                    break

                self._wait_for_next_check()

            except Exception as error:
                if not self.monitoring:
                    break

                print(
                    "[NetWatch Monitor Error] "
                    f"{type(error).__name__}: "
                    f"{error}"
                )

                self._safe_wait(
                    1.0
                )

    def _wait_for_next_check(self):
        try:
            interval = float(
                self.settings[
                    "check_interval"
                ]
            )

        except (
            KeyError,
            TypeError,
            ValueError,
        ):
            interval = 2.0

        self._safe_wait(
            interval
        )

    def _safe_wait(
        self,
        seconds,
    ):
        waited = 0.0

        while (
            self.monitoring
            and waited < seconds
        ):
            step = min(
                0.1,
                seconds - waited,
            )

            time.sleep(
                step
            )

            waited += step

    # =========================================================
    # UI UPDATE
    # =========================================================

    def update_dashboard(
        self,
        ping_result,
        detection,
    ):
        if (
            not self.monitoring
            or self.closing
        ):
            return

        try:
            self.dashboard_page.update_monitor(
                ping_result=ping_result,
                detection=detection,
                connection_lost=(
                    self.detector.connection_lost
                ),
            )

        except Exception as error:
            if (
                not self.monitoring
                or self.closing
            ):
                return

            print(
                "[NetWatch UI Error] "
                f"{type(error).__name__}: "
                f"{error}"
            )

    # =========================================================
    # SHUTDOWN
    # =========================================================

    def shutdown(self):
        if self.closing:
            return

        self.closing = True
        self.monitoring = False
        self.transitioning = False

        self._cancel_transition_callbacks()

        try:
            if self.winfo_exists():
                super().destroy()

        except Exception:
            pass

    def on_close(self):
        self.shutdown()