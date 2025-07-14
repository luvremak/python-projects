import pygame
import sys
import random
import math
from typing import List, Tuple, Optional
import time

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
GRID_SIZE = 600
GRID_OFFSET_X = (WINDOW_WIDTH - GRID_SIZE) // 2
GRID_OFFSET_Y = (WINDOW_HEIGHT - GRID_SIZE) // 2
CELL_SIZE = GRID_SIZE // 9
SMALL_BOARD_SIZE = GRID_SIZE // 3

BACKGROUND = (20, 20, 25)
GRID_COLOR = (60, 60, 70)
ACTIVE_BOARD = (80, 120, 180)
PLAYER_X = (220, 80, 80)
PLAYER_O = (80, 150, 220)
TEXT_COLOR = (180, 180, 180)
WINNER_OVERLAY = (40, 40, 50)

class UltimateTicTacToe:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Ultimate Tic-Tac-Toe")
        self.clock = pygame.time.Clock()

        self.board = [[['.' for _ in range(3)] for _ in range(3)] for _ in range(9)]
        self.small_board_winners = [None for _ in range(9)]
        self.current_player = 'X'  
        self.active_board = None  
        self.game_winner = None
        
        self.hover_cell = None
        self.last_ai_move_time = 0
        
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
    def get_board_index(self, mouse_pos: Tuple[int, int]) -> Optional[Tuple[int, int, int]]:
        """Convert mouse position to board indices (board_idx, row, col)"""
        x, y = mouse_pos

        if (x < GRID_OFFSET_X or x >= GRID_OFFSET_X + GRID_SIZE or 
            y < GRID_OFFSET_Y or y >= GRID_OFFSET_Y + GRID_SIZE):
            return None

        rel_x = x - GRID_OFFSET_X
        rel_y = y - GRID_OFFSET_Y

        board_col = rel_x // SMALL_BOARD_SIZE
        board_row = rel_y // SMALL_BOARD_SIZE
        board_idx = board_row * 3 + board_col
        
        cell_x = (rel_x % SMALL_BOARD_SIZE) // CELL_SIZE
        cell_y = (rel_y % SMALL_BOARD_SIZE) // CELL_SIZE
        
        return (board_idx, cell_y, cell_x)
    
    def is_valid_move(self, board_idx: int, row: int, col: int) -> bool:
        """Check if a move is valid"""
        if self.board[board_idx][row][col] != '.':
            return False

        if self.small_board_winners[board_idx] is not None:
            return False

        if self.active_board is not None and board_idx != self.active_board:
            return False
            
        return True
    
    def make_move(self, board_idx: int, row: int, col: int, player: str) -> bool:
        """Make a move and return True if successful"""
        if not self.is_valid_move(board_idx, row, col):
            return False
            
        self.board[board_idx][row][col] = player

        winner = self.check_small_board_winner(board_idx)
        if winner:
            self.small_board_winners[board_idx] = winner

        next_board = row * 3 + col
        if (self.small_board_winners[next_board] is None and 
            any(self.board[next_board][r][c] == '.' for r in range(3) for c in range(3))):
            self.active_board = next_board
        else:
            self.active_board = None

        self.game_winner = self.check_game_winner()
        
        return True
    
    def check_small_board_winner(self, board_idx: int) -> Optional[str]:
        """Check if a small board has a winner"""
        board = self.board[board_idx]

        for row in range(3):
            if board[row][0] == board[row][1] == board[row][2] != '.':
                return board[row][0]

        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != '.':
                return board[0][col]

        if board[0][0] == board[1][1] == board[2][2] != '.':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != '.':
            return board[0][2]
            
        return None
    
    def check_game_winner(self) -> Optional[str]:
        """Check if there's an overall game winner"""
        for row in range(3):
            if (self.small_board_winners[row * 3] == 
                self.small_board_winners[row * 3 + 1] == 
                self.small_board_winners[row * 3 + 2] is not None):
                return self.small_board_winners[row * 3]
                
        for col in range(3):
            if (self.small_board_winners[col] == 
                self.small_board_winners[col + 3] == 
                self.small_board_winners[col + 6] is not None):
                return self.small_board_winners[col]

        if (self.small_board_winners[0] == 
            self.small_board_winners[4] == 
            self.small_board_winners[8] is not None):
            return self.small_board_winners[0]
        if (self.small_board_winners[2] == 
            self.small_board_winners[4] == 
            self.small_board_winners[6] is not None):
            return self.small_board_winners[2]
            
        return None
    
    def get_valid_moves(self) -> List[Tuple[int, int, int]]:
        """Get all valid moves"""
        moves = []
        
        if self.active_board is not None:
            for row in range(3):
                for col in range(3):
                    if self.is_valid_move(self.active_board, row, col):
                        moves.append((self.active_board, row, col))
        else:
            for board_idx in range(9):
                if self.small_board_winners[board_idx] is None:
                    for row in range(3):
                        for col in range(3):
                            if self.is_valid_move(board_idx, row, col):
                                moves.append((board_idx, row, col))
        
        return moves
    
    def ai_move(self) -> bool:
        """AI makes a move using minimax strategy"""
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return False

        best_move = None

        for move in valid_moves:
            board_idx, row, col = move
            self.board[board_idx][row][col] = 'O'
            if self.check_small_board_winner(board_idx) == 'O':
                temp_winners = self.small_board_winners[:]
                temp_winners[board_idx] = 'O'
                if self.would_win_game(temp_winners, 'O'):
                    self.board[board_idx][row][col] = '.'
                    best_move = move
                    break
            self.board[board_idx][row][col] = '.'
            
        if best_move is None:
            for move in valid_moves:
                board_idx, row, col = move
                self.board[board_idx][row][col] = 'X'
                if self.check_small_board_winner(board_idx) == 'X':
                    temp_winners = self.small_board_winners[:]
                    temp_winners[board_idx] = 'X'
                    if self.would_win_game(temp_winners, 'X'):
                        self.board[board_idx][row][col] = '.'
                        best_move = move
                        break
                self.board[board_idx][row][col] = '.'
        
        if best_move is None:
            best_move = random.choice(valid_moves)
            
        board_idx, row, col = best_move
        return self.make_move(board_idx, row, col, 'O')
    
    def would_win_game(self, winners: List[Optional[str]], player: str) -> bool:
        """Check if a given winner configuration would win the game"""
        for row in range(3):
            if (winners[row * 3] == winners[row * 3 + 1] == winners[row * 3 + 2] == player):
                return True

        for col in range(3):
            if (winners[col] == winners[col + 3] == winners[col + 6] == player):
                return True

        if (winners[0] == winners[4] == winners[8] == player):
            return True
        if (winners[2] == winners[4] == winners[6] == player):
            return True
            
        return False
    
    def draw_board(self):
        """Draw the game board and all visual elements"""
        self.screen.fill(BACKGROUND)
        
        if self.active_board is not None:
            board_row = self.active_board // 3
            board_col = self.active_board % 3

            glow_rect = pygame.Rect(
                GRID_OFFSET_X + board_col * SMALL_BOARD_SIZE - 2,
                GRID_OFFSET_Y + board_row * SMALL_BOARD_SIZE - 2,
                SMALL_BOARD_SIZE + 4,
                SMALL_BOARD_SIZE + 4
            )
            pygame.draw.rect(self.screen, ACTIVE_BOARD, glow_rect, 2)

        for i in range(10):
            x = GRID_OFFSET_X + i * CELL_SIZE
            y = GRID_OFFSET_Y + i * CELL_SIZE
            
            width = 2 if i % 3 == 0 else 1
            color = GRID_COLOR
            
            pygame.draw.line(self.screen, color, (x, GRID_OFFSET_Y), (x, GRID_OFFSET_Y + GRID_SIZE), width)
            pygame.draw.line(self.screen, color, (GRID_OFFSET_X, y), (GRID_OFFSET_X + GRID_SIZE, y), width)

        for board_idx in range(9):
            board_row = board_idx // 3
            board_col = board_idx % 3
            
            for row in range(3):
                for col in range(3):
                    cell = self.board[board_idx][row][col]
                    if cell != '.':
                        x = GRID_OFFSET_X + board_col * SMALL_BOARD_SIZE + col * CELL_SIZE + CELL_SIZE // 2
                        y = GRID_OFFSET_Y + board_row * SMALL_BOARD_SIZE + row * CELL_SIZE + CELL_SIZE // 2
                        
                        if cell == 'X':
                            pygame.draw.line(self.screen, PLAYER_X, (x - 20, y - 20), (x + 20, y + 20), 3)
                            pygame.draw.line(self.screen, PLAYER_X, (x - 20, y + 20), (x + 20, y - 20), 3)
                        else:  
                            pygame.draw.circle(self.screen, PLAYER_O, (x, y), 18, 3)

        for board_idx in range(9):
            winner = self.small_board_winners[board_idx]
            if winner:
                board_row = board_idx // 3
                board_col = board_idx % 3
                
                winner_color = PLAYER_X if winner == 'X' else PLAYER_O
                overlay = pygame.Surface((SMALL_BOARD_SIZE, SMALL_BOARD_SIZE))
                overlay.set_alpha(40)
                overlay.fill(winner_color)
                self.screen.blit(overlay, (
                    GRID_OFFSET_X + board_col * SMALL_BOARD_SIZE,
                    GRID_OFFSET_Y + board_row * SMALL_BOARD_SIZE
                ))

        if self.game_winner:
            winner_text = self.font.render(f"Player {self.game_winner} Wins!", True, TEXT_COLOR)
            winner_rect = winner_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
            self.screen.blit(winner_text, winner_rect)
            
            restart_text = self.small_font.render("Press R to restart", True, TEXT_COLOR)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, 80))
            self.screen.blit(restart_text, restart_rect)
        else:
            player_color = PLAYER_X if self.current_player == 'X' else PLAYER_O
            player_text = self.small_font.render(f"Player {self.current_player}", True, player_color)
            player_rect = player_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
            self.screen.blit(player_text, player_rect)
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.current_player == 'X' and self.game_winner is None:
                        board_info = self.get_board_index(event.pos)
                        if board_info:
                            board_idx, row, col = board_info
                            if self.make_move(board_idx, row, col, 'X'):
                                self.current_player = 'O'
                                self.last_ai_move_time = time.time()
                                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()
            
            if (self.current_player == 'O' and self.game_winner is None and 
                time.time() - self.last_ai_move_time > 1.0):
                if self.ai_move():
                    self.current_player = 'X'
            
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = UltimateTicTacToe()
    game.run()