from textual.app import App, ComposeResult
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Footer, Header, SelectionList, Label, Static, Pretty
from textual.widgets.selection_list import Selection


class PathTakenList(Static):
    """A widget to display the path of the thesaurus."""

    def compose(self) -> ComposeResult:
        yield Label("Word 1", classes="far-guess path-taken-item start-word")
        yield Label("Word 2", classes="far-guess light-10 path-taken-item")
        yield Label("Word 3", classes="path-taken-item")
        yield Label("Word 4", classes="path-taken-item")
        yield Label("Word 5", classes="path-taken-item")
        yield Label("Word 6", classes="near-guess path-taken-item")


class GuessHighlightedMessage(Message):
    """Custom message sent when a guess is highlighted."""

    def __init__(self, selection: str) -> None:
        super().__init__()
        self.selection = selection


class GuessOptionsComponent(Widget):
    """A custom widget that contains a SelectionList of Options."""

    def compose(self) -> ComposeResult:
        words = ["Word 1", "Word 2"]
        self.selection_list = SelectionList[str](
            *[Selection(word, word) for word in words]
        )
        yield self.selection_list

    def on_selection_list_selection_highlighted(self, event: SelectionList.SelectionHighlighted) -> None:
        """Handle selection highlight and broadcast which item is selected."""
        highlighted_item = event.selection.value

        self.app.post_message(
            GuessHighlightedMessage(highlighted_item))


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
        self.next_synonyms.update([message.selection])

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
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
