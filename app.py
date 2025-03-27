from textual.app import App, ComposeResult
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Footer, Header, SelectionList, Label, Static, Pretty
from textual.widgets.selection_list import Selection
from app_game import Game

TOTAL_MOVES = 10


class PathTakenList(Static):
    """A widget to display all previous moves by the user, and the ultimate goal."""

    def __init__(self) -> None:
        super().__init__()
        self.path = [self.app.game.start_word]

    def compose(self) -> ComposeResult:
        """Yield each path item as a Label inside the Static widget."""
        for p in self.path:
            yield Label(p, classes="path-taken-item")

    def append(self, new_item: str) -> None:
        """Update the path and refresh the widget."""
        self.path.append(new_item)
        self.update()

    def update(self) -> None:
        """Clear current items and re-yield the updated list of Labels."""
        # Remove existing labels by querying for children and removing each one
        for child in list(self.query(Label)):  # Query all Label widgets
            child.remove()  # Remove each child one by one

        # Add updated labels
        for p in self.path:
            self.mount(Label(p, classes="path-taken-item"))


class GuessHighlightedMessage(Message):
    """Custom message sent when a guess is highlighted."""

    def __init__(self, selection: str) -> None:
        super().__init__()
        self.selection = selection


class GuessSelectedMessage(Message):
    """Custom message sent when a guess is selected."""

    def __init__(self, selection: str) -> None:
        super().__init__()
        self.selection = selection


class GuessOptionsComponent(Widget):
    """A custom widget that contains a SelectionList of Options."""

    def compose(self) -> ComposeResult:
        words = self.app.game.available_guesses()
        self.selection_list = SelectionList[str](
            *[Selection(word, word) for word in words]
        )
        yield self.selection_list

    def on_selection_list_selection_highlighted(self, event: SelectionList.SelectionHighlighted) -> None:
        """Handle selection highlight and broadcast which item is selected."""
        highlighted_item = event.selection.value

        self.app.post_message(
            GuessHighlightedMessage(highlighted_item))

    def on_selection_list_selection_toggled(self, event: SelectionList.SelectionToggled) -> None:
        self.app.post_message(GuessSelectedMessage(event.selection.value))


class NextSynonyms(Widget):
    """A custom widget that displays the upcoming possible synonyms."""

    def __init__(self) -> None:
        super().__init__()
        self.data = []

    def compose(self) -> ComposeResult:
        self.component = Pretty(self.data)
        yield self.component

    def update(self, new_data: list[str]) -> None:
        """Update the data and refresh the widget."""
        self.data = new_data
        self.component.update(self.data)


class ThesaurleApp(App):
    """An app to explore synonyms."""
    CSS_PATH = "app.tcss"

    def on_mount(self) -> None:
        self.theme = "tokyo-night"

    def on_guess_highlighted_message(self, message: GuessHighlightedMessage) -> None:
        """Update the label when receiving a selection highlight event."""
        options = self.game.get_synonyms(message.selection)
        self.next_synonyms.update(options)

    def on_guess_selected_message(self, message: GuessSelectedMessage) -> None:
        # this is the core event
        # we need to take a turn but then fire other events
        self.path_taken.append(message.selection)
        print(f"selected {message.selection}")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        self.game = Game()
        self.start_word = self.game.start_word
        self.target_word = self.game.target_word

        self.path_taken = PathTakenList()
        self.guess_options = GuessOptionsComponent()
        self.next_synonyms = NextSynonyms()

        # Set border titles
        self.guess_options.border_title = "Make a word selection"
        self.path_taken.border_title = "Path"
        self.next_synonyms.border_title = "Your Next Options"

        yield Header()
        yield Footer()
        yield self.path_taken
        yield self.guess_options
        yield self.next_synonyms


if __name__ == "__main__":
    app = ThesaurleApp()
    app.run()
