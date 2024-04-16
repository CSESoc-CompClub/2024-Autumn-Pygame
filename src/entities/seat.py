import pygame
# from pygame.locals import *
from src.entities.entity import Entity
from src.constants import *
from src.util.vec2d import Vec2d


class Seat(Entity):
    def __init__(self, pos: Vec2d):
        self.pos = pos
        self.customer = None

    def addCustomer():
        self.customer = Customer