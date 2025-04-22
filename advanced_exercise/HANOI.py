#!/usr/bin/env python3
import turtle
import time

screen = turtle.Screen()
screen.bgcolor("white")
screen.title("Tower of Hanoi")

t = turtle.Turtle()
t.speed(0)
t.hideturtle()

DISK_HEIGHT = 20
PEG_X = {"A": -150, "B": 0, "C": 150}
PEG_Y = -100
disk_turtles = []
peg_stacks = {"A": [], "B": [], "C": []}


def draw_pegs(): 
    #Implement together
    pass

draw_pegs()


def draw_disks(n):
    #Implement together
    pass

def move_disk(from_peg, to_peg):
    #implement together
    pass

#HERE IS THE CHALLENGE
def hanoi_logic(n, source, target, spare):
    #YOUR CHALLENGE
    pass


num_disks = 3 
draw_disks(num_disks)
hanoi_logic(num_disks, "A", "C", "B")

turtle.done()
