import math

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
