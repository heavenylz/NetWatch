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


class IncidentsPage(ctk.CTkFrame):
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

        self.incident_cards = []
        self.card_animators = []

        self.grid_columnconfigure(
            0,
            weight=1,
        )

        self.grid_rowconfigure(
            2,
            weight=1,
        )

        self._build_header()
        self._build_summary()
        self._build_incident_list()

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
            text="Incidents",
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
                "Network anomalies, latency spikes "
                "and connection events"
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

        self.refresh_button = ctk.CTkButton(
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

        self.refresh_button.grid(
            row=0,
            column=1,
            rowspan=2,
            sticky="e",
        )

    # =========================================================
    # SUMMARY BAR
    # =========================================================

    def _build_summary(self):
        self.summary = ctk.CTkFrame(
            self,
            height=62,
            corner_radius=RADIUS_LARGE,
            fg_color=SURFACE,
            border_width=1,
            border_color=BORDER,
        )

        self.summary.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=28,
            pady=(0, 16),
        )

        self.summary.grid_propagate(
            False
        )

        self.summary.grid_columnconfigure(
            1,
            weight=1,
        )

        indicator = ctk.CTkFrame(
            self.summary,
            width=10,
            height=10,
            corner_radius=5,
            fg_color=ONLINE,
        )

        indicator.grid(
            row=0,
            column=0,
            padx=(18, 10),
        )

        self.summary_label = ctk.CTkLabel(
            self.summary,
            text="Incident history ready",
            text_color=TEXT_PRIMARY,
            anchor="w",
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
        )

        self.summary_label.grid(
            row=0,
            column=1,
            sticky="w",
        )

        self.summary_count = ctk.CTkLabel(
            self.summary,
            text="0 events",
            text_color=TEXT_MUTED,
            anchor="e",
            font=ctk.CTkFont(
                size=11,
            ),
        )

        self.summary_count.grid(
            row=0,
            column=2,
            sticky="e",
            padx=18,
        )

    # =========================================================
    # INCIDENT LIST
    # =========================================================

    def _build_incident_list(self):
        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )

        self.scroll.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=(28, 20),
            pady=(0, 22),
        )

        self.scroll.grid_columnconfigure(
            0,
            weight=1,
        )

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):
        self._clear_cards()

        try:
            incidents = (
                self.database.get_incidents(
                    limit=100
                )
            )

        except Exception as error:
            self._show_error(
                error
            )
            return

        incident_count = len(
            incidents
        )

        self.summary_count.configure(
            text=(
                f"{incident_count} "
                f"{'event' if incident_count == 1 else 'events'}"
            )
        )

        if not incidents:
            self.summary_label.configure(
                text="No network incidents detected"
            )

            self._show_empty_state()
            return

        self.summary_label.configure(
            text="Network incident history"
        )

        for row, incident in enumerate(
            incidents
        ):
            self._create_incident_card(
                incident=incident,
                row=row,
            )

    # =========================================================
    # INCIDENT CARD
    # =========================================================

    def _create_incident_card(
        self,
        incident,
        row,
    ):
        incident_type = self._get_value(
            incident,
            "type",
            1,
            "UNKNOWN",
        )

        severity = self._get_value(
            incident,
            "severity",
            2,
            "NORMAL",
        )

        started_at = self._get_value(
            incident,
            "started_at",
            3,
            None,
        )

        duration = self._get_value(
            incident,
            "duration_seconds",
            5,
            None,
        )

        latency = self._get_value(
            incident,
            "latency_ms",
            6,
            None,
        )

        baseline = self._get_value(
            incident,
            "baseline_ms",
            8,
            None,
        )

        message = self._get_value(
            incident,
            "message",
            9,
            "",
        )

        severity_color = (
            self._severity_color(
                severity
            )
        )

        card = ctk.CTkFrame(
            self.scroll,
            corner_radius=RADIUS_LARGE,
            fg_color=SURFACE,
            border_width=1,
            border_color=BORDER,
        )

        card.grid(
            row=row,
            column=0,
            sticky="ew",
            pady=(0, 10),
        )

        card.grid_columnconfigure(
            2,
            weight=1,
        )

        # -----------------------------------------------------
        # Severity indicator
        # -----------------------------------------------------

        indicator = ctk.CTkFrame(
            card,
            width=4,
            corner_radius=4,
            fg_color=severity_color,
        )

        indicator.grid(
            row=0,
            column=0,
            rowspan=3,
            sticky="ns",
            padx=(0, 14),
            pady=10,
        )

        # -----------------------------------------------------
        # Icon
        # -----------------------------------------------------

        icon_frame = ctk.CTkFrame(
            card,
            width=42,
            height=42,
            corner_radius=13,
            fg_color=self._severity_background(
                severity
            ),
        )

        icon_frame.grid(
            row=0,
            column=1,
            rowspan=3,
            padx=(0, 14),
            pady=16,
        )

        icon_frame.grid_propagate(
            False
        )

        icon = ctk.CTkLabel(
            icon_frame,
            text=self._incident_icon(
                incident_type
            ),
            text_color=severity_color,
            font=ctk.CTkFont(
                size=17,
                weight="bold",
            ),
        )

        icon.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )

        # -----------------------------------------------------
        # Incident information
        # -----------------------------------------------------

        title = ctk.CTkLabel(
            card,
            text=self._format_type(
                incident_type
            ),
            text_color=TEXT_PRIMARY,
            anchor="w",
            font=ctk.CTkFont(
                size=14,
                weight="bold",
            ),
        )

        title.grid(
            row=0,
            column=2,
            sticky="sw",
            pady=(13, 0),
        )

        message_label = ctk.CTkLabel(
            card,
            text=message or "Network event detected",
            text_color=TEXT_SECONDARY,
            anchor="w",
            justify="left",
            font=ctk.CTkFont(
                size=11,
            ),
        )

        message_label.grid(
            row=1,
            column=2,
            sticky="ew",
            pady=(2, 1),
        )

        details = self._build_details(
            latency=latency,
            baseline=baseline,
            duration=duration,
        )

        details_label = ctk.CTkLabel(
            card,
            text=details,
            text_color=TEXT_MUTED,
            anchor="w",
            font=ctk.CTkFont(
                size=10,
            ),
        )

        details_label.grid(
            row=2,
            column=2,
            sticky="nw",
            pady=(0, 13),
        )

        # -----------------------------------------------------
        # Right side
        # -----------------------------------------------------

        severity_label = ctk.CTkLabel(
            card,
            text=str(
                severity
            ).upper(),
            text_color=severity_color,
            fg_color=self._severity_background(
                severity
            ),
            corner_radius=8,
            height=25,
            font=ctk.CTkFont(
                size=9,
                weight="bold",
            ),
        )

        severity_label.grid(
            row=0,
            column=3,
            sticky="e",
            padx=16,
            pady=(13, 0),
            ipadx=7,
        )

        time_label = ctk.CTkLabel(
            card,
            text=self._format_datetime(
                started_at
            ),
            text_color=TEXT_MUTED,
            anchor="e",
            font=ctk.CTkFont(
                size=10,
            ),
        )

        time_label.grid(
            row=1,
            column=3,
            rowspan=2,
            sticky="ne",
            padx=16,
            pady=(5, 0),
        )

        # -----------------------------------------------------
        # Hover animation
        # -----------------------------------------------------

        animator = ColorAnimator(
            card,
            "fg_color",
        )

        self.incident_cards.append(
            card
        )

        self.card_animators.append(
            animator
        )

        hover_widgets = [
            card,
            indicator,
            icon_frame,
            icon,
            title,
            message_label,
            details_label,
            severity_label,
            time_label,
        ]

        for widget in hover_widgets:
            widget.bind(
                "<Enter>",
                lambda event,
                a=animator: self._hover_enter(
                    a
                ),
            )

            widget.bind(
                "<Leave>",
                lambda event,
                a=animator: self._hover_leave(
                    a
                ),
            )

    # =========================================================
    # HOVER
    # =========================================================

    def _hover_enter(
        self,
        animator,
    ):
        animator.animate(
            start_color=SURFACE,
            end_color=SURFACE_HOVER,
            duration=140,
        )

    def _hover_leave(
        self,
        animator,
    ):
        animator.animate(
            start_color=SURFACE_HOVER,
            end_color=SURFACE,
            duration=200,
        )

    # =========================================================
    # EMPTY / ERROR STATES
    # =========================================================

    def _show_empty_state(self):
        container = ctk.CTkFrame(
            self.scroll,
            height=190,
            corner_radius=RADIUS_LARGE,
            fg_color=SURFACE,
            border_width=1,
            border_color=BORDER,
        )

        container.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        container.grid_propagate(
            False
        )

        icon = ctk.CTkLabel(
            container,
            text="✓",
            text_color=ONLINE,
            font=ctk.CTkFont(
                size=28,
                weight="bold",
            ),
        )

        icon.pack(
            pady=(35, 8),
        )

        title = ctk.CTkLabel(
            container,
            text="Everything looks good",
            text_color=TEXT_PRIMARY,
            font=ctk.CTkFont(
                size=15,
                weight="bold",
            ),
        )

        title.pack()

        description = ctk.CTkLabel(
            container,
            text=(
                "No network anomalies "
                "have been recorded yet."
            ),
            text_color=TEXT_MUTED,
            font=ctk.CTkFont(
                size=11,
            ),
        )

        description.pack(
            pady=(4, 0),
        )

        self.incident_cards.append(
            container
        )

    def _show_error(
        self,
        error,
    ):
        self.summary_label.configure(
            text="Unable to load incidents"
        )

        self.summary_count.configure(
            text="Error"
        )

        error_card = ctk.CTkFrame(
            self.scroll,
            corner_radius=RADIUS_LARGE,
            fg_color=SURFACE,
            border_width=1,
            border_color=CRITICAL,
        )

        error_card.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        label = ctk.CTkLabel(
            error_card,
            text=(
                "Incident history could not "
                f"be loaded.\n{error}"
            ),
            text_color=CRITICAL,
            justify="left",
            font=ctk.CTkFont(
                size=11,
            ),
        )

        label.pack(
            padx=20,
            pady=20,
        )

        self.incident_cards.append(
            error_card
        )

    # =========================================================
    # HELPERS
    # =========================================================

    def _clear_cards(self):
        for animator in (
            self.card_animators
        ):
            animator.stop()

        self.card_animators.clear()

        for card in (
            self.incident_cards
        ):
            try:
                card.destroy()
            except Exception:
                pass

        self.incident_cards.clear()

    @staticmethod
    def _get_value(
        incident,
        key,
        index,
        default=None,
    ):
        try:
            if hasattr(
                incident,
                "keys",
            ):
                keys = incident.keys()

                if key in keys:
                    value = incident[key]

                    if value is not None:
                        return value

            value = incident[index]

            if value is not None:
                return value

        except (
            IndexError,
            KeyError,
            TypeError,
        ):
            pass

        return default

    @staticmethod
    def _severity_color(
        severity,
    ):
        severity = str(
            severity
        ).upper()

        if severity == "CRITICAL":
            return CRITICAL

        if severity == "HIGH":
            return HIGH

        if severity == "WARNING":
            return WARNING

        return ONLINE

    @staticmethod
    def _severity_background(
        severity,
    ):
        severity = str(
            severity
        ).upper()

        if severity == "CRITICAL":
            return "#341719"

        if severity == "HIGH":
            return "#2D1E12"

        if severity == "WARNING":
            return "#2B230F"

        return "#16261C"

    @staticmethod
    def _incident_icon(
        incident_type,
    ):
        incident_type = str(
            incident_type
        ).upper()

        if "CONNECTION" in incident_type:
            return "×"

        if "SPIKE" in incident_type:
            return "↗"

        if "PING" in incident_type:
            return "!"

        return "•"

    @staticmethod
    def _format_type(
        incident_type,
    ):
        return (
            str(incident_type)
            .replace("_", " ")
            .title()
        )

    @staticmethod
    def _format_datetime(
        value,
    ):
        if not value:
            return "--"

        value = str(value)

        try:
            from datetime import datetime

            parsed = (
                datetime.fromisoformat(
                    value
                )
            )

            return parsed.strftime(
                "%d %b %Y  •  %H:%M:%S"
            )

        except ValueError:
            return value

    @staticmethod
    def _format_duration(
        seconds,
    ):
        if seconds is None:
            return None

        try:
            seconds = float(
                seconds
            )

        except (
            TypeError,
            ValueError,
        ):
            return None

        if seconds < 60:
            return f"{seconds:.1f}s"

        minutes = (
            seconds / 60
        )

        if minutes < 60:
            return f"{minutes:.1f}m"

        hours = (
            minutes / 60
        )

        return f"{hours:.1f}h"

    def _build_details(
        self,
        latency,
        baseline,
        duration,
    ):
        details = []

        if latency is not None:
            try:
                details.append(
                    f"Ping  {float(latency):.0f} ms"
                )
            except (
                TypeError,
                ValueError,
            ):
                pass

        if baseline is not None:
            try:
                details.append(
                    "Baseline  "
                    f"{float(baseline):.1f} ms"
                )
            except (
                TypeError,
                ValueError,
            ):
                pass

        formatted_duration = (
            self._format_duration(
                duration
            )
        )

        if formatted_duration:
            details.append(
                f"Duration  {formatted_duration}"
            )

        if not details:
            return "Network event"

        return "     •     ".join(
            details
        )

    # =========================================================
    # CLEANUP
    # =========================================================

    def destroy(self):
        for animator in (
            self.card_animators
        ):
            try:
                animator.stop()
            except Exception:
                pass

        super().destroy()