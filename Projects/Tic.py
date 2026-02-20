import os

# Clear screen (works on Windows & Mac/Linux)
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_board(board):
    print("\n")
    print("     TIC TAC TOE")
    print("  -------------------")
    print(f"     {board[0]} | {board[1]} | {board[2]}")
    print("    ---+---+---")
    print(f"     {board[3]} | {board[4]} | {board[5]}")
    print("    ---+---+---")
    print(f"     {board[6]} | {board[7]} | {board[8]}")
    print("  -------------------\n")


def check_win(board, player):
    win_positions = [
        [0,1,2], [3,4,5], [6,7,8],  # Rows
        [0,3,6], [1,4,7], [2,5,8],  # Columns
        [0,4,8], [2,4,6]            # Diagonals
    ]

    for pos in win_positions:
        if all(board[i] == player for i in pos):
            return True
    return False


def is_draw(board):
    return all(cell in ['X', 'O'] for cell in board)


def get_valid_input(board):
    while True:
        try:
            value = int(input("👉 Choose position (0-8): "))
            if value < 0 or value > 8:
                print("❌ Please enter number between 0 and 8.")
            elif board[value] in ['X', 'O']:
                print("⚠️ Position already taken. Try again.")
            else:
                return value
        except ValueError:
            print("❌ Invalid input! Enter a number.")


def play_game():
    board = [str(i) for i in range(9)]
    current_player = "X"

    while True:
        clear_screen()
        print_board(board)
        print(f"🎮 Player {current_player}'s Turn")

        move = get_valid_input(board)
        board[move] = current_player

        if check_win(board, current_player):
            clear_screen()
            print_board(board)
            print(f"🏆 Player {current_player} Wins! Congratulations!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("🤝 It's a Draw!")
            break

        current_player = "O" if current_player == "X" else "X"


if __name__ == "__main__":
    print("✨ Welcome to Tic Tac Toe ✨")
    input("Press Enter to start...")
    play_game()