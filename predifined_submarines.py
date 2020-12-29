SUBMARINES_LOCATIONS = (((0, 0), (0, 1)),
                       ((2, 0), (2, 1), (2, 2)),
                       ((4, 0), (4, 1), (4, 2)),
                       ((6, 0), (6, 1), (6, 2), (6, 3)),
                       ((8, 0), (8, 1), (8, 2), (8, 3), (8, 4)))


def insert_predefined_submarines(board):
    for submarine_locations in SUBMARINES_LOCATIONS:
        board.place_submarine(submarine_locations)