class Coordinate:

    X_AXIS = 'abcdefgh'
    Y_AXIS = '12345678'

    @staticmethod
    def x(coord: str): return coord[0]

    @staticmethod
    def y(coord: str): return coord[1]

    @staticmethod
    def ind_x(coord: str): return Coordinate.X_AXIS.find(coord[0])

    @staticmethod
    def ind_y(coord: str): return Coordinate.Y_AXIS.find(coord[1])

    @staticmethod
    def is_valid_move(coord1: str, coord2: str) -> bool:
        if Coordinate.is_coord(coord1) and Coordinate.is_coord(coord2):
            return True if coord1 != coord2 else False
        else:
            return False

    @staticmethod
    def is_coord(coord: str) -> bool:
        if len(coord) != 2:
            return False

        return True if (Coordinate.ind_x(coord) != -1 and
                        Coordinate.ind_y(coord) != -1) else False

    @staticmethod
    def get_coord_by_ind(index_x, index_y):
        if index_x < 0 or index_x > 7 or index_y < 0 or index_y > 7:
            return None
        return Coordinate.X_AXIS[index_x] + Coordinate.Y_AXIS[index_y]

    @staticmethod
    def dif_coord_x(coord1: str, coord2: str) -> int:
        return abs(Coordinate.ind_x(coord1) - Coordinate.ind_x(coord2))

    @staticmethod
    def dif_coord_y(coord1: str, coord2: str) -> int:
        return abs(int(Coordinate.y(coord1)) - int(Coordinate.y(coord2)))

    @staticmethod
    def get_trek_move(first_coord: str, last_coord: str) -> list[str]:
        # получаем путь от first_coord до last_coord
        trek = []

        trek_x_axis = Coordinate.get_trek_x_axis_move(first_coord, last_coord)
        trek_y_axis = Coordinate.get_trek_y_axis_move(first_coord, last_coord)

        if len(trek_x_axis) == 0 and len(trek_y_axis) != 0:
            for coord_y in trek_y_axis:
                trek.append(Coordinate.x(first_coord) + coord_y)

        if len(trek_x_axis) != 0 and len(trek_y_axis) == 0:
            for coord_x in trek_x_axis:
                trek.append(coord_x + Coordinate.y(first_coord))

        if len(trek_x_axis) != 0 and len(trek_y_axis) != 0:
            for index in range(len(trek_x_axis)):
                trek.append(trek_x_axis[index] + trek_y_axis[index])

        return trek

    @staticmethod
    def get_trek_x_axis_move(first_coord: str, last_coord: str) -> str:
        # получаем путь хода по оси Х
        if Coordinate.ind_x(first_coord) <= Coordinate.ind_x(last_coord):
            return Coordinate.X_AXIS[Coordinate.ind_x(first_coord) + 1: Coordinate.ind_x(last_coord)]
        else:
            return Coordinate.X_AXIS[Coordinate.ind_x(last_coord) + 1: Coordinate.ind_x(first_coord)][::-1]

    @staticmethod
    def get_trek_y_axis_move(first_coord: str, last_coord: str) -> str:
        # получаем путь хода по оси У
        if Coordinate.ind_y(first_coord) <= Coordinate.ind_y(last_coord):
            return Coordinate.Y_AXIS[Coordinate.ind_y(first_coord) + 1: Coordinate.ind_y(last_coord)]
        else:
            return Coordinate.Y_AXIS[Coordinate.ind_y(last_coord) + 1: Coordinate.ind_y(first_coord)][::-1]

    @staticmethod
    def get_extreme_coords_on_straight(coord: str) -> list:
        extreme_coords = []
        edges = '18ah'
        for edge_board in edges:
            extreme_coord = Coordinate.x(coord) + edge_board if edge_board.isdigit() \
                            else edge_board + Coordinate.y(coord)
            if not (extreme_coord in extreme_coords):
                extreme_coords.append(Coordinate.x(coord) + edge_board if edge_board.isdigit()
                                      else edge_board + Coordinate.y(coord))

        return extreme_coords

    @staticmethod
    def get_extreme_coords_on_diagonal(coord: str) -> list:
        extreme_coords = []
        coord_x = Coordinate.x(coord)
        coord_y = Coordinate.y(coord)

        ops = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            }

        corner_ops = {
            'a1': {'x': '-', 'y': '-'},
            'a8': {'x': '-', 'y': '+'},
            'h8': {'x': '+', 'y': '+'},
            'h1': {'x': '+', 'y': '-'},
        }

        for corner_board in corner_ops.keys():

            if coord_x == Coordinate.x(corner_board) or coord_y == Coordinate.y(corner_board):
                if not (coord in extreme_coords):
                    extreme_coords.append(coord)
                continue

            dif_x = Coordinate.dif_coord_x(coord, corner_board)
            dif_y = Coordinate.dif_coord_y(coord, corner_board)

            dif = dif_x if dif_x <= dif_y else dif_y

            ind_last_coord_x = ops[corner_ops[corner_board]['x']](Coordinate.ind_x(coord), dif)
            ind_last_coord_y = ops[corner_ops[corner_board]['y']](Coordinate.ind_y(coord), dif)

            extreme_coords.append(Coordinate.X_AXIS[ind_last_coord_x] + Coordinate.Y_AXIS[ind_last_coord_y])

        return extreme_coords
