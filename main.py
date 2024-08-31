from World import World

if __name__ == "__main__":
    # example
    # create and 5x4 world with obstacles on 1,1 and 3,4 position
    world = World(5, 5, [[1, 1], [3, 4]])
    # Fill cols 0, 1 and line 2 with dirt
    world.generateDirt(cols=[0, 1], rows=[2])

    # Print result matrix
    for linha in world.environment:
        print(linha)
