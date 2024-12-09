import reflex as rx
from ..backend.backend import State


def product_card(name: str, details: dict) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.box(
                rx.image(
                    src=f"https://source.unsplash.com/random/400x300/?{name.lower()}",
                    width="100%",
                    height="300px",
                    object_fit="cover",
                ),
                rx.badge(
                    f"${details['price']}",
                    color_scheme="green",
                    position="absolute",
                    top="4",
                    right="4",
                ),
                position="relative",
            ),
            rx.heading(name, size="3"),
            rx.text(
                details["description"],
                color="gray.500",
                height="80px",
                overflow="hidden",
            ),
            rx.button(
                rx.hstack(
                    rx.icon("shopping-cart"),
                    rx.text("Add to Cart"),
                ),
                width="100%",
                color_scheme="blue",
            ),
            padding="4",
            background="white",
            border_radius="lg",
            border="1px solid",
            border_color="gray.200",
            height="100%",
            spacing="4",
        ),
        width="100%",
        transition_property="transform, box-shadow",
        transition_duration="200ms",
        _hover={
            "transform": "translateY(-4px)",
            "box_shadow": "lg",
        },
    )


def products_gallery() -> rx.Component:
    """Display products in a gallery layout."""
    return rx.vstack(
        rx.heading(
            "Our Products",
            size="1",
            margin_bottom="6",
        ),
        rx.text(
            "Discover our curated collection of high-quality products",
            color="gray.500",
            font_size="lg",
            margin_bottom="8",
        ),
        rx.box(
            rx.flex(
                rx.foreach(
                    State.products.items(),
                    lambda item: rx.box(
                        product_card(item[0], item[1]),
                        width=["100%", "45%", "30%", "22%"],
                    ),
                ),
                flex_wrap="wrap",
                gap="6",
                justify="center",
            ),
            width="100%",
            padding="4",
        ),
        width="100%",
        align_items="stretch",
        padding_x=["4", "6", "8"],
        padding_y="8",
        background="var(--accent-1)",
    )
