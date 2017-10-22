

class AntColony(object):
    def __init__(self, num_ants, iterations, pher, a, b, decay):
        self.num_ants = num_ants
        self.iterations = iterations
        self.initial_pheromone = pher
        self.pheromone_concentration = a
        self.function_quality = b
        self.decay_factor = decay

    def update_pheromone(self):
        return

    def run(self):
        # Inicializa τij (igualmente para cada aresta)
        # Distribui cada uma das k formigas em um nó selecionado aleatoriamente

        for i in range(self.iterations):
            for j in range(self.num_ants):
                # Constrói uma solução aplicando uma regra de transição
                # probabilística (e-1) vezes // e é o número de arestas do
                # grafo

                # Avalia o custo de cada solução construída
                # solution.eval()

                # update best solution
                1

            self.update_pheromone()
