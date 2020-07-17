from room import Room
from player import Player
from world import World
from util import Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

traversal_path = []
reverse = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}

# Creates dict for starting room path
room_path = {}
room_path[player.current_room.id] = {x: '?' for x in player.current_room.get_exits()}
# Creates set to store starting room and its exits
rooms = set()
for exit in player.current_room.get_exits():
    rooms.add(f'{player.current_room.id}{exit}')


def find_next_move(room):
    if 'n' in room_path[room] and room_path[room]['n'] == '?':
        return 'n'
    elif 'e' in room_path[room] and room_path[room]['e'] == '?':
        return 'e'
    elif 's' in room_path[room] and room_path[room]['s'] == '?':
        return 's'
    elif 'w' in room_path[room] and room_path[room]['w'] == '?':
        return 'w'

while rooms:
    if '?' in room_path[player.current_room.id].values():
        next_move = None
        starting_room = player.current_room.id
        next_move = find_next_move(starting_room)
        rooms.remove(f'{player.current_room.id}{next_move}')
        player.travel(next_move)
        new_room = player.current_room.id
        traversal_path.append(next_move)

        if new_room not in room_path:
            room_path[new_room] = {
                x: '?' for x in player.current_room.get_exits()}

        room_path[starting_room][next_move] = new_room
        room_path[new_room][reverse[next_move]] = starting_room

        for exit, value in room_path[new_room].items():
            if value == '?':
                rooms.add(f'{new_room}{exit}')

        if f'{new_room}{reverse[next_move]}' in rooms:
            rooms.remove(f'{new_room}{reverse[next_move]}')
    else:
        starting_room = player.current_room.id
        q = Queue()

        for direction, room in room_path[starting_room].items():
            q.enqueue([[direction, room]])

        while q.size:
            current_path = q.dequeue()
            current = current_path[-1]

            if '?' in [room for direction, room in room_path[current[1]].items()]:
                for direction, room in current_path:
                    player.travel(direction)
                    traversal_path.append(direction)
                break

            else:
                for direction, room in room_path[current[1]].items():
                    if room != starting_room and room not in [y for x, y in current_path]:
                        q.enqueue(list(current_path) + [[direction, room]])

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
