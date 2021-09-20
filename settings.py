RESOLUTION = (1280, 720)
DISPLAY = (672, 352)
TARGET_FPS = 60
tile_size = 32

def load_map(path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = data.split('\n')
        game_map = []
        for row in data:
            game_map.append(list(row))
        return game_map

room_layout = load_map("map.txt")

wall_tile = "wall"
corner_wall_tile = "corner_wall"
