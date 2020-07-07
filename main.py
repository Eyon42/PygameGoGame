if __name__ == "__main__":
    import pygame
    from engine import *

    #window setup
    version = 0.4
    win_width = 600
    win_height = win_width + 40
    win = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption(f"Go game v:{version}, Funciona!")
    clock = pygame.time.Clock()
    framerate = 10
    debug = False

    #main_menu = Menu(win_width, win_height, framerate, win)
    #main_menu.main()

    game = Game(13, framerate, win_width, win_height, 10, win, clock)
    game.main()
    #when there is nothing running it quits
    pygame.quit()
