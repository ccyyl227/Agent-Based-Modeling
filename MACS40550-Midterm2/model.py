from mesa import Model
from mesa.time import RandomActivation
from agent import SupportAgent

class SupportModel(Model):
    def __init__(self, N=100, strategy_distribution=None, adaptivity_level=None): #change adaptivity level
        self.num_agents = N
        self.schedule = RandomActivation(self)

        for i in range(self.num_agents):
            strategy_pref = strategy_distribution if strategy_distribution else None
            adaptivity = adaptivity_level if adaptivity_level is not None else None
            agent = SupportAgent(i, self, strategy_preferences=strategy_pref, adaptivity=adaptivity)
            self.schedule.add(agent)

    def step(self):
        self.schedule.step()