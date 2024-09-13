from World import World
from typing import List
import random
import time

class SimpleReactiveAgent():
    def __init__(self, world: World, position: List = None) -> None:
        self.world = world
        self.on = False
        if position != None and position[0] <= world.width and position[1] <= world.height and world.environment[position[0]][position[1]] != '#':
            self.position = position
        else:
            self.position = [random.randint(
                0, world.width), random.randint(0, world.height)]
        self.score_measure_1 = 0  # Medida 1: Pontos para quadrados limpos
        self.score_measure_2 = 0  # Medida 2: Pontos para quadrados limpos e penalização por movimento
        self.moves = 0  # Contabiliza os movimentos para a Medida 2

    def isValidPosition(self, position: List) -> bool:
        return 0 <= position[0] < self.world.width and 0 <= position[1] < self.world.height

    def move(self, position: List):
        if self.isValidPosition(position):
            self.position = position
            self.score_measure_2 -= 1  # Penaliza um ponto para cada movimento
            self.moves += 1  # Incrementa o número de movimentos para a Medida 2

    def clear(self):
        if self.world.environment[self.position[0]][self.position[1]] == "1":
            self.world.environment[self.position[0]][self.position[1]] = '0'
            self.score_measure_1 += 1  # Medida 1: Pontos por limpar
            self.score_measure_2 += 1  # Medida 2: Pontos por limpar

    # Funções de movimento...
    def moveLeft(self):
        self.move([self.position[0], self.position[1] - 1])

    def moveUpLeft(self):
        self.move([self.position[0] - 1, self.position[1] - 1])

    def moveUp(self):
        self.move([self.position[0] - 1, self.position[1]])

    def moveUpRight(self):
        self.move([self.position[0] - 1, self.position[1] + 1])

    def moveRight(self):
        self.move([self.position[0], self.position[1] + 1])

    def moveDownRight(self):
        self.move([self.position[0] + 1, self.position[1] + 1])

    def moveDown(self):
        self.move([self.position[0] + 1, self.position[1]])

    def moveDownLeft(self):
        self.move([self.position[0] + 1, self.position[1] - 1])

    def getLeft(self):
        leftPosition = [self.position[0], self.position[1] - 1]
        return self.world.environment[leftPosition[0]][leftPosition[1]] if self.isValidPosition(leftPosition) else None

    def getRight(self):
        rightPosition = [self.position[0], self.position[1] + 1]
        return self.world.environment[rightPosition[0]][rightPosition[1]] if self.isValidPosition(rightPosition) else None

    def getUpLeft(self):
        upLeftPosition = [self.position[0] - 1, self.position[1] - 1]
        return self.world.environment[upLeftPosition[0]][upLeftPosition[1]] if self.isValidPosition(upLeftPosition) else None

    def getUpRight(self):
        upRightPosition = [self.position[0] - 1, self.position[1] + 1]
        return self.world.environment[upRightPosition[0]][upRightPosition[1]] if self.isValidPosition(upRightPosition) else None

    def getUp(self):
        upPosition = [self.position[0] - 1, self.position[1]]
        return self.world.environment[upPosition[0]][upPosition[1]] if self.isValidPosition(upPosition) else None

    def getDown(self):
        downPosition = [self.position[0] + 1, self.position[1]]
        return self.world.environment[downPosition[0]][downPosition[1]] if self.isValidPosition(downPosition) else None

    def getDownLeft(self):
        downLeftPosition = [self.position[0] + 1, self.position[1] - 1]
        return self.world.environment[downLeftPosition[0]][downLeftPosition[1]] if self.isValidPosition(downLeftPosition) else None

    def getDownRight(self):
        downRightPosition = [self.position[0] + 1, self.position[1] + 1]
        return self.world.environment[downRightPosition[0]][downRightPosition[1]] if self.isValidPosition(downRightPosition) else None

    def getFreeCleanPosition(self):
        available_positions = []
        if self.getLeft() == "0":
            available_positions.append(self.moveLeft)
        if self.getUpLeft() == "0":
            available_positions.append(self.moveUpLeft)
        if self.getUp() == "0":
            available_positions.append(self.moveUp)
        if self.getUpRight() == "0":
            available_positions.append(self.moveUpRight)
        if self.getRight() == "0":
            available_positions.append(self.moveRight)
        if self.getDownRight() == "0":
            available_positions.append(self.moveDownRight)
        if self.getDown() == "0":
            available_positions.append(self.moveDown)
        if self.getDownLeft() == "0":
            available_positions.append(self.moveDownLeft)

        if available_positions:
            random.choice(available_positions)()
        else:
            self.on = False  # Sem espaço livre para mover, desligar dispositivo

    def analyzeAround(self):
        if self.getLeft() == "1":
            return self.moveLeft()
        if self.getUpLeft() == "1":
            return self.moveUpLeft()
        if self.getUp() == "1":
            return self.moveUp()
        if self.getUpRight() == "1":
            return self.moveUpRight()
        if self.getRight() == "1":
            return self.moveRight()
        if self.getDownRight() == "1":
            return self.moveDownRight()
        if self.getDown() == "1":
            return self.moveDown()
        if self.getDownLeft() == "1":
            return self.moveDownLeft()

    def startCleaning(self):
        self.on = True
        self.clear()  # Limpa a posição inicial
        while self.on:
            self.analyzeAround()
            self.clear()
            self.getFreeCleanPosition()

        # Retornar pontuações ao final do processo de limpeza
        return {
            'score_measure_1': self.score_measure_1,
            'score_measure_2': self.score_measure_2
        }

    def stopCleaning(self):
        self.on = False
