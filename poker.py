class Node:
    
    def __init__(self, NUM_ACTIONS):
        self.infoSet = None
        self.regretSum = [0.0] * NUM_ACTIONS
        self.strategy = [0.0] * NUM_ACTIONS
        self.strategySum = [0.0] * NUM_ACTIONS

    #Get current information set mixed strategy through regret-matching    
    def getStrategy(self, realizationWeight):
        normSum = 0
        for a in range(self.NUM_ACTIONS):
            self.strategy[a] = max(self.regretSum[a], 0)
            normSum += self.strategy[a]
            
        for a in range(self.NUM_ACTIONS):
            if normSum > 0:
                self.strategy[a] /= normSum
            else:
                self.strategy[a] = 1.0 / self.NUM_ACTIONS
            self.strategySum[a] += realizationWeight * self.strategy[a]
        return self.strategy
            
    #Get average information set mixed strategy across all training iterations       
    def getAverageStrategy(self):
        avgStrategy = [0.0]* self.NUM_ACTIONS
        normSum = 0
        for a in range(self.NUM_ACTIONS):
            normSum += self.strategySum[a]
        for a in range(self.NUM_ACTIONS):
            if normSum > 0:
                avgStrategy[a] = self.strategySum[a] / normSum
            else:
                avgStrategy[a] = 1.0 / self.NUM_ACTIONS
        return avgStrategy
    
    #Get information set string representation
    def __str__(self):
       print(f"{self.info_set}: {self.get_average_strategy()}")

class Player:
    
    def __init__(self, balance=0):
        self.balance = 0
        self.action = {0:"check", 1:"call", 2:"fold", 3:"raise 2bb", 4:"raise 8bb", 5:"all-in"}
    
    

# 0 - fold
# 1 - call
# 2 - raise 2bb
# 3 - raise 8bb
# 4 - all-in