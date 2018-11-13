import utils


class Environment:

    def __init__(self, statement, target):
        self.field = statement
        self.zero_index = self.__find2dindex(statement, 0)
        self.finish = target
        self.n = len(statement)
        self.pos_state = self.__generate_pos_state(statement)
        self.pos_target = self.__generate_pos_state(target)
        self.was_dict = {}

    def __str__(self):
        str_repr = str(self.field).replace('], ', '\n')
        str_repr = str_repr.replace('[', '').replace(']', '').replace(',', '')
        return str_repr

    def get_actions(self):
        actions = []
        actions.append(self.go_left) if not self.zero_index[1] == 0 and not self.__was('left') else None
        actions.append(self.go_right) if not self.zero_index[1] == self.n - 1 and not self.__was('right') else None
        actions.append(self.go_up) if not self.zero_index[0] == 0 and not self.__was('up') else None
        actions.append(self.go_down) if not self.zero_index[0] == self.n - 1 and not self.__was('down') else None
        return actions

    def get_scores(self):
        scores = []
        scores.append(self.score_go_left()) if not self.zero_index[1] == 0 and not self.__was('left') else None
        scores.append(self.score_go_right()) if not self.zero_index[1] == self.n - 1 and not self.__was('right') else None
        scores.append(self.score_go_up()) if not self.zero_index[0] == 0 and not self.__was('up') else None
        scores.append(self.score_go_down()) if not self.zero_index[0] == self.n - 1 and not self.__was('down') else None
        return scores

    @utils.parse_zero_index
    def go_left(self, x, y):
        self.pos_state[self.field[x][y - 1]] = x, y
        self.pos_state[0] = x, y - 1
        self.field[x][y], self.field[x][y - 1] = self.field[x][y - 1], self.field[x][y]
        return x, y - 1

    @utils.parse_zero_index
    def go_right(self, x, y):
        self.pos_state[self.field[x][y + 1]] = x, y
        self.pos_state[0] = x, y + 1
        self.field[x][y], self.field[x][y + 1] = self.field[x][y + 1], self.field[x][y]
        return x, y + 1

    @utils.parse_zero_index
    def go_up(self, x, y):
        self.pos_state[self.field[x - 1][y]] = x, y
        self.pos_state[0] = x - 1, y
        self.field[x - 1][y], self.field[x][y] = self.field[x][y], self.field[x - 1][y]
        return x - 1, y

    @utils.parse_zero_index
    def go_down(self, x, y):
        self.pos_state[self.field[x + 1][y]] = x, y
        self.pos_state[0] = x + 1, y
        self.field[x + 1][y], self.field[x][y] = self.field[x][y], self.field[x + 1][y]
        return x + 1, y

    def score_go_left(self):
        self.go_left()
        score = self.__distance_l1()
        self.go_right()
        return score

    def score_go_right(self):
        self.go_right()
        score = self.__distance_l1()
        self.go_left()
        return score

    def score_go_up(self):
        self.go_up()
        score = self.__distance_l1()
        self.go_down()
        return score

    def score_go_down(self):
        self.go_down()
        score = self.__distance_l1()
        self.go_up()
        return score

    def loss(self, flag=False):
        return self.__distance_l1(flag)

    def remind(self):
        self.was_dict[self.flatten()] = True

    def get_anti_func(self, func):
        if func == self.go_left:
            return self.go_right
        elif func == self.go_right:
            return self.go_left
        elif func == self.go_up:
            return self.go_down
        else:
            return self.go_up

    @staticmethod
    def __generate_pos_state(statement):
        new_dict = {}
        for i, row in enumerate(statement):
            for j, elem in enumerate(row):
                new_dict[elem] = (i, j)
        return new_dict

    @staticmethod
    def __find2dindex(arr2d, value):
        point = (None, None)
        for i, arr1d in enumerate(arr2d):
            for j, elem in enumerate(arr1d):
                if elem == value:
                    point = (i, j)
        return point

    def __was(self, side):
        if side == 'left':
            self.go_left()
            key = self.flatten()
            self.go_right()
        elif side == 'right':
            self.go_right()
            key = self.flatten()
            self.go_left()
        elif side == 'up':
            self.go_up()
            key = self.flatten()
            self.go_down()
        else:
            self.go_down()
            key = self.flatten()
            self.go_up()
        return self.was_dict.get(key)

    def flatten(self):
        key = tuple(num for row in self.field for num in row)
        return key

    def __distance_l1(self, flag=False):
        loss = 0
        for key in self.pos_state.keys():
            if flag:
                print(key, ': ', self.pos_state[key], self.pos_target[key])
            points = self.pos_state[key], self.pos_target[key]
            loss += abs(points[0][0] - points[1][0]) + abs(points[0][1] - points[1][1])
        return loss
