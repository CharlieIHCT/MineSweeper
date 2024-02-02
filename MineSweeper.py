import random
import time
import os
def number_to_emoji(num):
    # Define the mapping between numbers and emojis
    emoji_mapping = {
        0: "0️⃣ ",
        1: "1️⃣ ",
        2: "2️⃣ ",
        3: "3️⃣ ",
        4: "4️⃣ ",
        5: "5️⃣ ",
        6: "6️⃣ ",
        7: "7️⃣ ",
        8: "8️⃣ ",
        9: "9️⃣ ",
    }

    # Convert the number to a string and map each digit to its corresponding emoji
    emoji_str = "".join(emoji_mapping[int(digit)] for digit in str(num))

    return emoji_str

class Board:
    def __init__(self, size, num_bombs):
        #size and num_bombs
        self.width = size[0]
        self.height = size[1]
        self.size = self.width * self.height
        self.num_bombs = num_bombs

        #create_board
        self.board = self.create_board()
        self.set_block_values()

        #save blocks which have dug
        self.dug = set()

    def create_board(self):
        #create empty board
        board =  [[None for c in range(self.width)] for r in range(self.height)]
        """
        board = 
        [None, None, ...,  None],
        [None, None, ...,  None],
        [None, None, ...,  None],
        [None, None, ...,  None]
        """
    
        for _ in range(self.num_bombs):
            location = random.randint(0, self.size -1)
            row = location // self.height#y
            col = location % self.width#x
            board[row][col] = '💣'
            """
            #this is fine also
            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)
            board[row][col] = '💣'
            """

        return board
    
    def set_block_values(self):
        for r in range(self.height):
            for c in range(self.width):
                if self.board[r][c] == '💣':#bomb
                    continue
                self.board[r][c] = self.calculate_nearby_bombs(r, c)

    def calculate_nearby_bombs(self, row, col):
        #make sure not to go out of bounds
        """
        [None -> None -> None],
        [None -> block(continue) -> None],
        [None -> None -> None],
        """
        num_nearby_bombs = 0
        for r in range(max(0, row-1), min(self.height-1, row+1) + 1):
            for c in range(max(0, col-1), min(self.width-1, col+1) + 1):
                if (r==row and c==col):
                    continue#don't count the spot itself as a nearby bomb
                elif self.board[r][c] == '💣':
                    num_nearby_bombs += 1
        return num_nearby_bombs
    
    def dig(self, row, col):
        self.dug.add((row, col))#add to set

        if self.board[row][col] == '💣':#bomb
            return False
        
        elif self.board[row][col] > 0:#have bombs nearby, don't dig outside
            return True
        
        #if self.board[row][col] == 0: 
        for r in range(max(0, row-1), min(self.height-1, row+1) + 1):
            for c in range(max(0, col-1), min(self.width-1, col+1) + 1):
                if (r, c) in self.dug:
                    continue #checked
                self.dig(r, c)#recursion
        return True

    def show(self):
        visible_board = [[None for c in range(self.width)] for r in range(self.height)]
        for row in range(self.height):
            for col in range(self.width):
                if (row, col) in self.dug:
                    tmp = number_to_emoji(self.board[row][col]) if  self.board[row][col] != '💣' else '💣'
                    visible_board[row][col] = tmp
                else:
                    visible_board[row][col] = "🧱"
                print(visible_board[row][col],end=" ")
            print("")
        
    def reveal(self):
        for row in range(self.height):
            for col in range(self.width):
                tmp = number_to_emoji(self.board[row][col]) if  self.board[row][col] != '💣' else '💣'
                self.board[row][col] = tmp
                print(self.board[row][col],end=" ")
            print("")


def play(size, num_bombs):
    #Step 1. create board
    board = Board(size, num_bombs)
    is_safe = True 
    while len(board.dug) < board.size - board.num_bombs:
        #Step 2. print boards
        board.show()
        print("")
        #Step 3. Input
        tmp = input("Where would you like to dig?(col:x) (row:y):")#from 1
        if tmp == "reveal":
            board.reveal()
            break
        else:
            col, row = map(int, tmp.split())
            col, row = col -1, row -1#from 0

        #check if invalid input
        if row < 0 or row >= board.height or col < 0 or col >= board.width:
            print("Invalid location. Please try again.")
            continue
        
        
        #Step 4. & 5. check result of dug
        is_safe = board.dig(row, col)
        if not is_safe:
            break #game over
        time.sleep(0.5)
    
    time.sleep(1)#wait for game over screen show up
    #Step 6. win or lose
    if is_safe:
        print("CONGRATULATIONS! YOU WIN!!!")
        time.sleep(1)

        tmp = input("again?(Y/N):")
        if tmp == "Y":
            os.system('cls')
            size, num_bombs= title_screen()
            play(size, num_bombs)
        else:
            print("byebye ^ ^")
    else:
        print("SORRY, GAME OVER :(")
        #reveal complete board
        board.reveal()
        time.sleep(2)

        tmp = input("again?(Y/N):")
        if tmp == "Y":
            os.system('cls')
            size, num_bombs= title_screen()
            play(size, num_bombs)
        else:
            print("byebye ^ ^")

def title_screen():
    while(True):
        difficulty = int(input("Please Choose the Difficulty(enter number)\n1 Beginner\n2 Intermediate\n3 Expert\n4 Custom\nmode:"))
        match(difficulty):
            case 1:
                size = (8, 8)
                num_bombs = 10
            case 2:
                size = (16, 16)
                num_bombs = 40
            case 3:
                size = (16, 30)
                num_bombs = 99
            case 4:
                while(True):
                    w,h = map(int, input("Please Enter Width and Height for the board(up to 80, 80):").split()) 
                    if w > 35 or w < 0 or h > 35  or h < 0:
                        print("Width and Height of map should be between 0 and 35. Please Try Again.")
                        continue
                    else:
                        num_bombs = int(input("Please Enter The Number of Bombs:"))
                        if num_bombs > 300 or num_bombs < 0:
                            print("Number of bombs should be between 0 and 300. Please Try Again.")
                            continue
                    break
                size = (w, h)
            case _:
                print("Invalid Input")
                time.sleep(1.5)
                os.system('cls')
                continue
        break
    return size, num_bombs
size, num_bombs= title_screen()
play(size, num_bombs)
