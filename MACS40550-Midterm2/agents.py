from mesa import Agent
import random

class SupportAgent(Agent):
    def __init__(self, unique_id, model, strategy_preferences=None, adaptivity=None):
        super().__init__(unique_id, model)
        self.depression = random.uniform(20, 80)
        self.fatigue = 0
        self.adaptivity = adaptivity if adaptivity is not None else random.uniform(0, 1)

        # Strategy preference distribution: must sum to 1
        if strategy_preferences is not None:
            self.strategy_preferences = strategy_preferences
        else:
            self.strategy_preferences = { #change initial strategy distribution
                "affirmation": 0.25,
                "empathy": 0.25,
                "sarcasm": 0.25,
                "dismissal": 0.25
            }

    def step(self):
        partner = self.random.choice(self.model.schedule.agents)
        if partner.unique_id == self.unique_id:
            return  # skip self-interaction

        # Determine which strategy to use based on adaptivity
        if self.adaptivity > 0.5:
            # High adaptivity: align to partner's depression level
            if partner.depression > 60:
                strategy = self.weighted_choice({"affirmation": 0.5, "empathy": 0.4, "sarcasm": 0.05, "dismissal": 0.05})
            elif partner.depression < 30:
                strategy = self.weighted_choice({"sarcasm": 0.4, "dismissal": 0.4, "affirmation": 0.1, "empathy": 0.1})
            else:
                strategy = self.weighted_choice(self.strategy_preferences)
        else:
            # Low adaptivity: fixed strategy preference
            strategy = self.weighted_choice(self.strategy_preferences)

        # Apply effect
        self.apply_strategy_effect(strategy, partner)

    def apply_strategy_effect(self, strategy, partner):
        if strategy == "affirmation":
            partner.depression = max(0, partner.depression - 10)
            self.fatigue += 5
        elif strategy == "empathy":
            partner.depression = max(0, partner.depression - 7)
            self.fatigue += 4
        elif strategy == "sarcasm":
            partner.depression = min(100, partner.depression + 7)
            self.fatigue += 2
        elif strategy == "dismissal":
            partner.depression = min(100, partner.depression + 5)
            self.fatigue += 1

    def weighted_choice(self, weights):
        total = sum(weights.values()) # Get total weight (should be 1 if normalized)
        r = random.uniform(0, total) # Pick a random number between 0 and total
        upto = 0
        for k, w in weights.items():
            if upto + w >= r:
                return k # Return the strategy where the random number lands
            upto += w