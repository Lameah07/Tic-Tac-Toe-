import random

# --------- Helpers ---------
def print_board(b):
    print("\n")
    print(f" {b[0]} | {b[1]} | {b[2]} ")
    print("---+---+---")
    print(f" {b[3]} | {b[4]} | {b[5]} ")
    print("---+---+---")
    print(f" {b[6]} | {b[7]} | {b[8]} ")
    print("\n")

def winning_lines():
    return [
        (0,1,2), (3,4,5), (6,7,8),  # rows
        (0,3,6), (1,4,7), (2,5,8),  # cols
        (0,4,8), (2,4,6)            # diagonals
    ]

def check_winner(b):
    # returns 'X' or 'O' if winner, 'D' if draw, None if game ongoing
    for a, c, d in winning_lines():
        if b[a] == b[c] == b[d] and b[a] in ("X", "O"):
            return b[a]
    if all(s in ("X", "O") for s in b):
        return "D"
    return None

def available_moves(b):
    return [i for i, s in enumerate(b) if s not in ("X", "O")]

# --------- Minimax (Hard AI) ---------
def minimax(board, maximizing, ai, human):
    winner = check_winner(board)
    if winner == ai:
        return 10
    if winner == human:
        return -10
    if winner == "D":
        return 0

    if maximizing:
        best_score = -float("inf")
        for move in available_moves(board):
            board[move] = ai
            score = minimax(board, False, ai, human)
            board[move] = str(move+1)
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for move in available_moves(board):
            board[move] = human
            score = minimax(board, True, ai, human)
            board[move] = str(move+1)
            best_score = min(best_score, score)
        return best_score

def best_move(board, ai="O", human="X"):
    # Try winning, then block, else minimax
    # 1) Can AI win now?
    for m in available_moves(board):
        board[m] = ai
        if check_winner(board) == ai:
            board[m] = str(m+1)  # undo
            return m
        board[m] = str(m+1)
    # 2) Can human win next? Block it.
    for m in available_moves(board):
        board[m] = human
        if check_winner(board) == human:
            board[m] = str(m+1)
            return m
        board[m] = str(m+1)
    # 3) Otherwise use minimax for perfect play
    best_score = -float("inf")
    move_choice = None
    for m in available_moves(board):
        board[m] = ai
        score = minimax(board, False, ai, human)
        board[m] = str(m+1)
        if score > best_score:
            best_score = score
            move_choice = m
    return move_choice

# --------- Game Loops ---------
def get_human_move(board, player_symbol):
    while True:
        try:
            cell = input(f"Player {player_symbol}, choose (1-9): ").strip()
            idx = int(cell) - 1
            if idx not in range(9):
                print("Please choose a number 1–9.")
                continue
            if board[idx] in ("X", "O"):
                print("That cell is taken. Try another.")
                continue
            return idx
        except ValueError:
            print("Numbers only, 1–9.")

def game_pvp():
    board = [str(i+1) for i in range(9)]
    turn = "X"
    print("\nTic-Tac-Toe — Player vs Player\n")
    print_board(board)
    while True:
        move = get_human_move(board, turn)
        board[move] = turn
        print_board(board)
        result = check_winner(board)
        if result:
            if result == "D":
                print("It's a draw! 🤝")
            else:
                print(f"Player {result} wins! 🎉")
            break
        turn = "O" if turn == "X" else "X"

def game_pvc(difficulty="easy"):
    board = [str(i+1) for i in range(9)]
    human, ai = "X", "O"
    print(f"\nTic-Tac-Toe — Player vs Computer ({difficulty.title()})\n")
    print_board(board)
    turn = "X"  # human always goes first (you can change if you want)
    while True:
        if turn == human:
            move = get_human_move(board, human)
        else:
            if difficulty == "easy":
                move = random.choice(available_moves(board))
            else:  # hard
                move = best_move(board, ai=ai, human=human)
            print(f"Computer chooses: {move+1}")
        board[move] = turn if turn == human else ai
        print_board(board)
        result = check_winner(board)
        if result:
            if result == "D":
                print("It's a draw! 🤝")
            elif result == human:
                print("You win! 🎉")
            else:
                print("Computer wins! 🤖")
            break
        turn = ai if turn == human else human

def main():
    print("===== TIC-TAC-TOE =====")
    print("1) Player vs Player")
    print("2) Player vs Computer (Easy)")
    print("3) Player vs Computer (Hard / Unbeatable)")
    choice = input("Choose mode (1/2/3): ").strip()
    if choice == "1":
        game_pvp()
    elif choice == "2":
        game_pvc("easy")
    else:
        game_pvc("hard")

if __name__ == "__main__":
    main()
