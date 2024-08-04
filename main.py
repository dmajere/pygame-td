import sys
import pygame
from lib.screen import Screen


def main():
    pygame.init()
    clock = pygame.time.Clock()

    screen_width = 800
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))

    game = Screen(screen_width, screen_height)
    while True:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.process_event(event)

        screen.fill("white")
        game.draw(screen)
        game.update(dt)

        pygame.display.flip()


if __name__ == "__main__":
    main()
