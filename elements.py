import pygame
debug = False

class Board(object):

    """This is the board object, it holds all the stones's positions in the
    board_array list, the data and functions for it to draw itself and handles
    the placement and deletion of stones"""

    def __init__(self, game, size):
        self.game = game

        #This creates the board_array list and sets up the points on the board
        #according to the size
        if size == 19:
            self.board_array = [[0 for x in range(0, size)] for y in range(0, size)]
            self.points = [(3,3), (3,9), (3, 15), (9,3), (9,9), (9, 15), (15,3), (15,9), (15, 15)]
            print("The board has been set to 19 x 19")
        if size == 13:
            self.board_array = [[0 for x in range(0, size)] for y in range(0, size)]
            self.points = [(3,3), (3,6), (3, 9), (6,3), (6,6), (6, 9), (9,3), (9,6), (9, 9)]
            print("The board has been set to 13 x 13")
        if size == 9:
            self.board_array = [[0 for x in range(0, size)] for y in range(0, size)]
            self.points = [(2,2), (2,6), (4, 4), (6,2), (6,6)]
            print("The board has been set to 9 x 9")
        self.size = size

        self.square_size = (self.game.win_width - self.game.margin * 2) // self.size
        self.start_grid = (4 + self.game.margin, 40 + self.game.margin)
        self.tablesize = self.square_size * self.size

        #A list containing the stones eaten on previous turns to check against repetition
        self.last_eaten = []


    def draw(self):
        pygame.draw.rect(self.game.win, (45, 45, 45), (self.start_grid[0] + 6, self.start_grid[1] + 6, self.tablesize, self.tablesize))
        pygame.draw.rect(self.game.win, (40, 40, 40), (self.start_grid[0] + 4, self.start_grid[1] + 4, self.tablesize, self.tablesize))
        pygame.draw.rect(self.game.win, (35, 35, 35), (self.start_grid[0] + 2, self.start_grid[1] + 2, self.tablesize, self.tablesize))
        pygame.draw.rect(self.game.win, (220, 200, 100), (self.start_grid[0], self.start_grid[1], self.tablesize, self.tablesize))

        #draw grid
        if debug:
            for x in range(self.size):
                for y in range(self.size):
                    pygame.draw.rect(self.game.win, (240, 220, 120),
                    (self.start_grid[0] + x * self.square_size,
                     self.start_grid[1] + y * self.square_size,
                     self.square_size, self.square_size), 1)

        #draw board}
        for x in range(self.size -1):
            for y in range(self.size -1):
                pygame.draw.rect(self.game.win, (0,0,0),
                (self.start_grid[0] + x * self.square_size + self.square_size // 2,
                 self.start_grid[1] + y * self.square_size + self.square_size // 2,
                 self.square_size, self.square_size), 1)

                if (x, y) in self.points:
                     pygame.draw.circle(self.game.win, (0, 0, 0), (self.start_grid[0] + x * self.square_size + self.square_size // 2,
                      self.start_grid[1] + y * self.square_size + self.square_size // 2), int(self.square_size * .15))

    #The next two functions are self-explanatory
    def addStone(self, color, location):
        self.board_array[location[0]][location[1]] = Stone(color, location, self, self.game.win)

    def removeStone(self, location):
        self.board_array[(location[0])][location[1]] = 0

    def update(self):
        #Updates all the stones, nessesary for the undo function
        for x in self.board_array:
            for y in x:
                if y:
                    y.update()

    def move(self, player_color):
        """This handles the movement of the player
        It first checks if the move is legal withing the game and then proceeds
        to save a copy of the board for the undo function, adds the stoneremove
        the stones that must be removed if any, resets the temporal stone and
        passes the turn.
        """

        legal_move, delete = self.moveCheck(player_color)
        if legal_move:
            self.game.history[0].append([x[:] for x in self.board_array])
            self.game.history[1] == self.game.pass_count
            self.game.turn_count += 1
            self.game.scores = [self.game.black_player.eaten_stones, self.game.white_player.eaten_stones]

            if delete:
                for group in delete:
                    for stone_loc in group.stones:
                        self.removeStone(stone_loc)
                        if self.game.turn_black:
                            self.game.black_player.eaten_stones += 1
                        else:
                            self.game.white_player.eaten_stones += 1

            #Setting up all the turn change and writing the changes
            self.addStone(player_color, (self.game.temp_stone.pos_x, self.game.temp_stone.pos_y))
            print(self.game.temp_stone.pos_x, self.game.temp_stone.pos_y)
            self.game.temp_stone.pos_x = (self.size - 1) // 2
            self.game.temp_stone.pos_y = (self.size - 1) // 2
            self.game.temp_stone.update()
            self.game.turn_black = not self.game.turn_black
            self.game.pass_count = 0 #if a move was made it does not count towards finishing the game

    def moveCheck(self, player_color):
        if self.board_array[self.game.temp_stone.pos_x][self.game.temp_stone.pos_y] == 0:
            #gets the stone groups arround the stone to place and decides if a group should be deleted
            player_group, enemy_groups = self.game.temp_stone.createGroup()
            delete_groups = []
            for group in enemy_groups:
                if not group.free_spaces:
            #    if group.getFreedomLevel() == 0:
                    delete_groups.append(group)

            #checks for repetition moves
            if delete_groups:
                for group in delete_groups:
                    if group.stones == self.last_eaten:
                        return False, []

                self.last_eaten = [(self.game.temp_stone.pos_x, self.game.temp_stone.pos_y)]
                return True, delete_groups
            self.last_eaten = []

            #This checks if the player isn't killing his own stones
            if not player_group.free_spaces:
                return False, []

            #if nothing interesting happens we get here
            return True, delete_groups
        else:
            return False, []

class Player(object):
    #this is a very boring class
    def __init__(self, color, game):
        self.color = color
        self.game = game
        self.action_cooldown = 0
        self.eaten_stones = 0

    def play(self,keys):

        #This handles the movement and actions of the current player
        if keys[pygame.K_RIGHT]:
            if self.game.temp_stone.pos_x < self.game.game_board.size - 1:
                self.game.temp_stone.pos_x += 1
                self.game.temp_stone.update()

        if keys[pygame.K_LEFT]:
            if self.game.temp_stone.pos_x > 0:
                self.game.temp_stone.pos_x -= 1
                self.game.temp_stone.update()

        if keys[pygame.K_DOWN]:
            if self.game.temp_stone.pos_y < self.game.game_board.size - 1:
                self.game.temp_stone.pos_y += 1
                self.game.temp_stone.update()

        if keys[pygame.K_UP]:
            if self.game.temp_stone.pos_y > 0:
                self.game.temp_stone.pos_y -= 1
                self.game.temp_stone.update()

        if self.action_cooldown == 0:
            if keys[pygame.K_RETURN]:
                self.game.game_board.move(self.color)
                self.action_cooldown = 5

            if keys[pygame.K_SPACE]:
                self.game.turn_black = not self.game.turn_black
                self.game.history[0].append([x[:] for x in self.game.game_board.board_array])
                self.game.history[1] == self.game.pass_count
                self.game.turn_count += 1
                self.game.pass_count += 1
                self.action_cooldown = 5

            if keys[pygame.K_BACKSPACE]:
                self.game.undoTurn()
                self.action_cooldown = 5

        else:
            self.action_cooldown -= 1

class Stone(object):

    def __init__(self, color, location, board, win):

        self.color = color
        if color == "white":
            self.draw_colors = [(240, 220, 220), (250, 240, 240), (255, 255, 255)]
        elif color == "black":
            self.draw_colors = [(30, 15, 15), (50, 30, 30), (60, 60, 60)]

        self.pos_x = location[0]
        self.pos_y = location[1]
        self.board = board
        self.win = win
        self.update()

    def draw(self):

        size = int(self.board.square_size * .4)
        pygame.draw.circle(self.win, self.draw_colors[0], (self.x, self.y), size)
        pygame.draw.circle(self.win, self.draw_colors[1], (self.x - size // 3, self.y - size // 3), size // 2)
        pygame.draw.circle(self.win, self.draw_colors[2], (int(self.x - size // 2.8), int(self.y - size // 2.8)), size // 3)

    def update(self):

        self.x = self.board.start_grid[0] + self.pos_x * self.board.square_size + self.board.square_size // 2

        self.y = self.board.start_grid[1] + self.pos_y * self.board.square_size + self.board.square_size // 2



    def createGroup(self):

        self.board.board_array[self.pos_x][self.pos_y] = self

        print("")
        all_groups = [StoneGroup(self.color, self.board), StoneGroup(self.color, self.board), StoneGroup(self.color, self.board), StoneGroup(self.color, self.board)]

        all_groups[0].detectStones([-1, 0, 0, self.pos_x], (self.pos_x, self.pos_y), 0)
        #print("left ", all_groups[0].color, all_groups[0].stones, all_groups[0].free_spaces )
        all_groups[1].detectStones([1, 0, self.board.size - 1, self.pos_x], (self.pos_x, self.pos_y), 0)
        #print("right", all_groups[1].color, all_groups[1].stones, all_groups[1].free_spaces )
        all_groups[2].detectStones([0, -1, 0, self.pos_y], (self.pos_x, self.pos_y), 0)
        #print("up   ", all_groups[2].color, all_groups[2].stones, all_groups[2].free_spaces )
        all_groups[3].detectStones([0, 1, self.board.size - 1, self.pos_y], (self.pos_x, self.pos_y), 0)
        #print("down ", all_groups[3].color , all_groups[3].stones, all_groups[3].free_spaces)
        pl_group = StoneGroup(self.color, self.board)
        #unifies all the player groups into one
        for  group in all_groups:
            #print("\n", group.stones)
            if group.color == self.color:
                for stone in group.stones:
                    if stone not in pl_group.stones:
                        pl_group.stones.append(stone)
                for space in group.free_spaces:
                    if space not in pl_group.free_spaces:
                        pl_group.free_spaces.append(space)

        #group sorting
        enm_groups = []
        for  group in all_groups:
            if  group.color != self.color:
                if not enm_groups:
                    enm_groups.append(group)
                else:
                    for i in enm_groups:
                        for stone in i.stones:
                            if group.stones[0] == stone:
                                pass
                            else:
                                enm_groups.append(group)
                                loop = False
                                break
                        if not loop:
                            break

        self.board.board_array[self.pos_x][self.pos_y] = 0
        return pl_group, enm_groups


class StoneGroup(object):

    def __init__(self, color, board):
        self.color = color
        self.stones = []
        self.freedom = 0
        self.free_spaces = []
        self.board = board
        self.onlyfree = False

    def isRockHere(self, loc):
        for stone in self.stones:
            if stone == loc:
                return True

    def createSubGroup(self, stone):
        self.detectStones([-1, 0, 0, stone[0]], stone)
        self.detectStones([1, 0, self.board.size - 1, stone[0]], stone)
        self.detectStones([0, -1, 0, stone[1]], stone)
        self.detectStones([0, 1, self.board.size - 1, stone[1]], stone)


    def detectStones(self, direction, stone, level = 1):
        #"left"   >>>   [-1, 0, 0, self.pos_x] x move, y move, max pos, current pos
        #"right"  >>>   [1, 0, game_board.size - 1, self.pos_x]
        #"up"     >>>   [0, -1, 0, self.pos_y]
        #"down"   >>>   [0, 1, game_board.size - 1, self.pos_y]
        if direction[2] != direction[3]:
            new_stone = (stone[0] + direction[0], stone[1] + direction[1])

            if self.board.board_array[new_stone[0]][new_stone[1]] == 0:
                if level == 0:
                    self.stones.append(stone)
                self.free_spaces.append(new_stone)

            else:
                color = self.board.board_array[new_stone[0]][new_stone[1]].color

                if color == self.color and not self.isRockHere(new_stone):
                    #group.addStone((self.pos_x, self.pos_y))
                    if level == 0:
                        self.stones.append(stone)
                    self.stones.append(new_stone)
                    self.createSubGroup(new_stone)

                else:
                    if level == 0:
                        self.color = color
                        #group.addStone((self.pos_x, self.pos_y))
                        self.stones.append(new_stone)
                        self.createSubGroup(new_stone)
                        #return self.board.board_array[self.pos_x + direction[0]][self.pos_y + direction[1]].createSubGroup(color, group)
