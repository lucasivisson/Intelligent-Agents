from typing import List


class World():
    def __init__(self, width: int, height: int, obstacles: List[List[int]]) -> None:
        self.width = width
        self.height = height
        self.environment: List[List[str]] = [
            ['0' for _ in range(width)] for _ in range(height)]

        # Preencher obstáculos com '#'
        for row, col in obstacles:
            if col < self.width and row < self.height:
                self.environment[row][col] = '#'

    def generateDirt(self, cols: List, rows: List) -> None:
        # Preencher colunas com 1
        for col in cols:
            if 0 < col < self.width:  # verifica se coluna está dentro dos limites
                for row in range(self.height):
                    if self.environment[row][col] != '#':
                        self.environment[row][col] = '1'

        # Preenche linhas com 1
        for row in rows:
            if 0 < row < self.height:  # verfica se linha está dentro dos limites
                for col in range(self.width):
                    if self.environment[row][col] != '#':
                        self.environment[row][col] = '1'
