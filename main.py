from chessboard import Chessboard


class Player:
    is_king_taken = False

    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color

    @property
    def is_having_king(self):
        return self.is_king_taken

    def move(self, chessboard: Chessboard) -> bool:
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
                print("invalid input of coordinates")
                continue
            coord1 = input_coord1
            coord2 = input_coord2
        self.is_king_taken = chessboard.move_player(coord1, coord2)
        return self.is_king_taken


def play():
    chessboard = Chessboard()
    player1 = Player('Player1', 'white')
    player2 = Player('Player2', 'black')

    while True:
        is_mate = player1.move(chessboard)
        if is_mate:
            break
        is_mate = player2.move(chessboard)
        if is_mate:
            break

    winner = player1 if player1.is_king_taken else player2

    print(f'Winner {winner.name} ({winner.color})')


if __name__ == '__main__':
    play()

# TODO: реализовать нечью и возможность сдаться
# TODO: реализовать проверку на "шах" (до и после хода)
# TODO: реализовать рокировку
# TODO: реализовать превращение пешки
# TODO: реализовать взятие на проходе (может быть)
