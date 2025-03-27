from textual.app import App, ComposeResult
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Footer, Header, SelectionList, Label, Static, Pretty
from textual.widgets.selection_list import Selection
from app_game import Game


class PathTakenList(Static):
    """A widget to display all previous moves by the user, and the ultimate goal."""

    def __init__(self) -> None:
        super().__init__()
        # Initialize path as a list of tuples, e.g., [(word, dist)]
        # Correctly structured as a list of tuples
        self.path = [(self.app.game.start_word, self.app.game.initial_path_length)]

    def compose(self) -> ComposeResult:
        for word, dist in self.path:
            # Display the word and distance
            yield self.label(word, dist)

    def update(self, new_path: list[tuple[str, int]]) -> None:
        """Update the path with a new list of tuples."""
        self.path = new_path

        # Clear current items and re-yield the updated list of Labels
        for child in list(self.query(Label)):
            child.remove()

        for word, dist in self.path:
            self.mount(self.label(word, dist))

    def label(self, word, dist):
      extra_class = ""
      if dist >= 10:
        extra_class += "far-guess"
      elif dist == 9:
        extra_class += "far-guess light-10"
      elif dist == 8:
        extra_class += "far-guess light-20"
      elif dist == 7:
        extra_class += "far-guess light-30"
      elif dist == 6:
        extra_class += "far-guess light-40"
      elif dist == 5:
        extra_class += "far-guess light-50"
      elif dist == 4:
        extra_class += "near-guess light-40"
      elif dist == 3:
        extra_class += "near-guess light-30"
      elif dist == 2:
        extra_class += "near-guess light-20"
      elif dist == 1:
        extra_class += "near-guess light-10"

      return Label(f"{word} {dist}", classes=(f"near-guess path-taken-item {extra_class}"))


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

    def __init__(self) -> None:
        super().__init__()
        self.options = self.app.game.available_guesses()

    def compose(self) -> ComposeResult:
        self.selection_list = SelectionList[str](
            *[Selection(word, word) for word in self.options]
        )
        yield self.selection_list

    def update(self) -> None:
        """Update the options in the SelectionList."""
        self.selection_list.clear_options()

        for word in self.app.game.available_guesses():
            self.selection_list.add_option(Selection(word, word))

    def on_selection_list_selection_highlighted(self, event: SelectionList.SelectionHighlighted) -> None:
        """Handle selection highlight and broadcast which item is highlighted."""
        self.app.post_message(
            GuessHighlightedMessage(event.selection.value))

    def on_selection_list_selection_toggled(self, event: SelectionList.SelectionToggled) -> None:
        """Handle selected item and broadcast which item is selected."""
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
        self.game.receive_guess(message.selection)
        self.path_taken.update([(guess, distance) for guess, distance in self.game.taken_guesses])
        self.guess_options.update()

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
