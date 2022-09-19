from __future__ import annotations
from random import randrange
import os

#ToDo расспределить по файлам
CROSSES = "X"
NOUGHTS = "0"
EMPTY_CELL = "-"

SCOPE_WINS = "WINS"
SCOPE_DRAWS = "DRAWS"
SCOPE_DEFEATS = "DEFEATS"

MODE_MENU = "M"
MODE_GAME = "G"

SETTING_MODE = "mode"
SETTING_SCOPE = "scope"
SETTING_PLAYER = "player"
SETTING_FIELD = "field"
SETTING_PLAYER_MOVE = "move"
SETTING_LIST_OF_WINS = "list_of_wins"

CHOICE = "Выбирете сторону (x - крестики, o - нолики, r - рандом, e - выйти): "
ERROR_INPUT_COMMAND = "К сожалению непонимаю =( Давай еще раз попробуем"
PLAYER_MOVE = "Ход игрока"
COMPUTER_MOVE = "Ход компьютера"
COMMAND_MOVE = "Укажите координаты хода (Пример: 0 0, e - выйти): "
ERROR_MOVE = "Недоступный ход"


def move(_move: tuple, _setting: dict):
    _setting[SETTING_FIELD][_move[0]][_move[1]] = _setting[SETTING_PLAYER_MOVE]
    next_player(_setting)


def get_move(_setting: dict) -> tuple:
    empty = get_empty_cell(_setting[SETTING_FIELD])
    # ToDo заменить на дерево возможных ходов
    indx = randrange(0, len(empty) - 1)
    return empty[indx]


def clear_screen() -> None:
    # os.system("cls")
    print("\n" * 10)


def show_field(field: list) -> None:
    print(f"y|x\t0\t1\t2")

    _line = ""
    for y, line in enumerate(field):
        _line = f"{y}"
        for x, cell in enumerate(line):
            _line += f"\t{cell}"
        print(_line)


def get_empty_cell(field: list) -> list:
    list_empty = []

    for y, line in enumerate(field):
        for x, cell in enumerate(line):
            if cell == EMPTY_CELL:
                list_empty.append((y, x))

    return list_empty


def check_end_game(_setting: dict) -> bool:
    player = get_player_win(_setting)

    if player == _setting[SETTING_PLAYER]:
        print("Победа")
        add_win(_setting, player, SCOPE_WINS)
        return True
    elif player is None:
        print("Следующий ход")
        return False
    elif player == EMPTY_CELL:
        print("Ничья")
        add_win(_setting, player, SCOPE_DRAWS)
        return True
    else:
        print("Поражение")
        add_win(_setting, player, SCOPE_DEFEATS)
        return True


def get_player_win(_setting: dict) -> str:
    _field = _setting[SETTING_FIELD]

    if all([_field[0][0] != EMPTY_CELL,
            _field[0][1] != EMPTY_CELL,
            _field[0][2] != EMPTY_CELL,
            _field[0][0] == _field[0][1] == _field[0][2]]):
        return _field[0][0]
    elif all([_field[1][0] != EMPTY_CELL,
              _field[1][1] != EMPTY_CELL,
              _field[1][2] != EMPTY_CELL,
              _field[1][0] == _field[1][1] == _field[1][2]]):
        return _field[1][0]
    elif all([_field[2][0] != EMPTY_CELL,
              _field[2][1] != EMPTY_CELL,
              _field[2][2] != EMPTY_CELL,
              _field[2][0] == _field[2][1] == _field[2][2]]):
        return _field[2][0]
    elif all([_field[0][0] != EMPTY_CELL,
              _field[1][0] != EMPTY_CELL,
              _field[2][0] != EMPTY_CELL,
              _field[0][0] == _field[1][0] == _field[2][0]]):
        return _field[0][0]
    elif all([_field[0][1] != EMPTY_CELL,
              _field[1][1] != EMPTY_CELL,
              _field[2][1] != EMPTY_CELL,
              _field[0][1] == _field[1][1] == _field[2][1]]):
        return _field[0][1]
    elif all([_field[0][2] != EMPTY_CELL,
              _field[1][2] != EMPTY_CELL,
              _field[2][2] != EMPTY_CELL,
              _field[0][2] == _field[1][2] == _field[2][2]]):
        return _field[0][2]
    elif all([_field[0][0] != EMPTY_CELL,
              _field[1][1] != EMPTY_CELL,
              _field[2][2] != EMPTY_CELL,
              _field[0][0] == _field[1][1] == _field[2][2]]):
        return _field[0][0]
    elif all([_field[0][2] != EMPTY_CELL,
              _field[1][1] != EMPTY_CELL,
              _field[2][0] != EMPTY_CELL,
              _field[0][2] == _field[1][1] == _field[2][0]]):
        return _field[0][2]
    else:
        _empty = get_empty_cell(_field)
        if _empty:
            return None
        else:
            return EMPTY_CELL


def add_win(_setting: dict, player: str, scope: str):
    _setting[SETTING_MODE] = MODE_MENU
    add_scope(_setting[SETTING_SCOPE], scope)
    _setting[SETTING_LIST_OF_WINS].append(player)


def show_titel():
    print(f"Игра: Крестики-Нолики")


def show_scope(scope: dict):
    print(f"Победы: {scope[SCOPE_WINS]}\t Ничьи: {scope[SCOPE_DRAWS]}\t Поражения: {scope[SCOPE_DEFEATS]}")


def add_scope(scope: dict, mode: str):
    scope[mode] += 1


def input_command_menu(_setting: dict, _text_command: str) -> bool:
    while True:
        command = input(_text_command)
        command = command.upper()

        if command == "E":
            return True
        elif command == "R":
            new_game(_setting, CROSSES if randrange(0, 1) else NOUGHTS)
            break
        elif command == "X":
            new_game(_setting, CROSSES)
            break
        elif command == "O":
            new_game(_setting, NOUGHTS)
            break
        else:
            print(ERROR_INPUT_COMMAND)
            continue

    return False


def input_command_game(_setting: dict, _text_command: str) -> bool:
    while True:
        command = input(_text_command)
        command = command.upper()

        command_list = command.split(' ')

        if command == "E":
            return True
        elif len(command_list) == 2:
            try:
                x = int(command_list[0])
                y = int(command_list[1])
            except ValueError:
                print(ERROR_INPUT_COMMAND)
                break

            if is_cell_empty((y, x), _setting):
                move((y, x), _setting)
            else:
                print(ERROR_MOVE)

            break

        else:
            print(ERROR_INPUT_COMMAND)
            continue

    return False


def is_cell_empty(_move: tuple, _settting: dict) -> bool:
    _field = _settting[SETTING_FIELD]

    if _field[_move[0]][_move[1]] == EMPTY_CELL:
        return True
    else:
        return False


def install_setting(_setting: dict):
    _setting[SETTING_MODE] = MODE_MENU
    _setting[SETTING_SCOPE] = {
        SCOPE_WINS: 0,
        SCOPE_DRAWS: 0,
        SCOPE_DEFEATS: 0
    }
    _setting[SETTING_FIELD] = []
    _setting[SETTING_PLAYER_MOVE] = CROSSES
    _setting[SETTING_LIST_OF_WINS] = []


def next_player(_setting: dict):
    _setting[SETTING_PLAYER_MOVE] = CROSSES if _setting[SETTING_PLAYER_MOVE] == NOUGHTS else NOUGHTS


def new_game(_setting: dict, _player: str):
    _setting[SETTING_FIELD] = [[EMPTY_CELL for j in range(3)] for i in range(3)]
    _setting[SETTING_PLAYER] = _player
    _setting[SETTING_MODE] = MODE_GAME
    _setting[SETTING_PLAYER_MOVE] = CROSSES


def is_move_player(_setting: dict) -> bool:
    return setting[SETTING_PLAYER] == setting[SETTING_PLAYER_MOVE]


if __name__ == "__main__":
    setting = {}
    install_setting(setting)

    while True:
        mode = setting[SETTING_MODE]
        field = setting[SETTING_FIELD]

        if mode == MODE_MENU:
            clear_screen()
            show_titel()
            show_scope(setting[SETTING_SCOPE])

            if input_command_menu(setting, CHOICE):
                break

        elif mode == MODE_GAME:
            clear_screen()

            if is_move_player(setting):
                # Ход игрока
                print(PLAYER_MOVE)
                show_field(field)

                if input_command_game(setting, COMMAND_MOVE):
                    break

            else:
                # Ход компьютора
                print(COMPUTER_MOVE)
                move(get_move(setting), setting)
                show_field(field)

            if check_end_game(setting):
                continue
        else:
            break
