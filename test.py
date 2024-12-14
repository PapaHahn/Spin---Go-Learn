from treys import Card

ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
suits = ["h", "d", "c", "s"]

# Liste für alle möglichen Hände
all_hands = []

# Iteriere durch alle Kartenkombinationen
for first_rank in ranks:
    for first_suit in suits:
        first_card = Card.new(first_rank + first_suit)

        for second_rank in ranks:
            for second_suit in suits:
                # Erstelle die zweite Karte
                second_card = Card.new(second_rank + second_suit)

                # Überprüfen, dass keine Karte doppelt in der Hand ist
                if first_card == second_card:
                    continue

                # Sortiere so, dass die höhere Karte vorne ist
                hand = sorted([first_card, second_card], reverse=True)

                # Nur hinzufügen, wenn diese Hand noch nicht existiert
                if hand not in all_hands:
                    all_hands.append(hand)

# Ausgabe der Anzahl der Hände und Beispiele
print(f"Anzahl der einzigartigen Hände: {len(all_hands)}")
print("Beispiele für Hände:")
for hand in all_hands:
    print(f"[{Card.int_to_pretty_str(hand[0])}, {Card.int_to_pretty_str(hand[1])}]")