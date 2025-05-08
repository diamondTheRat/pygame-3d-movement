from typing import Union, Any
from functools import reduce
import pygame
import math


class Vector3:
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self.x = x
        self.y = y
        self.z = z

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Vector3(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        return Vector3(self.x / other, self.y / other, self.z / other)

    def cross(self, other):
        cross = Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
        return cross

    def distance(self, other):
        return (self - other).magnitude()

    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        mag = self.magnitude()
        if mag == 0: mag = 1
        return Vector3(self.x / mag, self.y / mag, self.z / mag)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def rotate(self, rotation):
        # Convert rotation angles from degrees to radians
        rx = math.radians(rotation.x)
        ry = math.radians(rotation.y)
        rz = math.radians(rotation.z)

        # Rotation matrix for X-axis (pitch)
        Rx = [
            [1, 0, 0],
            [0, math.cos(rx), -math.sin(rx)],
            [0, math.sin(rx), math.cos(rx)]
        ]

        # Rotation matrix for Y-axis (roll)
        Ry = [
            [math.cos(ry), 0, math.sin(ry)],
            [0, 1, 0],
            [-math.sin(ry), 0, math.cos(ry)]
        ]

        # Rotation matrix for Z-axis (yaw)
        Rz = [
            [math.cos(rz), -math.sin(rz), 0],
            [math.sin(rz), math.cos(rz), 0],
            [0, 0, 1]
        ]

        # Multiply the rotation matrices (Rz * Ry * Rx)
        # First, apply the X-axis rotation (Rx)
        temp = [
            self.x * Rx[0][0] + self.y * Rx[0][1] + self.z * Rx[0][2],
            self.x * Rx[1][0] + self.y * Rx[1][1] + self.z * Rx[1][2],
            self.x * Rx[2][0] + self.y * Rx[2][1] + self.z * Rx[2][2]
        ]

        # Then, apply the Y-axis rotation (Ry)
        temp2 = [
            temp[0] * Ry[0][0] + temp[1] * Ry[0][1] + temp[2] * Ry[0][2],
            temp[0] * Ry[1][0] + temp[1] * Ry[1][1] + temp[2] * Ry[1][2],
            temp[0] * Ry[2][0] + temp[1] * Ry[2][1] + temp[2] * Ry[2][2]
        ]

        # Finally, apply the Z-axis rotation (Rz)
        new_x = temp2[0] * Rz[0][0] + temp2[1] * Rz[0][1] + temp2[2] * Rz[0][2]
        new_y = temp2[0] * Rz[1][0] + temp2[1] * Rz[1][1] + temp2[2] * Rz[1][2]
        new_z = temp2[0] * Rz[2][0] + temp2[1] * Rz[2][1] + temp2[2] * Rz[2][2]

        return Vector3(new_x, new_y, new_z)

    def step_rotate(self, rotation):
        return self.rotate(Vector3(0, rotation.y, 0)).rotate(Vector3(rotation.x, 0, 0))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"


class Box:
    def __init__(self, size: Vector3, center: Vector3):
        self.lx = center.x - size.x / 2
        self.ux = center.x + size.x / 2
        self.ly = center.y - size.y / 2
        self.uy = center.y + size.y / 2
        self.lz = center.z - size.z / 2
        self.uz = center.z + size.z / 2

    def collides_box(self, box):
        if box.ux < self.lx or box.lx > self.ux: return False
        if box.uy < self.ly or box.ly > self.uy: return False
        if box.uz < self.lz or box.lz > self.uz: return False
        return True

    def __repr__(self):
        return f"Box(lx: {self.lx} , ux: {self.ux} , ly: {self.ly} , uy: {self.uy} , lz: {self.lz} , uz: {self.uz})"

class Vertex:
    def __init__(self, position: Vector3):
        self.position = position

    def __hash__(self):
        return hash((round(self.position.x, 5), round(self.position.y, 5), round(self.position.z, 5)))

    def __eq__(self, other):
        return self.position == other.position

    def get_projection(self, surface: pygame.Surface, offset: Vector3, rotation: Vector3, FOV: int):
        relative = (self.position + offset).step_rotate(rotation)

        fov_rad = math.radians(FOV)
        scale = surface.get_width() / (2 * math.tan(fov_rad / 2))

        relative.z = max(1, relative.z)
        x_proj = (relative.x / relative.z) * scale + surface.get_width() / 2
        y_proj = (-relative.y / relative.z) * scale + surface.get_height() / 2

        return x_proj, y_proj

    def distance_from_camera(self, offset: Vector3):
        return self.position.distance(offset)

    def display(self, surface: pygame.Surface, offset: Vector3, rotation: Vector3, FOV: int):
        if (offset + self.position).step_rotate(rotation).z <= 0: return
        x_proj, y_proj = self.get_projection(surface, offset, rotation, FOV)
        if x_proj == None: return

        pygame.draw.circle(surface, (255, 255, 255), (int(x_proj), int(y_proj)), 3)

    def __repr__(self):
        return self.position.__repr__()


class Triangle:
    def __init__(self, vertex0: Vertex, vertex1: Vertex, vertex2: Vertex, color: Union[tuple[int, int, int], list[int, int, int], None] = None):
        self.vertices = [vertex0, vertex1, vertex2]
        self.color = color or (255, 0, 0)

    def get_normal(self) -> Vector3:
        ab = self.vertices[1].position - self.vertices[0].position
        ac = self.vertices[2].position - self.vertices[0].position
        normal = ab.cross(ac)
        return normal.normalize()

    def center(self, offset: Vector3) -> Vector3:
        return reduce(lambda a, b: a + b, [(vert.position + offset) for vert in self.vertices]) / 3

    def is_visible(self, screen_width: int, screen_height: int, offset: Vector3, rotation: Vector3) -> bool:
        return any(
            (vert.position + offset).step_rotate(rotation).z > 5
            for vert in self.vertices
        )

    def distance_from_camera(self, offset: Vector3) -> float:
        return self.center(Vector3(0, 0, 0)).distance(-offset)

    def display(self, surface: pygame.Surface, offset: Vector3, rotation: Vector3, FOV: int) -> None:
        # normal = self.get_normal()
        # camera_dir = -offset - self.center(offset)
        # if normal.dot(camera_dir) < 0:
        #     return

        vertices = [i.get_projection(surface, offset, rotation, FOV) for i in self.vertices]

        if self.is_visible(surface.get_width(), surface.get_height(), offset, rotation):
            light_dir = Vector3(0.4, -1, 0)
            normal = self.get_normal()

            light_dir = light_dir.normalize()
            normal = normal.normalize()

            intensity = normal.dot(-light_dir)
            intensity = max(0.2, intensity)
            pygame.draw.polygon(surface, [i * intensity for i in self.color], vertices)

class Environment:
    def __init__(self, FOV: int):
        self.offset = Vector3()
        self.rotation = Vector3(0, 0, 0)
        self.FOV = FOV

        self.children = []

    def add_child(self, object: Any):
        self.children.append(object)

    def set_camera(self, position: Vector3):
        self.offset = -position

    def move_camera(self, vector: Vector3):
        self.offset += vector.rotate(-self.rotation)

    def rotate_camera(self, vector: Vector3):
        self.rotation += -vector
        self.rotation.x %= 360
        self.rotation.y %= 360
        self.rotation.z %= 360

    def display(self, surface: pygame.Surface):
        for child in sorted(self.children, key = (lambda x: x.distance_from_camera(self.offset)), reverse=True):
            if hasattr(child, "display"):
                child.display(surface, self.offset, self.rotation, self.FOV)

