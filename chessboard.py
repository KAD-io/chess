from chessman import *
from coordinate import Coordinate
import copy
from typing import List


class Chessboard:

    squares = {}

    def __init__(self):
        self.squares = self.home_position()

    @staticmethod
    def home_position() -> dict:
        dict_home_pos = dict.fromkeys(Coordinate.COORDINATE_X)
        for x in Coordinate.COORDINATE_X:
            dict_home_pos[x] = dict.fromkeys(Coordinate.COORDINATE_Y)

        dict_home_pos['a']['1'] = Rook('white')
        dict_home_pos['b']['1'] = Knight('white')
        dict_home_pos['c']['1'] = Bishop('white')
        dict_home_pos['d']['1'] = Queen('white')
        dict_home_pos['e']['1'] = King('white')
        dict_home_pos['f']['1'] = Bishop('white')
        dict_home_pos['g']['1'] = Knight('white')
        dict_home_pos['h']['1'] = Rook('white')

        dict_home_pos['a']['8'] = Rook('black')
        dict_home_pos['b']['8'] = Knight('black')
        dict_home_pos['c']['8'] = Bishop('black')
        dict_home_pos['d']['8'] = Queen('black')
        dict_home_pos['e']['8'] = King('black')
        dict_home_pos['f']['8'] = Bishop('black')
        dict_home_pos['g']['8'] = Knight('black')
        dict_home_pos['h']['8'] = Rook('black')

        for x in Coordinate.COORDINATE_X:
            dict_home_pos[x]['2'] = Pawn('white')
            dict_home_pos[x]['7'] = Pawn('black')

        return dict_home_pos

    @staticmethod
    def get_trek_move(coord1: str, coord2: str) -> List[str]:
        trek = []

        trek_x_axis = Chessboard.get_trek_x_axis_move(coord1, coord2)
        trek_y_axis = Chessboard.get_trek_y_axis_move(coord1, coord2)

        if len(trek_x_axis) == 0 and len(trek_y_axis) != 0:
            for coord_y in trek_y_axis:
                trek.append(Coordinate.x(coord1) + coord_y)

        if len(trek_x_axis) != 0 and len(trek_y_axis) == 0:
            for coord_x in trek_x_axis:
                trek.append(coord_x + Coordinate.y(coord1))

        if len(trek_x_axis) != 0 and len(trek_y_axis) != 0:
            for index in range(len(trek_x_axis)):
                trek.append(trek_x_axis[index] + trek_y_axis[index])

        return trek

    @staticmethod
    def get_trek_x_axis_move(coord1: str, coord2: str) -> str:
        if Coordinate.ind_x(coord1) <= Coordinate.ind_x(coord2):
            return Coordinate.COORDINATE_X[Coordinate.ind_x(coord1) + 1: Coordinate.ind_x(coord2)]
        else:
            return Coordinate.COORDINATE_X[Coordinate.ind_x(coord2) + 1: Coordinate.ind_x(coord1)][::-1]

    @staticmethod
    def get_trek_y_axis_move(coord1: str, coord2: str) -> str:
        if Coordinate.ind_y(coord1) <= Coordinate.ind_y(coord2):
            return Coordinate.COORDINATE_Y[Coordinate.ind_y(coord1) + 1: Coordinate.ind_y(coord2)]
        else:
            return Coordinate.COORDINATE_Y[Coordinate.ind_y(coord2) + 1: Coordinate.ind_y(coord1)][::-1]

    def get_status_square(self, coord: str) -> Chessman:
        return self.squares[Coordinate.x(coord)][Coordinate.y(coord)]

    def render(self):
        FIRST_LINE = "  ╔══ A ══╕╒═ B ══╕╒═ C ══╕╒═ D ══╕╒═ E ══╕╒═ F ══╕╒═ G ══╕╒══ H ══╗"
        FINAL_LINE = "  ╚══ A ══╛╘═ B ══╛╘═ C ══╛╘═ D ══╛╘═ E ══╛╘═ F ══╛╘═ G ══╛╘══ H ══╝"
        print(FIRST_LINE)
        for y in Coordinate.COORDINATE_Y[::-1]:
            first_str = str(y) + ' ║'
            second_str = '  ║'
            for x in Coordinate.COORDINATE_X:       #чет начинается с белой
                if int(y) % 2:                      #у-неч.
                    if Coordinate.ind_x(x) % 2:     #х-чет.
                        first_str += Chessboard.render_square_first_str(self.squares[x][y], '█')
                        second_str += Chessboard.render_square_second_str(self.squares[x][y], '█')
                    else:                           #х-неч.
                        first_str += Chessboard.render_square_first_str(self.squares[x][y], ' ')
                        second_str += Chessboard.render_square_second_str(self.squares[x][y], ' ')
                else:                               #у-чет.
                    if Coordinate.ind_x(x) % 2:     #х-чет.
                        first_str += Chessboard.render_square_first_str(self.squares[x][y], ' ')
                        second_str += Chessboard.render_square_second_str(self.squares[x][y], ' ')
                    else:                           #х-нетч.
                        first_str += Chessboard.render_square_first_str(self.squares[x][y], '█')
                        second_str += Chessboard.render_square_second_str(self.squares[x][y], '█')
            first_str += '║ ' + str(y)
            second_str += '║'
            print(first_str)
            print(second_str)
        print(FINAL_LINE)

    @staticmethod
    def render_square_first_str(chessman: Chessman, square_color: str) -> str:
        return f"{chessman.name:{square_color}^8}" if chessman else f"{'':{square_color}^8}"

    @staticmethod
    def render_square_second_str(chessman: Chessman, square_color: str) -> str:
        return f"{chessman.color:{square_color}^8}" if chessman else f"{'':{square_color}^8}"

    def move_player(self, coord1: str, coord2: str) -> bool:
        is_king_taken = False
        if self.squares[Coordinate.x(coord2)][Coordinate.y(coord2)]:
            if self.squares[Coordinate.x(coord2)][Coordinate.y(coord2)].name == 'King':
                is_king_taken = True

        self.squares[Coordinate.x(coord2)][Coordinate.y(coord2)] = None

        self.squares[Coordinate.x(coord2)][Coordinate.y(coord2)] = copy.deepcopy(
            self.squares[Coordinate.x(coord1)][Coordinate.y(coord1)])

        self.squares[Coordinate.x(coord1)][Coordinate.y(coord1)] = None

        return is_king_taken

    def is_valid_move_player(self, color_player: str, coord1: str, coord2: str) -> bool:

        #  не выходятли координаты за пределы доски
        #  клетка_А != клетка_Б
        is_valid_coord = Coordinate.is_valid_move(coord1, coord2)
        if not is_valid_coord:
            return False

        #   не пусто ли на клетке_А
        status_squar1 = self.get_status_square(coord1)
        status_squar2 = self.get_status_square(coord2)
        if not status_squar1:
            return False

        #  стоит ли на клетке_А фигура цвета игрока
        is_valid_color = status_squar1.color == color_player
        if not is_valid_color:
            return False

        #  не стоит ли на клетке_Б фигура того же цвета что на клетке_А
        if status_squar2:
            if status_squar1.color == status_squar2.color:
                return False

        #  может ли фигура с А попасть на Б в принцепе (через метод фигуры)
        is_move_chessman = status_squar1.can_move(coord1, coord2)
        if not is_move_chessman:
            return False

        # нет ли фигур на промежутке пути А-Б ( доска возвращает list клеток для проверки)
        # исключение проверки пути для коня
        if status_squar1.name == 'Knight':
            return True
        trek_move = self.get_trek_move(coord1, coord2)
        for square in trek_move:
            if self.get_status_square(square):
                return False

        return True




# class Squares:
#     def __init__(self, color, coordinate, status):
#         self.color = color
#         self.coordinate = coordinate
#         self.status = status
#
#     def get_status(self):
#         return self.status

