import reflex as rx
import reflex_clerk as clerk
import os
from dotenv import load_dotenv

from .views.navbar import navbar
from .views.email import email_gen_ui
from .views.table import main_table
from .views.products import products_gallery
from .backend.backend import State

# Load environment variables
load_dotenv()


style = {
    "background_color": "var(--background)",
    "min_height": "100vh",
    "padding": "0",
}


def sales_panel() -> rx.Component:
    """Protected sales panel component."""
    return rx.vstack(
        navbar(),
        rx.flex(
            rx.box(main_table(), width=["100%", "100%", "100%", "60%"]),
            email_gen_ui(),
            spacing="6",
            width="100%",
            flex_direction=["column", "column", "column", "row"],
        ),
        height="100vh",
        bg=rx.color("accent", 1),
        width="100%",
        spacing="6",
        padding_x=["1.5em", "1.5em", "3em"],
        padding_y=["1em", "1em", "2em"],
    )


def index() -> rx.Component:
    """Root page that shows product gallery."""
    return rx.center(
        rx.box(
            navbar(),
            products_gallery(),
            width="100%",
            max_width="1400px",
        ),
        width="100%",
        style=style,
    )


def admin() -> rx.Component:
    """Admin page that shows sales panel."""
    return clerk.clerk_provider(
        rx.center(
            rx.container(
                clerk.protect(
                    rx.cond(
                        State.is_admin(),
                        sales_panel(),
                        rx.heading("Access Denied: Admin Only", color="red"),
                    ),
                    fallback=clerk.redirect_to_sign_in(),
                ),
            )
        ),
    )


def email() -> rx.Component:
    """Email generation page."""
    return rx.center(
        rx.container(
            navbar(),
            email_gen_ui(),
            width="100%",
            max_width="1400px",
        ),
        width="100%",
        style=style,
    )


# Configure the app
app = rx.App(
    # state=State,  # Set the state class
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="large",
        accent_color="blue",
    ),
)

# Install Clerk signin page
clerk.install_signin_page(app)

# Add pages
app.add_page(
    index,
    route="/",
    title="Sales App",
    description="Generate personalized sales emails.",
)

app.add_page(
    admin,
    route="/admin",
    on_load=State.load_entries,
)

app.add_page(
    email,
    route="/email",
    title="Email | Sales App",
    description="Generate personalized sales emails.",
)

