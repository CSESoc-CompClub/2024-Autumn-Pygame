import random
import time
from src.entities.food import FOODS, num_food
from src.entities.customer import Customer
from src.util.vec2d import *

RESPAWN_COUNTDOWN: int = 8 # 8 seconds

# Return a random food
foods = list(FOODS.keys())
def getRandomFood():
    return foods[random.randint(0, num_food() - 1)]

# Respawn a customer that has left after 8 seconds
def respawn_customer(customers, customer_pos, entities, player):
    for i, customer in enumerate(customers):
        if customer not in entities:
            time_passed = time.time() - customer.time_at_leaving
            if time_passed > RESPAWN_COUNTDOWN:
                customer = Customer(getRandomFood(), player, Vec2d(customer_pos[i]))
                customers[i] = customer
                entities.append(customer)
