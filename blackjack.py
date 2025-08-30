import tkinter as tk
import random

# Suits and Ranks
suits = ["♥ Hearts", "♦ Diamonds", "♣ Clubs", "♠ Spades"]
ranks = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10,
    "Jack": 10, "Queen": 10, "King": 10, "Ace": 11
}

# Build deck
def build_deck():
    deck = []
    for suit in suits:
        for rank, value in ranks.items():
            deck.append((rank, suit, value))
    random.shuffle(deck)
    return deck

# Calculate hand value with Ace handling
def calculate_hand(hand):
    value = sum(card[2] for card in hand)
    aces = sum(1 for card in hand if card[0] == "Ace")
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

# Display hand as string
def display_hand(hand):
    return ", ".join([f"{rank} {suit}" for rank, suit, val in hand])

# Game class
class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack 🎴")
        self.root.geometry("700x500")  # Bigger dashboard
        self.root.configure(bg="#F5E6E8")  # Nude pink-beige background

        self.deck = []
        self.player_hand = []
        self.dealer_hand = []

        # Frames
        self.top_frame = tk.Frame(root, bg="#F5E6E8")
        self.top_frame.pack(pady=20)

        self.middle_frame = tk.Frame(root, bg="#F5E6E8")
        self.middle_frame.pack(pady=20)

        self.bottom_frame = tk.Frame(root, bg="#F5E6E8")
        self.bottom_frame.pack(pady=20)

        # Dealer section
        self.dealer_label = tk.Label(self.top_frame, text="Dealer's Hand", font=("Arial", 18, "bold"), bg="#F5E6E8", fg="#8D6E63")
        self.dealer_label.pack()
        self.dealer_hand_label = tk.Label(self.top_frame, text="", font=("Arial", 14), bg="#F5E6E8", fg="#5D4037")
        self.dealer_hand_label.pack()

        # Player section
        self.player_label = tk.Label(self.middle_frame, text="Your Hand", font=("Arial", 18, "bold"), bg="#F5E6E8", fg="#6D4C41")
        self.player_label.pack()
        self.player_hand_label = tk.Label(self.middle_frame, text="", font=("Arial", 14), bg="#F5E6E8", fg="#3E2723")
        self.player_hand_label.pack()

        # Result section
        self.result_label = tk.Label(root, text="", font=("Arial", 18, "bold"), bg="#F5E6E8", fg="#4E342E")
        self.result_label.pack(pady=15)

        # Buttons
        self.hit_button = tk.Button(self.bottom_frame, text="Hit", command=self.player_hit, width=12, height=2,
                                    bg="#FFE0B2", fg="black", font=("Arial", 12, "bold"))
        self.hit_button.grid(row=0, column=0, padx=10)

        self.stand_button = tk.Button(self.bottom_frame, text="Stand", command=self.player_stand, width=12, height=2,
                                      bg="#FFCCBC", fg="black", font=("Arial", 12, "bold"))
        self.stand_button.grid(row=0, column=1, padx=10)

        self.new_game_button = tk.Button(self.bottom_frame, text="New Game", command=self.new_game, width=14, height=2,
                                         bg="#D7CCC8", fg="black", font=("Arial", 12, "bold"))
        self.new_game_button.grid(row=0, column=2, padx=10)

        self.new_game()

    def new_game(self):
        self.deck = build_deck()
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]

        self.update_display(hide_dealer=True)
        self.result_label.config(text="")

        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)

    def update_display(self, hide_dealer=False):
        if hide_dealer:
            dealer_text = "[Hidden], " + f"{self.dealer_hand[1][0]} {self.dealer_hand[1][1]}"
        else:
            dealer_text = display_hand(self.dealer_hand) + f"  => {calculate_hand(self.dealer_hand)}"
        self.dealer_hand_label.config(text=dealer_text)

        player_text = display_hand(self.player_hand) + f"  => {calculate_hand(self.player_hand)}"
        self.player_hand_label.config(text=player_text)

    def player_hit(self):
        self.player_hand.append(self.deck.pop())
        self.update_display(hide_dealer=True)

        if calculate_hand(self.player_hand) > 21:
            self.result_label.config(text="💥 You busted! Dealer wins.", fg="red")
            self.hit_button.config(state=tk.DISABLED)
            self.stand_button.config(state=tk.DISABLED)
            self.update_display(hide_dealer=False)

    def player_stand(self):
        while calculate_hand(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())

        self.update_display(hide_dealer=False)

        player_score = calculate_hand(self.player_hand)
        dealer_score = calculate_hand(self.dealer_hand)

        if dealer_score > 21 or player_score > dealer_score:
            self.result_label.config(text="🎉 You win!", fg="green")
        elif dealer_score == player_score:
            self.result_label.config(text="🤝 It's a tie!", fg="orange")
        else:
            self.result_label.config(text="😢 Dealer wins.", fg="red")

        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)


# Run Game
if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()