# Create a tic-tac-toe game.

def print_board(board):
    print("   1   2   3")
    print("  +---+---+---+")
    for i, row in enumerate(board):
        print(f"{i+1} | " + " | ".join(row) + " |")
        print("  +---+---+---+")

def check_winner(board, player):
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True

    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

def is_full(board):
    return all(cell in ['X', 'O'] for row in board for cell in row)


def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    print("Welcome to Tic Tac Toe!")
    print_board(board)

    while True:
        try:
            move = input(f"Player {current_player}, enter your move (row and column: 1 1): ")
            row, col = map(int, move.split())
            row -= 1
            col -= 1

            if not (0 <= row <= 2 and 0 <= col <= 2):
                print("Invalid input. Row and column must be between 1 and 3.")
                continue

            if board[row][col] != " ":
                print("Cell already taken. Try again.")
                continue

            board[row][col] = current_player
            print_board(board)

            if check_winner(board, current_player):
                print(f"Player {current_player} wins!")
                break

            if is_full(board):
                print("It's a draw!")
                break

            current_player = "O" if current_player == "X" else "X"
        except ValueError:
            print("Invalid input. Please enter two numbers separated by space.")

# Run the game
tic_tac_toe()
