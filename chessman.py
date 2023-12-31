from coordinate import Coordinate


class Chessman:
    name = ''
    count_move = 0
    available_coordinates = []
    coordinate = ''

    def __init__(self, color, coordinate):
        self.color = color
        self.coordinate = coordinate

    def is_same_color(self, another_chessman):
        if not another_chessman:
            return False
        return another_chessman.color == self.color

    def find_available_coordinates(self, chess_pieces: list):
        raise NotImplementedError

    def get_available_coordinates(self, extreme_coords: list, chess_pieces: list):
        available_coordinates = []
        for extreme_coord in extreme_coords:
            trek = Coordinate.get_trek_move(self.coordinate, extreme_coord)
            trek.append(extreme_coord)
            for square in trek:
                status_coord = self.is_coordinate_available(square, chess_pieces)
                if status_coord:
                    available_coordinates.append(square)
                    if status_coord == 'final':
                        break
                else:
                    break
        return available_coordinates

    def is_coordinate_available(self, coordinate: str, chess_pieces: list):
        for chessman in chess_pieces:
            if coordinate == chessman.coordinate:
                if self.is_same_color(chessman):
                    return False
                else:
                    return 'final'
        return True


class King(Chessman):
    """"Король"""
    name = 'King'

    def can_move(self, coord_a, coord_b, chessman_on_coord_b):
        if self.is_same_color(chessman_on_coord_b):
            return False
        return ((Coordinate.dif_coord_x(coord_a, coord_b) == 0 or Coordinate.dif_coord_x(coord_a, coord_b) == 1) and
                (Coordinate.dif_coord_y(coord_a, coord_b) == 0 or Coordinate.dif_coord_y(coord_a, coord_b) == 1))

    def find_available_coordinates(self, chess_pieces: list):
        available_coordinates = []

        ind_x = Coordinate.ind_x(self.coordinate)
        ind_y = Coordinate.ind_y(self.coordinate)

        coordinates = []

        dif = [-1, 0, 1]
        for dif_x in dif:
            for dif_y in dif:
                if dif_x == 0 and dif_y == 0:
                    continue
                coord = Coordinate.get_coord_by_ind(ind_x + dif_x, ind_y + dif_y)
                if coord:
                    coordinates.append(coord)

        for coord in coordinates:
            if self.is_coordinate_available(coord, chess_pieces):
                available_coordinates.append(coord)
        return available_coordinates


class Queen(Chessman):
    """Королева"""
    name = 'Queen'

    def find_available_coordinates(self, chess_pieces: list):
        extreme_coords = Coordinate.get_extreme_coords_on_straight(self.coordinate)
        extreme_coords.extend(Coordinate.get_extreme_coords_on_diagonal(self.coordinate))
        return self.get_available_coordinates(extreme_coords, chess_pieces)


class Rook(Chessman):
    """Ладья"""
    name = 'Rook'

    def find_available_coordinates(self, chess_pieces: list):
        extreme_coords = Coordinate.get_extreme_coords_on_straight(self.coordinate)
        return self.get_available_coordinates(extreme_coords, chess_pieces)


class Bishop(Chessman):
    """"Слон"""
    name = 'Bishop'

    def find_available_coordinates(self, chess_pieces: list):
        extreme_coords = Coordinate.get_extreme_coords_on_diagonal(self.coordinate)
        return self.get_available_coordinates(extreme_coords, chess_pieces)


class Knight(Chessman):
    """Конь"""
    name = 'Knight'

    def find_available_coordinates(self, chess_pieces: list):
        available_coordinates = []
        ind_x = Coordinate.ind_x(self.coordinate)
        ind_y = Coordinate.ind_y(self.coordinate)

        coordinates = []

        dif = [-2, -1, 1, 2]
        for dif_x in dif:
            for dif_y in dif:
                if abs(dif_x) == abs(dif_y):
                    continue
                coord = Coordinate.get_coord_by_ind(ind_x + dif_x, ind_y + dif_y)
                if coord:
                    coordinates.append(coord)

        for coord in coordinates:
            if self.is_coordinate_available(coord, chess_pieces):
                available_coordinates.append(coord)
        return available_coordinates


class Pawn(Chessman):
    """"Пешка"""
    name = 'Pawn'
    en_passant = False

    def find_available_coordinates(self, chess_pieces: list):
        available_coordinates = []
        ind_x = Coordinate.ind_x(self.coordinate)
        ind_y = Coordinate.ind_y(self.coordinate)

        coordinates = []
        coordinates_en_passant = []

        if self.color == 'white':
            dif_move = [1]
            dif_attack = {'x': [-1, 1], 'y': 1}
            if ind_y == 1:
                dif_move.append(2)
        else:
            dif_move = [-1]
            dif_attack = {'x': [-1, 1], 'y': -1}
            if ind_y == 6:
                dif_move.append(-2)

        for dif_move_y in dif_move:
            coord = Coordinate.get_coord_by_ind(ind_x, ind_y + dif_move_y)
            if coord:
                coordinates.append(coord)

        for coord in coordinates:
            if self.is_coordinate_available_for_move_pawn(coord, chess_pieces):
                available_coordinates.append(coord)
            else:
                break

        coordinates.clear()

        for dif_attack_x in dif_attack['x']:
            coord = Coordinate.get_coord_by_ind(ind_x + dif_attack_x, ind_y + dif_attack['y'])
            if coord:
                coordinates.append(coord)
            coord_en_passant = Coordinate.get_coord_by_ind(ind_x + dif_attack_x, ind_y)
            if coord_en_passant:
                coordinates_en_passant.append(coord_en_passant)

        for coord, coord_en_passant in zip(coordinates, coordinates_en_passant):
            if self.is_coordinate_available_for_attack_pawn(coord, chess_pieces):
                available_coordinates.append(coord)
            if self.is_coordinate_available_for_en_passant(coord_en_passant, chess_pieces):
                available_coordinates.append(coord)
        return available_coordinates

    def is_coordinate_available_for_attack_pawn(self, coordinate: str, chess_pieces: list):
        for chessman in chess_pieces:
            if chessman == self:
                continue
            if coordinate == chessman.coordinate:
                if self.is_same_color(chessman):
                    return False
                else:
                    return True
        return False

    def is_coordinate_available_for_move_pawn(self, coordinate: str, chess_pieces: list):
        for chessman in chess_pieces:
            if chessman == self:
                continue
            if coordinate == chessman.coordinate:
                return False
        return True

    def is_coordinate_available_for_en_passant(self, coordinate: str, chess_pieces: list):
        for chessman in chess_pieces:
            if chessman == self:
                continue
            if coordinate == chessman.coordinate and chessman.name == self.name:
                if chessman.en_passant:
                    return True
        return False
