import random
import time
import sys
import os


def clear_screen():
    """Clears the console screen for better game flow."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_valid_input(prompt, valid_options):
    """Helper function to get user input and ensure it's in the valid_options list."""
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        print(f"❌ Invalid input. Please enter one of: {', '.join(valid_options)}")

def select_mode_and_play(game_name, computer_func, user_func):
    """Handles the mode selection logic for games with two modes."""
    while True:
        print(f"\n╔═════════════════════════════════╗")
        print(f"║ 🎮 You selected {game_name.ljust(21)} ║")
        print(f"╚═════════════════════════════════╝")
        print("Choose a game mode:")
        print("  1. Computer vs. User (Play against the AI)")
        print("  2. User vs. User (Two-player local game)")
        print("  3. Go back to Main Menu")

        mode_choice = input("Enter your choice (1, 2, or 3): ").strip()

        clear_screen()
        
        if mode_choice == '1':
            if computer_func:
                computer_func()
            else:
                print(f"Note: {game_name} only supports User vs. User mode in this version.")
                if user_func: user_func()
            break
        elif mode_choice == '2':
            if user_func:
                user_func()
            else:
                print(f"Note: {game_name} only supports Computer vs. User mode in this version.")
                if computer_func: computer_func()
            break
        elif mode_choice == '3':
            break # Exit mode selection, back to main loop
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

#GAME 1: TIC-TAC-TOE
def display_board(board):
    print("\n")
    print("  " + board[1] + " | " + board[2] + " | " + board[3])
    print(" ---|---|---")
    print("  " + board[4] + " | " + board[5] + " | " + board[6])
    print(" ---|---|---")
    print("  " + board[7] + " | " + board[8] + " | " + board[9])
    print("\n")

def check_win(board, mark):
    return ((board[1] == mark and board[2] == mark and board[3] == mark) or
            (board[4] == mark and board[5] == mark and board[6] == mark) or
            (board[7] == mark and board[8] == mark and board[9] == mark) or
            (board[1] == mark and board[4] == mark and board[7] == mark) or
            (board[2] == mark and board[5] == mark and board[8] == mark) or
            (board[3] == mark and board[6] == mark and board[9] == mark) or
            (board[1] == mark and board[5] == mark and board[9] == mark) or
            (board[3] == mark and board[5] == mark and board[7] == mark))

def get_available_moves(board):
    return [i for i, x in enumerate(board) if x == ' ' and i != 0]

def computer_move(board, computer_mark, player_mark):
  
    available_moves = get_available_moves(board)

    # 1. Check if the computer can win in the next move
    for i in available_moves:
        board_copy = list(board)
        board_copy[i] = computer_mark
        if check_win(board_copy, computer_mark):
            return i
    
    # 2. Check if the player can win in the next move and block them
    for i in available_moves:
        board_copy = list(board)
        board_copy[i] = player_mark
        if check_win(board_copy, player_mark):
            return i

    # 3. Take the center (5) if available
    if 5 in available_moves:
        return 5

    # 4. Take a random corner
    corners = [1, 3, 7, 9]
    available_corners = [c for c in corners if c in available_moves]
    if available_corners:
        return random.choice(available_corners)

    # 5. Take a random side
    return random.choice(available_moves) if available_moves else None

def play_tic_tac_toe(is_user_vs_user):
    board = [' '] * 10 # Ignore index 0 for 1-9 board reference
    current_player = 'X'
    game_over = False

    print("\nTic-Tac-Toe: Positions are 1-9 (top-left to bottom-right).")
    
    while not game_over:
        display_board(board)
        
        if is_user_vs_user:
            print(f"It's Player {current_player}'s turn.")
            mark = current_player
        elif current_player == 'X':
            print("It's your (X) turn.")
            mark = 'X'
        else: # Computer's turn
            print("Computer (O) is thinking...")
            time.sleep(1)
            move = computer_move(board, 'O', 'X')
            if move:
                board[move] = 'O'
            
            if check_win(board, 'O'):
                display_board(board)
                print("🤖 Computer (O) wins!")
                game_over = True
            elif ' ' not in board[1:]:
                display_board(board)
                print("It's a draw!")
                game_over = True
            
            current_player = 'X' # Switch back to User
            continue

        # Get Player/User Move
        while not game_over:
            try:
                move = int(input(f"Enter your move (1-9): "))
                if move in range(1, 10) and board[move] == ' ':
                    board[move] = mark
                    break
                else:
                    print("That position is taken or invalid. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 9.")
        
        if check_win(board, mark):
            display_board(board)
            if is_user_vs_user:
                print(f"🎉 Player {mark} wins!")
            else:
                print("You (X) win! Excellent!")
            game_over = True
        elif ' ' not in board[1:]:
            display_board(board)
            print("It's a draw!")
            game_over = True

        if not game_over:
            current_player = 'O' if current_player == 'X' else 'X'

def play_tic_tac_toe_computer():
    print("\n--- Starting Tic-Tac-Toe (User (X) vs. Computer (O)) ---")
    play_tic_tac_toe(False)

def play_tic_tac_toe_user():
    print("\n--- Starting Tic-Tac-Toe (User (X) vs. User (O)) ---")
    play_tic_tac_toe(True)



#GAME 2: ROCK-PAPER-SCISSORS (Standard Random)

def determine_winner(p1_choice, p2_choice, p1_name, p2_name):
    """Determines the winner of a single round."""
    if p1_choice == p2_choice:
        return "It's a tie!", None
    
    # Check winning conditions for P1
    if (p1_choice == 'rock' and p2_choice == 'scissors') or \
       (p1_choice == 'scissors' and p2_choice == 'paper') or \
       (p1_choice == 'paper' and p2_choice == 'rock'):
        return f"🎉 {p1_name} wins! ({p1_choice.capitalize()} beats {p2_choice.capitalize()})", p1_name
    else:
        return f"🎉 {p2_name} wins! ({p2_choice.capitalize()} beats {p1_choice.capitalize()})", p2_name

def play_rps_computer():
    print("\n--- Starting Rock-Paper-Scissors (User vs. Computer) ---")
    options = ['rock', 'paper', 'scissors']
    
    user_choice = get_valid_input("Enter your choice (rock, paper, scissors): ", options)
    
    # Computer uses standard Python random
    computer_choice = random.choice(options)
    
    print(f"\nYou chose: {user_choice.capitalize()}")
    print(f"Computer chose: {computer_choice.capitalize()}")
    
    result, _ = determine_winner(user_choice, computer_choice, "You", "Computer")
    print(result)

def play_rps_user():
    print("\n--- Starting Rock-Paper-Scissors (User 1 vs. User 2) ---")
    options = ['rock', 'paper', 'scissors']
    
    p1_choice = get_valid_input("Player 1, enter your choice (rock, paper, scissors): ", options)
    
    # Clear the screen (to hide P1's choice)
    clear_screen()
    print("Player 1 has chosen. Player 2, it's your turn.")
    
    p2_choice = get_valid_input("Player 2, enter your choice (rock, paper, scissors): ", options)
    
    print("\n--- Results ---")
    print(f"Player 1 chose: {p1_choice.capitalize()}")
    print(f"Player 2 chose: {p2_choice.capitalize()}")
    
    result, _ = determine_winner(p1_choice, p2_choice, "Player 1", "Player 2")
    print(result)


#GAME 3: GUESS THE NUMBER 
def play_guess_the_number_logic(secret_number, max_guesses, guesser_name):
    """Core logic for Guess the Number."""
    print(f"\n{guesser_name}, you have {max_guesses} guesses.")
    
    for attempt in range(1, max_guesses + 1):
        try:
            guess = int(input(f"Attempt {attempt}: Enter your guess: "))
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            continue
            
        if guess < secret_number:
            print("Too low!")
        elif guess > secret_number:
            print("Too high!")
        else:
            print(f"🎉 Congratulations, {guesser_name}! You guessed the number {secret_number} in {attempt} attempts!")
            return True
    
    print(f"\nGame over! {guesser_name} failed to guess the number. The secret number was {secret_number}.")
    return False

def play_guess_the_number_computer():
    print("\n--- Starting Guess the Number (User vs. Computer) ---")
    LOWER_BOUND = 1
    UPPER_BOUND = 100
    MAX_ATTEMPTS = 7 # Good for a 1-100 range
    
    secret_number = random.randint(LOWER_BOUND, UPPER_BOUND)
    print(f"I'm thinking of a number between {LOWER_BOUND} and {UPPER_BOUND}.")
    
    play_guess_the_number_logic(secret_number, MAX_ATTEMPTS, "You")

def play_guess_the_number_user():
    print("\n--- Starting Guess the Number (User 1 sets, User 2 guesses) ---")
    
    while True:
        try:
            LOWER_BOUND = int(input("Player 1, enter the lower bound (e.g., 1): "))
            UPPER_BOUND = int(input("Player 1, enter the upper bound (e.g., 100): "))
            if LOWER_BOUND >= UPPER_BOUND:
                print("The lower bound must be less than the upper bound.")
                continue
            
            secret_number = int(input(f"Player 1, enter the secret number between {LOWER_BOUND} and {UPPER_BOUND}: "))
            if not (LOWER_BOUND <= secret_number <= UPPER_BOUND):
                print("The secret number must be within the specified range.")
                continue
            
            MAX_ATTEMPTS = int(input("Player 1, enter the maximum number of guesses: "))
            if MAX_ATTEMPTS <= 0:
                print("Maximum guesses must be a positive number.")
                continue
            
            # Clear the screen for the guessing player
            clear_screen()
            break
            
        except ValueError:
            print("Invalid input. Please enter whole numbers.")

    print("Player 2, it's your turn to guess!")
    play_guess_the_number_logic(secret_number, MAX_ATTEMPTS, "Player 2")



# GAME 4: HAND CRICKET (USER vs. COMPUTER)
def play_hand_cricket_computer():
    print("\n--- Starting Hand Cricket (User vs. Computer) ---")
    print("Rules: Enter a number from 1 to 6. If your number matches the computer's, you're OUT.")
    
    # 1. TOSS
    while True:
        toss_choice = get_valid_input("Toss: Enter 'odd' or 'even': ", ['odd', 'even'])
        user_toss = random.randint(1, 6)
        comp_toss = random.randint(1, 6)
        toss_sum = user_toss + comp_toss
        toss_result = "even" if toss_sum % 2 == 0 else "odd"
        
        print(f"You showed {user_toss}, Computer showed {comp_toss}. Sum is {toss_sum} ({toss_result}).")
        
        if toss_result == toss_choice:
            print("You won the toss!")
            bat_or_bowl = get_valid_input("Choose to 'bat' or 'bowl': ", ['bat', 'bowl'])
            
            user_batting = bat_or_bowl == 'bat'
            break
        else:
            print("Computer won the toss!")
            # Simple computer decision: always choose to bat first
            user_batting = False
            print("Computer chose to bat first.")
            break
            
    # 2. INNINGS 1
    def play_innings(player_name, is_user_batting, target=sys.maxsize):
        score = 0
        print(f"\n--- {player_name} is {'BATTING' if is_user_batting else 'BOWLING'}{f' (Target: {target})' if target != sys.maxsize else ''} ---")
        
        while True:
            try:
                if is_user_batting:
                    user_run = int(input(f"Enter runs (1-6): "))
                    if not 1 <= user_run <= 6:
                        raise ValueError
                    comp_bowl = random.randint(1, 6)
                    print(f"You: {user_run}, Computer: {comp_bowl}")
                    
                    if user_run == comp_bowl:
                        print(f"OUT! Match (Computer)!")
                        break
                    
                    score += user_run
                else: # Computer Batting
                    comp_run = random.randint(1, 6)
                    user_bowl = int(input(f"Enter bowl (1-6): "))
                    if not 1 <= user_bowl <= 6:
                        raise ValueError
                    print(f"You: {user_bowl}, Computer: {comp_run}")

                    if user_bowl == comp_run:
                        print(f"OUT! Match (You)!")
                        break
                    
                    score += comp_run
                
                print(f"Current Score: {score}")
                
                if score >= target:
                    print(f"Target {target} reached!")
                    return score # Target achieved
                
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 6.")
                continue
                
        return score
        
    p1_score = play_innings("You" if user_batting else "Computer", user_batting)
    target = p1_score + 1
    
    # 3. INNINGS 2
    p2_score = play_innings("Computer" if user_batting else "You", not user_batting, target)

    # 4. RESULT
    print("\n--- Final Scorecard ---")
    print(f"Team 1 Score ({'You' if user_batting else 'Computer'}): {p1_score}")
    print(f"Team 2 Score ({'Computer' if user_batting else 'You'}): {p2_score}")
    
    if p1_score > p2_score and user_batting:
        print(f"🎉 You won by {p1_score - p2_score} runs!")
    elif p2_score > p1_score and not user_batting:
        print(f"🎉 You won by scoring {p2_score} runs (Target: {target-1})!")
    elif p1_score > p2_score and not user_batting:
        print(f"🎉 Computer won by scoring {p1_score} runs (Target: {target-1})!")
    elif p2_score > p1_score and user_batting:
        print(f"🎉 Computer won by scoring {p2_score} runs (Target: {target-1})!")
    else:
        print("It's a tie!")

def play_hand_cricket_user():
    print("Hand Cricket is currently only available in Computer vs. User mode.")
    play_hand_cricket_computer()


#GAME 5: BINGO 
def create_bingo_card():
    """Generates a 5x5 Bingo card (B:1-15, I:16-30, N:31-45, G:46-60, O:61-75)."""
    
    def generate_col(start, end, count):
        return random.sample(range(start, end + 1), count)

    b_col = generate_col(1, 15, 5)
    i_col = generate_col(16, 30, 5)
    n_col = generate_col(31, 45, 4)
    g_col = generate_col(46, 60, 5)
    o_col = generate_col(61, 75, 5)
    
    # Place columns into a structure
    card = [b_col, i_col, n_col[:2] + [0] + n_col[2:], g_col, o_col]
    
    # Transpose the card structure from columns to rows
    rows = [
        [card[col][row] for col in range(5)]
        for row in range(5)
    ]
    return rows

def display_bingo_card(card, player_name):
    """Prints the Bingo card, marking matched numbers with an 'X'."""
    print(f"\n--- {player_name}'s Bingo Card ---")
    print("  B   I   N   G   O")
    print("-------------------------")
    
    for row in card:
        row_str = "|"
        for num in row:
            if num == 'X':
                # Displays the cross (X) as requested
                row_str += " X  |" 
            elif num == 0:
                row_str += "F R |" # Free space
            else:
                row_str += f"{num:2} |"
        print(row_str)
        print("-------------------------")

def check_bingo(card):
    """Checks for 5 in a row, column, or diagonal."""
    
    def is_marked(val):
        # A cell is considered marked if it's 'X' or 0 (Free Space)
        return val == 'X' or val == 0

    # 1. Rows
    if any(all(is_marked(val) for val in row) for row in card):
        return True
    
    # 2. Columns
    for c in range(5):
        column = [card[r][c] for r in range(5)]
        if all(is_marked(val) for val in column):
            return True
            
    # 3. Diagonals
    diag1 = [card[i][i] for i in range(5)] # Top-left to bottom-right
    diag2 = [card[i][4 - i] for i in range(5)] # Top-right to bottom-left
    
    if all(is_marked(val) for val in diag1) or all(is_marked(val) for val in diag2):
        return True
        
    return False

def mark_card(card, number):
    """Marks the given number on the card with 'X'."""
    found = False
    for r in range(5):
        for c in range(5):
            if card[r][c] == number:
                card[r][c] = 'X'
                found = True
    return found

def play_bingo_user():
    print("--- Starting Bingo (User 1 vs. User 2) ---")
    
    p1_card = create_bingo_card()
    p2_card = create_bingo_card()
    
    # Mark the Free space (0) as 'X' from the start
    mark_card(p1_card, 0)
    mark_card(p2_card, 0)
    
    called_numbers = set()
    numbers_to_call = random.sample(range(1, 76), 75)
    player_turn = 1
    
    while numbers_to_call:
        clear_screen()
        print("🎲 Current Called Numbers: ", sorted(list(called_numbers)))
        display_bingo_card(p1_card, "Player 1")
        display_bingo_card(p2_card, "Player 2")
        
        input(f"\nPlayer {player_turn}, press Enter to call the next number...")
        
        called_num = numbers_to_call.pop(0)
        called_numbers.add(called_num)
        
        print(f"\n\nBINGO CALL: 📢 {called_num} 📢")
        
        mark_card(p1_card, called_num)
        mark_card(p2_card, called_num)
        
        time.sleep(1)
        
        # Check for Bingo
        if check_bingo(p1_card):
            clear_screen()
            display_bingo_card(p1_card, "Player 1")
            display_bingo_card(p2_card, "Player 2")
            print("\n=================================")
            print("🎉🎉🎉 PLAYER 1 WINS BINGO! 🎉🎉🎉")
            print("=================================")
            return
            
        if check_bingo(p2_card):
            clear_screen()
            display_bingo_card(p1_card, "Player 1")
            display_bingo_card(p2_card, "Player 2")
            print("\n=================================")
            print("🎉🎉🎉 PLAYER 2 WINS BINGO! 🎉🎉🎉")
            print("=================================")
            return
            
        # Switch turn
        player_turn = 2 if player_turn == 1 else 1

    print("No more numbers to call! It's a draw.")

def play_bingo_computer():
    print("Bingo is currently only available in User vs. User mode.")
    play_bingo_user()



#GAME 6: MEMORY GAME (MATCHING PAIRS)
def create_memory_board(size=4):
    """Creates a shuffled board of matching pairs (e.g., AA BB CC...)."""
    num_pairs = size * size // 2
    

    symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
    if num_pairs > len(symbols):
        raise ValueError("Board size is too large for the available symbols.")
        
    board_values = symbols[:num_pairs] * 2
    random.shuffle(board_values)
    
  
    board = [board_values[i:i + size] for i in range(0, size * size, size)]
    return board

def display_memory_board(board, revealed, board_size):
    """Displays the board, showing uncovered tiles or their coordinates."""
    
    
    header = "    " + " ".join(f"{c:2}" for c in range(board_size))
    print(header)
    print("  " + "---" * board_size + "-")
    
    for r in range(board_size):
        row_str = f"{r} | "
        for c in range(board_size):
            # Check if the tile is permanently revealed (part of a found pair)
            if (r, c) in revealed:
                row_str += f"{board[r][c]:2} "
            else:
                # Tile is hidden
                row_str += "XX "
        print(row_str)
    print("  " + "---" * board_size + "-")

def get_coordinates(prompt_text, board_size):
    """Gets valid row and column coordinates from the user."""
    while True:
        try:
            coord_str = input(prompt_text).strip()
            if ',' not in coord_str:
                print("❌ Invalid format. Use 'row,col' (e.g., '0,1').")
                continue
                
            r, c = map(int, coord_str.split(','))
            
            if 0 <= r < board_size and 0 <= c < board_size:
                return (r, c)
            else:
                print(f"❌ Coordinates must be between 0 and {board_size - 1}.")
        except ValueError:
            print("❌ Invalid input. Please enter numbers separated by a comma.")

def play_memory_game_user():
    print("--- Starting Memory Game (User 1 vs. User 2) ---")
    
    
    BOARD_SIZE = 4
    board = create_memory_board(BOARD_SIZE)
    
    
    revealed_coords = set()
    
   
    scores = {'P1': 0, 'P2': 0}
    current_player = 'P1'
    total_pairs = BOARD_SIZE * BOARD_SIZE // 2
    
    while sum(scores.values()) < total_pairs:
        clear_screen()
        print(f"Current Scores: P1: {scores['P1']} | P2: {scores['P2']}")
        print(f"It's {current_player}'s turn. Find a pair!")
        display_memory_board(board, revealed_coords, BOARD_SIZE)
        
        # --- First Card ---
        print("\nCard 1:")
        while True:
            c1_coords = get_coordinates("Enter coordinates for the first card (row,col): ", BOARD_SIZE)
            if c1_coords not in revealed_coords:
                break
            print("❌ That card is already revealed. Choose a hidden card.")
            
        r1, c1 = c1_coords
        val1 = board[r1][c1]
        
        
        temp_revealed = revealed_coords.union({c1_coords})
        clear_screen()
        print(f"Current Scores: P1: {scores['P1']} | P2: {scores['P2']}")
        print(f"It's {current_player}'s turn. Find a pair!")
        display_memory_board(board, temp_revealed, BOARD_SIZE)
        print(f"Flipped Card 1 ({r1},{c1}): {val1}")
        
        # --- Second Card ---
        print("\nCard 2:")
        while True:
            c2_coords = get_coordinates("Enter coordinates for the second card (row,col): ", BOARD_SIZE)
            if c2_coords == c1_coords:
                print("❌ You must choose a different card.")
                continue
            if c2_coords not in revealed_coords:
                break
            print("❌ That card is already revealed. Choose a hidden card.")
            
        r2, c2 = c2_coords
        val2 = board[r2][c2]
        
       
        temp_revealed = revealed_coords.union({c1_coords, c2_coords})
        clear_screen()
        print(f"Current Scores: P1: {scores['P1']} | P2: {scores['P2']}")
        print(f"It's {current_player}'s turn. Find a pair!")
        display_memory_board(board, temp_revealed, BOARD_SIZE)
        print(f"Flipped Card 1 ({r1},{c1}): {val1}")
        print(f"Flipped Card 2 ({r2},{c2}): {val2}")
        
        if val1 == val2:
            print(f"\n✅ MATCH! {current_player} scores a pair!")
            scores[current_player] += 1
            revealed_coords.update({c1_coords, c2_coords})
            
            if sum(scores.values()) == total_pairs:
                break # Exit loop early if game ends
                
            print("🎉 Keep the turn!")
            time.sleep(2)
        else:
            print("\n❌ NO MATCH. Cards flip back over.")
            time.sleep(3)
            
            current_player = 'P2' if current_player == 'P1' else 'P1'

   
    clear_screen()
    display_memory_board(board, revealed_coords, BOARD_SIZE)
    print("\n==================================")
    print("        🎉 GAME OVER 🎉")
    print("==================================")
    print(f"Final Scores: Player 1: {scores['P1']} | Player 2: {scores['P2']}")
    
    if scores['P1'] > scores['P2']:
        print("🏆 Player 1 wins!")
    elif scores['P2'] > scores['P1']:
        print("🏆 Player 2 wins!")
    else:
        print("🤝 It's a draw!")
    time.sleep(5)

def play_memory_game_computer():
    print("Memory Game is currently only available in User vs. User mode.")
    play_memory_game_user()


#MAIN PROGRAM LOOP
def main_menu():
    """The main entry point for the multi-game program."""
    clear_screen()
    print("╔═════════════════════════════════╗")
    print("║ 👾 PYTHON CONSOLE ARCADE 👾      ║")
    print("║   Your destination for text-    ║")
    print("║   based gaming fun!             ║")
    print("╚═════════════════════════════════╝")

    while True:
        print("\n--- MAIN MENU ---")
        print("Select a game to play:")
        print("  1. Tic-Tac-Toe")
        print("  2. Rock-Paper-Scissors")
        print("  3. Guess the Number")
        print("  4. Hand Cricket (U vs C only)")
        print("  5. Bingo (U vs U only)")
        print("  6. Memory Game (U vs U only)")
        print("  Q. Quit")

        game_choice = input("Enter your choice (1-6, Q): ").strip().upper()

        clear_screen()

        if game_choice == '1':
            select_mode_and_play("Tic-Tac-Toe", play_tic_tac_toe_computer, play_tic_tac_toe_user)
        
        elif game_choice == '2':
            select_mode_and_play("Rock-Paper-Scissors", play_rps_computer, play_rps_user)

        elif game_choice == '3':
            select_mode_and_play("Guess the Number", play_guess_the_number_computer, play_guess_the_number_user)
        
        elif game_choice == '4':
            # Hand Cricket (U vs C only)
            select_mode_and_play("Hand Cricket", play_hand_cricket_computer, play_hand_cricket_user)

        elif game_choice == '5':
            # Bingo (U vs U only)
            select_mode_and_play("Bingo", play_bingo_computer, play_bingo_user)
        
        elif game_choice == '6':
            # Memory Game (U vs U only)
            select_mode_and_play("Memory Game", play_memory_game_computer, play_memory_game_user)
        
        elif game_choice == 'Q':
            print("\n👋 Thanks for playing! Goodbye!")
            break
        
        else:
            print("❌ Invalid selection. Please try again.")


# Start the program
if __name__ == "__main__":
    main_menu()
