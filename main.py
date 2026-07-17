import random
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QStackedWidget, QLineEdit, QMessageBox

app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("Sudoku")
main_window.setGeometry(100,100,600,400)
main_window.resize(900, 800)
main_window.setStyleSheet("background-color:#e0f7fa;")
is_active = False
selected_cell = None

# Helper functions to solve Sudoku
def generate_full_solution(grid):
    """Solve the Sudoku grid using backtracking."""
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num   
                        if generate_full_solution(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True 

def is_valid(grid, row, col, num):
    """Check if a number is valid in the given position."""
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False
    return True


def generate_sudoku(difficulty="easy"):
    """Generates a Sudoku puzzle with a given difficulty level."""
    # Start with an empty grid
    grid = [[0] * 9 for _ in range(9)]
    
    # Fill the grid with a solved Sudoku puzzle
    generate_full_solution(grid)
    
    # Remove cells based on difficulty level
    num_cells_to_remove = {
        "easy": random.randint(30, 35),
        "medium": random.randint(36, 40),
        "hard": random.randint(41, 44),
        "expert": random.randint(45, 49)
    }
    
    # Difficulty level logic
    cells_to_remove = num_cells_to_remove[difficulty]
    
    while cells_to_remove > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        
        # Remove the cell only if it's not already empty
        if grid[row][col] != 0:
            grid[row][col] = 0
            cells_to_remove -= 1
    
    return grid


def solve(grid):
    """Solve the Sudoku using backtracking."""
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if solve(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True

def update_puzzle():
    global puzzle
    puzzle = generate_sudoku(difficulty)
    set_grid_to_cells(cells, puzzle)

def set_difficulty_easy():
    global difficulty
    difficulty = "easy"
    update_puzzle()

def set_difficulty_medium():
    global difficulty
    difficulty = "medium"
    update_puzzle()

def set_difficulty_hard():
    global difficulty
    difficulty = "hard"
    update_puzzle()

def set_difficulty_expert():
    global difficulty
    difficulty = "expert"
    update_puzzle()

#

def get_grid_from_cells(cells):
    """Retrieve the grid from the input fields."""
    grid = []
    for row in cells:
        grid_row = []
        for cell in row:
            val = cell.text()
            grid_row.append(int(val) if val.isdigit() else 0)
        grid.append(grid_row)
    return grid

def set_grid_to_cells(cells, grid):
    """Set the grid into the input fields."""
    for row in range(9):
        for col in range(9):
            value = str(grid[row][col]) if grid[row][col] != 0 else ""
            cells[row][col].setText(value)


def solve_sudoku(cells):
    """Solve the Sudoku and display the solution or clear the grid if invalid."""
    grid = get_grid_from_cells(cells)
    reset_highlights(cells)
    if is_grid_valid(grid):
        if solve(grid):
            set_grid_to_cells(cells, grid)
    else:
        QMessageBox.warning(None, "Invalid Input", "The input Sudoku is invalid. Clearing the grid.")
        clear_grid(cells)

def is_grid_valid(grid):
    """Check if the current grid is valid (follows Sudoku rules)."""
    for row in range(9):
        for col in range(9):
            num = grid[row][col]
            if num != 0:
                grid[row][col] = 0  
                if not is_valid(grid, row, col, num):
                    grid[row][col] = num 
                    return False
                grid[row][col] = num  
    return True

#

def give_hint(cells):
    """Provide a hint by filling one correct number."""
    reset_highlights(cells)
    empty_cells = [(row, col) for row in range(9) for col in range(9) if cells[row][col].text() == ""]
    if empty_cells:
        row, col = random.choice(empty_cells)
        grid = get_grid_from_cells(cells)
        solve(grid)
        if grid[row][col] == 0:
            QMessageBox.warning(None, "Invalid Input", "The input Sudoku is invalid.")
        correct_number = grid[row][col]
        cells[row][col].setText(str(correct_number))
        cells[row][col].setStyleSheet("color: green; font-weight: bold; border: 1px solid black;")
        if puzzle[row][col] != 0:
            cells[row][col].setStyleSheet("color: blue; font-weight: bold; background-color: white; border: 1px solid black;")   

def clear_grid(cells):
    """Clear only the user-entered cells in the grid."""
    reset_highlights(cells)
    # Iterate through all the cells
    for row in range(9):
        for col in range(9):
            cell = cells[row][col]
            # Only clear editable (user-entered) cells, not the pre-filled ones
            if not cell.isReadOnly():
                cell.clear()  
                cell.setStyleSheet("background-color: white; border: 1px solid black;font-size:30px;") 

def number_button_clicked(cells, number):
    """Handle number button click."""
    if selected_cell:
        row, col = selected_cell
        cell = cells[row][col]
        # Only change the value of the selected cell
        if not cell.isReadOnly():
         cell.setText(str(number))

def highlight_row_and_column(cells, row, col):
    """Highlight the entire row and column for the clicked cell."""
    reset_highlights(cells)
    for r in range(9):
        cells[r][col].setStyleSheet("background: lightgrey; border: 1px solid black;font-size:30px;")  # Highlight column
    for c in range(9):
        cells[row][c].setStyleSheet("background: lightgrey; border: 1px solid black;font-size:30px;")  # Highlight row

    cells[row][col].setStyleSheet("background: lightyellow; border: 1px solid black; font-weight: bold;font-size:30px;")  # Highlight the cell itself

def reset_highlights(cells):
    """Reset all cells to their default background color."""
    for row in range(9):
        for col in range(9):
            if cells[row][col].isReadOnly() is False:
                cells[row][col].setStyleSheet("background-color: white; border: 1px solid black;font-size:30px;")
            else:
                if puzzle[row][col] != 0:
                    cells[row][col].setStyleSheet("color: blue; font-weight: bold; background-color: white; border: 1px solid black;font-size:30px;")

# page1
def create_sudoku_page(puzzle):
    """Creates a Sudoku page with a grid and number buttons."""
    page = QWidget()
    layout = QVBoxLayout()
    grid_layout = QGridLayout()
    grid_layout.setAlignment(Qt.AlignCenter)

    cells = []
    for row in range(9):
        row_cells = []
        for col in range(9):
            cell = QLineEdit()
            cell.setMaxLength(1)
            cell.setAlignment(Qt.AlignCenter)
            cell.setStyleSheet("background-color: white; border: 1px solid black;")
            cell.setFixedSize(100,100)
            # If the puzzle has a pre-filled value, make the cell read-only
            if puzzle[row][col] != 0:
                cell.setText(str(puzzle[row][col]))
                cell.setReadOnly(True)  # Pre-filled cells should be read-only
                # Change the color of pre-filled numbers
                cell.setStyleSheet("color: blue; font-weight: bold; background-color: white; border: 1px solid black;")
            else:
                cell.setReadOnly(False)  # Empty cells should be editable
                cell.setStyleSheet("background-color: white;")
            grid_layout.addWidget(cell, row, col)
            row_cells.append(cell)
        cells.append(row_cells)    
    # Number buttons
    number_layout = QHBoxLayout()
    for num in range(1, 10):
        button = QPushButton(str(num))
        button.setStyleSheet(" background-color: #fdf6e3;")
        button.clicked.connect(lambda _, num=num: number_button_clicked(cells, num))
        button.clicked.connect(lambda:reset_highlights(cells))
        number_layout.addWidget(button)

    # other buttons
    button_layout = QHBoxLayout()
    
    hint_button = QPushButton("Hint")
    hint_button.setStyleSheet(" background-color: lightgreen;")
    hint_button.clicked.connect(lambda: give_hint(cells))
    button_layout.addWidget(hint_button)
    
    clear_button = QPushButton("Clear")
    clear_button.setStyleSheet(" background-color: white;")
    clear_button.clicked.connect(lambda: clear_grid(cells))
    button_layout.addWidget(clear_button)

    close_button = QPushButton("Close")
    close_button.setStyleSheet(" background-color: #ff4d4d;color:white;")
    close_button.clicked.connect(lambda: show_main_page())
    button_layout.addWidget(close_button)

    layout.addLayout(grid_layout)
    layout.addLayout(number_layout)
    layout.addLayout(button_layout)
    page.setLayout(layout)
    
    return page, cells

# page2
def create_blank_page():
    """Creates a blank Sudoku page with solve, clear, and close buttons."""
    blank_page = QWidget()
    layout = QVBoxLayout()
    grid_layout = QGridLayout()
    grid_layout.setAlignment(Qt.AlignCenter)

    blank_cells = []
    for row in range(9):
        row_cells = []
        for col in range(9):
            cell = QLineEdit()
            cell.setMaxLength(1)
            cell.setAlignment(Qt.AlignCenter)
            cell.setFixedSize(100,100)
            grid_layout.addWidget(cell, row, col)
            row_cells.append(cell)
        blank_cells.append(row_cells)

        # Number buttons
    number_layout = QHBoxLayout()
    for num in range(1, 10):
        button = QPushButton(str(num))
        button.setStyleSheet(" background-color: #fdf6e3;")
        button.clicked.connect(lambda _, num=num: number_button_clicked(blank_cells, num))
        button.clicked.connect(lambda:reset_highlights(blank_cells))
        number_layout.addWidget(button)    

    # other buttons
    button_layout = QHBoxLayout()

    solve_button = QPushButton("Solve")
    solve_button.setStyleSheet(" background-color: lightgreen;")
    solve_button.clicked.connect(lambda: solve_sudoku(blank_cells))
    button_layout.addWidget(solve_button)

    clear_button = QPushButton("Clear")
    clear_button.setStyleSheet(" background-color: white;")
    clear_button.clicked.connect(lambda: clear_grid(blank_cells))
    button_layout.addWidget(clear_button)

    close_button = QPushButton("Close")
    close_button.setStyleSheet(" background-color: red;")
    close_button.clicked.connect(lambda: show_main_page())
    button_layout.addWidget(close_button)

    layout.addLayout(grid_layout)
    layout.addLayout(number_layout)
    layout.addLayout(button_layout)
    blank_page.setLayout(layout)

    return blank_page, blank_cells


difficulty = "easy"  # Default to easy
difficulty_buttons_layout = QHBoxLayout()

   # Buttons for difficulty levels
easy_button = QPushButton("Easy", clicked=set_difficulty_easy)
easy_button.setStyleSheet("background-color:#c8e6c9;")
medium_button = QPushButton("Medium", clicked=set_difficulty_medium)
medium_button.setStyleSheet("background-color:#f1c40f;")
hard_button = QPushButton("Hard", clicked=set_difficulty_hard)
hard_button.setStyleSheet("background-color:#ffb74d;")
expert_button = QPushButton("Expert", clicked=set_difficulty_expert)
expert_button.setStyleSheet("background-color:#f44336;")

difficulty_buttons_layout.addWidget(easy_button)
difficulty_buttons_layout.addWidget(medium_button)
difficulty_buttons_layout.addWidget(hard_button)
difficulty_buttons_layout.addWidget(expert_button)

puzzle = generate_sudoku(difficulty)

# Main window and page switching
stacked_widget = QStackedWidget()
main_page = QWidget()
main_layout = QVBoxLayout()

page1, cells = create_sudoku_page(puzzle)
stacked_widget.addWidget(main_page)
stacked_widget.addWidget(page1)


def cell_clicked(row, col):
    global selected_cell
    selected_cell = (row, col)
    highlight_row_and_column(cells, row, col)
    highlight_row_and_column(blank_cells, row, col)

def inti(cells):
    """Activate the action when button1 is clicked."""
    global is_active
    if not is_active:
        is_active = True
    for row in range(9):
        for col in range(9):
            cells[row][col].mousePressEvent = lambda event, r=row, c=col: cell_clicked(r, c)


blank_page, blank_cells = create_blank_page()
stacked_widget.addWidget(blank_page)

def show_blank_page():
    reset_highlights(blank_cells)
    stacked_widget.setCurrentWidget(blank_page)

def show_page1():
    reset_highlights(cells)
    stacked_widget.setCurrentWidget(page1)

def show_main_page():
    reset_highlights(cells)
    reset_highlights(blank_cells)
    stacked_widget.setCurrentWidget(main_page)

def resize():
    title.setGeometry(0,0,main_window.width(),50)

title = QLabel("Sudoku")
title.setStyleSheet("font-size:90px;font-weight:bold;color:black;")
title1 = QLabel("Sudoku Puzzle")
title1.setStyleSheet("font-size:40px;font-weight:bold;color:black;")
title2 = QLabel("Sudoku Solver")
title2.setStyleSheet("font-size:40px;font-weight:bold;color:black;")
Button1 = QPushButton("Start Sudoku", clicked=show_page1)
Button1.clicked.connect(lambda:inti(cells))
Button1.clicked.connect(lambda:clear_grid(cells))
Button1.setContentsMargins(200,0,200,0)
Button1.setStyleSheet("background-color:white;font-weight:bold;color:black;")

Button2 = QPushButton("Sudoku Solver", clicked=show_blank_page)
Button2.clicked.connect(lambda:inti(blank_cells))
Button2.clicked.connect(lambda:clear_grid(blank_cells))
Button2.setStyleSheet("background-color:white;font-weight:bold;color:black;")
difficulty_buttons_layout.setContentsMargins(200,0,200,0)

layout = QVBoxLayout()
layout1=QVBoxLayout()
layout1.addWidget(title,alignment=Qt.AlignHCenter|Qt.AlignTop)
layout1.addWidget(title1,alignment=Qt.AlignCenter)
layout1.addLayout(difficulty_buttons_layout)
layout1.addWidget(Button1)
layout1.addWidget(title2,alignment=Qt.AlignCenter)
layout1.addWidget(Button2,alignment=Qt.AlignTop)
main_page.setLayout(layout1)

# Set stacked widget as the main window's layout
main_layout.addWidget(stacked_widget)
main_window.setLayout(main_layout)
main_window.show()

# Start the app
app.exec_()