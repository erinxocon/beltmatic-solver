from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static, Input, Button, Label
from solver import heapq_solve


class BeltmaticCompanion(App):
    """A Textual app to manage stopwatches."""

    async def _on_submit(self, event: Button.Pressed) -> None:
        result_field = self.query_one("#result_field", Static)
        number_input = self.query_one("#number_input", Input)
        target_input = self.query_one("#target_input", Input)
        try:
            numbers = [int(n.strip()) for n in number_input.value.split(",") if n.strip()]
            target = int(target_input.value.strip())
        except Exception as e:
            result_field.update("Could not parse list of numbers, check commas")
        else:
            node = heapq_solve(target=target, start_numbers=numbers, allowed_ops={"+", "-", "*"})
            if node:
                result_field.update(f"Here is the result: {node} | Steps: {node.node_id}")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "submit_btn":
                await self._on_submit(event=event)
            case _:
                print("unknown button press")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Label("Enter available numbers (comma separated):")
        yield Input(placeholder="1,2,3,5,7", id="number_input")
        yield Label("Enter target value:")
        yield Input(placeholder="4975", id="target_input")
        yield Static("Result: ", id="result_field")
        yield Button("Submit", id="submit_btn")
        yield Footer()


if __name__ == "__main__":
    app = BeltmaticCompanion()
    app.run()
