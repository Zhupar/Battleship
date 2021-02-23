import exceptions


class Dot:
    dots = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
            (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
            (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6),
            (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),
            (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),
            (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


class Ship:
    def __init__(self, head, ship_len, direction):
        self.ship_len = ship_len
        self.head = head
        self.direction = direction
        self.lives = ship_len
        self.s_dots = [self.head]

    @property
    def ship_dots(self):
        cur_x = self.head.x
        cur_y = self.head.y
        for i in range(1, self.ship_len):
            if self.direction == 0:
                cur_x += 1
                self.s_dots.append(Dot(cur_x, cur_y))
            elif self.direction == 1:
                cur_y += 1
                self.s_dots.append(Dot(cur_x, cur_y))
        return self.s_dots

    def shooten(self, shot):
        return shot in self.s_dots


class Board:
    def __init__(self, hid=False):
        self.board = [
            ['  ', '1', '2', '3', '4', '5', '6'],
            ['1 ', 'O', 'O', 'O', 'O', 'O', 'O'],
            ['2 ', 'O', 'O', 'O', 'O', 'O', 'O'],
            ['3 ', 'O', 'O', 'O', 'O', 'O', 'O'],
            ['4 ', 'O', 'O', 'O', 'O', 'O', 'O'],
            ['5 ', 'O', 'O', 'O', 'O', 'O', 'O'],
            ['6 ', 'O', 'O', 'O', 'O', 'O', 'O']
        ]
        self.hid = hid
        self.count = 0
        self.busy = []
        self.ships = []
        self.ships_d = []

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.ship_dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if (cur.x, cur.y) in Dot.dots and (cur.x, cur.y) not in self.busy:
                    if verb:
                        self.board[cur.x][cur.y] = "."
                    self.busy.append((cur.x, cur.y))


    def add_ship(self, ship):
        for dot in ship.ship_dots:
            if (dot.x, dot.y) not in Dot.dots or (dot.x, dot.y) in self.busy:
                raise exceptions.BoardWrongShipException()
        for dot in ship.ship_dots:
            self.board[dot.x][dot.y] = "■"
            self.busy.append((dot.x, dot.y))
            self.ships_d.append((dot.x, dot.y))
        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if (d.x, d.y) not in Dot.dots:
            print((d.x, d.y))
            raise exceptions.BoardOutException
        if (d.x, d.y) in self.busy:
            raise exceptions.BoardUsedException()

        self.busy.append((d.x, d.y))

        for ship in self.ships:
            if d in ship.ship_dots:
                ship.lives -= 1
                self.board[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.board[d.x][d.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []

    def __str__(self):
        board = ''
        for line in self.board:
            board += '|'.join(line) + '\n'
        if self.hid:
            board = board.replace('■', 'O')
        return board


