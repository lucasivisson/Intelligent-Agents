from typing import List


class World():
    def __init__(self, width: int, height: int, obstacles: List[List[int]]) -> None:
        self.width = width
        self.height = height
        self.environment: List[List[str]] = [
            ['0' for _ in range(width)] for _ in range(height)]

        # Fill obstacles with '#'
        for row, col in obstacles:
            if col < self.width and row < self.height:
                self.environment[row][col] = '#'

    def generateDirt(self, cols: List, rows: List) -> None:
        # Fill cols with 1
        for col in cols:
            if 0 < col < self.width:  # verify if col is inside limits
                for i in range(self.height):
                    if self.environment[i][col] != '#':
                        self.environment[i][col] = '1'

        # Fill rows with 1
        for row in rows:
            if 0 < row < self.height:  # verify if row is inside limits
                for j in range(self.width):
                    if self.environment[row][j] != '#':
                        self.environment[row][j] = '1'
