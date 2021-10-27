from __future__ import annotations
import copy
from typing import Tuple
from typing import Tuple, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from game_map import GameMap

T = TypeVar("T", bound="Entity")

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        char: str = "?",  # modifiable char, color, name, etc.
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        blocks_movement: bool = False, # items should not block movement, enemies should.
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
    
    # takes the GameMap instance, along with x and y for locations. 
    # It then creates a clone of the instance of Entity, and assigns 
    # the x and y variables to it (this is why we don’t need x and y 
    # in the initializer anymore, they’re set here).
    
    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        gamemap.entities.add(clone)
        return clone

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy