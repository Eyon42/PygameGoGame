#This class is the main game engine
from elements import Board, Player, Stone
import pygame

class Game(object):

    def __init__(self, board_size, framerate, win_width, win_height, margin, win, clock):
        self.framerate = framerate
        self.win_width = win_width
        self.win_height = win_height
        self.win = win
        self.margin = margin
        self.clock = clock
        #the self.game_board's second argument is the margin of the board
        self.game_board = Board(self, board_size)
        #this is the stone object that appears when placing a stone
        #It's set to black because black goes first
        self.temp_stone = Stone("black", ((board_size - 1) // 2,(board_size - 1) // 2), self.game_board, self.win)

        self.history = [[],0]
        self.turn_count = 0
        self.scores = []

        self.ended = False
        self.pass_count = 0

        self.run = True
        self.turn_black = True

        self.black_player = Player("black", self)
        self.white_player = Player("white", self)
        #self.game_board.addStone("black", (1,1))
        #self.game_board.addStone("white", (1,0))

    def main(self):
        while self.run:
            #system stuff
            self.clock.tick(self.framerate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            keys = pygame.key.get_pressed()

            if not self.ended:
                self.turn(keys)

            if self.pass_count == 2 and not self.ended:
                self.endgame()

            self.drawGame()

    def turn(self, keys):
        #Turn management
        if self.turn_black:
            self.temp_stone.color = "black"
            self.temp_stone.draw_colors = [(40, 40, 30), (60, 60, 50), (100, 100, 100)]
            self.black_player.play(keys)
        else:
            self.temp_stone.color = "white"
            self.temp_stone.draw_colors = [(230, 230, 200), (240, 240, 230), (255, 255, 255)]
            self.white_player.play(keys)

    def drawGame(self):
        self.win.fill((50,50,50))

        self.game_board.draw()

        #This for loop loops through all the stone in the array matrix
        for stone_x in self.game_board.board_array:
            for stone_y in stone_x:
                if stone_y != 0:
                    stone_y.draw()
        self.temp_stone.draw()

        pygame.display.update()

    def undoTurn(self):
        if self.history:
            self.turn_black = not self.turn_black
            self.turn_count -= 1
            self.black_player.eaten_stones, self.white_player.eaten_stones = self.scores
            self.game_board.board_array = self.history[0][self.turn_count]
            self.pass_count = self.history[1]
            self.history[0].pop()
            self.game_board.update()

    def endgame(self):
        print("Both players passed, game ended")
        print(f"Black ate {self.black_player.eaten_stones} stones \nWhite ate {self.white_player.eaten_stones} stones")
        self.ended = True

class Menu(object):

    def __init__(self, win_width, win_height, framerate, win):
        pass

    def draw(self):
        pass

    def main(self):
        pass
