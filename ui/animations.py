import customtkinter as ctk


def hex_to_rgb(hex_color: str):
    """
    Convert #RRGGBB to an RGB tuple.
    """

    hex_color = hex_color.lstrip("#")

    return tuple(
        int(
            hex_color[i:i + 2],
            16,
        )
        for i in (0, 2, 4)
    )


def rgb_to_hex(rgb):
    """
    Convert an RGB tuple to #RRGGBB.
    """

    return "#{:02x}{:02x}{:02x}".format(
        *rgb
    )


def interpolate_color(
    start_color: str,
    end_color: str,
    progress: float,
):
    """
    Interpolate between two colors.

    progress:
        0.0 = start color
        1.0 = end color
    """

    progress = max(
        0.0,
        min(
            1.0,
            progress,
        ),
    )

    start = hex_to_rgb(
        start_color
    )

    end = hex_to_rgb(
        end_color
    )

    current = tuple(
        int(
            start[i]
            + (
                end[i]
                - start[i]
            )
            * progress
        )
        for i in range(3)
    )

    return rgb_to_hex(
        current
    )


def ease_out_cubic(
    progress: float,
):
    """
    Smooth deceleration animation curve.
    """

    return (
        1
        - pow(
            1 - progress,
            3,
        )
    )


def ease_in_out_cubic(
    progress: float,
):
    """
    Smooth acceleration and deceleration.
    """

    if progress < 0.5:
        return (
            4
            * progress
            * progress
            * progress
        )

    return (
        1
        - pow(
            -2 * progress + 2,
            3,
        )
        / 2
    )


class ColorAnimator:
    """
    Smoothly animates a CustomTkinter widget color.
    """

    def __init__(
        self,
        widget,
        property_name="fg_color",
    ):
        self.widget = widget
        self.property_name = (
            property_name
        )

        self.animation_id = None

    def animate(
        self,
        start_color,
        end_color,
        duration=200,
        fps=60,
        on_complete=None,
    ):
        self.stop()

        frame_delay = max(
            1,
            int(
                1000 / fps
            ),
        )

        total_frames = max(
            1,
            int(
                duration
                / frame_delay
            ),
        )

        current_frame = 0

        def update():
            nonlocal current_frame

            if not self._widget_exists():
                return

            progress = (
                current_frame
                / total_frames
            )

            eased = (
                ease_out_cubic(
                    progress
                )
            )

            color = (
                interpolate_color(
                    start_color,
                    end_color,
                    eased,
                )
            )

            try:
                self.widget.configure(
                    **{
                        self.property_name:
                            color
                    }
                )

            except Exception:
                return

            if (
                current_frame
                >= total_frames
            ):
                try:
                    self.widget.configure(
                        **{
                            self.property_name:
                                end_color
                        }
                    )

                except Exception:
                    return

                self.animation_id = None

                if on_complete:
                    on_complete()

                return

            current_frame += 1

            try:
                self.animation_id = (
                    self.widget.after(
                        frame_delay,
                        update,
                    )
                )

            except Exception:
                self.animation_id = None

        update()

    def stop(self):
        if self.animation_id is None:
            return

        try:
            self.widget.after_cancel(
                self.animation_id
            )

        except Exception:
            pass

        self.animation_id = None

    def _widget_exists(self):
        try:
            return bool(
                self.widget.winfo_exists()
            )

        except Exception:
            return False


class PulseAnimator:
    """
    Repeatedly animates between two colors.

    Useful for:
    - online indicator
    - connection status
    - activity indicator
    """

    def __init__(
        self,
        widget,
        color_a,
        color_b,
        property_name="fg_color",
        duration=800,
    ):
        self.widget = widget

        self.color_a = color_a
        self.color_b = color_b

        self.property_name = (
            property_name
        )

        self.duration = duration

        self.running = False

        self.animator = (
            ColorAnimator(
                widget,
                property_name,
            )
        )

        self.direction = True

    def start(self):
        if self.running:
            return

        self.running = True
        self.direction = True

        self._pulse()

    def _pulse(self):
        if not self.running:
            return

        if self.direction:
            start = self.color_a
            end = self.color_b

        else:
            start = self.color_b
            end = self.color_a

        self.direction = (
            not self.direction
        )

        self.animator.animate(
            start_color=start,
            end_color=end,
            duration=self.duration,
            on_complete=self._pulse,
        )

    def stop(self):
        self.running = False

        self.animator.stop()


class AnimatedFrame(ctk.CTkFrame):
    """
    CTkFrame with basic animation support.
    """

    def __init__(
        self,
        master,
        **kwargs,
    ):
        super().__init__(
            master,
            **kwargs,
        )

        self.color_animator = (
            ColorAnimator(
                self
            )
        )

    def animate_color(
        self,
        start_color,
        end_color,
        duration=200,
    ):
        self.color_animator.animate(
            start_color,
            end_color,
            duration,
        )