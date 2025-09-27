```python
#!/usr/bin/env python3
"""
Terminal Tetris Clone
A complete Tetris game implementation for terminal/console play.
"""

import random
import time
import sys
import os
from typing import List, Tuple, Optional, Dict, Any
from enum import Enum

# Platform-specific imports for terminal handling
try:
    import curses
    CURSES_AVAILABLE = True
except ImportError:
    CURSES_AVAILABLE = False
    try:
        import msvcrt
        MSVCRT_AVAILABLE = True
    except ImportError:
        MSVCRT_AVAILABLE = False

# Game constants
GRID_WIDTH = 10
GRID_HEIGHT = 20
INITIAL_FALL_SPEED = 1.0  # seconds per row
MIN_FALL_SPEED = 0.1
SPEED_INCREASE_FACTOR = 0.9
LINES_PER_LEVEL = 10

# Scoring system
SCORE_VALUES = {
    1: 100,   # Single
    2: 300,   # Double
    3: 500,   # Triple
    4: 800    # Tetris
}

# Key mappings
class GameAction(Enum):
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"
    SOFT_DROP = "soft_drop"
    HARD_DROP = "hard_drop"
    ROTATE = "rotate"
    PAUSE = "pause"
    QUIT = "quit"

# Tetromino shapes (4 rotation states each)
TETROMINO_SHAPES = {
    0: {  # I-piece
        'shape': [
            [['....', '####', '....', '....']],
            [['..#.', '..#.', '..#.', '..#.']],
            [['....', '....', '####', '....']],
            [['.#..', '.#..', '.#..', '.#..']]
        ],
        'color': 1
    },
    1: {  # O-piece
        'shape': [
            [['....', '.##.', '.##.', '....']],
            [['....', '.##.', '.##.', '....']],
            [['....', '.##.', '.##.', '....']],
            [['....', '.##.', '.##.', '....']],
        ],
        'color': 2
    },
    2: {  # T-piece
        'shape': [
            [['....', '.#..', '###.', '....']],
            [['....', '.#..', '.##.', '.#..']],
            [['....', '....', '###.', '.#..']],
            [['.#..', '##..', '.#..', '....']],
        ],
        'color': 3
    },
    3: {  # S-piece
        'shape': [
            [['....', '.##.', '##..', '....']],
            [['.#..', '.##.', '..#.', '....']],
            [['....', '.##.', '##..', '....']],
            [['.#..', '.##.', '..#.', '....']],
        ],
        'color': 4
    },
    4: {  # Z-piece
        'shape': [
            [['....', '##..', '.##.', '....']],
            [['....', '..#.', '.##.', '.#..']],
            [['....', '##..', '.##.', '....']],
            [['....', '..#.', '.##.', '.#..']],
        ],
        'color': 5
    },
    5: {  # J-piece
        'shape': [
            [['....', '#...', '###.', '....']],
            [['....', '.##.', '.#..', '.#..']],
            [['....', '....', '###.', '..#.']],
            [['.#..', '.#..', '##..', '....']],
        ],
        'color': 6
    },
    6: {  # L-piece
        'shape': [
            [['....', '..#.', '###.', '....']],
            [['.#..', '.#..', '.##.', '....']],
            [['....', '###.', '#...', '....']],
            [['....', '##..', '.#..', '.#..']],
        ],
        'color': 7
    }
}

class Piece:
    """Represents a falling tetromino piece."""
    
    def __init__(self, shape_id: int, x: int = GRID_WIDTH // 2 - 2, y: int = 0):
        self.shape_id = shape_id
        self.x = x
        self.y = y
        self.rotation_state = 0
        self.color_id = TETROMINO_SHAPES[shape_id]['color']
    
    def move(self, dx: int, dy: int) -> None:
        """Move the piece by the given offset."""
        self.x += dx
        self.y += dy
    
    def rotate(self, clockwise: bool = True) -> None:
        """Rotate the piece clockwise or counterclockwise."""
        if clockwise:
            self.rotation_state = (self.rotation_state + 1) % 4
        else:
            self.rotation_state = (self.rotation_state - 1) % 4
    
    def get_blocks(self, rotation_state: Optional[int] = None) -> List[Tuple[int, int]]:
        """Get the absolute coordinates of all blocks in the piece."""
        if rotation_state is None:
            rotation_state = self.rotation_state
        
        blocks = []
        shape_matrix = TETROMINO_SHAPES[self.shape_id]['shape'][rotation_state][0]
        
        for row_idx, row in enumerate(shape_matrix):
            for col_idx, cell in enumerate(row):
                if cell == '#':
                    blocks.append((self.x + col_idx, self.y + row_idx))
        
        return blocks
    
    def get_color_id(self) -> int:
        """Get the color ID for this piece."""
        return self.color_id

class Grid:
    """Manages the game grid and collision detection."""
    
    def __init__(self, width: int = GRID_WIDTH, height: int = GRID_HEIGHT):
        self.width = width
        self.height = height
        self.grid_data = [[0 for _ in range(width)] for _ in range(height)]
    
    def is_valid_position(self, piece: Piece, dx: int = 0, dy: int = 0, 
                         rotation_state: Optional[int] = None) -> bool:
        """Check if the piece can be placed at the given position."""
        test_piece = Piece(piece.shape_id, piece.x + dx, piece.y + dy)
        if rotation_state is not None:
            test_piece.rotation_state = rotation_state
        else:
            test_piece.rotation_state = piece.rotation_state
        
        blocks = test_piece.get_blocks()
        
        for x, y in blocks:
            # Check boundaries
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                return False
            
            # Check collision with existing blocks
            if self.grid_data[y][x] != 0:
                return False
        
        return True
    
    def add_piece(self, piece: Piece) -> None:
        """Add a piece to the grid permanently."""
        blocks = piece.get_blocks()
        for x, y in blocks:
            if 0 <= y < self.height and 0 <= x < self.width:
                self.grid_data[y][x] = piece.color_id
    
    def clear_lines(self) -> int:
        """Clear full lines and return the number of lines cleared."""
        lines_to_clear = []
        
        # Find full lines
        for y in range(self.height):
            if all(self.grid_data[y][x] != 0 for x in range(self.width)):
                lines_to_clear.append(y)
        
        # Remove full lines and shift down
        for y in reversed(lines_to_clear):
            del self.grid_data[y]
            self.grid_data.insert(0, [0 for _ in range(self.width)])
        
        return len(lines_to_clear)
    
    def get_state(self) -> List[List[int]]:
        """Get a copy of the current grid state."""
        return [row[:] for row in self.grid_data]
    
    def reset(self) -> None:
        """Clear the grid."""
        self.grid_data = [[0 for _ in range(self.width)] for _ in range(self.height)]

class InputManager:
    """Handles non-blocking keyboard input across platforms."""
    
    def __init__(self):
        self.key_mapping = {
            # Curses key codes
            curses.KEY_LEFT if CURSES_AVAILABLE else 'a': GameAction.MOVE_LEFT,
            curses.KEY_RIGHT if CURSES_AVAILABLE else 'd': GameAction.MOVE_RIGHT,
            curses.KEY_DOWN if CURSES_AVAILABLE else 's': GameAction.SOFT_DROP,
            curses.KEY_UP if CURSES_AVAILABLE else 'w': GameAction.HARD_DROP,
            ord(' ') if CURSES_AVAILABLE else ' ': GameAction.HARD_DROP,
            ord('r') if CURSES_AVAILABLE else 'r': GameAction.ROTATE,
            ord('x') if CURSES_AVAILABLE else 'x': GameAction.ROTATE,
            ord('p') if CURSES_AVAILABLE else 'p': GameAction.PAUSE,
            ord('q') if CURSES_AVAILABLE else 'q': GameAction.QUIT,
            27: GameAction.QUIT,  # ESC key
        }
        
        # Additional mappings for non-curses mode
        if not CURSES_AVAILABLE:
            self.key_mapping.update({
                'a': GameAction.MOVE_LEFT,
                'd': GameAction.MOVE_RIGHT,
                's': GameAction.SOFT_DROP,
                'w': GameAction.HARD_DROP,
                ' ': GameAction.HARD_DROP,
                'r': GameAction.ROTATE,
                'x': GameAction.ROTATE,
                'p': GameAction.PAUSE,
                'q': GameAction.QUIT,
            })
    
    def get_key_press(self, stdscr=None) -> Optional[GameAction]:
        """Get a key press without blocking."""
        if CURSES_AVAILABLE and stdscr:
            stdscr.timeout(0)  # Non-blocking
            try:
                key = stdscr.getch()
                if key == -1:  # No key pressed
                    return None
                return self.key_mapping.get(key)
            except:
                return None
        elif MSVCRT_AVAILABLE:
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                return self.key_mapping.get(key)
        
        return None

class DisplayManager:
    """Handles terminal display rendering."""
    
    def __init__(self, width: int = GRID_WIDTH, height: int = GRID_HEIGHT):
        self.width = width
        self.height = height
        self.stdscr = None
        self.use_curses = CURSES_AVAILABLE
        
        # Color pairs for curses
        self.color_pairs = {
            0: 0,  # Empty
            1: 1,  # Cyan (I)
            2: 2,  # Yellow (O)
            3: 3,  # Purple (T)
            4: 4,  # Green (S)
            5: 5,  # Red (Z)
            6: 6,  # Blue (J)
            7: 7,  # Orange (L)
        }
    
    def setup_terminal(self):
        """Initialize terminal for game display."""
        if self.use_curses:
            self.stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()
            curses.curs_set(0)
            
            # Initialize colors if supported
            if curses.has_colors():
                curses.start_color()
                curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
                curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
                curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
                curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
                curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
                curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)
                curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
            
            return self.stdscr
        else:
            # Clear screen for non-curses mode
            os.system('cls' if os.name == 'nt' else 'clear')
            return None
    
    def teardown_terminal(self):
        """Restore terminal to original state."""
        if self.use_curses and self.stdscr:
            curses.nocbreak()
            curses.echo()
            curses.curs_set(1)
            curses.endwin()
    
    def clear_screen(self):
        """Clear the entire screen."""
        if self.use_curses and self.stdscr:
            self.stdscr.clear()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
    
    def draw_grid(self, grid_state: List[List[int]], current_piece: Optional[Piece] = None):
        """Draw the game grid with current piece."""
        if not self.use_curses:
            self._draw_grid_simple(grid_state, current_piece)
            return
        
        if not self.stdscr:
            return
        
        # Create a display grid that includes the current piece
        display_grid = [row[:] for row in grid_state]
        
        if current_piece:
            blocks = current_piece.get_blocks()
            for x, y in blocks:
                if 0 <= y < len(display_grid) and 0 <= x < len(display_grid[0]):
                    display_grid[y][x] = current_piece.color_id
        
        # Draw border
        self.stdscr.addstr(0, 0, "+" + "-" * (self.width * 2) + "+")
        
        # Draw grid content
        for y in range(self.height):
            line = "|"
            for x in range(self.width):
                cell_value = display_grid[y][x]
                if cell_value == 0:
                    line += "  "
                else:
                    if curses.has_colors():
                        self.stdscr.addstr(y + 1, len(line), "██", 
                                         curses.color_pair(self.color_pairs.get(cell_value, 0)))
                        line += "  "
                    else:
                        line += "██"
            
            if not curses.has_colors():
                line += "|"
                self.stdscr.addstr(y + 1, 0, line)
            else:
                self.stdscr.addstr(y + 1, len(line), "|")
        
        # Draw bottom border
        self.stdscr.addstr(self.height + 1, 0, "+" + "-" * (self.width * 2) + "+")
    
    def _draw_grid_simple(self, grid_state: List[List[int]], current_piece: Optional[Piece] = None):
        """Simple grid drawing for non-curses mode."""
        # Create a display grid that includes the current piece
        display_grid = [row[:] for row in grid_state]
        
        if current_piece:
            blocks = current_piece.get_blocks()
            for x, y in blocks:
                if 0 <= y < len(display_grid) and 0 <= x < len(display_grid[0]):
                    display_grid[y][x] = current_piece.color_id
        
        # Clear and draw
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("+" + "-" * (self.width * 2) + "+")
        for row in display_grid:
            line = "|"
            for cell in row:
                if cell == 0:
                    line += "  "
                else:
                    line += "██"
            line += "|"
            print(line)
        print("+" + "-" * (self.width * 2) + "+")
    
    def draw_next_piece(self, piece: Piece, start_x: int = 25, start_y: int = 2):
        """Draw the next piece preview."""
        if not self.use_curses or not self.stdscr:
            return
        
        self.stdscr.addstr(start_y, start_x, "Next:")
        
        shape_matrix = TETROMINO_SHAPES[piece.shape_id]['shape'][0][0]
        for row_idx, row in enumerate(shape_matrix):
            line = ""
            for cell in row:
                if cell == '#':
                    line += "██"
                else:
                    line += "  "
            if line.strip():
                if curses.has_colors():
                    self.stdscr.addstr(start_y + 1 + row_idx, start_x, line,
                                     curses.color_pair(self.color_pairs.get(piece.color_id, 0)))
                else:
                    self.stdscr.addstr(start_y + 1 + row_idx, start_x, line)
    
    def draw_score(self, score: int, lines: int, level: int, start_x: int = 25, start_y: int = 8):
        """Draw score information."""
        if self.use_curses and self.stdscr:
            self.stdscr.addstr(start_y, start_x, f"Score: {score}")
            self.stdscr.addstr(start_y + 1, start_x, f"Lines: {lines}")
            self.stdscr.addstr(start_y + 2, start_x, f"Level: {level}")
        else:
            print(f"Score: {score} | Lines: {lines} | Level: {level}")
    
    def draw_message(self, message: str, start_x: int = 5, start_y: int = 10):
        """Draw a message overlay."""
        if self.use_curses and self.stdscr:
            self.stdscr.addstr(start_y, start_x, message, curses.A_BOLD)
        else:
            print(f"\n{message}\n")
    
    def draw_controls(self, start_x: int = 25, start_y: int = 12):
        """Draw control instructions."""
        if not self.use_curses or not self.stdscr:
            return
        
        controls = [
            "Controls:",
            "← → : Move",
            "↓ : Soft drop",
            "↑/Space : Hard drop",
            "R/X : Rotate",
            "P : Pause",
            "Q : Quit"
        ]
        
        for i, control in enumerate(controls):
            self.stdscr.addstr(start_y + i, start_x, control)
    
    def refresh(self):
        """Refresh the display."""
        if self.use_curses and self.stdscr:
            self.stdscr.refresh()

class TetrisGame:
    """Main game controller and orchestrator."""
    
    def __init__(self):
        self.grid = Grid()
        self.display = DisplayManager()
        self.input_manager = InputManager()
        
        self.current_piece: Optional[Piece] = None
        self.next_piece: Optional[Piece] = None
        
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.fall_speed = INITIAL_FALL_SPEED
        
        self.game_over = False
        self.paused = False
        self.running = True
        
        self.fall_time_accumulator = 0.0
        self.last_update_time = time.time()
        
        # Generate first pieces
        self._spawn_new_piece()
        self.next_piece = self._create_random_piece()
    
    def run(self):
        """Main game loop."""
        stdscr = self.display.setup_terminal()
        
        try:
            while self.running:
                current_time = time.time()
                delta_time = current_time - self.last_update_time
                self.last_update_time = current_time
                
                # Handle input
                action = self.input_manager.get_key_press(stdscr)
                if action:
                    self._handle_input(action)
                
                if not self.paused and not self.game_over:
                    # Update game state
                    self._update_game_state(delta_time)
                
                # Draw everything
                self._draw()
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.016)  # ~60 FPS
                
        except KeyboardInterrupt:
            pass
        finally:
            self.display.teardown_terminal()
    
    def _create_random_piece(self) -> Piece:
        """Create a random tetromino piece."""
        shape_id = random.randint(0, 6)
        return Piece(shape_id)
    
    def _spawn_new_piece(self) -> bool:
        """Spawn a new piece. Returns False if game over."""
        if self.next_piece:
            self.current_piece = self.next_piece
        else:
            self.current_piece = self._create_random_piece()
        
        self.next_piece = self._create_random_piece()
        
        # Check for game over
        if not self.grid.is_valid_position(self.current_piece):
            self.game_over = True
            return False
        
        return True
    
    def _handle_input(self, action: GameAction):
        """Process user input."""
        if action == GameAction.QUIT:
            self.running = False
            return
        
        if action == GameAction.PAUSE:
            self.paused = not self.paused
            return
        
        if self.paused or self.game_over or not self.current_piece:
            return
        
        if action == GameAction.MOVE_LEFT:
            if self.grid.is_valid_position(self.current_piece, dx=-1):
                self.current_piece.move(-1, 0)
        
        elif action == GameAction.MOVE_RIGHT:
            if self.grid.is_valid_position(self.current_piece, dx=1):
                self.current_piece.move(1, 0)
        
        elif action == GameAction.SOFT_DROP:
            if self.grid.is_valid_position(self.current_piece, dy=1):
                self.current_piece.move(0, 1)
                self.score += 1  # Bonus for soft drop
        
        elif action == GameAction.HARD_DROP:
            drop_distance = 0
            while self.grid.is_valid_position(self.current_piece, dy=1):
                self.current_piece.move(0, 1)
                drop_distance += 1
            
            self.score += drop_distance * 2  # Bonus for hard drop
            self._lock_piece()
        
        elif action == GameAction.ROTATE:
            # Try rotation with wall kicks
            original_rotation = self.current_piece.rotation_state
            self.current_piece.rotate()
            
            # Simple wall kick system
            kick_offsets = [(0, 0), (-1, 0), (1, 0), (0, -1), (-1, -1), (1, -1)]
            
            valid_rotation = False
            for dx, dy in kick_offsets:
                if self.grid.is_valid_position(self.current_piece, dx, dy):
                    self.current_piece.move(dx, dy)
                    valid_rotation = True
                    break
            
            if not valid_rotation:
                # Revert rotation if no valid position found
                self.current_piece.rotation_state = original_rotation
    
    def _update_game_state(self, delta_time: float):
        """Update game logic."""
        if not self.current_piece:
            return
        
        # Handle automatic falling
        self.fall_time_accumulator += delta_time
        
        if self.fall_time_accumulator >= self.fall_speed:
            self.fall_time_accumulator = 0.0
            
            if self.grid.is_valid_position(self.current_piece, dy=1):
                self.current_piece.move(0, 1)
            else:
                self._lock_piece()
    
    def _lock_piece(self):
        """Lock the current piece into the grid."""
        if not self.current_piece:
            return
        
        self.grid.add_piece(self.current_piece)
        
        # Clear lines
        lines_cleared = self.grid.clear_lines()
        if lines_cleared > 0:
            self._update_score(lines_cleared)
        
        # Spawn new piece
        if not self._spawn_new_piece():
            self.game_over = True
    
    def _update_score(self, lines_cleared: int):
        """Update score and level based on lines cleared."""
        if lines_cleared in SCORE_VALUES:
            self.score += SCORE_VALUES[lines_cleared] * self.level
        
        self.lines_cleared += lines_cleared
        
        # Level up
        new_level = (self.lines_cleared // LINES_PER_LEVEL) + 1
        if new_level > self.level:
            self.level = new_level
            self.fall_speed = max(MIN_FALL_SPEED, 
                                INITIAL_FALL_SPEED * (SPEED_INCREASE_FACTOR ** (self.level - 1)))
    
    def _draw(self):
        """Draw the entire game state."""
        if self.display.use_curses:
            self.display.clear_screen()
        
        # Draw main grid
        self.display.draw_grid(self.grid.get_state(), self.current_piece)
        
        # Draw UI elements
        if self.next_piece:
            self.display.draw_next_piece(self.next_piece)
        
        self.display.draw_score(self.score, self.lines_cleared, self.level)
        self.display.draw_controls()
        
        # Draw status messages
        if self.game_over:
            self.display.draw_message("GAME OVER! Press Q to quit.")
        elif self.paused:
            self.display.draw_message("PAUSED - Press P to continue")
        
        self.display.refresh()

def main():
    """Entry point for the game."""
    try:
        game = TetrisGame()
        game.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```
