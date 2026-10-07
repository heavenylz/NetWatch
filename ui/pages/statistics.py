import customtkinter as ctk

from ui.animations import ColorAnimator
from ui.theme import (
    ACCENT,
    BACKGROUND,
    BORDER,
    CRITICAL,
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


class StatisticsPage(ctk.CTkFrame):
    def __init__(
        self,
        master,
        database,
    ):
        super().__init__(
            master,
            fg_color=BACKGROUND,
            corner_radius=0,
        )

        self.database = database

        self.card_animators = []
        self.progress_animation_ids = []

        self.grid_columnconfigure(
            0,
            weight=1,
        )

        self.grid_rowconfigure(
            3,
            weight=1,
        )

        self._build_header()
        self._build_metric_cards()
        self._build_content()

        self.refresh()

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
            text="Statistics",
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
                "Historical network performance "
                "and incident analytics"
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

        refresh_button = ctk.CTkButton(
            header,
            text="↻  Refresh",
            width=110,
            height=36,
            corner_radius=RADIUS_MEDIUM,
            fg_color=ACCENT,
            hover_color="#2563EB",
            text_color="#FFFFFF",
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
            command=self.refresh,
        )

        refresh_button.grid(
            row=0,
            column=1,
            rowspan=2,
            sticky="e",
        )

    # =========================================================
    # METRIC CARDS
    # =========================================================

    def _build_metric_cards(self):
        container = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        container.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=28,
            pady=(0, 16),
        )

        for column in range(4):
            container.grid_columnconfigure(
                column,
                weight=1,
                uniform="stat_cards",
            )

        (
            self.total_card,
            self.total_value,
            self.total_description,
        ) = self._create_metric_card(
            container,
            0,
            "TOTAL INCIDENTS",
            "0",
            "Recorded events",
            ACCENT,
        )

        (
            self.loss_card,
            self.loss_value,
            self.loss_description,
        ) = self._create_metric_card(
            container,
            1,
            "CONNECTION LOSSES",
            "0",
            "Recorded outages",
            CRITICAL,
        )

        (
            self.downtime_card,
            self.downtime_value,
            self.downtime_description,
        ) = self._create_metric_card(
            container,
            2,
            "TOTAL DOWNTIME",
            "0s",
            "Unavailable time",
            WARNING,
        )

        (
            self.highest_card,
            self.highest_value,
            self.highest_description,
        ) = self._create_metric_card(
            container,
            3,
            "HIGHEST PING",
            "--",
            "Peak incident latency",
            HIGH,
        )

    def _create_metric_card(
        self,
        parent,
        column,
        title,
        value,
        description,
        accent_color,
    ):
        card = ctk.CTkFrame(
            parent,
            height=125,
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
                0 if column == 0 else 5,
                0 if column == 3 else 5,
            ),
        )

        card.grid_propagate(
            False
        )

        accent = ctk.CTkFrame(
            card,
            width=28,
            height=3,
            corner_radius=3,
            fg_color=accent_color,
        )

        accent.pack(
            anchor="w",
            padx=17,
            pady=(15, 7),
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            text_color=TEXT_MUTED,
            anchor="w",
            font=ctk.CTkFont(
                size=9,
                weight="bold",
            ),
        )

        title_label.pack(
            fill="x",
            padx=17,
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            text_color=TEXT_PRIMARY,
            anchor="w",
            font=ctk.CTkFont(
                size=22,
                weight="bold",
            ),
        )

        value_label.pack(
            fill="x",
            padx=17,
        )

        description_label = ctk.CTkLabel(
            card,
            text=description,
            text_color=TEXT_MUTED,
            anchor="w",
            font=ctk.CTkFont(
                size=9,
            ),
        )

        description_label.pack(
            fill="x",
            padx=17,
        )

        animator = ColorAnimator(
            card,
            "fg_color",
        )

        self.card_animators.append(
            animator
        )

        widgets = [
            card,
            accent,
            title_label,
            value_label,
            description_label,
        ]

        for widget in widgets:
            widget.bind(
                "<Enter>",
                lambda event,
                a=animator: self._card_enter(a),
            )

            widget.bind(
                "<Leave>",
                lambda event,
                a=animator: self._card_leave(a),
            )

        return (
            card,
            value_label,
            description_label,
        )

    # =========================================================
    # MAIN CONTENT
    # =========================================================

    def _build_content(self):
        content = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        content.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=28,
            pady=(0, 28),
        )

        content.grid_columnconfigure(
            0,
            weight=1,
            uniform="statistics_content",
        )

        content.grid_columnconfigure(
            1,
            weight=1,
            uniform="statistics_content",
        )

        content.grid_rowconfigure(
            0,
            weight=1,
        )

        self._build_breakdown_panel(
            content
        )

        self._build_severity_panel(
            content
        )

    # =========================================================
    # INCIDENT BREAKDOWN
    # =========================================================

    def _build_breakdown_panel(
        self,
        parent,
    ):
        panel = ctk.CTkFrame(
            parent,
            corner_radius=RADIUS_LARGE,
            fg_color=SURFACE,
            border_width=1,
            border_color=BORDER,
        )

        panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 7),
        )

        title = ctk.CTkLabel(
            panel,
            text="Incident Breakdown",
            text_color=TEXT_PRIMARY,
            anchor="w",
            font=ctk.CTkFont(
                size=15,
                weight="bold",
            ),
        )

        title.pack(
            fill="x",
            padx=20,
            pady=(18, 2),
        )

        subtitle = ctk.CTkLabel(
            panel,
            text="Distribution by event type",
            text_color=TEXT_MUTED,
            anchor="w",
            font=ctk.CTkFont(
                size=10,
            ),
        )

        subtitle.pack(
            fill="x",
            padx=20,
            pady=(0, 20),
        )

        self.breakdown_rows = {}

        self._create_progress_row(
            parent=panel,
            key="connection_losses",
            label="Connection Loss",
            color=CRITICAL,
        )

        self._create_progress_row(
            parent=panel,
            key="ping_spikes",
            label="Ping Spike",
            color=WARNING,
        )

        self._create_progress_row(
            parent=panel,
            key="high_ping",
            label="High Ping",
            color=HIGH,
        )

        separator = ctk.CTkFrame(
            panel,
            height=1,
            fg_color=BORDER,
        )

        separator.pack(
            fill="x",
            padx=20,
            pady=(12, 15),
        )

        self.average_ping_label = (
            self._create_info_row(
                panel,
                "Average incident ping",
                "--",
            )
        )

        self.last_incident_label = (
            self._create_info_row(
                panel,
                "Last incident",
                "--",
            )
        )

    # =========================================================
    # SEVERITY PANEL
    # =========================================================

    def _build_severity_panel(
        self,
        parent,
    ):
        panel = ctk.CTkFrame(
            parent,
            corner_radius=RADIUS_LARGE,
            fg_color=SURFACE,
            border_width=1,
            border_color=BORDER,
        )

        panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(7, 0),
        )

        title = ctk.CTkLabel(
            panel,
            text="Severity Distribution",
            text_color=TEXT_PRIMARY,
            anchor="w",
            font=ctk.CTkFont(
                size=15,
                weight="bold",
            ),
        )

        title.pack(
            fill="x",
            padx=20,
            pady=(18, 2),
        )

        subtitle = ctk.CTkLabel(
            panel,
            text="Recorded incidents by severity",
            text_color=TEXT_MUTED,
            anchor="w",
            font=ctk.CTkFont(
                size=10,
            ),
        )

        subtitle.pack(
            fill="x",
            padx=20,
            pady=(0, 20),
        )

        self.severity_rows = {}

        self._create_severity_row(
            panel,
            "critical",
            "Critical",
            CRITICAL,
        )

        self._create_severity_row(
            panel,
            "high",
            "High",
            HIGH,
        )

        self._create_severity_row(
            panel,
            "warning",
            "Warning",
            WARNING,
        )

        self._create_severity_row(
            panel,
            "normal",
            "Normal",
            ONLINE,
        )

        self.severity_summary = ctk.CTkLabel(
            panel,
            text="No severity data yet",
            text_color=TEXT_MUTED,
            anchor="w",
            font=ctk.CTkFont(
                size=10,
            ),
        )

        self.severity_summary.pack(
            fill="x",
            padx=20,
            pady=(15, 15),
        )

    # =========================================================
    # PROGRESS ROW
    # =========================================================

    def _create_progress_row(
        self,
        parent,
        key,
        label,
        color,
    ):
        row = ctk.CTkFrame(
            parent,
            fg_color="transparent",
        )

        row.pack(
            fill="x",
            padx=20,
            pady=(0, 15),
        )

        row.grid_columnconfigure(
            0,
            weight=1,
        )

        label_widget = ctk.CTkLabel(
            row,
            text=label,
            text_color=TEXT_SECONDARY,
            anchor="w",
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
        )

        label_widget.grid(
            row=0,
            column=0,
            sticky="w",
        )

        value_widget = ctk.CTkLabel(
            row,
            text="0",
            text_color=TEXT_PRIMARY,
            anchor="e",
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
        )

        value_widget.grid(
            row=0,
            column=1,
            sticky="e",
        )

        progress = ctk.CTkProgressBar(
            row,
            height=7,
            corner_radius=4,
            fg_color="#202631",
            progress_color=color,
        )

        progress.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(7, 0),
        )

        progress.set(0)

        self.breakdown_rows[
            key
        ] = {
            "value": value_widget,
            "progress": progress,
        }

    # =========================================================
    # SEVERITY ROW
    # =========================================================

    def _create_severity_row(
        self,
        parent,
        key,
        label,
        color,
    ):
        row = ctk.CTkFrame(
            parent,
            height=50,
            corner_radius=RADIUS_MEDIUM,
            fg_color=BACKGROUND,
        )

        row.pack(
            fill="x",
            padx=20,
            pady=(0, 8),
        )

        row.pack_propagate(
            False
        )

        indicator = ctk.CTkFrame(
            row,
            width=9,
            height=9,
            corner_radius=5,
            fg_color=color,
        )

        indicator.pack(
            side="left",
            padx=(14, 10),
        )

        label_widget = ctk.CTkLabel(
            row,
            text=label,
            text_color=TEXT_SECONDARY,
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
        )

        label_widget.pack(
            side="left",
        )

        percentage = ctk.CTkLabel(
            row,
            text="0%",
            text_color=TEXT_MUTED,
            font=ctk.CTkFont(
                size=10,
            ),
        )

        percentage.pack(
            side="right",
            padx=(8, 14),
        )

        value = ctk.CTkLabel(
            row,
            text="0",
            text_color=TEXT_PRIMARY,
            font=ctk.CTkFont(
                size=13,
                weight="bold",
            ),
        )

        value.pack(
            side="right",
        )

        self.severity_rows[
            key
        ] = {
            "value": value,
            "percentage": percentage,
        }

    # =========================================================
    # INFO ROW
    # =========================================================

    def _create_info_row(
        self,
        parent,
        title,
        value,
    ):
        row = ctk.CTkFrame(
            parent,
            fg_color="transparent",
        )

        row.pack(
            fill="x",
            padx=20,
            pady=(0, 10),
        )

        title_label = ctk.CTkLabel(
            row,
            text=title,
            text_color=TEXT_MUTED,
            anchor="w",
            font=ctk.CTkFont(
                size=10,
            ),
        )

        title_label.pack(
            side="left",
        )

        value_label = ctk.CTkLabel(
            row,
            text=value,
            text_color=TEXT_PRIMARY,
            anchor="e",
            font=ctk.CTkFont(
                size=10,
                weight="bold",
            ),
        )

        value_label.pack(
            side="right",
        )

        return value_label

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):
        self._cancel_progress_animations()

        try:
            statistics = (
                self.database.get_statistics()
            )

            severity_statistics = (
                self.database
                .get_severity_statistics()
            )

        except Exception as error:
            print(
                "[NetWatch Statistics Error] "
                f"{type(error).__name__}: "
                f"{error}"
            )
            return

        total = self._number(
            self._get(
                statistics,
                "total_incidents",
                0,
            )
        )

        connection_losses = self._number(
            self._get(
                statistics,
                "connection_losses",
                0,
            )
        )

        ping_spikes = self._number(
            self._get(
                statistics,
                "ping_spikes",
                0,
            )
        )

        high_ping = self._number(
            self._get(
                statistics,
                "high_ping",
                0,
            )
        )

        downtime = self._float(
            self._get(
                statistics,
                "total_downtime",
                0,
            )
        )

        highest_ping = self._get(
            statistics,
            "highest_ping",
            None,
        )

        average_ping = self._get(
            statistics,
            "average_ping",
            None,
        )

        last_incident = self._get(
            statistics,
            "last_incident",
            None,
        )

        # -----------------------------------------------------
        # Top cards
        # -----------------------------------------------------

        self.total_value.configure(
            text=str(total)
        )

        self.loss_value.configure(
            text=str(connection_losses)
        )

        self.downtime_value.configure(
            text=self._format_duration(
                downtime
            )
        )

        if highest_ping is None:
            self.highest_value.configure(
                text="--"
            )

        else:
            try:
                self.highest_value.configure(
                    text=(
                        f"{float(highest_ping):.0f} ms"
                    )
                )

            except (
                TypeError,
                ValueError,
            ):
                self.highest_value.configure(
                    text="--"
                )

        # -----------------------------------------------------
        # Breakdown
        # -----------------------------------------------------

        breakdown = {
            "connection_losses":
                connection_losses,
            "ping_spikes":
                ping_spikes,
            "high_ping":
                high_ping,
        }

        maximum = max(
            total,
            1,
        )

        for key, value in (
            breakdown.items()
        ):
            row = self.breakdown_rows[
                key
            ]

            row["value"].configure(
                text=str(value)
            )

            target = min(
                1.0,
                value / maximum,
            )

            self._animate_progress(
                row["progress"],
                target,
            )

        # -----------------------------------------------------
        # Average
        # -----------------------------------------------------

        if average_ping is None:
            average_text = "--"

        else:
            try:
                average_text = (
                    f"{float(average_ping):.1f} ms"
                )

            except (
                TypeError,
                ValueError,
            ):
                average_text = "--"

        self.average_ping_label.configure(
            text=average_text
        )

        self.last_incident_label.configure(
            text=self._format_datetime(
                last_incident
            )
        )

        # -----------------------------------------------------
        # Severity
        # -----------------------------------------------------

        severity_values = {
            "critical": self._severity_count(
                severity_statistics,
                "CRITICAL",
            ),
            "high": self._severity_count(
                severity_statistics,
                "HIGH",
            ),
            "warning": self._severity_count(
                severity_statistics,
                "WARNING",
            ),
            "normal": self._severity_count(
                severity_statistics,
                "NORMAL",
            ),
        }

        severity_total = sum(
            severity_values.values()
        )

        for key, value in (
            severity_values.items()
        ):
            row = self.severity_rows[
                key
            ]

            row["value"].configure(
                text=str(value)
            )

            if severity_total:
                percentage = (
                    value
                    / severity_total
                    * 100
                )

            else:
                percentage = 0

            row[
                "percentage"
            ].configure(
                text=f"{percentage:.0f}%"
            )

        if severity_total:
            self.severity_summary.configure(
                text=(
                    f"{severity_total} classified "
                    "incident"
                    f"{'' if severity_total == 1 else 's'}"
                )
            )

        else:
            self.severity_summary.configure(
                text="No severity data yet"
            )

    # =========================================================
    # PROGRESS ANIMATION
    # =========================================================

    def _animate_progress(
        self,
        progress_bar,
        target,
        duration=500,
    ):
        target = max(
            0.0,
            min(
                1.0,
                target,
            ),
        )

        frames = 30
        delay = max(
            1,
            duration // frames,
        )

        current_frame = 0

        progress_bar.set(0)

        animation_id = None

        def update():
            nonlocal current_frame
            nonlocal animation_id

            try:
                if not progress_bar.winfo_exists():
                    return
            except Exception:
                return

            progress = (
                current_frame / frames
            )

            # Ease-out cubic
            eased = (
                1
                - pow(
                    1 - progress,
                    3,
                )
            )

            progress_bar.set(
                target * eased
            )

            if current_frame >= frames:
                progress_bar.set(
                    target
                )
                return

            current_frame += 1

            try:
                animation_id = self.after(
                    delay,
                    update,
                )

                self.progress_animation_ids.append(
                    animation_id
                )

            except Exception:
                pass

        update()

    def _cancel_progress_animations(self):
        for animation_id in (
            self.progress_animation_ids
        ):
            try:
                self.after_cancel(
                    animation_id
                )
            except Exception:
                pass

        self.progress_animation_ids.clear()

    # =========================================================
    # HOVER
    # =========================================================

    @staticmethod
    def _card_enter(
        animator,
    ):
        animator.animate(
            start_color=SURFACE,
            end_color=SURFACE_HOVER,
            duration=140,
        )

    @staticmethod
    def _card_leave(
        animator,
    ):
        animator.animate(
            start_color=SURFACE_HOVER,
            end_color=SURFACE,
            duration=200,
        )

    # =========================================================
    # DATA HELPERS
    # =========================================================

    @staticmethod
    def _get(
        data,
        key,
        default=None,
    ):
        if data is None:
            return default

        try:
            if hasattr(
                data,
                "keys",
            ):
                if key in data.keys():
                    value = data[key]

                    if value is not None:
                        return value

        except Exception:
            pass

        if isinstance(
            data,
            dict,
        ):
            value = data.get(
                key,
                default,
            )

            if value is not None:
                return value

        return default

    @staticmethod
    def _number(
        value,
    ):
        try:
            return int(
                value or 0
            )
        except (
            TypeError,
            ValueError,
        ):
            return 0

    @staticmethod
    def _float(
        value,
    ):
        try:
            return float(
                value or 0
            )
        except (
            TypeError,
            ValueError,
        ):
            return 0.0

    @staticmethod
    def _severity_count(
        statistics,
        severity,
    ):
        if statistics is None:
            return 0

        # Dictionary format:
        # {"CRITICAL": 2, ...}

        if isinstance(
            statistics,
            dict,
        ):
            try:
                return int(
                    statistics.get(
                        severity,
                        0,
                    )
                    or 0
                )
            except (
                TypeError,
                ValueError,
            ):
                return 0

        # SQLite row-list format.

        try:
            for row in statistics:
                if hasattr(
                    row,
                    "keys",
                ):
                    keys = row.keys()

                    if (
                        "severity" in keys
                        and str(
                            row["severity"]
                        ).upper()
                        == severity
                    ):
                        if "count" in keys:
                            return int(
                                row["count"]
                                or 0
                            )

                elif (
                    len(row) >= 2
                    and str(
                        row[0]
                    ).upper()
                    == severity
                ):
                    return int(
                        row[1] or 0
                    )

        except Exception:
            pass

        return 0

    # =========================================================
    # FORMATTING
    # =========================================================

        # =========================================================
    # FORMATTING
    # =========================================================

    @staticmethod
    def _format_duration(
        seconds,
    ):
        try:
            seconds = float(seconds)

        except (
            TypeError,
            ValueError,
        ):
            return "0s"

        if seconds < 60:
            return f"{seconds:.0f}s"

        minutes = seconds / 60

        if minutes < 60:
            return f"{minutes:.1f}m"

        hours = minutes / 60

        return f"{hours:.1f}h"

    @staticmethod
    def _format_datetime(
        value,
    ):
        if not value:
            return "--"

        # sqlite3.Row / dictionary
        if hasattr(value, "keys"):
            try:
                keys = value.keys()

                if "started_at" in keys:
                    value = value["started_at"]

                elif "timestamp" in keys:
                    value = value["timestamp"]

                else:
                    return "--"

            except Exception:
                return "--"

        # Tuple / list
        elif isinstance(
            value,
            (tuple, list),
        ):
            if not value:
                return "--"

            # incidents table:
            # id, type, severity, started_at, ...
            if len(value) > 3:
                value = value[3]
            else:
                value = value[0]

        if not value:
            return "--"

        try:
            from datetime import datetime

            parsed = datetime.fromisoformat(
                str(value)
            )

            return parsed.strftime(
                "%d %b • %H:%M"
            )

        except (
            ValueError,
            TypeError,
        ):
            return str(value)

    # =========================================================
    # CLEANUP
    # =========================================================

    def destroy(self):
        self._cancel_progress_animations()

        for animator in self.card_animators:
            try:
                animator.stop()
            except Exception:
                pass

        super().destroy()
    # =========================================================
    # CLEANUP
    # =========================================================

    def destroy(self):
        self._cancel_progress_animations()

        for animator in (
            self.card_animators
        ):
            try:
                animator.stop()
            except Exception:
                pass

        super().destroy()