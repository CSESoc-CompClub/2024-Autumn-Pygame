# 2024-Autumn-Pygame
2024 (Autumn) Pygame workshop SPEC

## Setup
### 1. Install python extension
<img width="303" alt="Screenshot 2024-04-18 at 4 56 50 pm" src="https://github.com/CSESoc-CompClub/2024-Autumn-Pygame/assets/96902642/a6cfe1c5-cd5c-4751-84d2-190b0906b271">
<img width="301" alt="Screenshot 2024-04-18 at 5 00 16 pm" src="https://github.com/CSESoc-CompClub/2024-Autumn-Pygame/assets/96902642/476ce84a-feb5-4276-8e4e-16c7f4cf7522">

### 2. Press play on main.py!
<img width="1277" alt="Screenshot 2024-04-18 at 5 03 08 pm" src="https://github.com/CSESoc-CompClub/2024-Autumn-Pygame/assets/96902642/834baa2d-d7b8-4a64-9c39-138f8302e9cd">

## Tasks

## Task 1

### [Task 1.1] Get Random Ingredient:
We want customers to spawn and request a random ingredient from our menu, to help us do this, we have a `getRandomIngredient` function!

**Fill in the `getRandomIngredient` function in `main.py`.** It should return a random ingredient string from the `ingredients` array.
> EXAMPLES
> -
> ```py
> ingredients = ["watermelon", "sushi", "peach", "banana", "grapes", "strawberry"]
> print(getRandomIngredient()) # "watermelon"
> print(getRandomIngredient()) # "shushi"
> print(getRandomIngredient()) # "peach"
> ```

> HINTS
> -
> - use `random.randint()`

---

## Task 2

### [Task 2.1] Drawing the customer:
The `draw` method draws the following onto the screen:
- The customer's `sprite`.
- If the customer is currently in the `EATING` state, then draw the `EATING_SPRITE` to the top left of the customer to indicate they are eating.
- If the customer is currently in the `WAITING_FOR_FOOD` state, then draw the `order` sprite to the top left of the customer to indicate what they are ordering.

**Fill in the `draw` method in `customer.py`.**.

> HINTS
> -
> - use `screen.blit(...)`
> - draw the customer sprite to the customer's `pos`
> - subtract from the x and y coordinates of the customer's `pos` to draw a sprite to the top left

### [Task 2.2] Start Eating!:
The `start_eating` method updates the customer's state to `EATING`, resets `cur_timer`, and sets the timeout to `EATING_TIMEOUT`:

**Fill in the `start_order` method in `customer.py`.**.

### [Task 2.2] Leaving!:
The `leave` method updates the customer's state to `LEAVING` and updates the players score. If the customer leaves angry, then decrease the score by 1, else increase it by 1.

> HINTS
> -
> - use `self.player.score` to update the players score

**Fill in the `leave` method in `customer.py`.**.

### [Task 2.3] Destroy 💔!:
The `destroy` method removes the customer from the `entities` list.

**Fill in the `destroy` method in `customer.py`.**.

> HINTS
> -
> - use `entities.remove(...)` to remove the customer from the array

### [Task 2.4] Trying to Receive Orders:
The customer receives orders using the `try_receive_order` method. It returns whether the order was successfully receieved.
- If the `food_retrieved` is equal to the customer's `order`, then start eating.
- Otherwise, leave the restaurant angrily.

**Fill in the `try_receive_order` method in `customer.py`.**.

> HINTS
> -
> - use `leave(False)` method to leave the restaurant angrily
> - start eating using the `start_eating` method

### [Task 2.5] Interact ❤️!:
The `interact` is used when the player interacts with the customer.
- If the current state is `WAITING_FOR_FOOD`, then try to receive the order.

**Fill in the `interact` method in `customer.py`.**.

> HINTS
> -
> - use the `try_receive_order(...)` method

### [Task 2.5] Update ❤️!:
The `update` method is called every single tick (that's 60 times a second). Here, we handle what the customer does while the game is running based on the state.

- If the state is `WAITING_FOR_FOOD`, then we increment the timer. If the customer has been waiting for food too long, then the leave angrily.
- If the state is `EATING`, then we increment the timer. If the customer has finished eating, then the customer leaves hapily.
- If the state is `LEAVING`, then we destroy the customer.

**Fill in the `update` method in `customer.py`.**.

> HINTS
> -
> - use the `leave` to handle the customer leaving
> - check if `cur_timer` is greater than or equal to `cur_timeout` to figure out whether the customer should leave

---

## Task 3

### [Task 3.1] Get Entities Distance
**Fill the `get_entities_distance` function in `player.py`**. This function finds the distance between the two entities `entity1` and `entity2`.

> EXAMPLES
> -
> ```py
> entity1 = Entity(Vec2d(0, 0))
> entity2 = Entity(Vec2d(0, 5))
> get_entities_distance(entity1, entity2) # 5
> ```

> HINTS
> -
> - get each entities position using `entity.get_position()`
> - get the distance between each entity using `pos.get_distance(other_pos)`

### [Task 3.2] Get Nearest Entity
**Fill the `get_nearest_entity` function in `player.py`**. This function finds the distance nearest entity to `player` from the `entities` list.

> EXAMPLES
> -
> ### Warning: the entities list contains `player` too
> ```py
> player = Player(..., pos: Vec2d(0, 4))
> entity1 = Entity(Vec2d(0, 0))
> entity2 = Entity(Vec2d(0, 5))
> get_entities_distance(player, [entity1, entity2, player]) # returns entity2
> ```

> HINTS
> -
> - use our `get_entities_distance` function we just made
> - be careful to make sure we don't return `player` as the nearest entity to `player`

---

## Task 4

### [Task 4.1] Drawing the player:
The `draw` method draws the following onto the screen:
- The player's `sprite`.
- If the customer is holding food, draw the food

**Fill in the `draw` method in `player.py`.**.

> HINTS
> -
> - use `screen.blit(...)`
> - draw the sprites to `self.hitbox.topleft`
> - get the ingredients sprite using the `INGREDIENTS` dictionary

### [Task 4.2] Interacting with Entities:
The `interact_nearest` method is activated when the player presses the `space bar`. It gets the nearest entity to the player and interacts with it!
- If the nearest entity is an `Ingredient` then pick it up and store the name of the food in `food_retrieved`
- If the nearest entity is a `Customer` AND the player is holding food, then interact with the customer. The customer also loses the food they were carrying.

**Fill in the `interact_nearest` method in `player.py`.**.

> HINTS
> -
> - check the type of the nearest entity using `type(entity) is Ingredient`

### [Task 4.3] Update:
The `update` method on the `Player` class is called 60 times every second (or once every tick). In this method we want to do 2 things:
- Move the player around.
- Check if the player is holding the space bar, if they are, then call the `interact_nearest` method.

**Fill in the `update` method in `player.py`.**.

> HINTS
> -
> - use `self.move`
> - access the pressed down keys using `pygame.key.get_pressed()`
> - the index for the space key is `K_SPACE`
