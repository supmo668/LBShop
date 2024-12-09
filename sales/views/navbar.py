import reflex as rx
import reflex_clerk as clerk

from reflex_clerk import clerk_provider, sign_in_button, install_signin_page

def user_menu() -> rx.Component:
    """User menu dropdown component."""
    return rx.menu.root(
        rx.menu.trigger(
            rx.button(
                rx.hstack(
                    rx.cond(
                        clerk.ClerkState.is_signed_in,
                        rx.cond(
                            clerk.ClerkState.user.has_image,
                            rx.avatar(
                                src=clerk.ClerkState.user.image_url,
                                size="5",
                            ),
                            rx.avatar(size="5"),
                        ),
                        rx.icon("user", size=24),
                    ),
                    rx.icon("chevron-down"),
                ),
                variant="ghost",
            ),
        ),
        rx.menu.content(
            rx.menu.item(
                clerk_provider(
                    rx.vstack(
                        sign_in_button(),
                        align="center",
                        spacing="7",
                    ),
                )
            ),
        ),
    )


def navbar():
    return rx.flex(
        rx.badge(
            # rx.icon(tag="mails", size=28),
            rx.heading("LongBio Sales", size="6"),
            radius="large",
            align="center",
            color_scheme="blue",
            variant="surface",
            padding="0.65rem",
        ),
        rx.spacer(),
        rx.hstack(
            rx.color_mode.button(),
            user_menu(),
            align="center",
            spacing="3",
        ),
        spacing="2",
        flex_direction=["column", "column", "row"],
        align="center",
        width="100%",
        top="0px",
    )
