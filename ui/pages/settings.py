import customtkinter as ctk

from core.validation import (
    TargetValidationError,
    validate_ping_target,
)

from ui.animations import ColorAnimator
from ui.theme import (
    ACCENT,
    BACKGROUND,
    BORDER,
    CRITICAL,
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


class SettingsPage(ctk.CTkFrame):
    def __init__(
        self,
        master,
        settings_manager,
        settings,
        on_settings_applied,
    ):
        super().__init__(
            master,
            fg_color=BACKGROUND,
            corner_radius=0,
        )

        self.settings_manager = settings_manager
        self.settings = settings
        self.on_settings_applied = (
            on_settings_applied
        )

        self.card_animators = []
        self.feedback_after_id = None

        self.entries = {}

        self.grid_columnconfigure(
            0,
            weight=1,
        )

        self.grid_rowconfigure(
            1,
            weight=1,
        )

        self._build_header()
        self._build_content()

        self.load_values()

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
            text="Settings",
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
                "Configure monitoring behaviour "
                "and anomaly detection"
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

        self.feedback_badge = ctk.CTkLabel(
            header,
            text="",
            width=0,
            height=32,
            corner_radius=RADIUS_MEDIUM,
            fg_color="transparent",
            text_color=TEXT_MUTED,
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
        )

        self.feedback_badge.grid(
            row=0,
            column=1,
            rowspan=2,
            sticky="e",
        )

    # =========================================================
    # CONTENT
    # =========================================================

    def _build_content(self):
        self.content = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )

        self.content.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(28, 20),
            pady=(0, 28),
        )

        self.content.grid_columnconfigure(
            0,
            weight=1,
            uniform="settings_columns",
        )

        self.content.grid_columnconfigure(
            1,
            weight=1,
            uniform="settings_columns",
        )

        # -----------------------------------------------------
        # Monitoring
        # -----------------------------------------------------

        monitoring_card = (
            self._create_section_card(
                parent=self.content,
                row=0,
                column=0,
                title="Monitoring",
                description=(
                    "Configure the target and "
                    "sampling behaviour."
                ),
                icon="◉",
            )
        )

        self._create_setting_field(
            parent=monitoring_card,
            key="ping_target",
            label="Ping Target",
            description=(
                "IP address or hostname "
                "used for connectivity checks."
            ),
            placeholder="1.1.1.1",
        )

        self._create_setting_field(
            parent=monitoring_card,
            key="check_interval",
            label="Check Interval",
            description=(
                "Seconds between each "
                "network measurement."
            ),
            placeholder="2.0",
            suffix="seconds",
        )

        self._create_setting_field(
            parent=monitoring_card,
            key="history_length",
            label="History Length",
            description=(
                "Number of recent samples "
                "shown in Ping History."
            ),
            placeholder="60",
            suffix="samples",
        )

        # -----------------------------------------------------
        # Detection
        # -----------------------------------------------------

        detection_card = (
            self._create_section_card(
                parent=self.content,
                row=0,
                column=1,
                title="Anomaly Detection",
                description=(
                    "Control how NetWatch "
                    "classifies network problems."
                ),
                icon="⌁",
            )
        )

        self._create_setting_field(
            parent=detection_card,
            key="spike_multiplier",
            label="Spike Multiplier",
            description=(
                "Latency multiplier required "
                "to classify a ping spike."
            ),
            placeholder="2.5",
            suffix="× baseline",
        )

        self._create_setting_field(
            parent=detection_card,
            key="minimum_spike_ms",
            label="Minimum Spike",
            description=(
                "Minimum latency before a "
                "sample can count as a spike."
            ),
            placeholder="60",
            suffix="ms",
        )

        self._create_setting_field(
            parent=detection_card,
            key="disconnect_threshold",
            label="Disconnect Threshold",
            description=(
                "Consecutive timeouts required "
                "before declaring connection loss."
            ),
            placeholder="3",
            suffix="timeouts",
        )

        # -----------------------------------------------------
        # Action panel
        # -----------------------------------------------------

        self._build_action_panel()

    # =========================================================
    # SECTION CARD
    # =========================================================

    def _create_section_card(
        self,
        parent,
        row,
        column,
        title,
        description,
        icon,
    ):
        card = ctk.CTkFrame(
            parent,
            corner_radius=RADIUS_LARGE,
            fg_color=SURFACE,
            border_width=1,
            border_color=BORDER,
        )

        card.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=(
                0 if column == 0 else 7,
                7 if column == 0 else 0,
            ),
        )

        card.grid_columnconfigure(
            0,
            weight=1,
        )

        header = ctk.CTkFrame(
            card,
            fg_color="transparent",
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(20, 16),
        )

        icon_frame = ctk.CTkFrame(
            header,
            width=42,
            height=42,
            corner_radius=13,
            fg_color="#172554",
        )

        icon_frame.pack(
            side="left",
            padx=(0, 12),
        )

        icon_frame.pack_propagate(
            False
        )

        icon_label = ctk.CTkLabel(
            icon_frame,
            text=icon,
            text_color=ACCENT,
            font=ctk.CTkFont(
                size=17,
                weight="bold",
            ),
        )

        icon_label.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )

        title_area = ctk.CTkFrame(
            header,
            fg_color="transparent",
        )

        title_area.pack(
            side="left",
            fill="x",
            expand=True,
        )

        title_label = ctk.CTkLabel(
            title_area,
            text=title,
            text_color=TEXT_PRIMARY,
            anchor="w",
            font=ctk.CTkFont(
                size=15,
                weight="bold",
            ),
        )

        title_label.pack(
            fill="x",
        )

        description_label = ctk.CTkLabel(
            title_area,
            text=description,
            text_color=TEXT_MUTED,
            anchor="w",
            justify="left",
            font=ctk.CTkFont(
                size=10,
            ),
        )

        description_label.pack(
            fill="x",
            pady=(2, 0),
        )

        separator = ctk.CTkFrame(
            card,
            height=1,
            fg_color=BORDER,
        )

        separator.pack(
            fill="x",
            padx=20,
            pady=(0, 4),
        )

        animator = ColorAnimator(
            card,
            "fg_color",
        )

        self.card_animators.append(
            animator
        )

        return card

    # =========================================================
    # SETTING FIELD
    # =========================================================

    def _create_setting_field(
        self,
        parent,
        key,
        label,
        description,
        placeholder,
        suffix=None,
    ):
        container = ctk.CTkFrame(
            parent,
            fg_color="transparent",
        )

        container.pack(
            fill="x",
            padx=20,
            pady=(12, 4),
        )

        label_widget = ctk.CTkLabel(
            container,
            text=label,
            text_color=TEXT_PRIMARY,
            anchor="w",
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
        )

        label_widget.pack(
            fill="x",
        )

        description_widget = ctk.CTkLabel(
            container,
            text=description,
            text_color=TEXT_MUTED,
            anchor="w",
            justify="left",
            font=ctk.CTkFont(
                size=9,
            ),
        )

        description_widget.pack(
            fill="x",
            pady=(2, 7),
        )

        entry_row = ctk.CTkFrame(
            container,
            fg_color="transparent",
        )

        entry_row.pack(
            fill="x",
        )

        entry_row.grid_columnconfigure(
            0,
            weight=1,
        )

        entry = ctk.CTkEntry(
            entry_row,
            height=38,
            corner_radius=RADIUS_MEDIUM,
            fg_color=BACKGROUND,
            border_width=1,
            border_color=BORDER,
            text_color=TEXT_PRIMARY,
            placeholder_text=placeholder,
            placeholder_text_color=TEXT_MUTED,
            font=ctk.CTkFont(
                size=11,
            ),
        )

        entry.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        if suffix:
            suffix_label = ctk.CTkLabel(
                entry_row,
                text=suffix,
                text_color=TEXT_MUTED,
                anchor="e",
                font=ctk.CTkFont(
                    size=9,
                ),
            )

            suffix_label.grid(
                row=0,
                column=1,
                padx=(10, 0),
            )

        error_label = ctk.CTkLabel(
            container,
            text="",
            text_color=CRITICAL,
            anchor="w",
            font=ctk.CTkFont(
                size=9,
            ),
        )

        error_label.pack(
            fill="x",
            pady=(3, 0),
        )

        self.entries[
            key
        ] = {
            "entry": entry,
            "error": error_label,
        }

    # =========================================================
    # ACTION PANEL
    # =========================================================

    def _build_action_panel(self):
        panel = ctk.CTkFrame(
            self.content,
            height=82,
            corner_radius=RADIUS_LARGE,
            fg_color=SURFACE,
            border_width=1,
            border_color=BORDER,
        )

        panel.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(16, 0),
        )

        panel.grid_propagate(
            False
        )

        panel.grid_columnconfigure(
            0,
            weight=1,
        )

        text_area = ctk.CTkFrame(
            panel,
            fg_color="transparent",
        )

        text_area.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
        )

        title = ctk.CTkLabel(
            text_area,
            text="Configuration",
            text_color=TEXT_PRIMARY,
            anchor="w",
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
        )

        title.pack(
            fill="x",
        )

        description = ctk.CTkLabel(
            text_area,
            text=(
                "Changes are applied immediately "
                "without restarting NetWatch."
            ),
            text_color=TEXT_MUTED,
            anchor="w",
            font=ctk.CTkFont(
                size=9,
            ),
        )

        description.pack(
            fill="x",
            pady=(2, 0),
        )

        self.reset_button = ctk.CTkButton(
            panel,
            text="Reset Defaults",
            width=125,
            height=38,
            corner_radius=RADIUS_MEDIUM,
            fg_color=BACKGROUND,
            hover_color=SURFACE_HOVER,
            border_width=1,
            border_color=BORDER,
            text_color=TEXT_SECONDARY,
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
            command=self.reset,
        )

        self.reset_button.grid(
            row=0,
            column=1,
            padx=(10, 8),
        )

        self.save_button = ctk.CTkButton(
            panel,
            text="Save Changes",
            width=125,
            height=38,
            corner_radius=RADIUS_MEDIUM,
            fg_color=ACCENT,
            hover_color="#2563EB",
            text_color="#FFFFFF",
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
            command=self.save,
        )

        self.save_button.grid(
            row=0,
            column=2,
            padx=(0, 20),
        )

    # =========================================================
    # LOAD VALUES
    # =========================================================

    def load_values(
        self,
        settings=None,
    ):
        if settings is not None:
            self.settings = settings

        for key, widgets in (
            self.entries.items()
        ):
            entry = widgets["entry"]

            entry.delete(
                0,
                "end",
            )

            value = self.settings.get(
                key,
                "",
            )

            entry.insert(
                0,
                str(value),
            )

            self._clear_field_error(
                key
            )   

    # =========================================================
    # SAVE
    # =========================================================

    def save(self):
        self._clear_all_errors()

        try:
            new_settings = (
                self._read_form()
            )

            self._validate(
                new_settings
            )

        except TargetValidationError as error:
            self._set_field_error(
                "ping_target",
                str(error),
            )

            self._show_feedback(
                "Invalid ping target",
                CRITICAL,
            )
            return

        except ValueError as error:
            self._show_feedback(
                str(error),
                CRITICAL,
            )
            return

        try:
            self._persist_settings(
                new_settings
            )

            self.settings.clear()
            self.settings.update(
                new_settings
            )

            if self.on_settings_applied:
                self.on_settings_applied(
                    self.settings
                )

            self._show_feedback(
                "✓  Settings saved",
                ONLINE,
            )

            self._flash_save_button()

        except Exception as error:
            self._show_feedback(
                "Unable to save settings",
                CRITICAL,
            )

            print(
                "[NetWatch Settings Error] "
                f"{type(error).__name__}: "
                f"{error}"
            )

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):
        self._clear_all_errors()

        try:
            defaults = (
                self._get_defaults()
            )

            self.settings.clear()
            self.settings.update(
                defaults
            )

            self._persist_settings(
                self.settings
            )

            self.load_values()

            if self.on_settings_applied:
                self.on_settings_applied(
                    self.settings
                )

            self._show_feedback(
                "↻  Defaults restored",
                WARNING,
            )

        except Exception as error:
            self._show_feedback(
                "Unable to reset settings",
                CRITICAL,
            )

            print(
                "[NetWatch Settings Error] "
                f"{type(error).__name__}: "
                f"{error}"
            )

    # =========================================================
    # FORM
    # =========================================================

    def _read_form(self):
        ping_target = (
            self.entries[
                "ping_target"
            ]["entry"]
            .get()
            .strip()
        )

        check_interval_text = (
            self.entries[
                "check_interval"
            ]["entry"]
            .get()
            .strip()
        )

        history_length_text = (
            self.entries[
                "history_length"
            ]["entry"]
            .get()
            .strip()
        )

        spike_multiplier_text = (
            self.entries[
                "spike_multiplier"
            ]["entry"]
            .get()
            .strip()
        )

        minimum_spike_text = (
            self.entries[
                "minimum_spike_ms"
            ]["entry"]
            .get()
            .strip()
        )

        disconnect_text = (
            self.entries[
                "disconnect_threshold"
            ]["entry"]
            .get()
            .strip()
        )

        try:
            check_interval = float(
                check_interval_text
            )
        except ValueError:
            self._set_field_error(
                "check_interval",
                "Enter a valid number.",
            )
            raise ValueError(
                "Check interval is invalid."
            )

        try:
            history_length = int(
                history_length_text
            )
        except ValueError:
            self._set_field_error(
                "history_length",
                "Enter a whole number.",
            )
            raise ValueError(
                "History length is invalid."
            )

        try:
            spike_multiplier = float(
                spike_multiplier_text
            )
        except ValueError:
            self._set_field_error(
                "spike_multiplier",
                "Enter a valid number.",
            )
            raise ValueError(
                "Spike multiplier is invalid."
            )

        try:
            minimum_spike_ms = float(
                minimum_spike_text
            )
        except ValueError:
            self._set_field_error(
                "minimum_spike_ms",
                "Enter a valid number.",
            )
            raise ValueError(
                "Minimum spike is invalid."
            )

        try:
            disconnect_threshold = int(
                disconnect_text
            )
        except ValueError:
            self._set_field_error(
                "disconnect_threshold",
                "Enter a whole number.",
            )
            raise ValueError(
                "Disconnect threshold is invalid."
            )

        return {
            "ping_target": ping_target,
            "check_interval": check_interval,
            "history_length": history_length,
            "spike_multiplier": spike_multiplier,
            "minimum_spike_ms": minimum_spike_ms,
            "disconnect_threshold":
                disconnect_threshold,
        }

    # =========================================================
    # VALIDATION
    # =========================================================

    def _validate(
        self,
        settings,
    ):
        validated_target = (
            validate_ping_target(
                settings[
                    "ping_target"
                ]
            )
        )

        settings[
            "ping_target"
        ] = validated_target

        has_error = False

        if settings["check_interval"] <= 0:
            self._set_field_error(
                "check_interval",
                "Must be greater than 0.",
            )
            has_error = True

        elif settings["check_interval"] > 3600:
            self._set_field_error(
                "check_interval",
                "Maximum is 3600 seconds.",
            )
            has_error = True

        if settings["history_length"] < 10:
            self._set_field_error(
                "history_length",
                "Minimum is 10 samples.",
            )
            has_error = True

        elif settings["history_length"] > 5000:
            self._set_field_error(
                "history_length",
                "Maximum is 5000 samples.",
            )
            has_error = True

        if settings["spike_multiplier"] <= 1:
            self._set_field_error(
                "spike_multiplier",
                "Must be greater than 1.",
            )
            has_error = True

        elif settings["spike_multiplier"] > 20:
            self._set_field_error(
                "spike_multiplier",
                "Maximum is 20.",
            )
            has_error = True

        if settings["minimum_spike_ms"] <= 0:
            self._set_field_error(
                "minimum_spike_ms",
                "Must be greater than 0.",
            )
            has_error = True

        elif settings["minimum_spike_ms"] > 10000:
            self._set_field_error(
                "minimum_spike_ms",
                "Maximum is 10000 ms.",
            )
            has_error = True

        if settings["disconnect_threshold"] < 1:
            self._set_field_error(
                "disconnect_threshold",
                "Minimum is 1 timeout.",
            )
            has_error = True

        elif settings["disconnect_threshold"] > 100:
            self._set_field_error(
                "disconnect_threshold",
                "Maximum is 100 timeouts.",
            )
            has_error = True

        if has_error:
            raise ValueError(
                "Check the highlighted settings."
            )

    # =========================================================
    # SETTINGS MANAGER COMPATIBILITY
    # =========================================================

    def _persist_settings(
        self,
        settings,
    ):
        """
        Supports the common SettingsManager APIs
        without changing the rest of NetWatch.
        """

        if hasattr(
            self.settings_manager,
            "save",
        ):
            self.settings_manager.save(
                settings
            )
            return

        if hasattr(
            self.settings_manager,
            "save_settings",
        ):
            self.settings_manager.save_settings(
                settings
            )
            return

        raise AttributeError(
            "SettingsManager does not provide "
            "save() or save_settings()."
        )

    def _get_defaults(self):
        if hasattr(
            self.settings_manager,
            "defaults",
        ):
            defaults = (
                self.settings_manager.defaults
            )

            if callable(defaults):
                defaults = defaults()

            return dict(
                defaults
            )

        if hasattr(
            self.settings_manager,
            "default_settings",
        ):
            defaults = (
                self.settings_manager
                .default_settings
            )

            if callable(defaults):
                defaults = defaults()

            return dict(
                defaults
            )

        if hasattr(
            self.settings_manager,
            "get_defaults",
        ):
            return dict(
                self.settings_manager
                .get_defaults()
            )

        # Fallback values match NetWatch V1.
        return {
            "ping_target": "1.1.1.1",
            "check_interval": 2.0,
            "history_length": 60,
            "spike_multiplier": 2.5,
            "minimum_spike_ms": 60.0,
            "disconnect_threshold": 3,
        }

    # =========================================================
    # FIELD ERRORS
    # =========================================================

    def _set_field_error(
        self,
        key,
        message,
    ):
        widgets = self.entries.get(
            key
        )

        if not widgets:
            return

        widgets["entry"].configure(
            border_color=CRITICAL
        )

        widgets["error"].configure(
            text=message
        )

    def _clear_field_error(
        self,
        key,
    ):
        widgets = self.entries.get(
            key
        )

        if not widgets:
            return

        widgets["entry"].configure(
            border_color=BORDER
        )

        widgets["error"].configure(
            text=""
        )

    def _clear_all_errors(self):
        for key in self.entries:
            self._clear_field_error(
                key
            )

    # =========================================================
    # FEEDBACK
    # =========================================================

    def _show_feedback(
        self,
        message,
        color,
    ):
        if self.feedback_after_id:
            try:
                self.after_cancel(
                    self.feedback_after_id
                )
            except Exception:
                pass

            self.feedback_after_id = None

        self.feedback_badge.configure(
            text=f"  {message}  ",
            text_color=color,
            fg_color=self._feedback_background(
                color
            ),
        )

        try:
            self.feedback_after_id = (
                self.after(
                    2800,
                    self._hide_feedback,
                )
            )

        except Exception:
            self.feedback_after_id = None

    def _hide_feedback(self):
        try:
            self.feedback_badge.configure(
                text="",
                fg_color="transparent",
            )
        except Exception:
            pass

        self.feedback_after_id = None

    @staticmethod
    def _feedback_background(
        color,
    ):
        if color == ONLINE:
            return "#16261C"

        if color == WARNING:
            return "#2B230F"

        if color == CRITICAL:
            return "#341719"

        return SURFACE

    # =========================================================
    # SAVE ANIMATION
    # =========================================================

    def _flash_save_button(self):
        original_text = (
            self.save_button.cget(
                "text"
            )
        )

        self.save_button.configure(
            text="✓  Saved",
            fg_color=ONLINE,
            hover_color=ONLINE,
        )

        try:
            self.after(
                1200,
                lambda: (
                    self._restore_save_button(
                        original_text
                    )
                ),
            )

        except Exception:
            pass

    def _restore_save_button(
        self,
        text,
    ):
        try:
            self.save_button.configure(
                text=text,
                fg_color=ACCENT,
                hover_color="#2563EB",
            )
        except Exception:
            pass

    # =========================================================
    # CLEANUP
    # =========================================================

    def destroy(self):
        if self.feedback_after_id:
            try:
                self.after_cancel(
                    self.feedback_after_id
                )
            except Exception:
                pass

        for animator in (
            self.card_animators
        ):
            try:
                animator.stop()
            except Exception:
                pass

        super().destroy()