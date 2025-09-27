The following document provides a comprehensive software design specification for a terminal-based Tetris game clone, implemented in Python as a single file. This specification serves as a detailed blueprint for development, ensuring all functional and non-functional requirements are met, and laying the groundwork for a robust and maintainable system.

---

# Software Design Specification: Terminal Tetris Clone

## 1. Executive Summary and Context

### Project Overview

This project aims to develop a classic Tetris game clone that operates entirely within a command-line interface (CLI) or terminal environment. The game will replicate the core mechanics of Tetris, including falling tetrominoes, rotation, horizontal movement, line clearing, scoring, and a game-over condition. The implementation will be in Python, designed to run as a single script file, leveraging standard or commonly available libraries to facilitate terminal interaction and game logic.

**Purpose:** To provide a simple, yet fully functional, terminal-based Tetris experience.
**Target Users:** Developers, students, and casual gamers who prefer a lightweight, text-based gaming experience or wish to run the game on systems without graphical interfaces.
**Primary Use Cases:**
*   Playing a classic Tetris game in a terminal.
*   Demonstrating Python programming skills for game development and CLI interaction.
**Success Criteria:**
*   Accurate replication of core Tetris mechanics.
*   Smooth and responsive user input and game display.
*   Stable operation without crashes or unexpected behavior.
*   Maintainability within a single-file structure.
**Project Scope:** Implementation of standard Tetris rules, single-player mode, basic scoring, and clear terminal rendering.
**Boundaries:** No network multiplayer, no persistent high scores, no advanced graphical elements beyond ASCII/Unicode characters.
**Constraints:** Single Python file implementation. Must run on common terminal emulators (e.g., Bash, PowerShell, CMD).

### Business Context

This project primarily serves as a technical exercise and a recreational tool. There are no direct business objectives, market requirements, or competitive considerations in a commercial sense. It aligns with organizational goals for fostering technical skill development, open-source contribution (if applicable), and demonstrating foundational software engineering principles. Regulatory compliance is not applicable for a non-commercial, local terminal game. Budget, timeline, and resource constraints are minimal, assuming a single developer for a short development cycle.

## 2. Requirements Analysis

### Functional Requirements

| ID    | Requirement                                 | Description                                                                                             | Priority | Acceptance Criteria                                                                                                                                                                                                                                                                                                                                                                       |
| :---- | :------------------------------------------ | :------------------------------------------------------------------------------------------------------ | :------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FR-001 | Game Grid Display                           | The game shall display a 10x20 cell grid.                                                              | High     | The terminal screen displays a clear 10-column by 20-row game area.                                                                                                                                                                                                                                                                                                                       |
| FR-002 | Tetromino Generation                        | New tetrominoes (I, O, T, S, Z, J, L shapes) shall appear at the top center of the grid.               | High     | Upon a piece locking or game start, a new tetromino is randomly selected and displayed, positioned at the top-center (spawn point) of the game grid.                                                                                                                                                                                                                                    |
| FR-003 | Tetromino Falling                           | Tetrominoes shall automatically fall one row per fixed time interval.                                   | High     | Pieces move down automatically at a consistent rate (e.g., 0.5-1.0 seconds per row).                                                                                                                                                                                                                                                                                                      |
| FR-004 | Horizontal Movement (Left/Right)            | Users shall be able to move the falling tetromino left or right using keyboard input.                   | High     | Pressing Left Arrow moves the piece one column left; Right Arrow moves it one column right, unless blocked by the grid boundary or other locked pieces.                                                                                                                                                                                                                               |
| FR-005 | Soft Drop (Accelerated Falling)             | Users shall be able to accelerate the falling of the current tetromino.                                 | High     | Pressing Down Arrow moves the piece one row down immediately. Releasing stops accelerated fall. Piece still falls automatically.                                                                                                                                                                                                                                                         |
| FR-006 | Hard Drop (Instant Lock)                    | Users shall be able to instantly drop the tetromino to the lowest possible position and lock it.        | High     | Pressing Up Arrow or Spacebar instantly moves the piece to its lowest valid position and locks it into the grid.                                                                                                                                                                                                                                                                          |
| FR-007 | Rotation                                    | Users shall be able to rotate the falling tetromino clockwise.                                          | High     | Pressing 'R' or 'X' (or a designated key) rotates the piece 90 degrees clockwise, applying Wall Kick System (WKS) if necessary, unless blocked.                                                                                                                                                                                                                                         |
| FR-008 | Collision Detection (Walls & Floor)         | The game shall prevent tetrominoes from moving outside grid boundaries or into locked blocks.           | High     | Tetrominoes stop moving horizontally/vertically and cannot rotate if the new position/orientation would overlap with grid walls, floor, or existing locked blocks.                                                                                                                                                                                                                        |
| FR-009 | Piece Locking                               | A tetromino shall lock in place once it collides with the floor or another locked piece from below.     | High     | When a falling piece cannot move down further, it remains in its current position and is integrated into the static grid, triggering a new piece spawn.                                                                                                                                                                                                                              |
| FR-010 | Line Clearing                               | Full horizontal rows shall be cleared from the grid, and blocks above shall fall down.                  | High     | When one or more full horizontal rows are formed, those rows disappear, and all blocks above them shift down by the number of cleared rows.                                                                                                                                                                                                                                            |
| FR-011 | Scoring System                              | Points shall be awarded for line clears and piece placements.                                           | Medium   | The score increases based on the number of lines cleared simultaneously (e.g., 1 line = 100, 2 lines = 300, 3 lines = 500, 4 lines = 800) and for hard/soft drops.                                                                                                                                                                                                                     |
| FR-012 | Next Piece Display                          | The next incoming tetromino shall be displayed.                                                         | Medium   | A small preview of the next tetromino to be spawned is shown alongside the main game grid.                                                                                                                                                                                                                                                                                              |
| FR-013 | Game Over Condition                         | The game shall end if a new tetromino cannot be spawned at its starting position due to blocked cells.  | High     | If a newly spawned piece immediately collides with existing locked blocks at its spawn position, the game ends, and a "Game Over" message is displayed.                                                                                                                                                                                                                             |
| FR-014 | Pause Functionality                         | Users shall be able to pause and unpause the game.                                                      | Medium   | Pressing 'P' toggles the game state between paused and active. While paused, game logic and piece falling stop, and a "Paused" message is displayed.                                                                                                                                                                                                                                |
| FR-015 | Real-time Display Updates                   | The terminal display shall update in real-time to reflect game state changes.                           | High     | The game grid, falling piece, score, and next piece are redrawn efficiently to show current state without flickering or excessive lag.                                                                                                                                                                                                                                                 |
| FR-016 | Exit Game                                   | Users shall be able to exit the game cleanly.                                                           | High     | Pressing 'Q' or 'ESC' exits the game, returning the terminal to its original state.                                                                                                                                                                                                                                                                                                       |

### Non-Functional Requirements

| ID    | Requirement           | Description                                                                                               | Priority | Measurement Criteria                                                                                                                                                                                                                                                                                                                                                                                                      |
| :---- | :-------------------- | :-------------------------------------------------------------------------------------------------------- | :------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| NFR-001 | Performance (Input)   | User input for movement and rotation shall be responsive.                                                 | High     | Input latency: < 50ms from key press to screen update.                                                                                                                                                                                                                                                                                                                                                                |
| NFR-002 | Performance (Display) | The terminal display shall update smoothly without noticeable flickering or tearing.                      | High     | Screen refresh rate should be consistent with game logic updates. No visual artifacts during redraws.                                                                                                                                                                                                                                                                                                                   |
| NFR-003 | Reliability           | The game shall operate without crashing or encountering unhandled exceptions during normal gameplay.      | High     | Zero unhandled exceptions observed during 1 hour of continuous play under various scenarios (rapid input, many line clears, game over).                                                                                                                                                                                                                                                                                  |
| NFR-004 | Usability             | Controls shall be intuitive, and the display shall be clear and easy to understand.                       | High     | New users can understand controls from an initial prompt or help screen. Game state (score, lines, next piece) is clearly legible.                                                                                                                                                                                                                                                                                       |
| NFR-005 | Maintainability       | The single-file codebase shall be structured for readability and ease of understanding.                   | Medium   | Code adheres to PEP 8 standards, utilizes clear variable/function names, and includes comments for complex logic. Modular design through classes despite being a single file.                                                                                                                                                                                                                                  |
| NFR-006 | Portability           | The game shall run on common terminal emulators across Linux, macOS, and Windows with minimal setup.      | Medium   | Successful execution on: <br> - Linux (Bash, xterm) <br> - macOS (Terminal.app, iTerm2) <br> - Windows (CMD, PowerShell, WSL) with Python installed. Avoid OS-specific low-level terminal calls where cross-platform alternatives exist.                                                                                                                                                                        |
| NFR-007 | Resource Efficiency   | The game shall have a low memory and CPU footprint.                                                       | Low      | Less than 50MB RAM usage. CPU usage below 10% on a modern system when idle (game paused) and below 30% during active gameplay.                                                                                                                                                                                                                                                                              |
| NFR-008 | Error Handling        | User errors (e.g., invalid key presses) or system errors shall be handled gracefully without crashing.    | Medium   | Invalid key presses are ignored or result in a brief, non-intrusive message. System errors log to console/file (if implemented) and prevent critical crashes.                                                                                                                                                                                                                                                  |
| NFR-009 | Time-based Difficulty | The falling speed of tetrominoes shall increase over time or with increasing score/lines cleared.         | Medium   | Falling interval decreases by a fixed percentage or absolute value after every 'N' lines cleared or 'X' points scored, or every 'Y' minutes of gameplay, up to a defined maximum speed.                                                                                                                                                                                                                           |

## 3. System Architecture Design

### High-Level Architecture

The system will employ a monolithic, layered architectural style contained within a single Python file. This design prioritizes simplicity and ease of distribution, aligning with the "single file" constraint.

**Architectural Style:** Monolithic (single file), Layered.
**Layers:**
1.  **Presentation Layer (Display & Input):** Handles terminal rendering and user input.
2.  **Game Logic Layer:** Manages game state, rules, piece movement, collision detection, and scoring.
3.  **Data Layer:** In-memory representation of the game grid and falling pieces.

```mermaid
graph TD
    A[User Input (Keyboard)] --> B(Input Manager)
    B --> C(Game Controller / Main Loop)
    C --> D(Game Logic Module)
    D --> E(Game Grid Module)
    D --> F(Piece Module)
    E --> C
    F --> C
    C --> G(Display Manager)
    G --> H[Terminal Output]
```

**Technology Stack Recommendations:**
*   **Language:** Python 3.x
*   **Terminal I/O (Unix/macOS):** `curses` library (standard Python library). Provides low-level control over terminal screen, non-blocking input, and color support.
*   **Terminal I/O (Windows):** `colorama` for basic cross-platform ANSI escape code support (for colors) and `msvcrt` for non-blocking input. A fallback to simple `print()` and `input()` with `time.sleep()` might be necessary for minimal environments or if `curses` is not feasible/desired on Windows. A shim layer will abstract this difference.
*   **Timing:** `time` module (standard Python library) for delays and game loop timing.
*   **Randomness:** `random` module (standard Python library) for tetromino generation.

**Deployment Architecture:** On-premise (local machine), single-user execution.
**Network Architecture:** No network communication required.

### Component Architecture

The single Python file will be structured using classes to encapsulate distinct functionalities, promoting modularity and maintainability despite the single-file constraint.

1.  **`TetrisGame` Class (Game Controller/Main Loop):**
    *   **Responsibilities:**
        *   Initializes game components (`Grid`, `Piece`, `DisplayManager`, `InputManager`).
        *   Manages the main game loop (`run()`).
        *   Handles game state (running, paused, game over).
        *   Orchestrates interaction between `InputManager`, `GameLogic`, and `DisplayManager`.
        *   Manages score and level progression.
        *   Coordinates piece falling, locking, and new piece generation.
    *   **Interfaces:** `__init__`, `run`, `pause_game`, `game_over`.

2.  **`Grid` Class:**
    *   **Responsibilities:**
        *   Stores the state of the game board (locked blocks).
        *   Manages grid dimensions (10x20).
        *   Provides methods for checking collisions with the grid's walls, floor, and existing blocks.
        *   Handles line clearing logic and shifting blocks down.
    *   **Interfaces:** `__init__(width, height)`, `is_valid_position(piece)`, `add_piece(piece)`, `clear_lines()`, `get_state()`.
    *   **Data Ownership:** Owns a 2D list/array representing the game board cells.

3.  **`Piece` Class:**
    *   **Responsibilities:**
        *   Represents a single falling tetromino.
        *   Stores its shape, current position (x, y), color, and rotation state.
        *   Provides methods for moving (left, right, down), rotating, and returning its current block coordinates.
        *   Manages the predefined shapes and their rotations for all 7 tetromino types.
    *   **Interfaces:** `__init__(shape_type, spawn_x, spawn_y)`, `move(dx, dy)`, `rotate()`, `get_blocks()`, `get_color()`.
    *   **Data Ownership:** Owns shape definition (list of block coordinates relative to origin), current (x,y) position, current rotation index.

4.  **`DisplayManager` Class:**
    *   **Responsibilities:**
        *   Abstracts terminal-specific rendering (e.g., `curses` or `colorama`).
        *   Initializes and cleans up the terminal environment.
        *   Draws the game grid, falling piece, next piece, score, and game messages.
        *   Handles clearing the screen and updating specific regions.
        *   Manages color display if supported by the terminal library.
    *   **Interfaces:** `__init__()`, `setup_terminal()`, `teardown_terminal()`, `draw_grid(grid_state)`, `draw_piece(piece)`, `draw_next_piece(piece)`, `draw_score(score)`, `draw_message(message)`, `refresh()`.

5.  **`InputManager` Class:**
    *   **Responsibilities:**
        *   Abstracts terminal-specific input handling (non-blocking).
        *   Reads user keystrokes without waiting for Enter.
        *   Maps raw keystrokes to predefined game actions (e.g., 'a' -> MOVE_LEFT).
    *   **Interfaces:** `__init__()`, `get_key_press()`.
    *   **Inter-component Communication:**
        *   `TetrisGame` orchestrates calls to `DisplayManager` for drawing and `InputManager` for input.
        *   `TetrisGame` passes `Piece` objects to `Grid` for collision checks and locking.
        *   `TetrisGame` updates its internal state based on `Grid`'s line clearing results.

### Data Architecture

The game's data will be entirely in-memory, managed by the respective classes.

*   **Game Grid Data:**
    *   A 2D list of integers or characters within the `Grid` class.
    *   Each cell represents an empty space (e.g., 0 or ' ') or a locked block (e.g., 1-7 representing piece type/color, or '#').
*   **Piece Data:**
    *   `Piece` objects will store their `shape` as a list of relative `(dx, dy)` coordinates for their constituent blocks.
    *   `position` (x, y tuple) representing the top-left corner or origin of the piece.
    *   `rotation_state` (integer index) to track current orientation.
    *   `color_id` (integer) for display purposes.
*   **Scoring Data:**
    *   Integer variables in the `TetrisGame` class for current score, lines cleared, and level.
*   **Caching Strategies:** No explicit caching is required as all data is transient and in-memory. Content delivery is not applicable.

## 4. Detailed Component Specifications

### Core Services and Modules

#### `TetrisGame` Class

*   **Purpose:** The central orchestrator of the game.
*   **Responsibilities:**
    *   Initialize `Grid`, `DisplayManager`, `InputManager`.
    *   Manage game state: `running`, `paused`, `game_over`.
    *   Main game loop: `run()` method.
    *   Generate random next piece and spawn current piece.
    *   Handle automatic piece falling based on a timer.
    *   Process user input and trigger piece actions (move, rotate, drop).
    *   Check for piece locking conditions.
    *   Integrate locked pieces into the `Grid`.
    *   Check for and process line clears.
    *   Update score and level.
    *   Check for game over condition.
    *   Manage falling speed.
*   **Input/Output Specifications:**
    *   **Input:** User key presses (via `InputManager`).
    *   **Output:** Updates to `DisplayManager` for rendering.
*   **API Design:**
    *   `__init__(self)`: Constructor, initializes components.
    *   `run(self)`: Main game loop, handles timing, input, updates, drawing.
    *   `_spawn_new_piece(self)`: Selects next piece, creates new `Piece` object, checks for game over.
    *   `_handle_input(self, key)`: Processes a single key press.
    *   `_update_game_state(self)`: Advances game logic (falling, locking, line clears).
    *   `_draw(self)`: Calls `DisplayManager` methods to update the screen.
    *   `_game_over(self)`: Sets game_over flag, displays message.
    *   `_calculate_score(self, lines_cleared)`: Updates score based on lines.
*   **State Management:** `self.grid`, `self.current_piece`, `self.next_piece`, `self.score`, `self.level`, `self.lines_cleared`, `self.game_over`, `self.paused`, `self.fall_time_accumulator`, `self.fall_speed`.
*   **Data Persistence:** None.
*   **Error Handling:** Catches potential errors from `curses` setup/teardown. Invalid inputs are silently ignored. Game over is a controlled state.

#### `Grid` Class

*   **Purpose:** Manages the static state of the Tetris board.
*   **Responsibilities:**
    *   Hold the 2D array representing the settled blocks.
    *   Detect collisions of a `Piece` with walls, floor, or other blocks.
    *   Add a `Piece` to the grid when it locks.
    *   Identify and clear full lines, shifting remaining blocks down.
*   **Input/Output Specifications:**
    *   **Input:** `Piece` object and its proposed `(x, y)` position and rotation state.
    *   **Output:** Boolean `True/False` for collision checks; list of cleared line indices.
*   **API Design:**
    *   `__init__(self, width, height)`: Initializes grid with empty cells.
    *   `is_valid_position(self, piece, dx=0, dy=0, rotation_state=None)`: Checks if `piece` at `(piece.x + dx, piece.y + dy)` with `rotation_state` collides.
    *   `add_piece(self, piece)`: Integrates `piece`'s blocks into the grid.
    *   `clear_lines(self)`: Scans for full lines, removes them, shifts down, returns count.
    *   `get_state(self)`: Returns a copy of the current grid state (for `DisplayManager`).
    *   `reset(self)`: Clears the grid.
*   **State Management:** `self._grid_data` (2D list of integers/enums for block types or empty).
*   **Data Persistence:** None.
*   **Error Handling:** Checks for out-of-bounds access internally.

#### `Piece` Class

*   **Purpose:** Represents a single, actively falling Tetromino.
*   **Responsibilities:**
    *   Store and manage the specific shape, color, and current position/rotation of a tetromino.
    *   Provide methods for transforming (moving, rotating) its shape.
    *   Expose its current block coordinates for collision detection and rendering.
*   **Input/Output Specifications:**
    *   **Input:** `dx, dy` for movement; no input for rotation.
    *   **Output:** Updated internal position/rotation; list of block coordinates `(x, y)` for rendering/collision.
*   **API Design:**
    *   `__init__(self, shape_id, x, y)`: Initializes a piece based on `shape_id` (0-6), spawn `x, y`.
    *   `move(self, dx, dy)`: Updates `self.x`, `self.y`.
    *   `rotate(self, clockwise=True)`: Updates `self.rotation_state` and applies rotation transformation to shape.
    *   `get_blocks(self)`: Returns absolute `(x, y)` coordinates of all blocks in the current piece.
    *   `get_shape_matrix(self, rotation_state=None)`: Returns the 2D matrix for a specific rotation (used for internal calculations).
    *   `get_color_id(self)`: Returns the color ID for the piece.
*   **State Management:** `self.x`, `self.y` (current position), `self.shape_id`, `self.rotation_state` (0-3), `self.color_id`. Predefined static `_SHAPES` and `_COLORS` dictionaries/lists.
*   **Data Persistence:** None.
*   **Error Handling:** None critical, invalid rotation states would be handled by `Grid` collision check.

### User Interface Components (via `DisplayManager`)

#### `DisplayManager` Class

*   **Purpose:** To abstract all terminal-specific display logic.
*   **Responsibilities:**
    *   Initialize and restore the terminal state (`curses.initscr()`, `curses.noecho()`, `curses.cbreak()`, `curses.curs_set(0)`, `curses.endwin()`).
    *   Manage `curses` windows/pads or `colorama` initialization.
    *   Render the game elements using appropriate characters and colors.
    *   Refresh the screen.
*   **Input/Output Specifications:**
    *   **Input:** `grid_state` (2D list from `Grid`), `Piece` object (for current/next), `score`, `message` strings.
    *   **Output:** Characters drawn to the terminal screen.
*   **API Design:**
    *   `__init__(self, width, height, next_piece_display_size)`: Defines display areas.
    *   `setup_terminal(self)`: Initializes `curses` (or platform-specific equivalent).
    *   `teardown_terminal(self)`: Restores terminal state.
    *   `_draw_border(self, window, width, height)`: Draws borders around game area.
    *   `draw_grid(self, grid_state, current_piece)`: Renders grid content and current falling piece.
    *   `draw_next_piece(self, piece)`: Renders the next piece in a separate area.
    *   `draw_score(self, score, lines, level)`: Displays game statistics.
    *   `draw_message(self, message)`: Overlays a message (e.g., "PAUSED", "GAME OVER").
    *   `clear_message(self)`: Clears any active message.
    *   `refresh(self)`: Updates the physical terminal screen.
*   **UI/UX Design Patterns:**
    *   Uses a fixed-size terminal window.
    *   ASCII/Unicode characters for blocks (e.g., '[]', '##', or custom block characters).
    *   Colors (if `curses` is available and terminal supports it) to differentiate pieces and improve readability.
    *   Clear separation of game area, score area, and next piece area.
*   **Responsive Design:** Not applicable for fixed-size terminal.
*   **Accessibility:** Relies on standard terminal fonts and colors. High contrast color palette will be chosen.

### Integration Components

#### `InputManager` Class

*   **Purpose:** To provide a unified interface for non-blocking keyboard input across platforms.
*   **Responsibilities:**
    *   Abstract `curses.getch()` on Unix/macOS or `msvcrt.getch()` on Windows.
    *   Return a normalized key code or identifier.
*   **Input/Output Specifications:**
    *   **Input:** None (reads from stdin).
    *   **Output:** String or integer representing the pressed key (e.g., 'a', 'KEY_LEFT', 'q').
*   **API Design:**
    *   `__init__(self)`: Initializes any platform-specific input configurations.
    *   `get_key_press(self)`: Attempts to read a key press without blocking. Returns `None` if no key is pressed.
*   **Authentication/Authorization:** Not applicable.
*   **Monitoring/Logging:** Basic logging of unhandled key presses could be added for debugging.

## 5. Data Design and Management

### Data Models

*   **Game `Grid`:**
    *   Represented as `List[List[int]]` (Python list of lists).
    *   `grid[y][x]` stores an integer: `0` for empty, `1-7` for different Tetromino types (corresponding to `Piece.shape_id`).
    *   **Validation Rules:** `0 <= x < GRID_WIDTH`, `0 <= y < GRID_HEIGHT`.
*   **`Piece`:**
    *   `x, y`: `int` (current top-left coordinate).
    *   `shape_id`: `int` (0-6, unique identifier for each tetromino type).
    *   `rotation_state`: `int` (0-3, current orientation index).
    *   `_SHAPES`: `Dict[int, List[List[List[int]]]]` - A dictionary where keys are `shape_id` and values are a list of 2D matrices, each matrix representing a rotation state. Each matrix uses `1` for a block, `0` for empty.
    *   `_COLORS`: `Dict[int, int]` - Mapping `shape_id` to `curses` color pair ID.
*   **Game State:**
    *   `score`: `int`
    *   `lines_cleared`: `int`
    *   `level`: `int`
    *   `fall_speed`: `float` (seconds per row)

### Database Design

No database is required. All game state is ephemeral and resides in memory.

### API Specifications

All "APIs" are internal class methods.

*   **`TetrisGame`:**
    *   `run()`: Starts the game loop.
    *   `_handle_input(key_char)`: Interprets input.
    *   `_update_game_state()`: Advances game time.
    *   `_draw()`: Renders the game.
*   **`Grid`:**
    *   `is_valid_position(piece_object, dx, dy, rotation_state_index)`: Checks for collision at a target location/orientation.
    *   `add_piece(piece_object)`: "Burns" a piece into the grid.
    *   `clear_lines()`: Removes full lines.
*   **`Piece`:**
    *   `move(dx, dy)`: Changes internal position.
    *   `rotate()`: Changes internal rotation state.
    *   `get_blocks()`: Returns a list of (x, y) coordinates of the piece's blocks.
*   **`DisplayManager`:**
    *   `draw_grid(grid_state_matrix, current_piece_object)`: Renders the main game area.
    *   `draw_score(score_int, lines_int, level_int)`: Renders statistics.
    *   `draw_message(message_string)`: Displays temporary messages.
*   **`InputManager`:**
    *   `get_key_press()`: Returns the last pressed key, or None.

## 6. Security and Compliance Design

### Security Architecture

*   **Authentication and Authorization:** Not applicable (single-user, local game).
*   **Data Encryption:** Not applicable (no sensitive data, no storage).
*   **Network Security:** Not applicable (no network communication).
*   **Secure Coding Practices:**
    *   Adhere to Python best practices (PEP 8).
    *   Avoid `eval()` or similar dangerous functions.
    *   Input sanitization is not strictly necessary as input is limited to single keystrokes, but robust error handling for unexpected input will be present.
*   **Vulnerability Mitigation:** Minimal attack surface. The primary risk is a denial-of-service (crashing the game) through malformed input, which is handled by ignoring unknown key presses.

### Compliance Requirements

*   **Regulatory Compliance:** Not applicable (non-commercial, local application).
*   **Industry Standards:** Adherence to Python coding standards (PEP 8).
*   **Data Governance/Privacy:** Not applicable (no user data collected or stored).
*   **Audit Trails/Reporting:** Not applicable.
*   **Risk Assessment:** Very low risk profile due to isolated, local execution and lack of external dependencies or sensitive data.

## 7. Performance and Scalability

### Performance Design

*   **Performance Targets:**
    *   Input latency: < 50ms.
    *   Display refresh: Smooth, visually uninterrupted.
    *   Game logic update rate: Consistent with `fall_speed`.
*   **Caching Strategies:** Not applicable.
*   **Database Optimization:** Not applicable.
*   **Resource Utilization:**
    *   Use of `time.sleep()` for game loop timing to avoid busy-waiting.
    *   Efficient `curses` (or `colorama`) screen updates by redrawing only changed areas where possible, or using `curses` `noutrefresh()` and `doupdate()` for optimized batch updates.
    *   Avoid unnecessary object creation within the main loop.
*   **Load Testing:** Not applicable. Manual playtesting will confirm performance.

### Scalability Planning

*   **Scalability Requirements:** Not applicable. The game is designed for a single user, single instance, on a local machine.
*   **Horizontal/Vertical Scaling:** Not applicable.
*   **Capacity Planning:** Not applicable.

## 8. Implementation Strategy

### Development Phases

The development will follow an iterative approach, starting with core mechanics and progressively adding features.

1.  **Phase 1: Foundation (MVP)**
    *   Set up terminal `DisplayManager` (init/teardown, basic `draw_grid`).
    *   Implement `InputManager` for non-blocking input.
    *   Create `Grid` class with empty 10x20 board.
    *   Implement `TetrisGame` main loop, drawing empty grid and accepting 'q' to quit.
2.  **Phase 2: Core Gameplay**
    *   `Piece` class with all 7 shapes, spawning.
    *   Implement piece falling (`TetrisGame` timer).
    *   Implement `Grid.is_valid_position()` for basic collision with walls/floor.
    *   Horizontal movement (`Piece.move()`, `Grid.is_valid_position()`).
    *   Piece locking (`Grid.add_piece()`).
    *   Game Over condition (`TetrisGame` spawn check).
3.  **Phase 3: Advanced Mechanics**
    *   Rotation (`Piece.rotate()`, `Grid.is_valid_position()` for collision, implement Wall Kick System rules).
    *   Soft Drop and Hard Drop.
    *   Line clearing (`Grid.clear_lines()`).
    *   Scoring (`TetrisGame` score calculation).
    *   Next Piece display.
    *   Pause functionality.
4.  **Phase 4: Refinement and Polish**
    *   Enhanced terminal display (colors, borders, score display).
    *   Difficulty scaling (falling speed increase).
    *   Final testing and bug fixing.

**MVP Definition:** A playable game with falling pieces, horizontal movement, rotation, piece locking, line clearing, and game over, running in the terminal.

### Technical Implementation

*   **Development Environment:** Python 3.x, preferred IDE/editor (VS Code, PyCharm).
*   **Code Organization:**
    *   All classes (`TetrisGame`, `Grid`, `Piece`, `DisplayManager`, `InputManager`) defined within a single Python file.
    *   Constants (grid dimensions, colors, key mappings) defined at the top level.
    *   `if __name__ == "__main__":` block to instantiate and run `TetrisGame`.
*   **Build/Deployment:** No build process. The `.py` file is the deliverable. Run via `python tetris_game.py`.
*   **Testing Strategies:** Primarily manual playtesting. Unit tests can be written for `Grid` collision/line clearing logic and `Piece` rotation/movement logic within the same file or as a separate temporary file.
*   **Quality Assurance:** Adherence to PEP 8. Self-review and peer-review (if applicable).

### Deployment and Operations

*   **Infrastructure Provisioning:** Minimal. Requires a Python 3.x installation and a compatible terminal emulator.
*   **Deployment Strategies:** Direct distribution of the `tetris_game.py` file.
*   **Monitoring and Alerting:** Basic `try-except` blocks for graceful handling of unexpected errors. No external monitoring.
*   **Backup and Disaster Recovery:** Not applicable.
*   **Maintenance and Support:** Manual bug fixes and updates to the single file.

## 9. Quality Assurance and Testing

### Testing Strategy

*   **Unit Testing:**
    *   `Grid` class: Test `is_valid_position` (edge cases for walls, floor, existing blocks), `add_piece`, `clear_lines` (single, double, triple, Tetris clears, no clears).
    *   `Piece` class: Test `move`, `rotate` (all rotations for each piece, Wall Kick System logic).
*   **Integration Testing:**
    *   Verify `TetrisGame` correctly integrates `Piece` and `Grid` for falling, locking, line clearing, and game over.
    *   Verify `InputManager` correctly translates keys to actions.
    *   Verify `DisplayManager` correctly renders game state.
*   **End-to-End Testing (Manual Playtesting):**
    *   Play multiple full games to identify bugs, performance issues, and UI quirks.
    *   Test all key inputs for expected behavior.
    *   Stress test with rapid input and high piece counts.
    *   Confirm game over condition functions correctly.
    *   Verify scoring is accurate.
*   **Performance/Load Testing:** Manual observation of responsiveness and smoothness during play. No automated load testing tools will be used.

### Quality Metrics

*   **Code Quality:** PEP 8 compliance. Code complexity (e.g., maintainable function lengths). Readability.
*   **Functional Correctness:** All FRs met and validated through testing.
*   **Stability:** Zero crashes during extended manual testing.
*   **User Experience:** Responsive controls, clear display, intuitive gameplay.
*   **Reproducibility:** Consistent behavior across different runs and environments (within portability limits).

## 10. Risk Management and Mitigation

### Technical Risks

| Risk ID | Risk                                        | Impact | Probability | Mitigation Strategy                                                                                                                                                                                                                                                                                                                                     |
| :------ | :------------------------------------------ | :----- | :---------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TR-001  | `curses` library incompatibility/issues     | Medium | Medium      | Provide platform-specific `DisplayManager` and `InputManager` implementations (e.g., `colorama`/`msvcrt` for Windows as fallback). Clearly document system requirements and potential workarounds in comments. Abstract terminal interaction behind interfaces.                                                                                         |
| TR-002  | Complex Tetromino Rotation Logic (WKS)      | High   | Medium      | Thoroughly research and implement the Super Rotation System (SRS) or a simplified Wall Kick System (WKS) for Tetris. Create detailed unit tests for all piece rotations and collision scenarios. Use clear data structures for rotation tables.                                                                                                    |
| TR-003  | Collision Detection Edge Cases              | High   | Medium      | Write comprehensive tests for piece collisions with walls, floor, and existing blocks, especially during rotations and rapid movement. Break down collision logic into small, testable functions.                                                                                                                                             |
| TR-004  | Single File Complexity                      | Medium | Medium      | Maintain strict adherence to class-based modularity within the single file. Use clear naming conventions, comments, and consistent coding style (PEP 8) to ensure readability and maintainability. Keep functions/methods concise.                                                                                                      |
| TR-005  | Performance Bottlenecks (Display Refresh)   | Medium | Low         | Utilize `curses` efficient update mechanisms (`noutrefresh`, `doupdate`). Optimize drawing loops to only redraw changed parts of the screen where feasible. Avoid excessive I/O operations in the game loop.                                                                                                                            |
| TR-006  | Input Latency / Non-blocking Input          | Medium | Medium      | Implement OS-specific non-blocking input handling carefully (`curses.getch()` on Unix/macOS, `msvcrt.getch()` on Windows). Ensure event loop processes input frequently. Test on target platforms to confirm responsiveness.                                                                                                               |

### Mitigation Strategies

*   **Risk Assessment Matrix:** (See table above).
*   **Contingency Plans:** For `curses` incompatibility, use simpler `colorama`/`msvcrt` based approaches or a basic `print()` based refresh with `os.system('cls')` or `os.system('clear')` as a last resort, sacrificing smoothness for compatibility.
*   **Monitoring:** Internal logging (print statements) for debugging.
*   **Regular Reviews:** Manual code review.
*   **Dependencies:** Standard Python libraries are considered stable.

## 11. Future Extensibility and Evolution

### Extensibility Design

The class-based structure, even within a single file, allows for relatively easy expansion:

*   **Plugin Architectures:**
    *   **New Tetrominoes:** Adding new shapes would involve updating the `Piece._SHAPES` and `Piece._COLORS` definitions.
    *   **New Game Modes:** Could be implemented by modifying `TetrisGame`'s update logic (e.g., timed mode, sprint mode).
*   **API Design for Integrations:** Not directly applicable to external APIs, but internal interfaces (method signatures) are designed to be stable.
*   **Configuration Management:** Game parameters like `GRID_WIDTH`, `GRID_HEIGHT`, initial `FALL_SPEED`, score values can be defined as constants at the top of the file for easy modification.
*   **Feature Flags:** Simple boolean variables could enable/disable experimental features during development.
*   **Backward Compatibility:** Future changes should strive to maintain the current game mechanics as a "classic" mode.

### Evolution Planning

*   **Technology Roadmap:**
    *   **Refactor to multiple files:** If the codebase grows significantly (e.g., adding AI opponent, more complex UI), it can be refactored into a package structure (e.g., `game/`, `display/`, `input/` modules).
    *   **Graphical User Interface (GUI):** Transition to a library like Pygame or PyQt for a richer visual experience, while reusing much of the `Grid` and `Piece` game logic.
*   **Feature Enhancement:**
    *   **Ghost Piece:** Display a shadow of where the current piece will hard drop.
    *   **Hold Piece:** Allow holding one piece to swap later.
    *   **Next-N Pieces:** Show multiple upcoming pieces.
    *   **High Score System:** Implement local file-based storage for high scores.
    *   **Sound Effects:** Add basic terminal beeps or integrate a simple audio library.
*   **Performance Optimization:** If moving to a GUI, more advanced rendering techniques might be needed.
*   **Architecture Refactoring:** The core game logic classes (`Grid`, `Piece`) are designed to be relatively independent and could be extracted into a separate "engine" module if a GUI is developed, allowing the same logic to power different frontends.

---
**END OF SPECIFICATION**
