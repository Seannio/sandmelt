from __future__ import annotations
import random
from typing import Iterator, List, Tuple, TYPE_CHECKING

import tcod
from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from entity import Entity

class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height 
        # this init function takes the top right corner and calculates the canvas size 
    
    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y
        # useful later on I guess
    
    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)
        # tis the part which gets DUG OUT. In order to make overlapping rooms, add +1 to x1 and y1
    
    def intersects(self, other: RectangularRoom) -> bool: # determines if a room is overlapping
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

def tunnel_between( start: Tuple[int, int], end: Tuple[int, int] ) -> Iterator[Tuple[int, int]]:
    # this function takes two x,y tupules from the map and makes a tunnel between them
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel. This uses bresenham lines, commonly used in bitmap files
    # to approximate straight lines. the yield tag suspends this function rather than returning it so we 
    # can dig out the tunnel in subsequent code (eg: replacing it with floor tiles, and bordering it)
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y

    # sometimes the tunnels are THICC. This could be optimized with some width variable in this specific
    # tunnel function, but I can do that later if this module is relevant lol. 
    if random.random() < 0.5:
        for x, y in tcod.los.bresenham((x1+1, y1+1), (corner_x+1, corner_y+1)).tolist():
            yield x, y
        for x, y in tcod.los.bresenham((corner_x+1, corner_y+1), (x2+1, y2+1)).tolist():
            yield x, y

def generate_dungeon(map_width, map_height) -> GameMap:
    dungeon = GameMap(map_width, map_height)

    room_1 = RectangularRoom(x=20, y=15, width=10, height=15)
    room_2 = RectangularRoom(x=35, y=15, width=10, height=15)

    dungeon.tiles[room_1.inner] = tile_types.floor
    dungeon.tiles[room_2.inner] = tile_types.floor
    for x, y in tunnel_between(room_2.center, room_1.center):
        dungeon.tiles[x, y] = tile_types.floor

    return dungeon

# sheesh. long. these are passed in from the main
def generate_dungeon( 
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    player: Entity,
) -> GameMap:
    """Generate a new dungeon map."""
    dungeon = GameMap(map_width, map_height)

    rooms: List[RectangularRoom] = [] # we'll keep a running list of all rooms

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1) # fetch a random coordinate and try to place the room
        y = random.randint(0, dungeon.height - room_height - 1)

        # "RectangularRoom" class makes rectangles easier to work with
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so toss it out and go to the next attempt.
        # If there are no intersections then the room is valid.

        # Dig out this rooms inner area.
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # The first room, where the player starts.
            player.x, player.y = new_room.center
        else:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        # Finally, append the new room to the list.
        rooms.append(new_room)

    return dungeon


class WeirdRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
    
    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 4)
        center_y = int((self.y1 + self.y2) * 2)

        return center_x, center_y
    
    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)