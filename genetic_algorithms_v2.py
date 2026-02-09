from robot import *
import math
import random

nb_robots = 0
debug = False

# Paramètres de l'algorithme génétique
POP_SIZE = 20
ELITE = 4
MUTATION_RATE = 0.1
WEIGHT_MIN, WEIGHT_MAX = -3.0, 3.0
MAX_GENERATIONS = 50  # arrêt automatique

class Robot_player(Robot):
    team_name = "OptimizerGA"
    robot_id = -1

    # État global du GA
    population = None
    fitnesses = None
    current_individual = 0
    current_iteration = 0
    generation = 0

    it_per_evaluation = 400

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a",
                 evaluations=0, it_per_evaluation=0):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1

        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0

        if it_per_evaluation > 0:
            self.it_per_evaluation = it_per_evaluation

        # Initialisation du GA (une seule fois)
        if Robot_player.population is None:
            Robot_player.population = [
                [random.uniform(WEIGHT_MIN, WEIGHT_MAX) for _ in range(8)]
                for _ in range(POP_SIZE)
            ]
            Robot_player.fitnesses = [0.0 for _ in range(POP_SIZE)]
            Robot_player.current_individual = 0
            Robot_player.current_iteration = 0
            Robot_player.generation = 0
            print("Init GA population")

        # Paramètres de l'individu courant
        self.param = Robot_player.population[Robot_player.current_individual]
        self.fitness_current = 0.0

        # Variables pour la fitness exploration
        self.prev_x = x_0
        self.prev_y = y_0
        self.last_rotation = 0.0
        self.current_rotation = 0.0
        self.turning_counter = 0
        self.sensors_last = None

        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        super().reset()
        self.param = Robot_player.population[Robot_player.current_individual]
        self.fitness_current = 0.0
        self.prev_x = self.x_0
        self.prev_y = self.y_0
        self.turning_counter = 0
        self.last_rotation = 0.0
        self.current_rotation = 0.0

    def evaluate_fitness(self):
        # 1. Distance parcourue
        dx = self.x - self.prev_x
        dy = self.y - self.prev_y
        dist = math.sqrt(dx*dx + dy*dy)
        self.fitness_current += dist

        # 2. Pénalité mur (capteur frontal)
        if self.sensors_last is not None:
            front = self.sensors_last[sensor_front]
            if front > 0.7:
                self.fitness_current -= 0.5 * (front - 0.7)

        # 3. Pénalité rotation excessive (évite les cercles)
        if abs(self.last_rotation) > 0.5:
            self.turning_counter += 1
        else:
            self.turning_counter = 0

        # pénalité croissante avec le temps passé à tourner
        self.fitness_current -= 0.05 * self.turning_counter

        # 4. Bonus si changement de direction (évite les cycles stables)
        if abs(self.current_rotation - self.last_rotation) > 0.3:
            self.fitness_current += 0.2

        # Mise à jour
        self.prev_x = self.x
        self.prev_y = self.y
        self.last_rotation = self.current_rotation

    @staticmethod
    def evolve_population():
        pop = Robot_player.population
        fit = Robot_player.fitnesses

        # Tri par fitness décroissante
        ranked = sorted(zip(pop, fit), key=lambda x: x[1], reverse=True)
        pop_sorted, fit_sorted = zip(*ranked)

        print(f"Generation {Robot_player.generation} best fitness = {fit_sorted[0]:.2f}")
        print("Best params:", pop_sorted[0])

        # Élites
        new_pop = [list(ind) for ind in pop_sorted[:ELITE]]

        # Sélection tournoi
        def select():
            k = 3
            candidates = random.sample(range(POP_SIZE), k)
            best_idx = max(candidates, key=lambda i: fit[i])
            return pop[best_idx]

        # Croisement + mutation
        while len(new_pop) < POP_SIZE:
            p1 = select()
            p2 = select()
            child = []
            for w1, w2 in zip(p1, p2):
                w = w1 if random.random() < 0.5 else w2
                if random.random() < MUTATION_RATE:
                    w += random.uniform(-1.0, 1.0)
                    w = max(WEIGHT_MIN, min(WEIGHT_MAX, w))
                child.append(w)
            new_pop.append(child)

        Robot_player.population = new_pop
        Robot_player.fitnesses = [0.0 for _ in range(POP_SIZE)]
        Robot_player.current_individual = 0
        Robot_player.current_iteration = 0
        Robot_player.generation += 1

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        # Fitness
        self.evaluate_fitness()

        Robot_player.current_iteration += 1

        # Fin d'évaluation d'un individu
        if Robot_player.current_iteration >= self.it_per_evaluation:
            idx = Robot_player.current_individual
            Robot_player.fitnesses[idx] = self.fitness_current

            print(f"Ind {idx} fitness = {self.fitness_current:.2f}")

            Robot_player.current_individual += 1
            Robot_player.current_iteration = 0

            # Fin de génération
            if Robot_player.current_individual >= POP_SIZE:
                Robot_player.evolve_population()

                # Arrêt automatique
                if Robot_player.generation >= MAX_GENERATIONS:
                    print("Training finished.")
                    print("Best params:", Robot_player.population[0])
                    return 0.0, 0.0, True

            return 0.0, 0.0, True

        # Contrôle Braitenberg
        translation = math.tanh(
            self.param[0]
            + self.param[1] * sensors[sensor_front_left]
            + self.param[2] * sensors[sensor_front]
            + self.param[3] * sensors[sensor_front_right]
        )
        rotation = math.tanh(
            self.param[4]
            + self.param[5] * sensors[sensor_front_left]
            + self.param[6] * sensors[sensor_front]
            + self.param[7] * sensors[sensor_front_right]
        )

        # Infos pour la fitness
        self.current_rotation = rotation
        self.sensors_last = sensors

        return translation, rotation, False