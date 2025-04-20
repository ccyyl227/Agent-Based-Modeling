from pathlib import Path
import numpy as np
import mesa
from agents import SugarAgent

from mesa.experimental.cell_space import OrthogonalVonNeumannGrid
from mesa.experimental.cell_space.property_layer import PropertyLayer

class SugarScapeModel(mesa.Model):
    def calc_gini(self):
        agent_sugars = [a.sugar for a in self.agents]
        sorted_sugars = sorted(agent_sugars)
        n = len(sorted_sugars)
        x = sum(el * (n - ind) for ind, el in enumerate(sorted_sugars)) / (n * sum(sorted_sugars))
        return 1 + (1 / n) - 2 * x

    def __init__(
        self,
        width=50,
        height=50,
        initial_population=200,
        endowment_min=25,
        endowment_max=50,
        metabolism_min=1,
        metabolism_max=5,
        vision_min=1,
        vision_max=5,
        seed=None
    ):
        super().__init__(seed=seed)
        self.width = width
        self.height = height
        self.running = True

        self.grid = OrthogonalVonNeumannGrid(
            (self.width, self.height), torus=False, random=self.random
        )

        self.datacollector = mesa.DataCollector(
            model_reporters={"Gini": self.calc_gini}
        )

        self.sugar_distribution = np.genfromtxt(Path(__file__).parent / "sugar-map.txt")
        self.grid.add_property_layer(
            PropertyLayer.from_data("sugar", self.sugar_distribution)
        )

        # Randomly assign behavior types
        behavior_types = self.random.choices(
            ["competitive", "cooperative"],
            k=initial_population
        )

        # Create agents
        SugarAgent.create_agents(
            self,
            initial_population,
            self.random.choices(self.grid.all_cells.cells, k=initial_population),
            sugar=self.rng.integers(endowment_min, endowment_max, (initial_population,), endpoint=True),
            metabolism=self.rng.integers(metabolism_min, metabolism_max, (initial_population,), endpoint=True),
            vision=self.rng.integers(vision_min, vision_max, (initial_population,), endpoint=True),
            behavior_type=behavior_types  # NEW 
        )

        self.datacollector.collect(self)

    def step(self):
        self.grid.sugar.data = np.minimum(
            self.grid.sugar.data + 1, self.sugar_distribution
        )
        self.agents.shuffle_do("move")
        self.agents.shuffle_do("gather_and_eat")
        self.agents.shuffle_do("see_if_die")
        self.datacollector.collect(self)
