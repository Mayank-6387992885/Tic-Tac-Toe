# ==========================================================
#  TIC-TAC-TOE PROJECT -- FINAL RELEASE
#  Tic-Tac-Toe Game with AI using Minimax Algorithm and Alpha-Beta Pruning
#  Features : Single Player, Two Player, AI Difficulty Levels, Move History
#  Author : Mayank Baranwal
# ==========================================================

# -------- Import necessary libraries --------
import math
import time
import sys
import json
import os
import colorama

# -------- Initialize colorama for Windows --------
colorama.init(autoreset=True)

SCORE_FILE = "tic_tac_toe_leaderboard.json"

# -------- Load leaderboard safely --------
def load_leaderboard():
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

# -------- Save leaderboard --------
def save_leaderboard(leaderboard):
    with open(SCORE_FILE, "w") as f:
        json.dump(leaderboard, f, indent=4)

# -------- Print board with colored AI moves and numbered empty cells --------
def print_board(board, highlight=[], blink=False, move_owners=None):
    print("\nCurrent Board:")
    print("  1   2   3")
    print(" +---+---+---+")
    for i, row in enumerate(board):
        row_display = []
        for j, cell in enumerate(row):
            owner = move_owners.get((i,j), "player") if move_owners else "player"
            if (i, j) in highlight:
                row_display.append(colorama.Fore.GREEN + colorama.Style.BRIGHT + cell if blink else colorama.Fore.GREEN + cell)
            elif cell == "X":
                row_display.append(colorama.Fore.RED + cell if owner=="player" else colorama.Fore.CYAN + cell)
            elif cell == "O":
                row_display.append(colorama.Fore.BLUE + cell if owner=="player" else colorama.Fore.CYAN + cell)
            else:
                row_display.append(str(i*3 + j + 1))
        print(f"{i+1} | " + " | ".join(row_display) + " |")
        print(" +---+---+---+")
    print()

# -------- Print move history --------
def print_move_history(history):
    print("\nMove History:")
    for idx, move in enumerate(history, 1):
        player, pos = move
        color = colorama.Fore.RED if player == "X" else colorama.Fore.BLUE
        print(f"{idx}. {color}{player}{colorama.Style.RESET_ALL} -> Cell {pos+1}")
    print()

# -------- Show available moves --------
def available_moves(board):
    moves = [str(i*3 + j + 1) for i in range(3) for j in range(3) if board[i][j] == " "]
    print("Available moves:", ", ".join(moves))

# -------- Check winner --------
def check_winner(board, player):
    for i, row in enumerate(board):
        if all(cell == player for cell in row):
            return True, [(i, j) for j in range(3)]
    for j in range(3):
        if all(board[i][j] == player for i in range(3)):
            return True, [(i, j) for i in range(3)]
    if all(board[i][i] == player for i in range(3)):
        return True, [(i, i) for i in range(3)]
    if all(board[i][2 - i] == player for i in range(3)):
        return True, [(i, 2 - i) for i in range(3)]
    return False, []

# -------- Check draw --------
def is_full(board):
    return all(cell in ['X', 'O'] for row in board for cell in row)

# -------- Minimax algorithm with alpha-beta pruning --------
def minimax(board, depth, is_maximizing, alpha, beta):
    if check_winner(board, "O")[0]:
        return 10 - depth
    if check_winner(board, "X")[0]:
        return depth - 10
    if is_full(board):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = " "
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        return max_eval
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = " "
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        return min_eval
        return min_eval

# -------- AI chooses best move --------
def ai_move(board):
    for _ in range(3):
        sys.stdout.write("\rAI is thinking" + "." * (_+1) + " " * (3-(_+1)))
        sys.stdout.flush()
        time.sleep(0.4)
    print("\r" + " " * 20 + "\r", end="")

    best_score = -math.inf
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(board, 0, False, -math.inf, math.inf)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    if best_move:
        board[best_move[0]][best_move[1]] = "O"
        return best_move[0]*3 + best_move[1]

# -------- Blink winning cells --------
def blink_winner(board, highlight, times=5, delay=0.3):
    for _ in range(times):
        print_board(board, highlight, blink=True)
        time.sleep(delay)
        print_board(board)
        time.sleep(delay)

# -------- Display leaderboard --------
def display_leaderboard(leaderboard):
    print("\n=== Leaderboard ===")
    sorted_board = sorted(leaderboard.items(), key=lambda x: x[1]["Player"], reverse=True)
    for idx, (player, stats) in enumerate(sorted_board, 1):
        print(f"{idx}. {player} - Wins: {stats['Player']}, AI Wins: {stats['AI']}, Draws: {stats['Draws']}")
    print("===================\n")

# -------- Play a single game --------
def play_game(player_names, vs_ai=True, first_player="X"):
    leaderboard = load_leaderboard()
    for name in player_names:
        if name not in leaderboard:
            leaderboard[name] = {"Player": 0, "AI": 0, "Draws": 0}

    board = [[" " for _ in range(3)] for _ in range(3)]
    move_history = []
    move_owners = {}  # tracks ownership: "player" or "AI"
    current_player = first_player

    # -------- If AI goes first --------
    if vs_ai and first_player == "O":
        move = ai_move(board)
        move_history.append(("X", move))
        row, col = divmod(move, 3)
        move_owners[(row, col)] = "AI"
        current_player = "O"

    print_board(board, move_owners=move_owners)

    while True:
        if vs_ai and current_player == "O":
            move = ai_move(board)
            move_history.append(("O", move))
            row, col = divmod(move, 3)
            move_owners[(row, col)] = "AI"
        else:
            player_index = 0
            player_name = player_names[player_index]
            available_moves(board)
            while True:
                try:
                    move = int(input(f"{player_name} ({current_player}) move (1-9): ")) - 1
                    row, col = divmod(move, 3)
                    if not (0 <= row <= 2 and 0 <= col <= 2):
                        print("Invalid cell number. Choose 1-9.")
                        continue
                    if board[row][col] != " ":
                        print("Cell already taken. Try again.")
                        continue
                    board[row][col] = current_player
                    move_history.append((current_player, move))
                    move_owners[(row, col)] = "player"
                    break
                except ValueError:
                    print("Enter a number 1-9.")

        print_board(board, move_owners=move_owners)
        print_move_history(move_history)

        winner, highlight = check_winner(board, current_player)
        if winner:
            print("\a")  # beep
            blink_winner(board, highlight, move_owners=move_owners)
            if vs_ai:
                if current_player == "X":
                    print(f"{colorama.Fore.YELLOW}{player_names[0]} wins!{colorama.Style.RESET_ALL}")
                    leaderboard[player_names[0]]["Player"] += 1
                else:
                    print(f"{colorama.Fore.YELLOW}AI wins!{colorama.Style.RESET_ALL}")
                    leaderboard[player_names[0]]["AI"] += 1
            else:
                winner_index = 0
                print(f"{colorama.Fore.YELLOW}{player_names[winner_index]} wins!{colorama.Style.RESET_ALL}")
                leaderboard[player_names[winner_index]]["Player"] += 1
            break

        if is_full(board):
            print("It's a draw!")
            if vs_ai:
                leaderboard[player_names[0]]["Draws"] += 1
            else:
                leaderboard[player_names[0]]["Draws"] += 1
                leaderboard[player_names[1]]["Draws"] += 1
            break

        current_player = "O" if current_player == "X" else "X"

    save_leaderboard(leaderboard)
    display_leaderboard(leaderboard)

# -------- Main menu --------
def tic_tac_toe():
    print("Welcome to Tic-Tac-Toe!")
    while True:
        mode = input("Choose mode:\n1. Player vs Player\n2. Player vs AI\nEnter 1 or 2: ")
        if mode in ["1","2"]:
            break
        print("Invalid choice. Enter 1 or 2.")

    if mode == "1":
        p1 = input("Enter Player 1 name: ").strip() or "Player 1"
        p2 = input("Enter Player 2 name: ").strip() or "Player 2"
        play_game([p1, p2], vs_ai=False)
    else:
        p1 = input("Enter your name: ").strip() or "Player"
        while True:
            choice = input(f"{p1}, do you want to be X or O? (X goes first): ").upper()
            if choice in ["X", "O"]:
                break
            print("Invalid choice. Enter X or O.")

        first_player = choice
        play_game([p1], vs_ai=True, first_player=first_player)

    replay = input("Do you want to play again? (y/n): ").lower()
    if replay == "y":
        tic_tac_toe()
    else:
        print("Thanks for playing!")

# -------- Run the game --------
tic_tac_toe()
