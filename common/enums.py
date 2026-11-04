import enum

class MovementType(enum.IntEnum):
    ENTRY = 1
    EXIT = 2
    ADJUSTMENT = 3
class Category(enum.IntEnum):
    FOOD = 1
    DRINK = 2
    ELECTRONICS = 3
    CLOTHING = 4
class Emplacement(enum.IntEnum):
    STORE = 0
    WAREHOUSE = 1
