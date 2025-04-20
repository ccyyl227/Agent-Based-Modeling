import math
from mesa.experimental.cell_space import CellAgent

def get_distance(cell_1, cell_2):
    x1, y1 = cell_1.coordinate
    x2, y2 = cell_2.coordinate
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx**2 + dy**2)

class SugarAgent(CellAgent):
    def __init__(self, model, cell, sugar=0, metabolism=0, vision=0, behavior_type=None):
        super().__init__(model)
        self.cell = cell
        self.sugar = sugar
        self.metabolism = metabolism
        self.vision = vision

        # Ensure that only competitive or cooperative agents are created
        # If behavior_type is not passed in, randomly choose between 'competitive' or 'cooperative'
        if behavior_type is None:
            behavior_type = "competitive" if model.random.random() < 0.5 else "cooperative"  # Randomly choose between the two
            
        self.behavior_type = behavior_type  # Agent behavior type (competitive or cooperative)

        

    def move(self):
        # Get empty cells in line of sight
        possibles = [
            cell
            for cell in self.cell.get_neighborhood(self.vision, include_center=True)
            if cell.is_empty
        ]

        # If no possible empty cells to move to, do nothing
        if not possibles:
            return  # Stay in place

        # Evaluate social comparison
        neighbors = self.cell.get_neighborhood(1, include_center=False)
        neighbor_sugars = [
        agent.sugar for cell in neighbors for agent in cell.agents if isinstance(agent, SugarAgent)
        ]
        # Compute the average sugar value of neighboring agents
        avg_neighbor_sugar = sum(neighbor_sugars) / len(neighbor_sugars) if neighbor_sugars else 0


        # Adjust sugar values based on behavior type
        sugar_values = []
        for cell in possibles:
            base_sugar = cell.sugar
            # Competitive behavior: prefer richer cells if the agent has less sugar than its neighbors
            if self.behavior_type == "competitive":
                if self.sugar < avg_neighbor_sugar:
                    base_sugar += 2  # Increase the attractiveness of richer cells
            # Cooperative behavior: avoid taking too much if the agent has more sugar than its neighbors
            elif self.behavior_type == "cooperative":
                if self.sugar > avg_neighbor_sugar:
                    base_sugar -= 2  # Reduce the attractiveness of cells with higher sugar

            sugar_values.append(base_sugar)
        # Find the cells with the highest sugar value
        max_sugar = max(sugar_values)
        candidates_index = [i for i in range(len(sugar_values)) if math.isclose(sugar_values[i], max_sugar)]
        candidates = [possibles[i] for i in candidates_index]

        # Choose among closest best options
        min_dist = min(get_distance(self.cell, cell) for cell in candidates)
        final_candidates = [cell for cell in candidates if math.isclose(get_distance(self.cell, cell), min_dist, rel_tol=1e-2)]
        
        self.move_to(self.random.choice(final_candidates))

    def gather_and_eat(self):
        gather_amount = self.cell.sugar  # Default to taking all sugar
        # Modify behavior for cooperative agents
        if self.behavior_type == "cooperative":
            # Get all neighboring cells within vision=1 (adjacent cells)
            neighbors = self.cell.get_neighborhood(1, include_center=False)
            # Gather sugar values of neighboring agents
            neighbor_sugars = [
                agent.sugar for cell in neighbors for agent in cell.agents if isinstance(agent, SugarAgent)
            ]
            # Compute average sugar of neighbors (avoid division by zero)
            avg_neighbor_sugar = sum(neighbor_sugars) / len(neighbor_sugars) if neighbor_sugars else 0

            # Take only half if agent already has more sugar than neighbors
            if self.sugar > avg_neighbor_sugar:
                gather_amount = self.cell.sugar / 2

        self.sugar += gather_amount
        self.cell.sugar -= gather_amount
        self.sugar -= self.metabolism


    def see_if_die(self):
        if self.sugar <= 0:
            self.remove()
