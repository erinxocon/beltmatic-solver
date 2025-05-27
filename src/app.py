from typing import Type
from textual.containers import Vertical, Horizontal, HorizontalGroup
from textual.app import App, ComposeResult
from textual.driver import Driver
from textual.widgets import Label, Placeholder, Footer, Header
from textual.screen import Screen
from textual.binding import Binding


class Home(Screen[None]):
    BINDING_GROUP_TITLE = "Home Screen"
    BINDINGS = [
        Binding(
            "ctrl+n", "show_numbers", "Numbers", tooltip="Modify numbers", id="modify-numbers"
        ),
        Binding(
            "ctrl+o",
            "modify_operators",
            "Operators",
            tooltip="Modify operators",
            id="modify-operators",
        ),
    ]

    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()


class BeltmaticSolver(App[None]):
    TITLE = "Beltmatic Solver"
    # SCREENS = {"home": Home}

    def on_mount(self) -> None:
        """Set up the application on startup."""
        self.push_screen(Home())


if __name__ == "__main__":
    BeltmaticSolver().run()
