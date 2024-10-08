from World import World
from typing import List
import random

class ModelReactiveAgent():
    def __init__(self, world: World, position: List = None) -> None:
        self.world = world
        self.on = False
        self.dirtySpots = 0
        self.positionsAlreadyCleaned = []
        # Medida 1: Pontos para quadrados limpos
        self.score_measure_1 = 0  
        # Medida 2: Pontos para quadrados limpos e penalização por movimento
        self.score_measure_2 = 0  
        self.moves = 0  # Contabiliza os movimentos para a Medida 2
        # Inicializando a posição do agente
        if position is not None and position[0] <= world.width and position[1] <= world.height and world.environment[position[0]][position[1]] != '#':
            self.position = position
        else:
            self.position = [random.randint(0, world.width - 1), random.randint(0, world.height - 1)]
            while world.environment[self.position[0]][self.position[1]] == '#':
                self.position = [random.randint(0, world.width - 1), random.randint(0, world.height - 1)]

    def scanArea(self):
        count = 0
        for row in self.world.environment:
            count += row.count("1")
        return count

    def isValidPosition(self, position: List) -> bool:
        return 0 <= position[0] < self.world.width and 0 <= position[1] < self.world.height

    def move(self, position: List):
        if self.isValidPosition(position):
            self.position = position
            self.positionsAlreadyCleaned.append(position)
            self.moves += 1  # Incrementa o número de movimentos para a Medida 2
            self.score_measure_2 -= 1  # Penaliza 1 ponto por movimento para a Medida 2

    def clear(self):
        if self.world.environment[self.position[0]][self.position[1]] == "1":
            self.world.environment[self.position[0]][self.position[1]] = '0'
            self.score_measure_1 += 1  # Incrementa a pontuação da Medida 1 ao limpar um quadrado
            self.dirtySpots -= 1  # Decrementa o número de manchas sujas restantes
            self.score_measure_2 += 1  # Incrementa 1 ponto por quadrado limpo na Medida 2

    # Movimentos do agente
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

    # Métodos para pegar posições adjacentes
    def getLeft(self):
        leftPosition = [self.position[0], self.position[1] - 1]
        return (self.world.environment[leftPosition[0]][leftPosition[1]], leftPosition) if self.isValidPosition(leftPosition) else (None, leftPosition)

    def getRight(self):
        rightPosition = [self.position[0], self.position[1] + 1]
        return (self.world.environment[rightPosition[0]][rightPosition[1]], rightPosition) if self.isValidPosition(rightPosition) else (None, rightPosition)

    def getUpLeft(self):
        upLeftPosition = [self.position[0] - 1, self.position[1] - 1]
        return (self.world.environment[upLeftPosition[0]][upLeftPosition[1]], upLeftPosition) if self.isValidPosition(upLeftPosition) else (None, upLeftPosition)

    def getUpRight(self):
        upRightPosition = [self.position[0] - 1, self.position[1] + 1]
        return (self.world.environment[upRightPosition[0]][upRightPosition[1]], upRightPosition) if self.isValidPosition(upRightPosition) else (None, upRightPosition)

    def getUp(self):
        upPosition = [self.position[0] - 1, self.position[1]]
        return (self.world.environment[upPosition[0]][upPosition[1]], upPosition) if self.isValidPosition(upPosition) else (None, upPosition)

    def getDown(self):
        downPosition = [self.position[0] + 1, self.position[1]]
        return (self.world.environment[downPosition[0]][downPosition[1]], downPosition) if self.isValidPosition(downPosition) else (None, downPosition)

    def getDownLeft(self):
        downLeftPosition = [self.position[0] + 1, self.position[1] - 1]
        return (self.world.environment[downLeftPosition[0]][downLeftPosition[1]], downLeftPosition) if self.isValidPosition(downLeftPosition) else (None, downLeftPosition)

    def getDownRight(self):
        downRightPosition = [self.position[0] + 1, self.position[1] + 1]
        return (self.world.environment[downRightPosition[0]][downRightPosition[1]], downRightPosition) if self.isValidPosition(downRightPosition) else (None, downRightPosition)

    # Métodos para pegar a melhor posição livre para mover
    def getFreeCleanPosition(self):
        availablePositions = []
        
        leftValue, leftPosition = self.getLeft()
        if leftValue == "0":
            availablePositions.append((self.moveLeft, leftPosition))

        upLeftValue, upLeftPosition = self.getUpLeft()
        if upLeftValue == "0":
            availablePositions.append((self.moveUpLeft, upLeftPosition))

        upValue, upPosition = self.getUp()
        if upValue == "0":
            availablePositions.append((self.moveUp, upPosition))

        upRightValue, upRightPosition = self.getUpRight()
        if upRightValue == "0":
            availablePositions.append((self.moveUpRight, upRightPosition))

        rightValue, rightPosition = self.getRight()
        if rightValue == "0":
            availablePositions.append((self.moveRight, rightPosition))

        downRightValue, downRightPosition = self.getDownRight()
        if downRightValue == "0":
            availablePositions.append((self.moveDownRight, downRightPosition))

        downValue, downPosition = self.getDown()
        if downValue == "0":
            availablePositions.append((self.moveDown, downPosition))

        downLeftValue, downLeftPosition = self.getDownLeft()
        if downLeftValue == "0":
            availablePositions.append((self.moveDownLeft, downLeftPosition))

        availablePositions.sort(key=lambda x: x[1] not in self.positionsAlreadyCleaned, reverse=True)

        if availablePositions:
            random.choice(availablePositions)[0]()
        else:
            self.on = False  # Sem espaço livre, desliga o agente

    # Método para começar a limpeza
    def startCleaning(self):
        self.on = True
        self.dirtySpots = self.scanArea()
        print(f"Manchas sujas: {self.dirtySpots}")
        self.clear()
        while self.on and self.dirtySpots > 0:
            self.analyzeAround()
            self.clear()
            self.getFreeCleanPosition()

    def stopCleaning(self):
        self.on = False

    def analyzeAround(self):
        # Análise das posições ao redor
        leftValue, _ = self.getLeft()
        if leftValue == "1":
            return self.moveLeft()
        upLeftValue, _ = self.getUpLeft()
        if upLeftValue == "1":
            return self.moveUpLeft()
        upValue, _ = self.getUp()
        if upValue == "1":
            return self.moveUp()
        upRightValue, _ = self.getUpRight()
        if upRightValue == "1":
            return self.moveUpRight()
        rightValue, _ = self.getRight()
        if rightValue == "1":
            return self.moveRight()
        downRightValue, _ = self.getDownRight()
        if downRightValue == "1":
            return self.moveDownRight()
        downValue, _ = self.getDown()
        if downValue == "1":
            return self.moveDown()
        downLeftValue, _ = self.getDownLeft()
        if downLeftValue == "1":
            return self.moveDownLeft()
