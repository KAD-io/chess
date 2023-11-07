from chessboard import Chessboard


class Player:
    mate = False
    check = False
    chess_pieces: list

    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color

    def move(self, opponent_player, chessboard: Chessboard) -> bool:
        mate = False
        if self.check:
            mate = chessboard.is_mate(self.color)
            if mate:
                return mate
        chessboard.render()
        coord1 = ''
        coord2 = ''
        is_valid_move_player = False
        while not is_valid_move_player:
            print(f'move: {self.name} ({self.color})')
            input_coord1 = input('input coordinate 1: ').lower()
            input_coord2 = input('input coordinate 2: ').lower()
            is_valid_move_player = chessboard.is_valid_move_player(self.color, input_coord1, input_coord2)
            if not is_valid_move_player:
                print('enter coordinates taking into account the warning')
                continue
            coord1 = input_coord1
            coord2 = input_coord2

        opponent_player.check = chessboard.move_player(coord1, coord2)

        return mate


def play():
    player1 = Player('Player1', 'white')
    player2 = Player('Player2', 'black')
    chessboard = Chessboard()
    chessboard.set_available_coordinates_for_chess_pieces()

    while True:
        player1.mate = player1.move(player2, chessboard)
        if player1.mate:
            break
        player2.mate = player2.move(player1, chessboard)
        if player2.mate:
            break

    winner = player1 if player2.mate else player2

    print(f'Winner {winner.name} ({winner.color})')


if __name__ == '__main__':
    play()

# TODO: реализовать нечью и возможность сдаться


# TODO: Общий алгоритм:
#  1. Игрок вводит координату А (А) и координату B (В)
#  2. Проверка на то можно ли походить с А на Б:
#   2.1 Проверка на то что введенные координаты коректны
#   2.2 Проверка на то что на А стоит фигура того же цвета что и у игрока
#   2.3 Проверка на то что на В не стоит фигура того же цвета что и у игрока
#   2.4 Проверка на то что на для фигуры на А, В находиться в диапазоне доступности /
#       для пути фигуры на А нет других фигур (для коня исключение)
#   2.5 Фигура в "песочнице" делает ход с А на В -> проверка не подставляет ли игрок своего короля под шаг
#  3.1 Если проверка 2 не прошла, -> переходим на п1
#  3.2 Если проверка 2 прошла -> фигура делает ход с А на В
#  4 Вычитаем диапазон возможных ходов для фигур
#  5 Проверка на то что поставлен ли противнику шаг
#   5.1 Если проверка 5 прошла -> Проверка на то что не поставлен ли противнику мат
#       (перебираем весь диапазон возможных ходов всех фигур противника в "песочнице",
#       смотрим может ли противник выйти из шага)
#       5.1.1 Если проверка 5.1 не прошла -> Игрок выиграл
#       5.1.2 Если проверка 5.1 прошла -> Передаем ход противнику -> переходим на п1
#   5.2 Если проверка 5 не прошла -> Передаем ход противнику -> переходим на п1



