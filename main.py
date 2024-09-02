from World import World
from SimpleReactiveAgent import SimpleReactiveAgent
import time
import threading

if __name__ == "__main__":
    # example
    # create and 5x4 world with obstacles on 1,1 and 3,4 position
    world = World(5, 5, [[1, 1], [3, 4]])
    # Fill cols 0, 1 and line 2 with dirt
    world.generateDirt(cols=[0, 1], rows=[2])

    # Print result matrix
    print("\n")
    print("# World before cleaning (simple agent):\n")
    for linha in world.environment:
        print(linha)
    print("\n##############################\n")

    agent = SimpleReactiveAgent(world, [0, 0])

    cleaning_thread = threading.Thread(target=agent.startCleaning)
    cleaning_thread.start()

    time.sleep(2)
    print("\n")
    print("# After 2 seconds we turn off the agent:\n")
    print("\n##############################\n")

    agent.stopCleaning()
    cleaning_thread.join()

    # Print world cleaned
    print("# World after cleaning (simple agent):\n")
    for linha in world.environment:
        print(linha)
    print("\n##############################\n")
