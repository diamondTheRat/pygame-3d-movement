import pygame
import trans
from terrain import Terrain

WIDTH, HEIGHT = 600, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)


BGCOLOR = (50, 54, 61)

CAMERA_SPEED = 2
env = trans.Environment(120)
env.set_camera(trans.Vector3(0, 0, -100))

terrain = Terrain(env, True)
terrain.generate(trans.Vector3(15, 5, 15), 20, trans.Vector3(0, 0, 0))
terrain.reset_mesh()
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.MOUSEMOTION:
            dy, dx = event.rel
            terrain.env.rotation.y = terrain.env.rotation.y - dy / 6
            terrain.env.rotation.x = terrain.env.rotation.x - dx / 6

def handle_input():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        quit()
    if terrain.player_simulation:
        terrain.handle_input()
        return

    if keys[pygame.K_w]:
        env.move_camera(trans.Vector3(0, 0, -CAMERA_SPEED))

    if keys[pygame.K_s]:
        env.move_camera(trans.Vector3(0, 0, CAMERA_SPEED))

    if keys[pygame.K_d]:
        env.move_camera(trans.Vector3(-CAMERA_SPEED, 0, 0))

    if keys[pygame.K_a]:
        env.move_camera(trans.Vector3(CAMERA_SPEED, 0, 0))

    if keys[pygame.K_q]:
        env.move_camera(trans.Vector3(0, CAMERA_SPEED, 0))

    if keys[pygame.K_e]:
        env.move_camera(trans.Vector3(0, -CAMERA_SPEED, 0))

    if keys[pygame.K_LEFT]:
        env.rotate_camera(trans.Vector3(0, -CAMERA_SPEED, 0))

    if keys[pygame.K_RIGHT]:
        env.rotate_camera(trans.Vector3(0, CAMERA_SPEED, 0))

    if keys[pygame.K_UP]:
        env.rotate_camera(trans.Vector3(-CAMERA_SPEED, 0, 0))

    if keys[pygame.K_DOWN]:
        env.rotate_camera(trans.Vector3(CAMERA_SPEED, 0, 0))


def draw():
    WIN.fill(BGCOLOR)

    env.display(WIN)

    pygame.display.update()


def main():


    clock = pygame.time.Clock()
    while True:
        clock.tick(60)

        handle_events()

        handle_input()

        terrain.tick()

        draw()


if __name__ == "__main__":
    main()