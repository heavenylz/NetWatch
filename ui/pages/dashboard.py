from collections import deque

import customtkinter as ctk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from ui.animations import ColorAnimator, PulseAnimator
from ui.theme import (
    ACCENT,
    BACKGROUND,
    BORDER,
    CRITICAL,
    GRAPH_BACKGROUND,
    GRAPH_GRID,
    GRAPH_LINE,
    HIGH,
    ONLINE,
    RADIUS_LARGE,
    RADIUS_MEDIUM,
    SURFACE,
    SURFACE_HOVER,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    WARNING,
)


class DashboardPage(ctk.CTkFrame):
    def __init__(
        self,
        master,
        monitor,
        history_length=60,
    ):
        super().__init__(
            master,
            fg_color=BACKGROUND,
            corner_radius=0,
        )

        self.monitor = monitor

        self.ping_history = deque(
            maxlen=history_length
        )

        self.last_latency = None
        self.connection_is_lost = False

        self._ping_flash_id = None

        self.grid_columnconfigure(
            0,
            weight=1,
        )

        self.grid_rowconfigure(
            4,
            weight=1,
        )

        self._build_header()
        self._build_status_panel()
        self._build_cards()
        self._build_graph()

        self.pulse_animator = PulseAnimator(
            self.status_orb,
            color_a=ONLINE,
            color_b="#14532D",
            duration=850,
        )

        self.ping_card_animator = ColorAnimator(
            self.ping_card,
            "fg_color",
        )

        self._redraw_graph()

    # =========================================================
    # HEADER
    # =========================================================

    def _build_header(self):
        header = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=28,
            pady=(26, 18),
        )

        header.grid_columnconfigure(
            0,
            weight=1,
        )

        title = ctk.CTkLabel(
            header,
            text="Dashboard",
            text_color=TEXT_PRIMARY,
            anchor="w",
            font=ctk.CTkFont(
                size=28,
                weight="bold",
            ),
        )

        title.grid(
            row=0,
            column=0,
            sticky="w",
        )

        subtitle = ctk.CTkLabel(
            header,
            text=(
                "Real-time network health "
                "and latency monitoring"
            ),
            text_color=TEXT_MUTED,
            anchor="w",
            font=ctk.CTkFont(
                size=12,
            ),
        )

        subtitle.grid(
            row=1,
            column=0,
            sticky="w",
            pady=(3, 0),
        )

        self.target_badge = ctk.CTkLabel(
            header,
            text="Target  •  --",
            height=32,
            corner_radius=10,
            fg_color=SURFACE,
            text_color=TEXT_SECONDARY,
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
        )

        self.target_badge.grid(
            row=0,
            column=1,
            rowspan=2,
            sticky="e",
            padx=(20, 0),
            ipadx=10,
        )

    # =========================================================
    # STATUS PANEL
    # =========================================================

    def _build_status_panel(self):
        self.status_panel = ctk.CTkFrame(
            self,
            height=92,
            corner_radius=RADIUS_LARGE,
            fg_color=SURFACE,
            border_width=1,
            border_color=BORDER,
        )

        self.status_panel.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=28,
            pady=(0, 16),
        )

        self.status_panel.grid_propagate(
            False
        )

        self.status_panel.grid_columnconfigure(
            1,
            weight=1,
        )

        # -----------------------------------------------------
        # Animated connection orb
        # -----------------------------------------------------

        self.status_orb_outer = ctk.CTkFrame(
            self.status_panel,
            width=50,
            height=50,
            corner_radius=25,
            fg_color="#16261C",
        )

        self.status_orb_outer.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(20, 14),
            pady=20,
        )

        self.status_orb_outer.grid_propagate(
            False
        )

        self.status_orb = ctk.CTkFrame(
            self.status_orb_outer,
            width=16,
            height=16,
            corner_radius=8,
            fg_color=ONLINE,
        )

        self.status_orb.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )

        # -----------------------------------------------------
        # Status text
        # -----------------------------------------------------

        self.connection_label = ctk.CTkLabel(
            self.status_panel,
            text="MONITORING",
            text_color=TEXT_MUTED,
            anchor="w",
            font=ctk.CTkFont(
                size=10,
                weight="bold",
            ),
        )

        self.connection_label.grid(
            row=0,
            column=1,
            sticky="sw",
            pady=(18, 0),
        )

        self.connection_value = ctk.CTkLabel(
            self.status_panel,
            text="Waiting for data...",
            text_color=TEXT_PRIMARY,
            anchor="w",
            font=ctk.CTkFont(
                size=18,
                weight="bold",
            ),
        )

        self.connection_value.grid(
            row=1,
            column=1,
            sticky="nw",
            pady=(0, 18),
        )

        self.status_detail = ctk.CTkLabel(
            self.status_panel,
            text="Initializing network monitor",
            text_color=TEXT_MUTED,
            anchor="e",
            font=ctk.CTkFont(
                size=11,
            ),
        )

        self.status_detail.grid(
            row=0,
            column=2,
            rowspan=2,
            sticky="e",
            padx=22,
        )

    # =========================================================
    # METRIC CARDS
    # =========================================================

    def _build_cards(self):
        cards = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        cards.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=28,
            pady=(0, 16),
        )

        for column in range(3):
            cards.grid_columnconfigure(
                column,
                weight=1,
                uniform="dashboard_cards",
            )

        # -----------------------------------------------------
        # Ping
        # -----------------------------------------------------

        (
            self.ping_card,
            self.ping_value,
            self.ping_description,
        ) = self._create_metric_card(
            parent=cards,
            column=0,
            title="CURRENT PING",
            value="-- ms",
            description="Waiting for measurement",
        )

        # -----------------------------------------------------
        # Baseline
        # -----------------------------------------------------

        (
            self.baseline_card,
            self.baseline_value,
            self.baseline_description,
        ) = self._create_metric_card(
            parent=cards,
            column=1,
            title="BASELINE",
            value="-- ms",
            description="Learning normal latency",
        )

        # -----------------------------------------------------
        # Network state
        # -----------------------------------------------------

        (
            self.health_card,
            self.health_value,
            self.health_description,
        ) = self._create_metric_card(
            parent=cards,
            column=2,
            title="NETWORK HEALTH",
            value="Learning",
            description="Collecting samples",
        )

    def _create_metric_card(
        self,
        parent,
        column,
        title,
        value,
        description,
    ):
        card = ctk.CTkFrame(
            parent,
            height=122,
            corner_radius=RADIUS_LARGE,
            fg_color=SURFACE,
            border_width=1,
            border_color=BORDER,
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=(
                0 if column == 0 else 6,
                0 if column == 2 else 6,
            ),
        )

        card.grid_propagate(
            False
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            text_color=TEXT_MUTED,
            anchor="w",
            font=ctk.CTkFont(
                size=10,
                weight="bold",
            ),
        )

        title_label.pack(
            fill="x",
            padx=18,
            pady=(16, 2),
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            text_color=TEXT_PRIMARY,
            anchor="w",
            font=ctk.CTkFont(
                size=24,
                weight="bold",
            ),
        )

        value_label.pack(
            fill="x",
            padx=18,
        )

        description_label = ctk.CTkLabel(
            card,
            text=description,
            text_color=TEXT_MUTED,
            anchor="w",
            font=ctk.CTkFont(
                size=10,
            ),
        )

        description_label.pack(
            fill="x",
            padx=18,
            pady=(2, 12),
        )

        return (
            card,
            value_label,
            description_label,
        )

    # =========================================================
    # GRAPH
    # =========================================================

    def _build_graph(self):
        graph_container = ctk.CTkFrame(
            self,
            corner_radius=RADIUS_LARGE,
            fg_color=SURFACE,
            border_width=1,
            border_color=BORDER,
        )

        graph_container.grid(
            row=4,
            column=0,
            sticky="nsew",
            padx=28,
            pady=(0, 28),
        )

        graph_container.grid_columnconfigure(
            0,
            weight=1,
        )

        graph_container.grid_rowconfigure(
            1,
            weight=1,
        )

        # -----------------------------------------------------
        # Graph header
        # -----------------------------------------------------

        graph_header = ctk.CTkFrame(
            graph_container,
            fg_color="transparent",
        )

        graph_header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=18,
            pady=(15, 5),
        )

        graph_header.grid_columnconfigure(
            0,
            weight=1,
        )

        graph_title = ctk.CTkLabel(
            graph_header,
            text="Ping History",
            text_color=TEXT_PRIMARY,
            anchor="w",
            font=ctk.CTkFont(
                size=15,
                weight="bold",
            ),
        )

        graph_title.grid(
            row=0,
            column=0,
            sticky="w",
        )

        self.graph_status = ctk.CTkLabel(
            graph_header,
            text="● LIVE",
            text_color=ONLINE,
            anchor="e",
            font=ctk.CTkFont(
                size=10,
                weight="bold",
            ),
        )

        self.graph_status.grid(
            row=0,
            column=1,
            sticky="e",
        )

        # -----------------------------------------------------
        # Matplotlib
        # -----------------------------------------------------

        self.figure = Figure(
            figsize=(8, 3.5),
            dpi=100,
            facecolor=GRAPH_BACKGROUND,
        )

        self.axis = (
            self.figure.add_subplot(111)
        )

        self.axis.set_facecolor(
            GRAPH_BACKGROUND
        )

        self.figure.subplots_adjust(
            left=0.075,
            right=0.98,
            top=0.94,
            bottom=0.16,
        )

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=graph_container,
        )

        canvas_widget = (
            self.canvas.get_tk_widget()
        )

        canvas_widget.configure(
            background=GRAPH_BACKGROUND,
            highlightthickness=0,
        )

        canvas_widget.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=14,
            pady=(5, 14),
        )

    # =========================================================
    # PUBLIC UPDATE API
    # =========================================================

    def update_monitor(
        self,
        ping_result,
        detection,
        connection_lost,
    ):
        latency = ping_result.latency_ms

        self.connection_is_lost = (
            connection_lost
        )

        # -----------------------------------------------------
        # Connection state
        # -----------------------------------------------------

        if connection_lost:
            self._set_offline_state()

        elif latency is None:
            self._set_timeout_state(
                detection
            )

        else:
            self._set_online_state(
                latency,
                detection,
            )

        # -----------------------------------------------------
        # Baseline
        # -----------------------------------------------------

        baseline = (
            detection.baseline_ms
        )

        if baseline is None:
            self.baseline_value.configure(
                text="Learning"
            )

            self.baseline_description.configure(
                text="Collecting normal samples"
            )

        else:
            self.baseline_value.configure(
                text=f"{baseline:.1f} ms"
            )

            self.baseline_description.configure(
                text="Average normal latency"
            )

        # -----------------------------------------------------
        # Graph
        # -----------------------------------------------------

        self.update_graph(
            latency
        )

    def update_target(
        self,
        target,
    ):
        self.target_badge.configure(
            text=f"Target  •  {target}"
        )

    def resize_history(
        self,
        history_length,
    ):
        old_history = list(
            self.ping_history
        )

        self.ping_history = deque(
            old_history[
                -history_length:
            ],
            maxlen=history_length,
        )

        self._redraw_graph()

    # =========================================================
    # CONNECTION STATES
    # =========================================================

    def _set_online_state(
        self,
        latency,
        detection,
    ):
        self.connection_value.configure(
            text="Online",
            text_color=ONLINE,
        )

        self.connection_label.configure(
            text="CONNECTION STATUS"
        )

        self.status_orb_outer.configure(
            fg_color="#16261C"
        )

        self.status_orb.configure(
            fg_color=ONLINE
        )

        self.status_detail.configure(
            text="Connection responding normally"
        )

        self.graph_status.configure(
            text="● LIVE",
            text_color=ONLINE,
        )

        if not self.pulse_animator.running:
            self.pulse_animator.start()

        self._update_ping_state(
            latency,
            detection,
        )

    def _set_timeout_state(
        self,
        detection,
    ):
        self.pulse_animator.stop()

        self.connection_value.configure(
            text="Unstable",
            text_color=WARNING,
        )

        self.status_orb_outer.configure(
            fg_color="#33270E"
        )

        self.status_orb.configure(
            fg_color=WARNING
        )

        self.status_detail.configure(
            text=detection.message
        )

        self.ping_value.configure(
            text="Timeout",
            text_color=WARNING,
        )

        self.ping_description.configure(
            text="No ping response received"
        )

        self.health_value.configure(
            text="Warning",
            text_color=WARNING,
        )

        self.health_description.configure(
            text="Packet response interrupted"
        )

        self.graph_status.configure(
            text="● DEGRADED",
            text_color=WARNING,
        )

    def _set_offline_state(self):
        self.pulse_animator.stop()

        self.connection_value.configure(
            text="Offline",
            text_color=CRITICAL,
        )

        self.status_orb_outer.configure(
            fg_color="#341719"
        )

        self.status_orb.configure(
            fg_color=CRITICAL
        )

        self.status_detail.configure(
            text="Connection unavailable"
        )

        self.ping_value.configure(
            text="-- ms",
            text_color=CRITICAL,
        )

        self.ping_description.configure(
            text="No connection"
        )

        self.health_value.configure(
            text="Critical",
            text_color=CRITICAL,
        )

        self.health_description.configure(
            text="Connection lost"
        )

        self.graph_status.configure(
            text="● OFFLINE",
            text_color=CRITICAL,
        )

    # =========================================================
    # PING STATE
    # =========================================================

    def _update_ping_state(
        self,
        latency,
        detection,
    ):
        if latency >= 200:
            ping_color = CRITICAL
            health = "Critical"
            description = "Severe latency"

        elif latency >= 100:
            ping_color = HIGH
            health = "Poor"
            description = "High latency"

        elif detection.severity.value == "WARNING":
            ping_color = WARNING
            health = "Warning"
            description = "Latency spike detected"

        else:
            ping_color = ONLINE
            health = "Healthy"
            description = "Connection looks stable"

        self.ping_value.configure(
            text=f"{latency:.0f} ms",
            text_color=ping_color,
        )

        self.health_value.configure(
            text=health,
            text_color=ping_color,
        )

        self.health_description.configure(
            text=description
        )

        if self.last_latency is None:
            self.ping_description.configure(
                text="First measurement"
            )

        else:
            difference = (
                latency
                - self.last_latency
            )

            if abs(difference) < 1:
                change_text = (
                    "Stable since last sample"
                )

            elif difference > 0:
                change_text = (
                    f"+{difference:.0f} ms "
                    "since last sample"
                )

            else:
                change_text = (
                    f"{difference:.0f} ms "
                    "since last sample"
                )

            self.ping_description.configure(
                text=change_text
            )

        self.last_latency = latency

        self._flash_ping_card(
            ping_color
        )

    # =========================================================
    # CARD ANIMATION
    # =========================================================

    def _flash_ping_card(
        self,
        status_color,
    ):
        if self._ping_flash_id:
            try:
                self.after_cancel(
                    self._ping_flash_id
                )
            except Exception:
                pass

            self._ping_flash_id = None

        # Use a subtle tint depending on
        # the current network state.

        if status_color == ONLINE:
            flash_color = "#14241B"

        elif status_color == WARNING:
            flash_color = "#2B230F"

        elif status_color == HIGH:
            flash_color = "#2D1E12"

        else:
            flash_color = "#2D1719"

        self.ping_card_animator.animate(
            start_color=SURFACE,
            end_color=flash_color,
            duration=120,
        )

        self._ping_flash_id = self.after(
            160,
            lambda: (
                self.ping_card_animator.animate(
                    start_color=flash_color,
                    end_color=SURFACE,
                    duration=260,
                )
            ),
        )

    # =========================================================
    # GRAPH
    # =========================================================

    def update_graph(
        self,
        latency,
    ):
        self.ping_history.append(
            latency
        )

        self._redraw_graph()

    def _redraw_graph(self):
        self.axis.clear()

        self.axis.set_facecolor(
            GRAPH_BACKGROUND
        )

        history = list(
            self.ping_history
        )

        # None values represent ping timeouts.
        valid_x = []
        valid_y = []

        for index, value in enumerate(
            history
        ):
            if value is not None:
                valid_x.append(index)
                valid_y.append(value)

        if valid_y:
            self.axis.plot(
                valid_x,
                valid_y,
                color=GRAPH_LINE,
                linewidth=2.0,
            )

            self.axis.fill_between(
                valid_x,
                valid_y,
                0,
                color=GRAPH_LINE,
                alpha=0.08,
            )

            latest_x = valid_x[-1]
            latest_y = valid_y[-1]

            self.axis.scatter(
                [latest_x],
                [latest_y],
                color=GRAPH_LINE,
                s=28,
                zorder=5,
            )

        # -----------------------------------------------------
        # Graph appearance
        # -----------------------------------------------------

        self.axis.grid(
            True,
            color=GRAPH_GRID,
            linewidth=0.7,
            alpha=0.55,
        )

        self.axis.tick_params(
            axis="x",
            colors=TEXT_MUTED,
            labelsize=8,
        )

        self.axis.tick_params(
            axis="y",
            colors=TEXT_MUTED,
            labelsize=8,
        )

        self.axis.set_ylabel(
            "Latency (ms)",
            color=TEXT_MUTED,
            fontsize=8,
        )

        for spine in (
            self.axis.spines.values()
        ):
            spine.set_visible(False)

        if history:
            self.axis.set_xlim(
                0,
                max(
                    len(history) - 1,
                    10,
                ),
            )

        if valid_y:
            highest = max(
                valid_y
            )

            upper_limit = max(
                50,
                highest * 1.25,
            )

            self.axis.set_ylim(
                0,
                upper_limit,
            )

        else:
            self.axis.set_ylim(
                0,
                100,
            )

        try:
            self.canvas.draw_idle()

        except Exception:
            pass

    # =========================================================
    # CLEANUP
    # =========================================================

    def destroy(self):
        try:
            if hasattr(
                self,
                "pulse_animator",
            ):
                self.pulse_animator.stop()

            if (
                self._ping_flash_id
                is not None
            ):
                self.after_cancel(
                    self._ping_flash_id
                )

        except Exception:
            pass

        super().destroy()