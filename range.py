import json
from treys import Card

class Range:
    def __init__(self):
        self.range = {}

    def generate_range(self):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        suits = ["h", "d", "c", "s"]

        for first_rank in ranks:
            for second_rank in ranks:
                if ranks.index(first_rank) < ranks.index(second_rank):
                    continue

                # Pocket Pairs (z.B. "22", "33", etc.)
                if first_rank == second_rank:
                    hand_key = first_rank + second_rank
                    self.range[hand_key] = {}
                    for i, first_suit in enumerate(suits):
                        for second_suit in suits[i + 1:]:
                            first_card = Card.new(first_rank + first_suit)
                            second_card = Card.new(first_rank + second_suit)
                            sorted_hand = tuple(sorted([first_card, second_card], reverse=True))
                            self.range[hand_key][f"{Card.int_to_str(sorted_hand[0])},{Card.int_to_str(sorted_hand[1])}"] = None

                # Suited Hände (z.B. "AKs", "KQs", etc.)
                elif first_rank != second_rank:
                    hand_key_suited = first_rank + second_rank + "s"
                    if hand_key_suited not in self.range:
                        self.range[hand_key_suited] = {}
                    for suit in suits:
                        first_card = Card.new(first_rank + suit)
                        second_card = Card.new(second_rank + suit)
                        sorted_hand = tuple(sorted([first_card, second_card], reverse=True))
                        self.range[hand_key_suited][f"{Card.int_to_str(sorted_hand[0])},{Card.int_to_str(sorted_hand[1])}"] = None

                    # Offsuit Hände (z.B. "AKo", "KQo", etc.)
                    hand_key_offsuit = first_rank + second_rank + "o"
                    if hand_key_offsuit not in self.range:
                        self.range[hand_key_offsuit] = {}
                    for first_suit in suits:
                        for second_suit in suits:
                            if first_suit != second_suit:
                                first_card = Card.new(first_rank + first_suit)
                                second_card = Card.new(second_rank + second_suit)
                                sorted_hand = tuple(sorted([first_card, second_card], reverse=True))
                                self.range[hand_key_offsuit][f"{Card.int_to_str(sorted_hand[0])},{Card.int_to_str(sorted_hand[1])}"] = None

    def save_to_file(self, filename):
        """
        Speichert die Range in einer Datei im JSON-Format.
        """
        with open(filename, "w") as f:
            json.dump(self.range, f, indent=4)

    def load_from_file(self, filename):
        """
        Lädt die Range aus einer JSON-Datei.
        """
        with open(filename, "r") as f:
            loaded_range = json.load(f)

        # Konvertiere die Kartenstrings zurück in Card-Objekte
        self.range = {
            hand: {
                tuple(Card.new(card) for card in cards.split(",")): equity
                for cards, equity in combinations.items()
            }
            for hand, combinations in loaded_range.items()
        }

    def print_range(self):
        """
        Gibt die Range im lesbaren Format aus.
        """
        for hand, combinations in self.range.items():
            formatted_combinations = ", ".join(
                f"[{Card.int_to_pretty_str(card1)} {Card.int_to_pretty_str(card2)}]: {value}"
                for (card1, card2), value in combinations.items()
            )
            print(f"{hand}: {formatted_combinations}")

if __name__ == "__main__":
    range_instance = Range()
    range_instance.generate_range()
    range_instance.save_to_file("AKQ.json")