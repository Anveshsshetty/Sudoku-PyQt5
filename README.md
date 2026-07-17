# Sudoku Generator and Solver (PyQt5)

A desktop Sudoku application developed using **Python** and **PyQt5**. The application can generate Sudoku puzzles with different difficulty levels and also solve any valid Sudoku entered by the user.

---

## Features

- Generate Sudoku puzzles
  - Easy
  - Medium
  - Hard
  - Expert
- Solve any valid Sudoku puzzle
- Hint system
- Clear user-entered cells
- Number pad for easy input
- Row and column highlighting
- Different interface for Puzzle Generator and Sudoku Solver
- Input validation for invalid Sudoku puzzles

---

## Technologies Used

- Python 3
- PyQt5
- Backtracking Algorithm

---

## Project Structure

```
Sudoku-PyQt5/
│
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Code Overview

### generate_sudoku()

Generates a Sudoku puzzle based on the selected difficulty level.

---

### generate_full_solution()

Creates a complete valid Sudoku grid using the backtracking algorithm.

---

### solve()

Uses recursive backtracking to solve a Sudoku puzzle.

---

### is_valid()

Checks whether placing a number in a particular cell satisfies Sudoku rules.

---

### is_grid_valid()

Validates the user's input before attempting to solve the puzzle.

---

### give_hint()

Finds one empty cell and fills it with the correct value.

---

### clear_grid()

Clears only the cells entered by the user while preserving the original puzzle.

---

### create_sudoku_page()

Creates the Sudoku Generator interface.

---

### create_blank_page()

Creates the Sudoku Solver interface where users can enter their own puzzle.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Sudoku-PyQt5.git
```

### 2. Open the project folder

```bash
cd Sudoku-PyQt5
```

### 3. Create a Virtual Environment

Windows

```bash
python -m venv venv
```

Linux / macOS

```bash
python3 -m venv venv
```

---

## Activate the Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

After activation, your terminal should look similar to

```
(venv)
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

or

```bash
pip install PyQt5
```

---

## Run the Application

```bash
python main.py
```

---

## How the Solver Works

The application uses the **Backtracking Algorithm**.

1. Find an empty cell.
2. Try numbers 1 to 9.
3. Check if the number is valid.
4. If valid, place the number.
5. Continue recursively.
6. If no number fits, backtrack.
7. Continue until the puzzle is solved.

---

## Screenshots

Add screenshots of your application here.

Example

```
screenshots/
    home_page.png
    sudoku_game.png
    sudoku_solver.png
```

---

## Future Improvements

- Dark mode
- Timer
- Score tracking
- Save and load puzzles
- Better puzzle generation with unique solution guarantee
- Keyboard shortcuts
- Sound effects

---

## Author

**Anvesh Shetty**

Electronics and Communication Engineering

Python | PyQt5 | VLSI | Embedded Systems
