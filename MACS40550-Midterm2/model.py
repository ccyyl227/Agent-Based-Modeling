from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import SocialSupportAgent
import random

class SocialSupportModel(Model):
    """
    A model that simulates the interactions between agents who provide emotional support to each other.
    """
    def __init__(self, num_agents, width, height):
        """
        Initialize the simulation model with a given number of agents.
        :param num_agents: Number of agents to simulate.
        :param width: Width of the grid.
        :param height: Height of the grid.
        """
        self.num_agents = num_agents
        self.width = width
        self.height = height
        self.schedule = RandomActivation(self)

        # Create a grid for agent movement
        self.grid = MultiGrid(self.width, self.height, True)

        # Create agents
        for i in range(self.num_agents):
            depression_level = random.randint(0, 100)
            fatigue_level = 0
            supportiveness = random.uniform(0.3, 1)
            strategy_preference = [0.4, 0.3, 0.2, 0.1]
            adaptivity = random.uniform(0, 1)

            a = SocialSupportAgent(i, self, depression_level, fatigue_level, supportiveness, strategy_preference, adaptivity)
            self.schedule.add(a)

            # Add the agent to a random grid location
            x = self.random.randint(0, self.grid.width - 1)
            y = self.random.randint(0, self.grid.height - 1)
            self.grid.place_agent(a, (x, y))

    def step(self):
        """
        Advance the model by one step, where each agent takes a step.
        """
        self.schedule.step()

    def get_agent_data(self):
        """
        Get the data of all agents for analysis or visualization.
        """
        data = []
        for agent in self.schedule.agents:
            data.append({
                'id': agent.unique_id,
                'depression_level': agent.depression_level,
                'fatigue_level': agent.fatigue_level
            })
        return data

