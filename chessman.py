from coordinate import Coordinate


class Chessman:
    name = ''

    def __init__(self, color):
        self.color = color

    def is_move(self, coord_a, coord_b):
        raise NotImplementedError

    def get_color(self):
        return self.color

    @classmethod
    def get_name(cls):
        return cls.name


class King(Chessman):
    """"Король"""
    name = 'King'

    def __init__(self, color):
        super().__init__(color)

    def is_move(self, coord_a, coord_b):
        return ((Coordinate.dif_coord_x(coord_a, coord_b) == 0 or Coordinate.dif_coord_x(coord_a, coord_b) == 1) and
                (Coordinate.dif_coord_y(coord_a, coord_b) == 0 or Coordinate.dif_coord_y(coord_a, coord_b) == 1))


class Queen(Chessman):
    """Королева"""
    name = 'Queen'

    def __init__(self, color):
        super().__init__(color)

    def is_move(self, coord_a, coord_b):
        return (Coordinate.is_move_horizontal(coord_a, coord_b) or
                Coordinate.is_move_vertical(coord_a, coord_b) or
                Coordinate.is_move_diogonal(coord_a, coord_b))


class Rook(Chessman):
    """Ладья"""
    name = 'Rook'

    def is_move(self, coord_a, coord_b):
        return (Coordinate.is_move_horizontal(coord_a, coord_b) or
                Coordinate.is_move_vertical(coord_a, coord_b))


class Bishop(Chessman):
    """"Слон"""
    name = 'Bishop'
    def __init__(self, color):
        super().__init__(color)

    def is_move(self, coord_a, coord_b):
        return Coordinate.is_move_diogonal(coord_a, coord_b)


class Knight(Chessman):
    """Конь"""
    name = 'Knight'

    def is_move(self, coord_a, coord_b):
        return ((Coordinate.dif_coord_x(coord_a, coord_b) == 1 and Coordinate.dif_coord_y(coord_a, coord_b) == 2) or
                (Coordinate.dif_coord_x(coord_a, coord_b) == 2 and Coordinate.dif_coord_y(coord_a, coord_b) == 1))


class Pawn(Chessman):
    """"Пешка"""
    name = 'Pawn'

    def is_move(self, coord_a, coord_b):
        if self.get_color() == 'white':
            if Coordinate.get_y(coord_a) == '2':
                return ((Coordinate.dif_coord_x(coord_a, coord_b) == 0 and (Coordinate.dif_dir_coord_y(coord_a, coord_b) == 1 or
                                                                            Coordinate.dif_dir_coord_y(coord_a, coord_b) == 2)) or
                        (Coordinate.dif_coord_x(coord_a, coord_b) == 1 and Coordinate.dif_dir_coord_y(coord_a, coord_b) == 1))
            else:
                return ((Coordinate.dif_coord_x(coord_a, coord_b) == 0 and Coordinate.dif_dir_coord_y(coord_a, coord_b) == 1) or
                        (Coordinate.dif_coord_x(coord_a, coord_b) == 1 and Coordinate.dif_dir_coord_y(coord_a, coord_b) == 1))
        else:
            if Coordinate.get_y(coord_a) == '7':
                return ((Coordinate.dif_coord_x(coord_a, coord_b) == 0 and (Coordinate.dif_dir_coord_y(coord_a, coord_b) == -1 or
                                                                            Coordinate.dif_dir_coord_y(coord_a, coord_b) == -2)) or
                        (Coordinate.dif_coord_x(coord_a, coord_b) == 1 and Coordinate.dif_dir_coord_y(coord_a, coord_b) == -1))
            else:
                return ((Coordinate.dif_coord_x(coord_a, coord_b) == 0 and Coordinate.dif_dir_coord_y(coord_a, coord_b) == -1) or
                        (Coordinate.dif_coord_x(coord_a, coord_b) == 1 and Coordinate.dif_dir_coord_y(coord_a, coord_b) == -1))