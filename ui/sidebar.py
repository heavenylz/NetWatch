import os
import sys

import customtkinter as ctk
from PIL import Image

from config import APP_VERSION

from ui.animations import ColorAnimator
from ui.theme import (
    ACCENT,
    BACKGROUND,
    BORDER,
    RADIUS_MEDIUM,
    SIDEBAR_BACKGROUND,
    SURFACE_HOVER,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


class Sidebar(ctk.CTkFrame):
    def __init__(
        self,
        master,
        on_dashboard,
        on_incidents,
        on_statistics,
        on_settings,
    ):
        super().__init__(
            master,
            width=230,
            corner_radius=0,
            fg_color=SIDEBAR_BACKGROUND,
            border_width=0,
        )

        self.page_callbacks = {
            "dashboard": on_dashboard,
            "incidents": on_incidents,
            "statistics": on_statistics,
            "settings": on_settings,
        }

        self.active_page = None

        self.buttons = {}
        self.button_animators = {}

        self.grid_propagate(False)

        self.grid_rowconfigure(
            10,
            weight=1,
        )

        self._build_header()
        self._build_navigation()
        self._build_footer()

            # =========================================================
    # RESOURCES
    # =========================================================

    @staticmethod
    def _resource_path(
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
            padx=18,
            pady=(22, 28),
        )

        header.grid_columnconfigure(
            1,
            weight=1,
        )

        # -----------------------------------------------------
        # NetWatch Logo
        # -----------------------------------------------------

        logo_path = self._resource_path(
            os.path.join(
                "assets",
                "netwatch_logo.png",
            )
        )

        try:
            logo_source = Image.open(
                logo_path
            )

            self.logo_image = ctk.CTkImage(
                light_image=logo_source,
                dark_image=logo_source,
                size=(48, 48),
            )

            self.logo_label = ctk.CTkLabel(
                header,
                text="",
                image=self.logo_image,
                width=48,
                height=48,
            )

        except Exception as error:
            print(
                "[NetWatch Logo Warning] "
                f"{type(error).__name__}: "
                f"{error}"
            )

            # Fallback if asset cannot be loaded.
            self.logo_label = ctk.CTkLabel(
                header,
                text="N",
                width=48,
                height=48,
                corner_radius=14,
                fg_color=ACCENT,
                text_color="#FFFFFF",
                font=ctk.CTkFont(
                    size=20,
                    weight="bold",
                ),
            )

        self.logo_label.grid(
            row=0,
            column=0,
            rowspan=2,
            sticky="w",
            padx=(0, 11),
        )

        # -----------------------------------------------------
        # App name
        # -----------------------------------------------------

        title = ctk.CTkLabel(
            header,
            text="NetWatch",
            text_color=TEXT_PRIMARY,
            anchor="w",
            font=ctk.CTkFont(
                size=19,
                weight="bold",
            ),
        )

        title.grid(
            row=0,
            column=1,
            sticky="sw",
        )

        subtitle = ctk.CTkLabel(
            header,
            text="Network Monitor",
            text_color=TEXT_MUTED,
            anchor="w",
            font=ctk.CTkFont(
                size=10,
            ),
        )

        subtitle.grid(
            row=1,
            column=1,
            sticky="nw",
        )

    # =========================================================
    # NAVIGATION
    # =========================================================

    def _build_navigation(self):
        section_label = ctk.CTkLabel(
            self,
            text="NAVIGATION",
            text_color=TEXT_MUTED,
            anchor="w",
            font=ctk.CTkFont(
                size=10,
                weight="bold",
            ),
        )

        section_label.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=22,
            pady=(0, 8),
        )

        navigation = [
            (
                "dashboard",
                "Dashboard",
                "◫",
            ),
            (
                "incidents",
                "Incidents",
                "!",
            ),
            (
                "statistics",
                "Statistics",
                "⌁",
            ),
            (
                "settings",
                "Settings",
                "⚙",
            ),
        ]

        row = 2

        for (
            page_name,
            label,
            icon,
        ) in navigation:
            self._create_nav_button(
                row=row,
                page_name=page_name,
                label=label,
                icon=icon,
            )

            row += 1

    def _create_nav_button(
        self,
        row,
        page_name,
        label,
        icon,
    ):
        container = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=46,
        )

        container.grid(
            row=row,
            column=0,
            sticky="ew",
            padx=12,
            pady=3,
        )

        container.grid_propagate(
            False
        )

        container.grid_columnconfigure(
            1,
            weight=1,
        )

        # -----------------------------------------------------
        # Active indicator
        # -----------------------------------------------------

        indicator = ctk.CTkFrame(
            container,
            width=3,
            height=24,
            corner_radius=3,
            fg_color=SIDEBAR_BACKGROUND,
        )

        indicator.grid(
            row=0,
            column=0,
            padx=(0, 5),
        )

        # -----------------------------------------------------
        # Button
        # -----------------------------------------------------

        button = ctk.CTkButton(
            container,
            text=f"{icon}    {label}",
            height=42,
            corner_radius=RADIUS_MEDIUM,
            anchor="w",
            border_width=0,
            fg_color=SIDEBAR_BACKGROUND,
            hover_color=SIDEBAR_BACKGROUND,
            text_color=TEXT_SECONDARY,
            font=ctk.CTkFont(
                size=13,
                weight="normal",
            ),
            command=lambda p=page_name: (
                self._on_click(p)
            ),
        )

        button.grid(
            row=0,
            column=1,
            sticky="ew",
        )

        animator = ColorAnimator(
            button,
            "fg_color",
        )

        # -----------------------------------------------------
        # Custom hover animation
        # -----------------------------------------------------

        button.bind(
            "<Enter>",
            lambda event,
            p=page_name: self._on_hover_enter(
                p
            ),
        )

        button.bind(
            "<Leave>",
            lambda event,
            p=page_name: self._on_hover_leave(
                p
            ),
        )

        self.buttons[
            page_name
        ] = {
            "button": button,
            "indicator": indicator,
        }

        self.button_animators[
            page_name
        ] = animator

    # =========================================================
    # INTERACTION
    # =========================================================

    def _on_click(
        self,
        page_name,
    ):
        if page_name == self.active_page:
            return

        self.set_active(
            page_name
        )

        callback = self.page_callbacks.get(
            page_name
        )

        if callback:
            callback()

    def _on_hover_enter(
        self,
        page_name,
    ):
        if (
            page_name
            == self.active_page
        ):
            return

        animator = (
            self.button_animators[
                page_name
            ]
        )

        animator.animate(
            start_color=SIDEBAR_BACKGROUND,
            end_color=SURFACE_HOVER,
            duration=140,
        )

    def _on_hover_leave(
        self,
        page_name,
    ):
        if (
            page_name
            == self.active_page
        ):
            return

        animator = (
            self.button_animators[
                page_name
            ]
        )

        animator.animate(
            start_color=SURFACE_HOVER,
            end_color=SIDEBAR_BACKGROUND,
            duration=180,
        )

    # =========================================================
    # ACTIVE PAGE
    # =========================================================

    def set_active(
        self,
        page_name,
    ):
        if (
            page_name
            not in self.buttons
        ):
            return

        previous_page = (
            self.active_page
        )

        self.active_page = page_name

        # -----------------------------------------------------
        # Disable previous selection
        # -----------------------------------------------------

        if (
            previous_page
            and previous_page
            in self.buttons
        ):
            previous = (
                self.buttons[
                    previous_page
                ]
            )

            previous_button = (
                previous["button"]
            )

            previous_indicator = (
                previous["indicator"]
            )

            previous_button.configure(
                text_color=TEXT_SECONDARY,
                font=ctk.CTkFont(
                    size=13,
                    weight="normal",
                ),
            )

            previous_indicator.configure(
                fg_color=SIDEBAR_BACKGROUND,
            )

            self.button_animators[
                previous_page
            ].animate(
                start_color=SURFACE_HOVER,
                end_color=SIDEBAR_BACKGROUND,
                duration=180,
            )

        # -----------------------------------------------------
        # Enable new selection
        # -----------------------------------------------------

        current = (
            self.buttons[
                page_name
            ]
        )

        current_button = (
            current["button"]
        )

        current_indicator = (
            current["indicator"]
        )

        current_button.configure(
            text_color=TEXT_PRIMARY,
            font=ctk.CTkFont(
                size=13,
                weight="bold",
            ),
        )

        current_indicator.configure(
            fg_color=ACCENT,
        )

        self.button_animators[
            page_name
        ].animate(
            start_color=SIDEBAR_BACKGROUND,
            end_color=SURFACE_HOVER,
            duration=220,
        )

    # =========================================================
    # FOOTER
    # =========================================================

    def _build_footer(self):
        separator = ctk.CTkFrame(
            self,
            height=1,
            fg_color=BORDER,
        )

        separator.grid(
            row=10,
            column=0,
            sticky="sew",
            padx=18,
            pady=(0, 91),
        )

        footer = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        footer.grid(
            row=10,
            column=0,
            sticky="sew",
            padx=20,
            pady=(0, 14),
        )

        # -----------------------------------------------------
        # Version
        # -----------------------------------------------------

        version = ctk.CTkLabel(
            footer,
            text=f"NetWatch v{APP_VERSION}",
            text_color=TEXT_SECONDARY,
            anchor="w",
            font=ctk.CTkFont(
                size=10,
                weight="bold",
            ),
        )

        version.pack(
            anchor="w",
        )

        # -----------------------------------------------------
        # Engine status
        # -----------------------------------------------------

        status = ctk.CTkLabel(
            footer,
            text="●  Monitoring Engine",
            text_color=TEXT_SECONDARY,
            anchor="w",
            font=ctk.CTkFont(
                size=9,
            ),
        )

        status.pack(
            anchor="w",
            pady=(3, 0),
        )

        # -----------------------------------------------------
        # Author
        # -----------------------------------------------------

        author = ctk.CTkLabel(
            footer,
            text="Built by heavenylz",
            text_color=TEXT_MUTED,
            anchor="w",
            font=ctk.CTkFont(
                size=9,
            ),
        )

        author.pack(
            anchor="w",
            pady=(8, 0),
        )

        # -----------------------------------------------------
        # Copyright
        # -----------------------------------------------------

        copyright_label = ctk.CTkLabel(
            footer,
            text=(
                "© 2026 heavenylz\n"
                "All rights reserved."
            ),
            text_color=TEXT_MUTED,
            anchor="w",
            justify="left",
            font=ctk.CTkFont(
                size=8,
            ),
        )

        copyright_label.pack(
            anchor="w",
            pady=(2, 0),
        )