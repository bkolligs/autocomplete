"""The interface for the terminal and autocomplete."""
from __future__ import annotations
import tty
import termios
import sys
import threading
from typing import Callable
from trie import Trie
import time

MAX_COMMAND_INPUT = 3
ESCAPE = chr(27)
BACKSPACE = chr(127)
END_OF_TEXT = chr(3)
END_OF_FILE = chr(4)
CANCEL = chr(24)
UP_ARROW = f"{ESCAPE}[A".encode()
DOWN_ARROW = f"{ESCAPE}[B".encode()
RIGHT_ARROW = f"{ESCAPE}[C".encode()
LEFT_ARROW = f"{ESCAPE}[D".encode()
ESCAPE_COLOR = "\033["
RED_COLOR = ESCAPE_COLOR + "31m"
GREEN_COLOR = ESCAPE_COLOR + "32m"
BLUE_COLOR = ESCAPE_COLOR + "34m"
BRIGHT_BLUE_COLOR = ESCAPE_COLOR + "34;1m"
RESET_COLOR = ESCAPE_COLOR + "0m"


class TerminalInterface:
    def __init__(
        self,
        vocabulary: list[str] | None = None,
        max_command_input: int = MAX_COMMAND_INPUT,
        input_prompt: str = "ambi>",
        query_function: Callable = lambda s: print(s),
    ) -> None:
        self._is_running = False
        self._shutdown = False
        self._vocabulary = Trie(vocabulary)
        self._input_prompt = input_prompt

        self._query = ""
        self._command_queue = []
        self._raw_input = b""
        self._max_command_input = max_command_input
        self._command_count = 0
        self._history = []
        self._history_index = 0
        self._query_function = query_function

        self._restore_terminal_settings = termios.tcgetattr(sys.stdin)
        self._input_thread: threading.Thread | None = None

    def _start_terminal(self):
        tty.setcbreak(sys.stdin)

    def _stop_terminal(self):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._restore_terminal_settings)
        sys.exit(0)

    def start(self):
        self._is_running = True
        self._start_terminal()
        self._input_thread = threading.Thread(target=self._process_input, daemon=True)
        self._input_thread.start()

        while True:
            if self._shutdown:
                self.stop()
            time.sleep(0.01)

    def stop(self):
        self._is_running = False

        if self._input_thread is not None and self._input_thread.is_alive():
            self._input_thread.join()

        self._stop_terminal()

    def _reset_prompt(self, line: str = ""):
        if not self._prompted:
            sys.stdout.write("\r\033[K")
            sys.stdout.write(BRIGHT_BLUE_COLOR + self._input_prompt + RESET_COLOR + " " + line)
            sys.stdout.flush()
            self._prompted = True

    def _process_input(self):
        input_key = ""
        self._prompted = False
        while self._is_running:
            self._reset_prompt()
            input_key = sys.stdin.read(1)
            self._process_command_key(input_key)

            if self._command_queue:
                cur_command = self._command_queue.pop()
                if cur_command == UP_ARROW:
                    if self._history_index < len(self._history):
                        self._history_index += 1
                if cur_command == DOWN_ARROW:
                    if self._history_index > 1:
                        self._history_index -= 1
                self._query = self._history[-self._history_index]
                # clear the current terminal entry
                self._prompted = False
                self._reset_prompt(self._query)

                if input_key.encode() in cur_command:
                    continue

            if not self._process_interactive_keys(input_key):
                break

        self._shutdown = True

    def _process_command_key(self, input_key: str):
        if input_key == ESCAPE:
            self._command_count += 1
        if self._command_count > 0:
            self._raw_input += input_key.encode()
            self._command_count += 1
        if self._command_count > self._max_command_input:
            self._command_count = 0
            self._command_queue.append(self._raw_input)
            self._raw_input = b""

    def _process_interactive_keys(self, input_key: str):
        if input_key.isalnum():
            self._query += input_key
            sys.stdout.write(input_key)

        elif input_key == BACKSPACE:
            # remove last letter of query
            self._query = self._query[:-1]
            # move cursor backwards one
            sys.stdout.write("\033[1D")
            # erase output to end of line
            sys.stdout.write("\033[K")

        elif input_key in {END_OF_TEXT, END_OF_FILE, CANCEL}:
            return False

        elif input_key == "\t" and self._query != "":
            self._prompted = False
            sys.stdout.flush()
            sys.stdout.writelines(
                [
                    "\n",
                    GREEN_COLOR,
                    self._vocabulary.query(self._query),
                    RESET_COLOR,
                    "\n",
                ]
            )
            self._reset_prompt(line=self._query)

        elif input_key == "\n":
            sys.stdout.write("\n")
            self._query_function(self._query)
            self._history.append(self._query)
            self._query = ""
            self._prompted = False

        sys.stdout.flush()

        return True


if __name__ == "__main__":
    keys = ["the", "there", "their", "robot", "robot1", "robot2_b", "robber", "robbed"]
    terminal = TerminalInterface(vocabulary=keys)
    terminal.start()
