from World import World
from ModelReactiveAgent import ModelReactiveAgent
from SimpleReactiveAgent import SimpleReactiveAgent
import threading
import copy

def run_simulation(world_size, dirt_configs, obstacle_configs, agent_positions):
    # Listas para armazenar as pontuações de cada configuração
    modelReactiveAgent_scores_measure_1 = []
    modelReactiveAgent_scores_measure_2 = []
    simpleReactiveAgent_scores_measure_1 = []
    simpleReactiveAgent_scores_measure_2 = []


    # Executa o simulador para cada configuração
    for i, (dirt_config, obstacle_config, agent_position) in enumerate(zip(dirt_configs, obstacle_configs, agent_positions)):
        # Cria o mundo com obstáculos
        world = World(world_size[0], world_size[1], obstacle_config)
        world.generateDirt(cols=dirt_config['cols'], rows=dirt_config['rows'])

        worldCleanedBySimpleAgent = copy.deepcopy(world)
        worldCleanedByReactiveAgent = copy.deepcopy(world)

        print(f"\n# Simulação {i+1} - Mundo antes da limpeza:\n")
        for linha in world.environment:
            print(linha)
        print("\n##############################\n")

        # Cria o agente reativo simples no mundo com a posição inicial especificada em
        # threads separadas para que o agente reativo simples possa ser desligado após 2 segundos
        simpleReactiveAgent = SimpleReactiveAgent(worldCleanedBySimpleAgent, agent_position)
        cleaning_thread = threading.Thread(target=simpleReactiveAgent.startCleaning)
        cleaning_thread.start()

        simpleReactiveAgent.stopCleaning()
        cleaning_thread.join()

        # Cria o agente reativo no mundo com a posição inicial especificada
        modelReactiveAgent = ModelReactiveAgent(worldCleanedByReactiveAgent, agent_position)
        modelReactiveAgent.startCleaning()

        # Registra as pontuações após a limpeza
        simpleReactiveAgent_scores_measure_1.append(simpleReactiveAgent.score_measure_1)
        simpleReactiveAgent_scores_measure_2.append(simpleReactiveAgent.score_measure_2)

        modelReactiveAgent_scores_measure_1.append(modelReactiveAgent.score_measure_1)
        modelReactiveAgent_scores_measure_2.append(modelReactiveAgent.score_measure_2)

        print(f"\n# Simulação {i+1} - Mundo após a limpeza (agente reativo simples):\n")
        for linha in worldCleanedBySimpleAgent.environment:
            print(linha)
        print("\n##############################\n")

        print(f"\n# Simulação {i+1} - Mundo após a limpeza (Agente reativo baseado em modelo):\n")
        for linha in worldCleanedByReactiveAgent.environment:
            print(linha)
        print("\n##############################\n")
    
        # Mostra as pontuações de cada simulação
        print(f"Simulação {i+1} (Agente reativo simples) - Pontuação Medida 1: {simpleReactiveAgent.score_measure_1}")
        print(f"Simulação {i+1} (Agente reativo simples) - Pontuação Medida 2: {simpleReactiveAgent.score_measure_2}")
        print("\n##############################\n")
        print(f"Simulação {i+1} (Agente reativo baseado em modelo) - Pontuação Medida 1: {modelReactiveAgent.score_measure_1}")
        print(f"Simulação {i+1} (Agente reativo baseado em modelo) - Pontuação Medida 2: {modelReactiveAgent.score_measure_2}")
        print("\n##############################\n")

    # Calcula as pontuações médias
    simpleReactiveAgent_avg_score_measure_1 = sum(simpleReactiveAgent_scores_measure_1) / len(simpleReactiveAgent_scores_measure_1)
    simpleReactiveAgent_avg_score_measure_2 = sum(simpleReactiveAgent_scores_measure_2) / len(simpleReactiveAgent_scores_measure_2)
    modelReactiveAgent_avg_score_measure_1 = sum(modelReactiveAgent_scores_measure_1) / len(modelReactiveAgent_scores_measure_1)
    modelReactiveAgent_avg_score_measure_2 = sum(modelReactiveAgent_scores_measure_2) / len(modelReactiveAgent_scores_measure_2)
    print(f"\nResultados finais:")
    print(f"Pontuação média Medida 1 (Agente reativo simples): {simpleReactiveAgent_avg_score_measure_1}")
    print(f"Pontuação média Medida 2 (Agente reativo simples): : {simpleReactiveAgent_avg_score_measure_2}")
    print("\n##############################\n")
    print(f"Pontuação média Medida 1 (Agente Agente reativo baseado em modelo): {modelReactiveAgent_avg_score_measure_1}")
    print(f"Pontuação média Medida 2 (Agente Agente reativo baseado em modelo): : {modelReactiveAgent_avg_score_measure_2}")

if __name__ == "__main__":
    # Tamanho do mundo
    world_size = (5, 5)

    # Configurações de sujeira e obstáculos para diferentes simulações
    dirt_configs = [
        {'cols': [0, 1], 'rows': [2]},  # Configuração 1
        {'cols': [0, 3], 'rows': [1, 4]},  # Configuração 2
        {'cols': [1], 'rows': [0, 3, 4]},  # Configuração 3
    ]

    obstacle_configs = [
        [[1, 1], [3, 4]],  # Obstáculos para simulação 1
        [[2, 2], [4, 1]],  # Obstáculos para simulação 2
        [[0, 4], [2, 3]],  # Obstáculos para simulação 3
    ]

    # Posições iniciais dos agentes para diferentes simulações
    agent_positions = [
        [0, 0],  # Posição do agente na simulação 1
        [4, 4],  # Posição do agente na simulação 2
        [2, 2],  # Posição do agente na simulação 3
    ]

    # Executar o simulador
    run_simulation(world_size, dirt_configs, obstacle_configs, agent_positions)
