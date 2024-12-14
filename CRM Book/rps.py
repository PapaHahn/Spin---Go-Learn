import random

class RPSTrainer():
    
    def __init__(self):
        self.ROCK, self.PAPER, self.SCISSORS = 0, 1, 2
        self.NUM_ACTIONS = 3
        self.regretSum = [0.0] * self.NUM_ACTIONS
        self.strategy = [0.0] * self.NUM_ACTIONS
        self.strategySum = [0.0] * self.NUM_ACTIONS
        self.opp_strategy = [0.4, 0.3, 0.3]

    # Funktion: Gemischte Strategie über Regret-Matching berechnen
    def getStrategy(self):
        normalizing_sum = 0.0

        # Berechnung der Strategie basierend auf den Regrets
        for a in range(self.NUM_ACTIONS):
            self.strategy[a] = max(self.regretSum[a], 0)
            normalizing_sum += self.strategy[a]
            
        # Normalisierung der Strategie
        for a in range(self.NUM_ACTIONS):
            if normalizing_sum > 0:
                self.strategy[a] /= normalizing_sum
            else:
                self.strategy[a] = 1.0 / self.NUM_ACTIONS
            self.strategySum[a] += self.strategy[a]

        return self.strategy


    def getAction(self, strategy):
        # Wählt eine Aktion basierend auf den Wahrscheinlichkeiten in 'strategy'
        action = random.choices(range(self.NUM_ACTIONS), weights=strategy)[0]
        
        return action

    def train(self, iterations):
        actionUtility = [0.0] * self.NUM_ACTIONS
        
        for i in range(iterations):
            # Get regret-matched mixed-strategy actions
         
            myAction = self.getAction(self.getStrategy())
    
            otherAction = self.getAction(self.opp_strategy)
            
            # Compute action utilities
            actionUtility[otherAction] = 0 
            actionUtility[(otherAction + 1) % self.NUM_ACTIONS] = 1
            actionUtility[(otherAction - 1 + self.NUM_ACTIONS) % self.NUM_ACTIONS] = -1
        
            #Accumulate action regrets
            for a in range(self.NUM_ACTIONS):
                self.regretSum[a] += actionUtility[a] - actionUtility[myAction]
                
            
    def getAverageStrategy(self):
        avgStrat = [0.0] * self.NUM_ACTIONS
        normSum = 0
        for a in range(self.NUM_ACTIONS):
            normSum += self.strategySum[a]
        for a in range(self.NUM_ACTIONS):
            if normSum > 0:
                avgStrat[a] = self.strategySum[a] / normSum
            else:
                avgStrat[a] = 1.0 / self.NUM_ACTIONS
        return avgStrat


trainer = RPSTrainer()
trainer.train(10000000)
print(trainer.getAverageStrategy())