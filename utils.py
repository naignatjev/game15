import functools


def parse_zero_index(method):
    @functools.wraps(method)
    def wrapper(self):
        x, y = self.zero_index
        self.zero_index = method(self, x, y)
    return wrapper


def input_matrix(n=4, file=None):
    if file:
        with open(file) as f:
            blob = f.read()
        print(blob)
        matrix = [[int(num) for num in string.split(' ')] for string in blob.split('\n')]
    else:
        matrix = [[int(num) for num in input().split(' ')] for _ in range(n)]
    return matrix
