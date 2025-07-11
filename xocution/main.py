import random
import copy

class UltimateTicTacToe:
    def __init__(self):
        self.board = [[['.' for _ in range(3)] for _ in range(3)] for _ in range(9)]
        self.small_board_winners = [None for _ in range(9)]
        self.current_player = 'X'
        self.active_board = None
        self.game_winner = None

    def is_valid_move(self, board_index, row, col):
        if self.active_board is not None and board_index != self.active_board:
            return False

        if self.board[board_index][row][col] != '.':
            return False

        if self.small_board_winners[board_index] is not None:
            return False

        return True

    def make_move(self, board_index, row, col):
        if not self.is_valid_move(board_index, row, col):
            return False

        self.board[board_index][row][col] = self.current_player

        if self.check_small_board_winner(board_index):
            self.small_board_winners[board_index] = self.current_player

        next_active = row * 3 + col
        if self.small_board_winners[next_active] is None and any(
            self.board[next_active][r][c] == '.' for r in range(3) for c in range(3)
        ):
            self.active_board = next_active
        else:
            self.active_board = None

        if self.check_game_winner():
            self.game_winner = self.current_player

        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def check_small_board_winner(self, board_index):
        b = self.board[board_index]

        for row in b:
            if row[0] == row[1] == row[2] != '.':
                return True

        for col in range(3):
            if b[0][col] == b[1][col] == b[2][col] != '.':
                return True

        if b[0][0] == b[1][1] == b[2][2] != '.':
            return True
        if b[0][2] == b[1][1] == b[2][0] != '.':
            return True

        return False

    def check_game_winner(self):
        w = self.small_board_winners

        for i in range(0, 9, 3):
            if w[i] == w[i + 1] == w[i + 2] and w[i] is not None:
                return True

        for i in range(3):
            if w[i] == w[i + 3] == w[i + 6] and w[i] is not None:
                return True

        if w[0] == w[4] == w[8] and w[0] is not None:
            return True
        if w[2] == w[4] == w[6] and w[2] is not None:
            return True

        return False

    def print_board(self):
        for big_row in range(3):
            for row in range(3):
                line = ''
                for big_col in range(3):
                    board_index = big_row * 3 + big_col
                    line += ' '.join(self.board[board_index][row]) + ' | '
                print(line.rstrip(' | '))
            print('-' * 25)

    def play(self):
        while not self.game_winner:
            print("\nCurrent player:", self.current_player)
            if self.active_board is not None:
                print("You must play in small board:", self.active_board)
            else:
                print("You can play in any open board.")
            self.print_board()

            try:
                board_index = int(input("Choose small board (0-8): "))
                row = int(input("Choose row (0-2): "))
                col = int(input("Choose col (0-2): "))
            except ValueError:
                print("Invalid input! Enter numbers only.")
                continue

            if not (0 <= board_index < 9 and 0 <= row < 3 and 0 <= col < 3):
                print("Invalid position! Try again.")
                continue

            if not self.make_move(board_index, row, col):
                print("Invalid move. Try again.")
                continue

        print(f"\nGame Over! {self.game_winner} wins the game!")

class TepuTepu:
    def __init__(self, game):
        self.game = game

        def get_valid_moves(self, game):
            moves = []

            for board_index in range(9):
                if self.game.active_board is not None and board_index != self.game.active_board:
                    continue
                if self.game.small_board_winners[board_index] is not None:
                    continue
                for row in range(3):
                    for col in range(3):
                        if self.game.board[board_index][row][col] == '.':
                            moves.append((board_index, row, col))
            return moves
    
        def simulate_move_win(self, move, player):
            temp_game = copy.deepcopy(self.game)

            board_index, row, col = move
            temp_game.current_player = player
            temp_game.make_move(board_index, row, col)

            return temp_game.game_winner == player

        def teputepu_move(self):
            current = self.game.current_player
            opponent = 'O' if current == 'X' else 'X'
            valid_moves = self.get_valid_moves()

            for move in valid_moves:
                if self.simulate_move_win(move, current):
                    return move
                
            for move in valid_moves:
                if self.simulate_move_win(move, opponent):
                    return move
                
            return random.choice(valid_moves)
        

