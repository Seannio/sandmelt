#!/usr/bin/env python3
# this module handles all of the shit 

# Ideas for MAIN post tutorial completion TODO:
# - obviously some kind of examine button which, when used with an arrow key, allows reading, etc.
# - some kind of tunnel/room random-chance which creates a secret room
# - doors! 
# - lore items
import tcod

from engine import Engine
from entity import Entity
from input_handlers import EventHandler
from procgen import generate_dungeon


def main() -> None:
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    room_max_size = 15
    room_min_size = 8
    max_rooms = 30

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()
    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))

    # call the procgen function to generate dungeon (though this one is preordained)
    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        player=player
    )
    engine = Engine(event_handler=event_handler, game_map=game_map, player=player)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)
            events = tcod.event.wait()
            engine.handle_events(events)

if __name__ == "__main__":
    main()