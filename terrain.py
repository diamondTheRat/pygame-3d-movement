import random
from pprint import pprint
from trans import Environment, Vertex, Triangle, Vector3, Box
import pygame


class Terrain:
    def __init__(self, env: Environment, player_simulation: bool):
        self.env = env
        self.player_simulation = True

        self.on_floor = False
        self.jump_power = 9
        self.camera_speed = 5
        self.movement_speed = 0.4

        self.friction = 0.9
        self.gravity = Vector3(0, -1, 0)
        self.velocity = Vector3(0, 0, 0)
        if player_simulation:
            env.set_camera(Vector3(0, 100, 0))
        self.vertices = []
        self.triangles = []

        self.blocks = [[[]]]
        self.size = Vector3(0, 0, 0)
        self.position = Vector3(0, 0, 0)
        self.block_size = 0

    def generate(self, size: Vector3, block_size: int, center: Vector3):
        assert (isinstance(size.x, int) and isinstance(size.y, int) and isinstance(size.z, int)), "terrain size must be a vector of integers"

        self.jump_power = block_size / 2
        self.block_size = block_size
        self.size = size
        self.position = center - size * block_size / 2
        self.blocks = [
            [
                [0] * size.z for i in range(size.y)
            ] for i in range(size.x)
        ]

        random_height_matrix = [
            [random.randint(0, size.y) for _ in range(size.z)] for _ in range(size.x)
        ]

        height_matrix = [
            [0] * size.z for _ in range(size.x)
        ]

        for x in range(size.x):
            for z in range(size.z):
                total = 0
                count = 0
                for dx in [-1, 0, 1]:
                    for dz in [-1, 0, 1]:
                        nx, nz = x + dx, z + dz
                        if 0 <= nx < size.x and 0 <= nz < size.z:
                            total += random_height_matrix[nx][nz]
                            count += 1
                height_matrix[x][z] = total // count
        # pprint(height_matrix, indent=2, depth=2)

        for x in range(size.x):
            for z in range(size.z):
                for y in range(height_matrix[x][z]):
                    self.blocks[x][y][z] = 1

    def reset_mesh(self):
        self.env.children = [i for i in self.env.children if i not in self.vertices and i not in self.triangles]

        self.vertices = {}
        self.triangles = []

        for x in range(self.size.x):
            for y in range(self.size.y):
                for z in range(self.size.z):
                    if not self.blocks[x][y][z]: continue

                    if (y + 1 < self.size.y and self.blocks[x][y + 1][z] == 0):
                        v1 = Vertex(self.position + Vector3(x, y + 1, z) * self.block_size)
                        v2 = Vertex(self.position + Vector3(x, y + 1, z + 1) * self.block_size)
                        v3 = Vertex(self.position + Vector3(x + 1, y + 1, z + 1) * self.block_size)
                        v4 = Vertex(self.position + Vector3(x + 1, y + 1, z) * self.block_size)

                        if v1 in self.vertices: v1 = self.vertices[v1]
                        else: self.vertices[v1] = v1
                        if v2 in self.vertices: v2 = self.vertices[v2]
                        else: self.vertices[v2] = v2
                        if v3 in self.vertices: v3 = self.vertices[v3]
                        else: self.vertices[v3] = v3
                        if v4 in self.vertices: v4 = self.vertices[v4]
                        else: self.vertices[v4] = v4

                        t1 = Triangle(v1, v2, v3)
                        t2 = Triangle(v1, v3, v4)
                        self.triangles.extend([t1, t2])

                    if (y > 0 and self.blocks[x][y - 1][z] == 0):
                        v1 = Vertex(self.position + Vector3(x, y, z) * self.block_size)
                        v2 = Vertex(self.position + Vector3(x, y, z + 1) * self.block_size)
                        v3 = Vertex(self.position + Vector3(x + 1, y, z + 1) * self.block_size)
                        v4 = Vertex(self.position + Vector3(x + 1, y, z) * self.block_size)

                        if v1 in self.vertices: v1 = self.vertices[v1]
                        else: self.vertices[v1] = v1
                        if v2 in self.vertices: v2 = self.vertices[v2]
                        else: self.vertices[v2] = v2
                        if v3 in self.vertices: v3 = self.vertices[v3]
                        else: self.vertices[v3] = v3
                        if v4 in self.vertices: v4 = self.vertices[v4]
                        else: self.vertices[v4] = v4

                        t1 = Triangle(v1, v3, v2)
                        t2 = Triangle(v1, v4, v3)
                        self.triangles.extend([t1, t2])

                    if  (z + 1 < self.size.z and self.blocks[x][y][z + 1] == 0):
                        v1 = Vertex(self.position + Vector3(x, y + 1, z + 1) * self.block_size)
                        v2 = Vertex(self.position + Vector3(x, y, z + 1) * self.block_size)
                        v3 = Vertex(self.position + Vector3(x + 1, y, z + 1) * self.block_size)
                        v4 = Vertex(self.position + Vector3(x + 1, y + 1, z + 1) * self.block_size)

                        if v1 in self.vertices: v1 = self.vertices[v1]
                        else: self.vertices[v1] = v1
                        if v2 in self.vertices: v2 = self.vertices[v2]
                        else: self.vertices[v2] = v2
                        if v3 in self.vertices: v3 = self.vertices[v3]
                        else: self.vertices[v3] = v3
                        if v4 in self.vertices: v4 = self.vertices[v4]
                        else: self.vertices[v4] = v4

                        t1 = Triangle(v1, v2, v3)
                        t2 = Triangle(v1, v3, v4)
                        self.triangles.extend([t1, t2])

                    if (z > 0 and self.blocks[x][y][z - 1] == 0):
                        v1 = Vertex(self.position + Vector3(x, y, z) * self.block_size)
                        v2 = Vertex(self.position + Vector3(x, y + 1, z) * self.block_size)
                        v3 = Vertex(self.position + Vector3(x + 1, y, z) * self.block_size)
                        v4 = Vertex(self.position + Vector3(x + 1, y + 1, z) * self.block_size)

                        if v1 in self.vertices: v1 = self.vertices[v1]
                        else: self.vertices[v1] = v1
                        if v2 in self.vertices: v2 = self.vertices[v2]
                        else: self.vertices[v2] = v2
                        if v3 in self.vertices: v3 = self.vertices[v3]
                        else: self.vertices[v3] = v3
                        if v4 in self.vertices: v4 = self.vertices[v4]
                        else: self.vertices[v4] = v4

                        t1 = Triangle(v1, v2, v4)
                        t2 = Triangle(v1, v4, v3)
                        self.triangles.extend([t1, t2])

                    if (x + 1 < self.size.x and self.blocks[x + 1][y][z] == 0):
                        v1 = Vertex(self.position + Vector3(x + 1, y + 1, z) * self.block_size)
                        v2 = Vertex(self.position + Vector3(x + 1, y + 1, z + 1) * self.block_size)
                        v3 = Vertex(self.position + Vector3(x + 1, y, z) * self.block_size)
                        v4 = Vertex(self.position + Vector3(x + 1, y, z + 1) * self.block_size)

                        if v1 in self.vertices: v1 = self.vertices[v1]
                        else: self.vertices[v1] = v1
                        if v2 in self.vertices: v2 = self.vertices[v2]
                        else: self.vertices[v2] = v2
                        if v3 in self.vertices: v3 = self.vertices[v3]
                        else: self.vertices[v3] = v3
                        if v4 in self.vertices: v4 = self.vertices[v4]
                        else: self.vertices[v4] = v4

                        t1 = Triangle(v1, v2, v4)
                        t2 = Triangle(v1, v4, v3)
                        self.triangles.extend([t1, t2])

                    if (x > 0 and self.blocks[x - 1][y][z] == 0):
                        v1 = Vertex(self.position + Vector3(x, y + 1, z + 1) * self.block_size)
                        v2 = Vertex(self.position + Vector3(x, y + 1, z) * self.block_size)
                        v3 = Vertex(self.position + Vector3(x, y, z) * self.block_size)
                        v4 = Vertex(self.position + Vector3(x, y, z + 1) * self.block_size)

                        if v1 in self.vertices: v1 = self.vertices[v1]
                        else: self.vertices[v1] = v1
                        if v2 in self.vertices: v2 = self.vertices[v2]
                        else: self.vertices[v2] = v2
                        if v3 in self.vertices: v3 = self.vertices[v3]
                        else: self.vertices[v3] = v3
                        if v4 in self.vertices: v4 = self.vertices[v4]
                        else: self.vertices[v4] = v4

                        t1 = Triangle(v1, v2, v3)
                        t2 = Triangle(v1, v3, v4)
                        self.triangles.extend([t1, t2])

        for i in self.triangles:
            i.color = (90, 200, 50)
        self.env.children.extend(self.triangles)

    def collides_box(self, box: Box):
        lx = self.position.x
        ly = self.position.y
        lz = self.position.z
        ux = self.position.x + self.size.x * self.block_size
        uy = self.position.y + self.size.y * self.block_size
        uz = self.position.z + self.size.z * self.block_size

        if box.ux < lx or box.lx > ux: return False
        if box.uy < ly or box.ly > uy: return False
        if box.uz < lz or box.lz > uz: return False

        stx = int((box.ux - self.position.x) / self.block_size)
        sty = int((box.uy - self.position.y) / self.block_size)
        stz = int((box.uz - self.position.z) / self.block_size)

        for x in range(max(stx - 1, 0), min(self.size.x, stx + 3)):
            for y in range(max(sty - 1, 0), min(self.size.y, sty + 3)):
                for z in range(max(stz - 1, 0), min(self.size.z, stz + 3)):
                    if not self.blocks[x][y][z]: continue

                    bx = Box(
                        Vector3(self.block_size, self.block_size, self.block_size),
                        self.position + Vector3(x, y, z) * self.block_size + Vector3(self.block_size, self.block_size, self.block_size) / 2
                    )
                    if bx.collides_box(box):
                        # print(bx, box, x, y, z, self.position, sep='\n')
                        return True

        return False

    def tick(self):
        if self.player_simulation == False: return

        self.velocity = (self.velocity + self.gravity) * self.friction

        self.env.offset.x = self.env.offset.x - self.velocity.x
        if self.collides_box(Box(Vector3(self.block_size / 2, self.block_size * 2, self.block_size / 2), -self.env.offset - Vector3(0, self.block_size * 3 / 2, 0))):
            self.env.offset.x = self.env.offset.x + self.velocity.x
            self.velocity.x = 0

        self.env.offset.y = self.env.offset.y - self.velocity.y
        if self.collides_box(Box(Vector3(self.block_size / 2, self.block_size * 2, self.block_size / 2), -self.env.offset - Vector3(0, self.block_size * 3 / 2, 0))):
            self.env.offset.y = self.env.offset.y + self.velocity.y
            self.velocity.y = 0
            self.on_floor = True
        else:
            self.on_floor = False

        self.env.offset.z = self.env.offset.z - self.velocity.z
        if self.collides_box(Box(Vector3(self.block_size / 2, self.block_size * 2, self.block_size / 2), -self.env.offset - Vector3(0, self.block_size * 3 / 2, 0))):
            self.env.offset.z = self.env.offset.z + self.velocity.z
            self.velocity.z = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.velocity += Vector3(0, 0, self.movement_speed).rotate(Vector3(0, -self.env.rotation.y, 0))

        if keys[pygame.K_s]:
            self.velocity += Vector3(0, 0, -self.movement_speed).rotate(Vector3(0, -self.env.rotation.y, 0))

        if keys[pygame.K_d]:
            self.velocity += Vector3(self.movement_speed, 0, 0).rotate(Vector3(0, -self.env.rotation.y, 0))

        if keys[pygame.K_a]:
            self.velocity += Vector3(-self.movement_speed, 0, 0).rotate(Vector3(0, -self.env.rotation.y, 0))

        if keys[pygame.K_SPACE] and self.on_floor:
            self.velocity.y = self.jump_power

        if keys[pygame.K_LEFT]:
            self.env.rotation.y = self.env.rotation.y + self.camera_speed

        if keys[pygame.K_RIGHT]:
            self.env.rotation.y = self.env.rotation.y - self.camera_speed

        if keys[pygame.K_UP]:
            self.env.rotation.x = self.env.rotation.x - self.camera_speed

        if keys[pygame.K_DOWN]:
            self.env.rotation.x = self.env.rotation.x + self.camera_speed