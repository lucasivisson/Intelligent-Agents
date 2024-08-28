from World import World

if __name__ == "__main__":
    # example
    world = World(5, 5, [[1, 1], [3, 4]])  # create and 5x4 world
    # Fill cols 0, 1 and line 2 with dirt
    world.generateDirt(cols=[0, 1], rows=[2])

    # Print result matrix
    for linha in world.environment:
        print(linha)
