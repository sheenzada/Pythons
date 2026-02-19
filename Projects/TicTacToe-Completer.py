def printBoard(xState, zState):
    # Board positions ko render karna
    board = []
    for i in range(9):
        if xState[i]:
            board.append('X')
        elif zState[i]:
            board.append('O')
        else:
            board.append(str(i))

    print(f"\n {board[0]} | {board[1]} | {board[2]} ")
    print(f"---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print(f"---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} \n")

def checkWin(xState, zState):
    # Winning combinations (Rows, Columns, Diagonals)
    wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    
    for win in wins:
        if sum(xState[win[0]], xState[win[1]], xState[win[2]]) == 3:
            print("--- X Won the match! 🏆 ---")
            return 1
        if sum(zState[win[0]], zState[win[1]], zState[win[2]]) == 3:
            print("--- O Won the match! 🏆 ---")
            return 0
    return -1

# Python ka sum function list ke liye aise use hota hai
def sum(a, b, c):
    return a + b + c

if __name__ == "__main__":
    xState = [0] * 9  # 9 positions ke liye 0 initialize kiya
    zState = [0] * 9
    turn = 1 # 1 for X and 0 for O
    
    print("Welcome to Tic Tac Toe")
    
    while True:
        printBoard(xState, zState)
        
        if turn == 1:
            print("X's Chance")
            player = 'X'
        else:
            print("O's Chance")
            player = 'O'
            
        try:
            value = int(input("Please enter a value (0-8): "))
            
            # Check agar jagah pehle se bhari hui to nahi
            if xState[value] == 1 or zState[value] == 1:
                print("⚠️ Position already occupied! Try again.")
                continue
                
            if turn == 1:
                xState[value] = 1
            else:
                zState[value] = 1
        except (ValueError, IndexError):
            print("❌ Invalid input! Please enter a number between 0 and 8.")
            continue

        # Win check karna
        cwin = checkWin(xState, zState)
        if cwin != -1:
            printBoard(xState, zState)
            print("Game Over!")
            break
        
        # Draw check karna
        if all(xState[i] or zState[i] for i in range(9)):
            printBoard(xState, zState)
            print("--- It's a Draw! 🤝 ---")
            break
            
        turn = 1 - turn