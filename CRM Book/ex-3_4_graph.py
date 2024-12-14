import random
import json
from graphviz import Digraph

class Node:
    def __init__(self, NUM_ACTIONS):
        self.NUM_ACTIONS = NUM_ACTIONS
        self.infoSet = None
        self.regretSum = [0.0] * NUM_ACTIONS
        self.strategy = [0.0] * NUM_ACTIONS
        self.strategySum = [0.0] * NUM_ACTIONS
    
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
            
    def getAverageStrategy(self):
        avgStrategy = [0.0] * self.NUM_ACTIONS
        normSum = sum(self.strategySum)
        for a in range(self.NUM_ACTIONS):
            if normSum > 0:
                avgStrategy[a] = self.strategySum[a] / normSum
            else:
                avgStrategy[a] = 1.0 / self.NUM_ACTIONS
        return avgStrategy
    
    def __str__(self):
        return f"{self.infoSet}: {self.getAverageStrategy()}"

class KuhnTrainer:
    def __init__(self):
        self.action = [0, 1]
        self.NUM_ACTIONS = 2
        self.nodeMap = {}
    
    def train(self, iterations):
        cards = [1, 2, 3, 4, 5]
        util = 0
        for i in range(iterations):
            random.shuffle(cards)
            util += self._crf_(cards, "", 1, 1)

        print("Average game value:" + str(util / iterations))
        print("Node Map:")
        for node in self.nodeMap.values():
            print(node)
        
    def _crf_(self, cards, history, p0, p1):
        plays = len(history)
        player = plays % 2
        opponent = 1 - player

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
        if infoSet not in self.nodeMap:
            node = Node(self.NUM_ACTIONS)
            node.infoSet = infoSet
            self.nodeMap[infoSet] = node
        else:
            node = self.nodeMap[infoSet]
        
        strategy = node.getStrategy(p0 if player == 0 else p1)
        util = [0.0] * node.NUM_ACTIONS
        nodeUtil = 0.0
        for a in range(node.NUM_ACTIONS):
            nextHistory = history + ("p" if a == 0 else "b")
            if player == 0:
                util[a] = self._crf_(cards, nextHistory, p0 * strategy[a], p1)
            else:
                util[a] = self._crf_(cards, nextHistory, p0, p1 * strategy[a])
            nodeUtil += strategy[a] * util[a]
        
        for a in range(node.NUM_ACTIONS):
            regret = util[a] - nodeUtil
            node.regretSum[a] += (p1 if player == 0 else p0) * regret
        
        return nodeUtil

def export_tree(nodeMap):
    def build_tree(infoSet):
        node = nodeMap[infoSet]
        children = []
        for a, action in enumerate(["p", "b"]):  # p für Pass, b für Bet
            nextInfoSet = infoSet + action
            if nextInfoSet in nodeMap:
                children.append(build_tree(nextInfoSet))
        return {
            "infoSet": infoSet,
            "strategy": node.getAverageStrategy(),
            "children": children
        }
    
    root = "1"  # Startzustand des Spiels (z.B. Karte 1)
    return build_tree(root)

def render_tree(tree, graph=None, parent=None):
    if graph is None:
        graph = Digraph()
    
    node_label = f"{tree['infoSet']}\n{tree['strategy']}"
    graph.node(tree['infoSet'], label=node_label)
    
    if parent:
        graph.edge(parent, tree['infoSet'])
    
    for child in tree['children']:
        render_tree(child, graph, tree['infoSet'])
    
    return graph

# Hauptprogramm
if __name__ == "__main__":
    kuhn = KuhnTrainer()
    kuhn.train(10000)
    
    # Spielbaum als JSON exportieren
    game_tree = export_tree(kuhn.nodeMap)
    with open("kuhn_game_tree.json", "w") as f:
        json.dump(game_tree, f, indent=4)
    
    # Spielbaum als Graph visualisieren
    tree_graph = render_tree(game_tree)
    tree_graph.render("kuhn_tree", format="png", cleanup=True)
    print("Baumgraph wurde als 'kuhn_tree.png' gespeichert.")
