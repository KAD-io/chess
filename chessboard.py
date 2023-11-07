from chessman import Chessman, Rook, Knight, Bishop, Queen, King, Pawn
from coordinate import Coordinate


class Chessboard:
    squares = {}
    coord_kings = {'white': 'e1', 'black': 'e8'}
    chess_pieces = {'white': [], 'black': []}

    def __init__(self):
        self.squares, self.chess_pieces['white'], self.chess_pieces['black'] = self.home_position()

    @staticmethod
    def home_position() -> tuple:
        dict_home_pos = dict.fromkeys(Coordinate.X_AXIS)
        for x in Coordinate.X_AXIS:
            dict_home_pos[x] = dict.fromkeys(Coordinate.Y_AXIS)

        white_pieces = []
        black_pieces = []
        chess_pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        for ind in range(8):
            x = Coordinate.X_AXIS[ind]
            chessman = chess_pieces[ind]
            dict_home_pos[x]['1'] = chessman('white', f'{x}1')
            white_pieces.append(dict_home_pos[x]['1'])
            dict_home_pos[x]['8'] = chessman('black', f'{x}8')
            black_pieces.append(dict_home_pos[x]['8'])

        for x in Coordinate.X_AXIS:
            dict_home_pos[x]['2'] = Pawn('white', f'{x}2')
            white_pieces.append(dict_home_pos[x]['2'])
            dict_home_pos[x]['7'] = Pawn('black', f'{x}7')
            black_pieces.append(dict_home_pos[x]['7'])

        return dict_home_pos, white_pieces, black_pieces

    def get_status_square(self, coord: str) -> Chessman:
        return self.squares[Coordinate.x(coord)][Coordinate.y(coord)]

    def render(self):

        FIRST_LINE = "  ╔══ A ══╕╒═ B ══╕╒═ C ══╕╒═ D ══╕╒═ E ══╕╒═ F ══╕╒═ G ══╕╒══ H ══╗"
        FINAL_LINE = "  ╚══ A ══╛╘═ B ══╛╘═ C ══╛╘═ D ══╛╘═ E ══╛╘═ F ══╛╘═ G ══╛╘══ H ══╝"

        print(FIRST_LINE)
        for y in Coordinate.Y_AXIS[::-1]:
            first_str = str(y) + ' ║'
            second_str = '  ║'
            for x in Coordinate.X_AXIS:  # чет начинается с белой
                if int(y) % 2:  # у-неч.
                    if Coordinate.ind_x(x) % 2:  # х-чет.
                        first_str += Chessboard.render_square_first_str(self.squares[x][y], '█')
                        second_str += Chessboard.render_square_second_str(self.squares[x][y], '█')
                    else:  # х-неч.
                        first_str += Chessboard.render_square_first_str(self.squares[x][y], ' ')
                        second_str += Chessboard.render_square_second_str(self.squares[x][y], ' ')
                else:  # у-чет.
                    if Coordinate.ind_x(x) % 2:  # х-чет.
                        first_str += Chessboard.render_square_first_str(self.squares[x][y], ' ')
                        second_str += Chessboard.render_square_second_str(self.squares[x][y], ' ')
                    else:  # х-нетч.
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
        moving_chessman = self.get_status_square(coord1)

        self.move(coord1, coord2)

        check = self.is_check(self.invert_color(moving_chessman.color))

        if self.can_promotion_pawn(coord2):
            self.promotion_pawn(coord2, self.get_status_square(coord2).color)

        # пересчет допустимого диапазона ходов для всех фигур
        self.set_available_coordinates_for_chess_pieces()

        return check

    def is_check_in_testing_move(self, coord1: str, coord2: str) -> bool:
        status_coord2 = self.get_status_square(coord2)

        self.move(coord1, coord2)

        if self.is_check(self.get_status_square(coord2).color):
            self.reverse_move(coord1, coord2, status_coord2)
            return True
        self.reverse_move(coord1, coord2, status_coord2)
        return False

    def move(self, coord1: str, coord2: str):

        moving_chessman = self.get_status_square(coord1)
        chessman_on_coord2 = self.get_status_square(coord2)

        self.squares[Coordinate.x(coord2)][Coordinate.y(coord2)] = \
            self.squares[Coordinate.x(coord1)][Coordinate.y(coord1)]
        self.squares[Coordinate.x(coord1)][Coordinate.y(coord1)] = None

        if chessman_on_coord2:
            # пересчет оставшихся фигур на доске
            self.chess_pieces[chessman_on_coord2.color].remove(chessman_on_coord2)

        if moving_chessman.name == 'King':
            self.coord_kings[moving_chessman.color] = coord2
        moving_chessman.count_move += 1
        moving_chessman.coordinate = coord2

        # пересчет допустимого диапазона ходов для всех фигур
        self.set_available_coordinates_for_chess_pieces()

    def reverse_move(self, coord1: str, coord2: str, buffer: Chessman):

        moving_chessman = self.get_status_square(coord2)

        self.squares[Coordinate.x(coord1)][Coordinate.y(coord1)] = \
            self.squares[Coordinate.x(coord2)][Coordinate.y(coord2)]
        self.squares[Coordinate.x(coord2)][Coordinate.y(coord2)] = buffer
        if buffer:
            self.chess_pieces[buffer.color].append(buffer)

        if moving_chessman.name == 'King':
            self.coord_kings[moving_chessman.color] = coord1
        moving_chessman.count_move -= 1
        moving_chessman.coordinate = coord1

        # пересчет допустимого диапазона ходов для всех фигур
        self.set_available_coordinates_for_chess_pieces()

    def is_valid_move_player(self, color_player: str, coord1: str, coord2: str):

        #  не выходятли координаты за пределы доски
        #  клетка_А != клетка_Б
        if not Coordinate.is_valid_move(coord1, coord2):
            print('invalid input of coordinates')
            return False

        #   не пусто ли на клетке_А
        chessman_on_coord1 = self.get_status_square(coord1)
        if not chessman_on_coord1:
            print(f'the square on {coord1} is empty')
            return False

        #  стоит ли на клетке_А фигура цвета игрока
        if not chessman_on_coord1.color == color_player:
            print(f'the chessman on {coord1} is not your color')
            return False

        if self.is_castling(coord1, coord2):
            return 'castling'

        #  может ли фигура с А попасть на Б в принцепе
        if coord2 not in chessman_on_coord1.available_coordinates:
            print(f'the square on {coord2} is not available for the {chessman_on_coord1.name} on {coord1}')
            return False

        # is_move_chessman = chessman_on_coord1.can_move(coord1, coord2, self.get_status_square(coord2))
        # if not is_move_chessman:
        #     return False
        #
        # # нет ли фигур на промежутке пути А-Б ( доска возвращает list клеток для проверки)
        # # исключение проверки пути для коня
        # if chessman_on_coord1.name == 'Knight':
        #     return True
        # trek_move = Coordinate.get_trek_move(coord1, coord2)
        # for square in trek_move:
        #     if self.get_status_square(square):
        #         return False

        # не ставит ли игрок своим ходом "шаг" самому себе
        if self.is_check_in_testing_move(coord1, coord2):
            print('you cannot make a move after which your king is placed in check')
            return False

        return True

    def can_promotion_pawn(self, coord: str) -> bool:
        if self.get_status_square(coord).name != 'Pawn':
            return False
        return Coordinate.y(coord) == '1' or Coordinate.y(coord) == '8'

    def promotion_pawn(self, coord, color):
        # превращение пешки
        FIGURES_FOR_PROMOTION = {'q': Queen, 'r': Rook, 'b': Bishop, 'k': Knight}
        valid_chessman = False
        while not valid_chessman:
            print('Your pawn is moved to its last rank!')
            print('q - Queen, r - Rook, b - Bishop, k - Knight')
            input_chessman = input('Enter one of the symbols to promotion the pawn: ').lower()

            valid_chessman = input_chessman in FIGURES_FOR_PROMOTION.keys()
            if not valid_chessman:
                print("invalid input of chessman for promotion")
                continue
            count_move = self.get_status_square(coord).count_move
            self.squares[Coordinate.x(coord)][Coordinate.y(coord)] = FIGURES_FOR_PROMOTION[input_chessman](color, coord)
            self.get_status_square(coord).count_move = count_move

    @staticmethod
    def invert_color(color_player: str) -> str:
        return 'white' if color_player == 'black' else 'black'

    def is_check(self, color_player: str) -> bool:
        opponent_color = self.invert_color(color_player)
        for chessman in self.chess_pieces[opponent_color]:
            if self.coord_kings[color_player] in chessman.available_coordinates:
                return True
        return False

    def is_mate(self, color_player: str) -> bool:
        for chessman in self.chess_pieces[color_player]:
            for coord in chessman.available_coordinates:
                if not self.is_check_in_testing_move(chessman.coordinate, coord):
                    return False
        return True

    def is_castling(self, coord1: str, coord2: str) -> bool:
        trek = Coordinate.get_trek_move(coord1, coord2)
        for square in trek:
            if self.get_status_square(square):
                return False

        chessman_on_coord1 = self.get_status_square(coord1)
        chessman_on_coord2 = self.get_status_square(coord2)

        if len(trek) == 2 or len(trek) == 3:
            for square in [chessman_on_coord1.coordinate, trek[0], trek[1]]:
                for chessman in self.chess_pieces[self.invert_color(chessman_on_coord1.color)]:
                    if square in chessman.available_coordinates:
                        return False
        else:
            return False

        if chessman_on_coord1.name == 'King' and \
                chessman_on_coord2.name == 'Rook' and \
                chessman_on_coord1.color == chessman_on_coord2.color and \
                chessman_on_coord1.count_move == 0 and \
                chessman_on_coord2.count_move == 0:
            return True

        return False

    def castling(self, coord1: str, coord2: str):

        coord_y = Coordinate.y(coord1)
        if Coordinate.x(coord2) == 'a':
            coord_king = 'c' + coord_y
            coord_rook = 'd' + coord_y
        else:
            coord_king = 'g' + coord_y
            coord_rook = 'f' + coord_y

        self.move_castling(coord1, coord_king)
        self.move_castling(coord2, coord_rook)

        # пересчет допустимого диапазона ходов для всех фигур
        self.set_available_coordinates_for_chess_pieces()

    def move_castling(self, coord1: str, coord2: str):

        moving_chessman = self.get_status_square(coord1)

        self.squares[Coordinate.x(coord2)][Coordinate.y(coord2)] = \
            self.squares[Coordinate.x(coord1)][Coordinate.y(coord1)]
        self.squares[Coordinate.x(coord1)][Coordinate.y(coord1)] = None

        if moving_chessman.name == 'King':
            self.coord_kings[moving_chessman.color] = coord2
        moving_chessman.count_move += 1
        moving_chessman.coordinate = coord2

    def set_available_coordinates_for_chess_pieces(self):

        chess_pieces = []
        chess_pieces.extend(self.chess_pieces['white'])
        chess_pieces.extend(self.chess_pieces['black'])

        for chessman in chess_pieces:
            chessman.available_coordinates = chessman.find_available_coordinates(chess_pieces)
