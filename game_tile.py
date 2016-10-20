

class GameTile(object):
    def __init__(self, column, row):
        self.row = row
        self.column = column
        self.bar = None

    def __lt__(self, other):
        return False