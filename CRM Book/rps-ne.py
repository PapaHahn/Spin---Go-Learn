import random

class RPSPlayer:
    def __init__(self, num_actions=3, assumed_opponent_strategy=[0.4, 0.3, 0.3]):
        self.NUM_ACTIONS = num_actions
        self.regretSum = [0.0] * self.NUM_ACTIONS
        self.strategy = [0.0] * self.NUM_ACTIONS
        self.strategySum = [0.0] * self.NUM_ACTIONS

        # Falls eine Gegnerstrategie übergeben wird, initialisiere die Strategie
        if assumed_opponent_strategy:
            self.initialize_strategy(assumed_opponent_strategy)

    def initialize_strategy(self, opponent_strategy):
        # Passe die initiale Strategie basierend auf der vermuteten Gegnerstrategie an
        for a in range(self.NUM_ACTIONS):
            self.regretSum[a] = max(opponent_strategy[(a - 1) % self.NUM_ACTIONS] - opponent_strategy[a], 0)

    def getStrategy(self):
        normalizing_sum = 0.0
        for a in range(self.NUM_ACTIONS):
            self.strategy[a] = max(self.regretSum[a], 0)
            normalizing_sum += self.strategy[a]
        
        for a in range(self.NUM_ACTIONS):
            if normalizing_sum > 0:
                self.strategy[a] /= normalizing_sum
            else:
                self.strategy[a] = 1.0 / self.NUM_ACTIONS
            self.strategySum[a] += self.strategy[a]
        return self.strategy

    def getAction(self):
        return random.choices(range(self.NUM_ACTIONS), weights=self.getStrategy())[0]

    def updateRegrets(self, my_action, other_action):
        actionUtility = [0.0] * self.NUM_ACTIONS
        actionUtility[other_action] = 0
        actionUtility[(other_action + 1) % self.NUM_ACTIONS] = 1
        actionUtility[(other_action - 1 + self.NUM_ACTIONS) % self.NUM_ACTIONS] = -1

        for a in range(self.NUM_ACTIONS):
            self.regretSum[a] += actionUtility[a] - actionUtility[my_action]

    def getAverageStrategy(self):
        avg_strategy = [0.0] * self.NUM_ACTIONS
        norm_sum = sum(self.strategySum)
        for a in range(self.NUM_ACTIONS):
            if norm_sum > 0:
                avg_strategy[a] = self.strategySum[a] / norm_sum
            else:
                avg_strategy[a] = 1.0 / self.NUM_ACTIONS
        return avg_strategy
    

def train_with_assumed_opponent_strategy(iterations, assumed_opponent_strategy):
    player1 = RPSPlayer(assumed_opponent_strategy=assumed_opponent_strategy)  # Spieler 1 kennt die Gegnerstrategie
    player2 = RPSPlayer()  # Spieler 2 startet neutral

    for i in range(iterations):
        action1 = player1.getAction()
        action2 = player2.getAction()

        # Beide Spieler passen ihre Regrets an
        player1.updateRegrets(action1, action2)
        player2.updateRegrets(action2, action1)

        # Debugging-Ausgabe
        if i % 100000 == 0:
            print(f"Iteration {i}:")
            print(f"  Player 1 Strategy: {player1.getAverageStrategy()}")
            print(f"  Player 2 Strategy: {player2.getAverageStrategy()}")

    return player1.getAverageStrategy(), player2.getAverageStrategy()

# Training starten mit einer angenommenen Gegnerstrategie
assumed_strategy = [0.8, 0.1, 0.1]  # Gegner spielt 80% Stein, 10% Papier, 10% Schere
final_strategy_p1, final_strategy_p2 = train_with_assumed_opponent_strategy(1000000, assumed_strategy)

print("Final Average Strategy Player 1:", final_strategy_p1)
print("Final Average Strategy Player 2:", final_strategy_p2)