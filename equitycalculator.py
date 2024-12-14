import json
import sys
import random
from itertools import combinations
from treys import Evaluator, Card
from range import Range


class EquityCalculator:
    def __init__(self):
        self.evaluator = Evaluator()
        self.deck = [Card.new(rank + suit) for rank in "23456789TJQKA" for suit in "hdcs"]

    def calculate_equity_with_sampling(self, my_cards, opponent_cards):
        """
        Berechnet die Equity für zwei Hände (my_cards vs opponent_cards) mit Monte-Carlo-Simulation.
        Zeigt Fortschritt innerhalb der Monte-Carlo-Simulation.
        """
        remaining_deck = [card for card in self.deck if card not in my_cards + opponent_cards]
        hand1_wins = 0
        ties = 0

        for i in range(100):
            random.shuffle(remaining_deck)
            board = remaining_deck[:5]
            hand1_score = self.evaluator.evaluate(board, my_cards)
            hand2_score = self.evaluator.evaluate(board, opponent_cards)

            if hand1_score < hand2_score:
                hand1_wins += 1
            elif hand1_score == hand2_score:
                ties += 0.5

        return hand1_score






    def calculate_and_update_range(self, my_range, opponent_range):
        category_counter = 0
        
        total_categories = len(my_range.range)
        print(total_categories)

        for mycategoryKey, myHands in my_range.range.items():
            category_counter += 1
            combination_counter = 0
            
            for myHandKey,_ in myHands.items():
                myHandscore = 0
                totalSimulations = 0
                myCards = [Card.new(card) for card in myHandKey.split(",")]
                
                #Gegnerische hand
                for opCatKey, opHands in opponent_range.range.items():
                    for opHandKey, _ in opHands.items():
                        
                        opCards = [Card.new(card) for card in opHandKey.split(",")]
                        
                        if set(myCards) & set(opCards):
                            continue
                        
                        print(f"Hand: {myHandKey} vs Hand: {opHandKey}")
                        score = self.calculate_equity_with_sampling(myCards,opCards)
                        myHandscore = myHandscore + score
                        totalSimulations = totalSimulations + 100
                
                equity = myHandscore / totalSimulations
                print(f"Equity für {myHandKey}: " + str(equity)+"%")
                my_range.range[mycategoryKey][myHandKey] = equity
        
        
        my_range.save_to_file("updated_my_range.json")                
                        
                        
                        
                
                
                
                
                
            
            
            
            
            

        # Aktualisierte Range speichern
        #my_range.save_to_file("updated_my_range.json")


if __name__ == "__main__":
    # Initialisiere den EquityCalculator
    calc = EquityCalculator()

    # Erstelle zwei Ranges
    my_range = Range()
    my_range.generate_range()

    opponent_range = Range()
    opponent_range.generate_range()

    # Berechne die Equity und aktualisiere die eigene Range
    calc.calculate_and_update_range(my_range, opponent_range)

    # Optional: Überprüfe die aktualisierte Range