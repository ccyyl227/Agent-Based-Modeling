from mesa import Agent
import random

class SocialSupportAgent(Agent):
    """
    A social support agent that interacts with other agents and provides emotional support
    based on its depression level, fatigue level, supportiveness, and strategy preference.
    """
    def __init__(self, unique_id, model, depression_level, fatigue_level, supportiveness, strategy_preference, adaptivity):
        """
        Initialize the agent with attributes.
        :param unique_id: Unique identifier for the agent.
        :param model: The model to which the agent belongs.
        :param depression_level: Initial depression level of the agent (0 to 100).
        :param fatigue_level: Fatigue level of the agent (0 to 100).
        :param supportiveness: Probability of offering support based on emotional availability.
        :param strategy_preference: List of strategy preferences for the agent.
        :param adaptivity: How adaptable the agent is to others' depression levels (0 to 1).
        """
        super().__init__(unique_id, model)
        self.depression_level = depression_level
        self.fatigue_level = fatigue_level
        self.supportiveness = supportiveness
        self.strategy_preference = strategy_preference  # Probability distribution over strategies
        self.adaptivity = adaptivity  # Adaptability based on depression levels of others

    def step(self):
        """
        Each agent takes a step in the simulation.
        The agent interacts with a random other agent and may provide support.
        """
        other_agent = self.random.choice(self.model.schedule.agents)
        if self != other_agent:
            self.interact(other_agent)

    def interact(self, other_agent):
        """
        Simulate an interaction where one agent provides emotional support to another.
        :param other_agent: The agent receiving support.
        """
        if random.random() < self.supportiveness and self.fatigue_level < 100:
            strategy = self.choose_strategy(other_agent)
            self.respond(strategy, other_agent)
            self.fatigue_level += 10  # Fatigue increases after each interaction
        else:
            print(f"Agent {self.unique_id} chose not to respond due to fatigue or low supportiveness.")

    def choose_strategy(self, recipient):
        """
        Choose an emotional support strategy based on the recipient's depression level
        and the agent's adaptivity.
        :param recipient: The agent to whom support is being provided.
        :return: Chosen strategy ('affirmation', 'empathy', 'sarcasm', 'dismissal').
        """
        if self.adaptivity > 0.5:
            # If the agent is highly adaptable, choose strategy based on recipient's depression level
            if recipient.depression_level > 70:
                return 'empathy'  # More empathetic responses to highly depressed individuals
            else:
                return 'affirmation'  # Affirmative response to less depressed individuals
        else:
            # Random choice based on the agent's preferences
            return random.choices(['affirmation', 'empathy]()
