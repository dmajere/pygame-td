import sys
import pygame
from scenes.bullet import BulletScene
from scenes.tower import TowerScene
from scenes.path import PathScene

SCENES = {
    "bullet": BulletScene,
    "tower": TowerScene,
    "path": PathScene,
}


def main(scene: str):
    pygame.init()
    clock = pygame.time.Clock()

    screen_width = 800
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))

    scene = SCENES[scene](screen_width, screen_height)
    while True:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            scene.process_event(event)

        screen.fill("white")
        scene.draw(screen)
        scene.update(dt)

        pygame.display.flip()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <scene>")
        sys.exit(1)

    argument = sys.argv[1]
    main(argument)
