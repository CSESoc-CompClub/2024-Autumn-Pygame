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
    peg = turtle.Turtle()
    peg.hideturtle()        #explain why we need to hidetutle()
    peg.pensize(5)
    for x in PEG_X.values(): #do the for loop up draw one peg
        peg.penup()         #explain why we need penup() even before we start drawing
        peg.goto(x, PEG_Y)
        peg.pendown()
        peg.goto(x, PEG_Y + 120)

draw_pegs()


def draw_disks(n):
    for i in range(n, 0, -1):
        disk = turtle.Turtle()
        disk.shape("turtle")        #explain how there are preset shapes
        disk.shapesize(stretch_wid=1, stretch_len=i)    # explain what is stretch_len
        disk.color("skyblue")       #explain how there are preset colours
        disk.penup()
        disk.goto(PEG_X["A"], PEG_Y + DISK_HEIGHT * (n - i))    #explain the logic here
        disk_turtles.append(disk)
        peg_stacks["A"].append(disk)

#Should we implement this for the kids already?
def move_disk(from_peg, to_peg):
    disk = peg_stacks[from_peg].pop()
    x = PEG_X[to_peg]
    y = PEG_Y + DISK_HEIGHT * len(peg_stacks[to_peg])
    disk.goto(x, y)
    peg_stacks[to_peg].append(disk)
    time.sleep(1)

#HERE IS THE CHALLENGE
def hanoi_logic(n, source, target, spare):
    if n == 1:
        move_disk(source, target)
    else:
        hanoi_logic(n - 1, source, spare, target)
        move_disk(source, target)
        hanoi_logic(n - 1, spare, target, source)


num_disks = 3 
draw_disks(num_disks)
hanoi_logic(num_disks, "A", "C", "B")

turtle.done()
