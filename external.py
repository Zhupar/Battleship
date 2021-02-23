from random import randint
from exceptions import *
from internal import *


class Player:
    def __init__(self, board, comp):
        self.board = board
        self.comp = comp

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                ask = self.ask()
                repeat = self.comp.shot(ask)
                return repeat
            except BoardException as e:
                print(e)


class User(Player):
    def ask(self):
        try:
            inp = input()
            inp_list = inp.split()
            x = inp_list[0]
            y = inp_list[1]
            d = Dot(int(x), int(y))
            return d
        except ValueError:
            print(" Введите числа! ")


class AI(Player):
    def ask(self):
        d = Dot(randint(1, 6), randint(1, 6))
        print(f"Ход компьютера: {d.x} {d.y}")
        return d


class Game:
    def __init__(self):
        pl = self.if_none(hid=False)
        co = self.if_none(hid=True)


        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self, hid):
        ships_len = [3, 2, 2, 1, 1, 1, 1]
        b = Board(hid)
        attempts = 0
        for ship_len in ships_len:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                try:
                    h = Dot(randint(1, 7), randint(1, 7))
                    s = Ship(h, ship_len, randint(0, 1))
                    b.add_ship(s)
                    break
                except BoardWrongShipException:
                    pass
        b.begin()
        return b

    def if_none(self, hid):
        board = None
        while board is None:
            board = self.random_board(hid)
        return board

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            print("-" * 20)
            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
