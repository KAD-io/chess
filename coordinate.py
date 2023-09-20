class Coordinate:

    COORDINATE_X = 'abcdefgh'
    COORDINATE_Y = '12345678'
    @staticmethod
    def x(coord: str): return coord[0]
    @staticmethod
    def y(coord: str): return coord[1]

    @staticmethod
    def ind_x(coord: str): return Coordinate.COORDINATE_X.find(coord[0])

    @staticmethod
    def ind_y(coord: str): return Coordinate.COORDINATE_Y.find(coord[1])

    @staticmethod
    def ind_axis(coord: str, coord_axis: str):
        return coord_axis.find(coord)

    @staticmethod
    def get_x(coord: str): return coord[0]

    @staticmethod
    def get_y(coord: str): return coord[1]

    @staticmethod
    def is_valid_move(coord1: str, coord2: str) -> bool:
        if Coordinate.is_coord(coord1) and Coordinate.is_coord(coord2):
            return True if coord1 != coord2 else False
        else:
            return False

    @staticmethod
    def is_coord(coord: str) -> bool:
        if len(coord) != 2: return False

        return True if (Coordinate.COORDINATE_X.find(coord[0]) != -1 and
                        Coordinate.COORDINATE_Y.find(coord[1]) != -1) else False

    @staticmethod
    def dif_coord_x(coord1: str, coord2: str) -> int:
        return abs(Coordinate.ind_x(coord1) - Coordinate.ind_x(coord2))

    @staticmethod
    def dif_coord_y(coord1: str, coord2: str) -> int:
        return abs(int(Coordinate.y(coord1)) - int(Coordinate.y(coord2)))

    @staticmethod
    def dif_dir_coord_y(coord1: str, coord2: str) -> int:
        return int(Coordinate.y(coord2)) - int(Coordinate.y(coord1))

    @staticmethod
    def is_move_vertical(coord1: str, coord2: str) -> bool:
        return Coordinate.dif_coord_x(coord1, coord2) == 0

    @staticmethod
    def is_move_horizontal(coord1: str, coord2: str) -> bool:
        return Coordinate.dif_coord_y(coord1, coord2) == 0

    @staticmethod
    def is_move_diogonal(coord1: str, coord2: str) -> bool:
        return Coordinate.dif_coord_x(coord1, coord2) == Coordinate.dif_coord_y(coord1, coord2)

