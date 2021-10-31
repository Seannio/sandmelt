#!/usr/bin/env python3
# this module handles all of the shit 

# Ideas for MAIN post tutorial completion TODO:
# - obviously some kind of examine button which, when used with an arrow key, allows reading, etc.
# - some kind of tunnel/room random-chance which creates a secret room
# - doors! 
# - lore items
import tcod
import copy

from engine import Engine
import entity_spawn
from procgen import generate_dungeon


def main() -> None:
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    room_max_size = 15
    room_min_size = 8
    max_rooms = 30

    max_monsters_per_room = 2

    tileset = tcod.tileset.load_tilesheet(
        "Redjack17.png", 16, 16, tcod.tileset.CHARMAP_CP437
    )

    player = copy.deepcopy(entity_spawn.player)
    engine = Engine(player=player)


    # call the procgen function to generate dungeon (though this one is preordained)
    engine.game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        engine=engine,
        max_monsters_per_room=max_monsters_per_room,
    )
    engine.update_fov()

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
            engine.event_handler.handle_events()

if __name__ == "__main__":
    main()