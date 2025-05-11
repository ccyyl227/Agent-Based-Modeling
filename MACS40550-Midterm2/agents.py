from mesa import Agent

class SupportAgent(Agent):
    def __init__(self, unique_id, model, depression_level):
        super().__init__(unique_id, model)
        self.depression_level = depression_level
        self.supportiveness = 1.0  # 0 to 1
        self.fatigue_level = 0.0   # 0 to 1
        self.memory = []          # Stores past interactions (simplified for now)

    def step(self):
        # Post if depressed enough
        if self.depression_level > 30:
            self.broadcast_post()

        # Respond to neighbor posts
        neighbors = self.model.grid.get_neighbors(self.pos, include_center=False)
        for neighbor_id in neighbors:
            neighbor = self.model.grid.get_cell_list_contents([neighbor_id])[0]
            if neighbor.depression_level > 30:
                self.consider_response(neighbor)

    def broadcast_post(self):
        # Placeholder function
        pass

    def consider_response(self, neighbor):
        if self.supportiveness <= 0:
            return  # Too fatigued to respond

        strategy = self.select_strategy(neighbor.depression_level)
        self.apply_strategy(neighbor, strategy)
        self.update_fatigue(strategy)

    def select_strategy(self, target_depression):
        # Simplified decision rule for now
        if self.fatigue_level > 0.7:
            return "sarcasm" if self.random.random() < 0.5 else "dismissal"

        if target_depression < 40:
            return "affirmation"
        elif target_depression <= 70:
            return "empathy"
        else:
            return "empathy"  # Fallback for high depression

    def apply_strategy(self, neighbor, strategy):
        if strategy == "affirmation":
            change = -5
        elif strategy == "empathy":
            change = -10
        elif strategy == "dismissal":
            change = 5
        elif strategy == "sarcasm":
            change = 10
        else:
            change = 0

        neighbor.depression_level = max(0, min(100, neighbor.depression_level + change))
        # Log the interaction
        self.memory.append((neighbor.unique_id, strategy, change))

    def update_fatigue(self, strategy):
        if strategy == "empathy":
            self.fatigue_level = min(1.0, self.fatigue_level + 0.1)
        elif strategy == "affirmation":
            self.fatigue_level = min(1.0, self.fatigue_level + 0.02)
        elif strategy in ["dismissal", "sarcasm"]:
            self.fatigue_level = max(0.0, self.fatigue_level - 0.05)

        # Adjust supportiveness accordingly
        self.supportiveness = max(0.0, 1.0 - self.fatigue_level)
