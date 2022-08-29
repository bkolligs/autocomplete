import tty
import termios
import sys
from trie import Trie

trie = Trie()
keys = ["the", "there", "their", "robot", "robot1", "robot2_b", "robber", "robbed"]
history = []
for k in keys:
    trie.insert(k)

ESCAPE = chr(27)
BACKSPACE = chr(127)
UP_ARROW = f'{ESCAPE}[A'
DOWN_ARROW = f'{ESCAPE}[B'
RIGHT_ARROW = f'{ESCAPE}[C'
LEFT_ARROW = f'{ESCAPE}[D'

settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)
input_key = 0
query = ""
raw = b''
command = False
command_count = 0
try:
    while True:
        input_key = sys.stdin.read(1)
        if input_key == ESCAPE:
            command = True
        if command:
            print(command_count)
            raw += input_key.encode()
            command_count += 1
        if command_count > 2:
            command_count = 0
            command = False
            print("COMMAND")
            print(raw)
            raw = b''
        elif input_key.isalnum():
            query += input_key
            sys.stdout.write(input_key)

        elif input_key == BACKSPACE:
            # remove last letter of query
            query = query[:-1] 
            # move cursor backwards one
            sys.stdout.write('\033[1D') 
            # erase output to end of line
            sys.stdout.write('\033[K') 

        elif ord(input_key) == ord("\t") and query != "":
            sys.stdout.flush()
            sys.stdout.writelines(['\n', trie.query(query), '\n', query])

        elif ord(input_key) == ord("\n"):
            history.append(query)
            sys.stdout.write('\n')
            query = ""
        sys.stdout.flush()


finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    sys.exit(0)
