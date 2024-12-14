import random

class ColonelPlayer:
    
    def __init__(self):
        self.NUM_ACTIONS = 21
        self.regretSum = [0.0] * self.NUM_ACTIONS
        self.strategy = [0.0] * self.NUM_ACTIONS
        self.strategySum = [0.0] * self.NUM_ACTIONS

    def getStrategyOfID(self, id):
        strat = [0, 0, 0]
        counter = 0
        s = 5
        next_value = s

        for first in range(next_value + 1):
            for second in range(next_value - first + 1):
                third = s - first - second
                strat = [first, second, third]

                if counter == id:
                    return strat
                counter += 1
        return None

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

    def updateRegrets(self, my_action_id, opponent_action_id):
        my_strategy = self.getStrategyOfID(my_action_id)
        opponent_strategy = self.getStrategyOfID(opponent_action_id)
        actual_utility = self.calculateUtility(my_strategy, opponent_strategy)

        for a in range(self.NUM_ACTIONS):
            alternative_strategy = self.getStrategyOfID(a)
            alternative_utility = self.calculateUtility(alternative_strategy, opponent_strategy)
            self.regretSum[a] += alternative_utility - actual_utility

    def calculateUtility(self, my_strategy, opponent_strategy):
        my_wins = 0
        opponent_wins = 0
        
        for my_soldiers, opp_soldiers in zip(my_strategy, opponent_strategy):
            if my_soldiers > opp_soldiers:
                my_wins += 1
            elif opp_soldiers > my_soldiers:
                opponent_wins += 1

        if my_wins > opponent_wins:
            return 1
        elif opponent_wins > my_wins:
            return -1
        else:
            return 0


def train_colonel_game(iterations):
    player1 = ColonelPlayer()
    player2 = ColonelPlayer()

    for i in range(iterations):
        # Beide Spieler wählen eine Aktion (ID der Strategie)
        action1 = player1.getAction()
        action2 = player2.getAction()

        # Spieler aktualisieren ihre Regrets
        player1.updateRegrets(action1, action2)
        player2.updateRegrets(action2, action1)

        # Optional: Debugging-Ausgabe alle 1000 Iterationen
        if i % 1000 == 0:
            strategy1 = player1.getStrategyOfID(action1)
            strategy2 = player2.getStrategyOfID(action2)
            print(f"Iteration {i}:")
            print(f"  Player 1 chose strategy ID {action1}: {strategy1}")
            print(f"  Player 2 chose strategy ID {action2}: {strategy2}")

    # Ergebnisse berechnen (keine Strategien ausgeschlossen)
    return player1, player2

# Training starten
player1, player2 = train_colonel_game(10000)

# Ergebnisse ausgeben
threshold = 0.01  # Wahrscheinlichkeiten kleiner als diese Schwelle werden ignoriert

print("Final Average Strategy Player 1:")
for i in range(player1.NUM_ACTIONS):
    prob = player1.strategySum[i] / sum(player1.strategySum)
    if prob > threshold:  # Nur Wahrscheinlichkeiten oberhalb der Schwelle ausgeben
        strat = player1.getStrategyOfID(i)
        print(f"  Strategy {i}: {strat} with probability {prob:.4f}")

print("Final Average Strategy Player 2:")
for i in range(player2.NUM_ACTIONS):
    prob = player2.strategySum[i] / sum(player2.strategySum)
    if prob > threshold:  # Nur Wahrscheinlichkeiten oberhalb der Schwelle ausgeben
        strat = player2.getStrategyOfID(i)
        print(f"  Strategy {i}: {strat} with probability {prob:.4f}")