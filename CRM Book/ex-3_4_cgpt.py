import random
import json


class Node:
    # Kuhn node definitions
    def __init__(self, NUM_ACTIONS):
        self.NUM_ACTIONS = NUM_ACTIONS
        self.infoSet = None
        self.regretSum = [0.0] * NUM_ACTIONS
        self.strategy = [0.0] * NUM_ACTIONS
        self.strategySum = [0.0] * NUM_ACTIONS
    
    # Get current information set mixed strategy through regret-matching    
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
            
    # Get average information set mixed strategy across all training iterations       
    def getAverageStrategy(self):
        avgStrategy = [0.0] * self.NUM_ACTIONS
        normSum = 0
        for a in range(self.NUM_ACTIONS):
            normSum += self.strategySum[a]
        for a in range(self.NUM_ACTIONS):
            if normSum > 0:
                avgStrategy[a] = self.strategySum[a] / normSum
            else:
                avgStrategy[a] = 1.0 / self.NUM_ACTIONS
        return avgStrategy
    
    # Get information set string representation
    def __str__(self):
        return f"{self.infoSet}: {self.getAverageStrategy()}"


class KuhnTrainer:
    # Kuhn's Poker definitions
    def __init__(self):
        self.NUM_ACTIONS = 2
        self.nodeMap = {}

    # Train Kuhn Poker
    def train(self, iterations):
        cards = [1, 2, 3]
        util = 0
        for i in range(iterations):
            random.shuffle(cards)
            util += self._crf_(cards, "", 1, 1)

        print("Average game value:" + str(util / iterations))
        
    def _crf_(self, cards, history, p0, p1):
        plays = len(history)
        player = plays % 2
        opponent = 1 - player

        # Return payoff for terminal states
        if plays > 1:
            terminalPass = history[plays - 1] == 'p'
            doubleBet = history[plays - 2:plays] == "bb"
            isPlayerCardHigher = cards[player] > cards[opponent]

            if terminalPass:
                if history == "pp":
                    return 1 if isPlayerCardHigher else -1
                else:
                    return 1
            elif doubleBet:
                return 2 if isPlayerCardHigher else -2
            
        infoSet = str(cards[player]) + history

        # Get information set node or create it if nonexistent
        if infoSet not in self.nodeMap:
            node = Node(self.NUM_ACTIONS)
            node.infoSet = infoSet
            self.nodeMap[infoSet] = node
        else:
            node = self.nodeMap[infoSet]
        
        # For each action, recursively call cfr with additional history and probability
        strategy = node.getStrategy(p0 if player == 0 else p1)
        util = [0.0] * node.NUM_ACTIONS
        nodeUtil = 0.0
        for a in range(self.NUM_ACTIONS):
            nextHistory = history + ("p" if a == 0 else "b")
            if player == 0:
                util[a] = self._crf_(cards, nextHistory, p0 * strategy[a], p1)
            else:
                util[a] = self._crf_(cards, nextHistory, p0, p1 * strategy[a])
            nodeUtil += strategy[a] * util[a]
        
        # For each action, compute and accumulate counterfactual regret
        for a in range(self.NUM_ACTIONS):
            regret = util[a] - nodeUtil
            node.regretSum[a] += (p1 if player == 0 else p0) * regret
        
        return nodeUtil
    
    def play_two_players(self, iterations=1000):
        results = []
        cards = [1, 2, 3]

        for _ in range(iterations):
            random.shuffle(cards)
            player1_card = cards[0]
            player2_card = cards[1]
            result = self.simulate_game(player1_card, player2_card)
            results.append(result)

        # Calculate statistics
        player1_wins = sum(1 for r in results if r > 0)
        player2_wins = sum(1 for r in results if r < 0)
        ties = sum(1 for r in results if r == 0)


    def simulate_game(self, player1_card, player2_card):
        history = ""
        plays = 0

        while True:
            player = plays % 2
            if plays > 1:
                terminalPass = history[-1] == "p"
                doubleBet = history[-2:] == "bb"
                isPlayerCardHigher = player1_card > player2_card

                if terminalPass:
                    if history == "pp":
                        return 1 if isPlayerCardHigher else -1
                    else:
                        return 1
                elif doubleBet:
                    return 2 if isPlayerCardHigher else -2

            # Action selection
            if player == 0:
                action = random.choice(["p", "b"])
            else:
                infoSet = str(player2_card) + history
                node = self.nodeMap.get(infoSet)
                if node:
                    action = random.choices(["p", "b"], weights=node.getAverageStrategy())[0]
                else:
                    action = "p"

            history += action
            plays += 1

kuhn = KuhnTrainer()
kuhn.train(100000)
kuhn.play_two_players(iterations=10000)
