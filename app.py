from textual.app import App, ComposeResult
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Footer, Header, SelectionList, Label, Static, Pretty, Button
from textual.widgets.selection_list import Selection
from textual.screen import Screen
from textual.containers import Container
from app_game import Game

GAME_GUESS_THRESHOLD = 10


class PathTakenList(Static):
    """A widget to display all previous moves by the user, and the ultimate goal."""

    def __init__(self, game: Game) -> None:
        super().__init__()
        self.game = game
        self.path = []

    def compose(self) -> ComposeResult:
        self.path = [(self.game.start_word,
                     self.game.initial_path_length)]
        for label in self.current_labels():
            yield label

    def update(self, new_path: list[tuple[str, int]]) -> None:
        """Update the path with a new list of tuples."""
        self.path = new_path

        # Clear current items and re-yield the updated list of Labels
        for child in list(self.query(Label)):
            child.remove()

        for label in self.current_labels():
            self.mount(label)

    def current_labels(self):
        labels = []
        for index, (word, dist) in enumerate(self.path):
            if index == 0:
                word = f"[b]{word}[/b]"
            elif index == len(self.path) - 1:
                word = f"{word} *"
            labels.append(self.label(word, dist))

        for _ in range(GAME_GUESS_THRESHOLD - len(self.path)):
            labels.append(self.label(".", None))

        labels.append(self.label(self.game.target_word, None))

        return labels

    def label(self, word, dist):
        extra_class = ""
        if not dist:
            extra_class = ""
        elif dist >= 8:
            extra_class += "far-guess"
        elif dist == 7:
            extra_class += "far-guess light-30"
        elif dist == 6:
            extra_class += "far-guess light-50"
        elif dist == 5:
            extra_class += "mid-guess"
        elif dist == 4:
            extra_class += "mid-guess light-30"
        elif dist == 3:
            extra_class += "near-guess light-40"
        elif dist == 2:
            extra_class += "near-guess light-20"
        elif dist == 1:
            extra_class += "near-guess"

        return Label(f"{word} {dist if dist is not None else ''}", classes=(f"path-taken-item {extra_class}"))


class GameOverMessage(Message):
    """Custom message sent when the game is over."""

    def __init__(self, game: Game) -> None:
        super().__init__()
        self.game = game


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

    def __init__(self, game: Game) -> None:
        super().__init__()
        self.game = game
        self.options = []

    def compose(self) -> ComposeResult:
        self.options = self.game.available_guesses()
        self.selection_list = SelectionList[str](
            *[Selection(word, word) for word in self.options]
        )
        yield self.selection_list

    def update(self) -> None:
        """Update the options in the SelectionList."""
        self.selection_list.clear_options()

        for word in self.game.available_guesses():
            self.selection_list.add_option(Selection(word, word))

    def on_selection_list_selection_highlighted(self, event: SelectionList.SelectionHighlighted) -> None:
        """Handle selection highlight and broadcast which item is highlighted."""
        self.post_message(GuessHighlightedMessage(event.selection.value))

    def on_selection_list_selection_toggled(self, event: SelectionList.SelectionToggled) -> None:
        """Handle selected item and broadcast which item is selected."""
        self.post_message(GuessSelectedMessage(event.selection.value))


class NextSynonyms(Widget):
    """A custom widget that displays the upcoming possible synonyms."""

    def __init__(self, game: Game) -> None:
        super().__init__()
        self.game = game
        self.data = []

    def compose(self) -> ComposeResult:
        self.component = Pretty(self.data)
        yield self.component

    def update(self, new_data: list[str]) -> None:
        """Update the data and refresh the widget."""
        self.data = new_data
        self.component.update(self.data)


class GameScreen(Screen):

    BINDINGS = []
    MESSAGES = [GuessHighlightedMessage, GuessSelectedMessage]
    """An app to explore synonyms."""

    def on_guess_highlighted_message(self, message: GuessHighlightedMessage) -> None:
        """Update the label when receiving a selection highlight event."""
        options = self.game.get_synonyms(message.selection)
        self.next_synonyms.update(options)

    def on_guess_selected_message(self, message: GuessSelectedMessage) -> None:
        # this is the core event
        # we need to take a turn but then fire other events
        self.game.send_guess(message.selection)
        if self.game.game_won:
            self.app.push_screen(WonScreen())
            self.game.complete_game()
        elif self.game.turns_taken >= GAME_GUESS_THRESHOLD:
            self.app.push_screen(LostScreen())
            self.game.complete_game()
        else:
            self.path_taken.update([(guess, distance)
                                    for guess, distance in self.game.taken_guesses])
            self.guess_options.update()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        self.game = Game()
        self.start_word = self.game.start_word
        self.target_word = self.game.target_word

        # Pass game instance to all widgets
        self.path_taken = PathTakenList(self.game)
        self.guess_options = GuessOptionsComponent(self.game)
        self.next_synonyms = NextSynonyms(self.game)

        # Set border titles
        self.guess_options.border_title = "Make a word selection"
        self.path_taken.border_title = "Path"
        self.next_synonyms.border_title = "Your Next Options"

        yield Header()
        yield Footer()
        yield self.path_taken
        yield self.guess_options
        yield self.next_synonyms


## Can be used for debugging :)
class LabelTest(Static):
    def compose(self) -> ComposeResult:
        classes = [
            "far-guess", "far-guess light-10", "far-guess light-20", "far-guess light-30", "far-guess light-40", "far-guess light-50", "mid-guess", "mid-guess light-10", "mid-guess light-20", "mid-guess light-30", "mid-guess light-40", "mid-guess light-50", "near-guess light-40", "near-guess light-30", "near-guess light-20", "near-guess light-10", ]

        for className in classes:
            yield Label(f"{className}", classes=(f"path-taken-item {className}"))


class SplashScreen(Screen):

    def __init__(self):
        super().__init__()
        self.message = "Welcome to\nThe Saurus 🦖"
        self.button_text = "Start Game"

    def compose(self) -> ComposeResult:
        yield Container(
            Container(
                Static(self.message, classes="title"),
                Button(self.button_text, id="start-button"),
                id="start-content",
            ),
            id="start-container",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        game_screen = GameScreen()
        self.app.push_screen(game_screen)


class WonScreen(SplashScreen):
    def __init__(self):
        super().__init__()
        self.message = "🦕You Won!🦕"
        self.button_text = "Play Again"


class LostScreen(SplashScreen):
    def __init__(self):
        super().__init__()
        self.message = "🌋 You Lose! ☄️"
        self.button_text = "Play Again"


class ThesaurleApp(App):

    CSS_PATH = "app.tcss"

    def on_mount(self) -> None:
        self.theme = "tokyo-night"
        self.push_screen(SplashScreen())


if __name__ == "__main__":
    app = ThesaurleApp()
    app.run()
