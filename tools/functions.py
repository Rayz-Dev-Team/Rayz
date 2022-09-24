import math
import random

## Paginate function
## thing = List()
## total = Int
## page = Int
def paginate(thing, total, page):
  textList = ""
  pages = math.ceil(total / 10)
  for num, item in enumerate(thing):
    placement = num + 1
    if page > 1:
      placement = placement + ((page - 1) * 10)
    textList += f"`{placement}.` {item[0]}: {item[1]:,}\n"
  return [textList, pages]

#Chance generator
def roll_chance(min,max,under):
  rolled_chance = random.randint(min,max)
  if_chance = False
  if rolled_chance <= under:
    if_chance = True
  return if_chance