import random
import datetime
import string
import discord


def generate_noise(width: int, height: int) -> list:
    """Generates a randomised 2d array of 1s and 0s

    Args:
        width (int): Width of the board
        height (int): Height of the board

    Returns:
        list: 2d array of generated noise
    """
    noise = [[r for r in range(width)] for i in range(height)]
    for i in range(0, height):
        for j in range(0, width):
            noise[i][j] = random.choice([0, 0, 0, 0, 1])
            # Expert has a Mine to NonMine ratio of 1 mine every 4.85 cells, we use 1:4 sas an approx
    return noise


def gen_users_board(user_id: int, width: int, height: int) -> list:
    """Takes a users ID and returns a generate_noise(width, height) using their ID as the random seed

    Args:
        user_id (int): ID of the user

    Returns:
        list: 2d array of noise
    """
    random.seed(user_id)
    noise = generate_noise(width, height)
    random.seed()  # reset the seed to avoid RNG abuse
    return noise


def get_neighbours(noise: list, x, y) -> int:
    neighbourValues = [
        noise[x_][y_]
        for x_ in range(x - 1, x + 2)
        for y_ in range(y - 1, y + 2)
        if (0 <= x_ < len(noise) and 0 <= y_ < len(noise) and (x_ != x or y_ != y))
    ]
    return neighbourValues.count(1)
    # return neighbourValues


def gen_numbers_from_noise(noise: list) -> list:
    """Takes a random noise array and gives out a playable board

    Args:
        noise (list): the noise generated from generate_noise

    Returns:
        list: a playable board
    """
    new_board = [[r for r in range(len(noise))] for i in range(len(noise[0]))]
    for x in range(0, len(noise)):
        for y in range(0, len(noise[0])):
            if noise[x][y] == 0:  # Check it's not a mine
                # Thanks stackoverflow
                n = get_neighbours(noise, x, y)
                new_board[x][y] = n
            else:
                # Fun fact, i debugged this entire thing for 30 minutes
                # Only to realise this read noise[x][y] == "m"
                # So yeah.
                new_board[x][y] = "m"  # So it doesn't get confused for the int tiles.
    return new_board


def get_daily(width: int, height: int) -> list:
    """uses the days since jan 1st as the random.seed for the noise

    Returns:
        list: noise generated
    """
    # Days since jan 1st 2022
    time_diff = datetime.datetime.now().date() - datetime.date(2022, 1, 1)
    random.seed(time_diff)
    noise = generate_noise(width, height)
    random.seed()  # reset the seed to avoid RNG abuse
    return noise


def get_daily_user(user_id: int, width: int, height: int) -> list:
    """like get_daily but takes a user_id and modulos it by the days since jan1st
    Since the min a users ID can be is 10chars,
    this means that this is safe for AT LEAST the next few billion years

    Args:
        user_id (int): ID of the user

    Returns:
        list: noise generated
    """
    # Days since jan 1st 2022
    time_diff = datetime.datetime.now().date() - datetime.date(2022, 1, 1)
    random.seed(user_id % time_diff)
    noise = generate_noise(width, height)
    random.seed()  # reset the seed to avoid RNG abuse
    return noise


def print_board(board: list, noise=False):
    """Mostly for debugging

    Args:
        board (list)
        noise (bool), whether it's a noise board
    """
    for i in board:
        print()
        for o in i:
            if noise:
                if o == 0:
                    print("-", end="")
                else:
                    print("#", end="")
            else:
                if o == "m":
                    print("#", end="")
                else:
                    print(o, end="")


def board_to_str(board: list) -> str:
    """Takes a board and spits out a string

    Args:
        board (list): The board to generate

    Returns:
        str: _description_
    """


def gen_blanks(board: list) -> list:
    return [["#" for r in range(len(board))] for i in range(len(board[0]))]


class MineSweeperGames:
    def __init__(
        self,
        game_type: str,
        interaction: discord.Interaction,
        height: int = 10,
        width: int = 10,
    ):
        self.board = None
        self.user_board = None
        self.mine_message = None
        self.finished = False

        # get game types
        # this could probably be an Enum, but i'm lazy rn
        self.game_type = game_type
        game_type = game_type.lower()
        if game_type == "daily":
            n = get_daily(width, height)
        elif game_type == "my daily":
            n = get_daily_user(interaction.user.id, width, height)
        elif game_type == "mysweep":
            n = gen_users_board(interaction.user.id, width, height)
        else:  # Must be random omegalul
            n = generate_noise(width, height)
        self.board = gen_numbers_from_noise(n)
        self.user_board = gen_blanks(self.board)

        # Make A1 notation style Column headers
        self.cols = []
        for k in range(len(self.board[0])):
            c = ""
            if (k // 26) > 1:  # If it's over 26
                c += string.ascii_uppercase[
                    (k // 26) - 1
                ]  # to be able to get 'A' we need to -1
            c += string.ascii_uppercase[k % 26]
            self.cols.append(c)

        # gen row names
        self.rows = [k + 1 for k in range(len(self.board))]
        self.won = False

    def make_message(self) -> str:
        """This is messy and could be cleaned up with f-string formatting
        # TODO: DESPERATELY NEEDS A REWRITE!!!
        Args:
            text_only (bool, optional): Whether to place it into a code block. Defaults to False.

        Returns:
            Message to Send
        """
        msg = "```"
        msg += f"__| {' '.join(self.cols)}|\n"
        msg += f"  |{'-' * ((len(self.cols) * 2))}|\n"
        for i in range(len(self.user_board)):
            if self.rows[i] < 10:  # Double digits require more space
                msg += " "
            msg += f"{self.rows[i]}|"
            for j in range(len(self.user_board[0])):
                if self.user_board[i][j] == "m":
                    msg += " @"  # Will only display once so idc about text limit
                elif self.user_board[i][j] == "#":
                    msg += " #"
                elif self.user_board[i][j] == "f":
                    msg += " f"  # Flag ! maybe put a unicode emoji later or whatever
                else:  # Must be a number
                    msg += f" {self.user_board[i][j]}"
            msg += "|\n"
        msg += f"  |{'-' * ((len(self.cols) * 2))}|\n```"
        emb = discord.Embed(
            title=f"💣 Minesweeper! 💣 - {self.game_type} - {len(self.board)}x{len(self.board[0])}⭐",
            description=msg,
        )
        emb.set_footer(
            text="Made with 💖 by Florence",
            icon_url="https://c.tenor.com/Gxa1JfN3334AAAAC/dm4uz3-sakamoto.gif",  # Spin gif
        )
        return emb

    def gen_game_over(self) -> str:
        """Generates a completely uncovered board"""
        msg = "```"
        msg += f"__| {' '.join(self.cols)}|\n"
        msg += f"  |{'-' * ((len(self.cols) * 2))}|\n"
        for i in range(len(self.user_board)):
            if self.rows[i] < 10:  # Double digits require more space
                msg += " "
            msg += f"{self.rows[i]}|"
            for j in range(len(self.user_board[0])):
                if self.board[i][j] == "m":
                    msg += " @"
                else:
                    msg += f" {self.board[i][j]}"
            msg += "|\n"
        msg += f"  |{'-' * ((len(self.cols) * 2))}|\n```"
        return "YOU LOST!!!" + msg + "#####################"

    def search_cardinals(self, col: int, row: int) -> None:
        """In the event of a 0, we search Up, Down, Left, Right, if we find another 0, repeat recursively

        Args:
            col (int): _description_
            row (int): _description_
        """
        cardinal_dirs = [[-1, 0], [0, -1], [+1, 0], [0, +1]]
        for c in cardinal_dirs:
            if 0 <= col + c[0] < len(self.board) and 0 <= row + c[1] < len(self.board):
                if self.board[col + c[0]][row + c[1]] == 0:
                    if self.user_board[col + c[0]][row + c[1]] != 0:
                        self.user_board[col + c[0]][row + c[1]] = self.board[
                            col + c[0]
                        ][row + c[1]]
                        self.search_cardinals(col + c[0], row + c[1])

                self.user_board[col + c[0]][row + c[1]] = self.board[col + c[0]][
                    row + c[1]
                ]
                # self.user_board[col+c[0]][row+c[1]] = self.board[col+c[0]][row+c[1]]

    def make_flag(self, col: int, row: int) -> None:
        row -= 1
        # It's indexed like that apparently
        self.user_board[row][col] = "f"  # Place flag !
        # No win checks for now, they need to reveal all good squares

    def make_guess(self, col: int, row: int):
        col, row = row, col  # User
        col -= 1
        cardinal_dirs = [[-1, -1], [-1, +1], [+1, -1], [+1, +1]]
        self.user_board[col][row] = self.board[col][row]
        if self.board[col][row] == 0:
            self.search_cardinals(col, row)
        elif self.board[col][row] == "m":  # It's a mine, gg
            self.finished = True
        else:
            pass
        # Check if they WON woot woot
        try:
            for i in range(len(self.board)):
                for j in range(len(self.board)):
                    if (
                        self.user_board[i][j] == "#" or self.user_board[i][j] == "f"
                    ) and self.board[i][j] != "m":
                        raise FloatingPointError  # This can be anything.
        except FloatingPointError:
            pass
        else:
            # They won!!!
            self.won = True
            self.finished = True
