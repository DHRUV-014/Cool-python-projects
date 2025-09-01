import tkinter as tk
import random

# Word list
names = ["jack", "charles", "oliver", "henry", "george"]

# --- Game State Variables ---
name_ = random.choice(names)
list1 = []
lives = 5
dashes = "_" * len(name_)
wrong_guesses = []


# --- Functions ---
def update_display():
    """Updates the word, lives, and wrong guesses on the screen"""
    word_label.config(text=" ".join(dashes))
    lives_label.config(text=f"Lives left: {lives}")
    wrong_label.config(text=f"Wrong guesses: {', '.join(wrong_guesses)}")


def check_guess():
    """Checks the guessed letter"""
    global lives, dashes

    guess = entry.get().lower()
    entry.delete(0, tk.END)

    if not guess.isalpha() or len(guess) != 1:
        result_label.config(text="❌ Enter only ONE letter!", fg="#FF6B6B")
        return

    new_dashes = ""
    correct = False

    for i in name_:
        if i == guess and i not in list1:
            new_dashes += i
            correct = True
            list1.append(i)
        elif i in list1:
            new_dashes += i
        else:
            new_dashes += "_"

    if new_dashes == dashes:  # No progress made
        if guess not in wrong_guesses:
            wrong_guesses.append(guess)
        lives -= 1
        result_label.config(text="😬 Wrong guess!", fg="#E07A5F")
    else:
        dashes = new_dashes
        result_label.config(text="✅ Correct guess!", fg="#3D405B")

    update_display()

    if "_" not in dashes:
        result_label.config(text="🎉 YOU WIN!", fg="#81B29A")
        disable_game()

    if lives <= 0:
        result_label.config(text=f"💀 YOU LOST! Word was: {name_}", fg="#FF6B6B")
        disable_game()


def give_hint():
    """Reveals one random hidden letter"""
    global dashes, lives
    hidden_indices = [i for i, ch in enumerate(dashes) if ch == "_"]
    if hidden_indices:
        random_index = random.choice(hidden_indices)
        reveal_letter = name_[random_index]
        list1.append(reveal_letter)

        new_dashes = ""
        for i in name_:
            if i in list1:
                new_dashes += i
            else:
                new_dashes += "_"
        dashes = new_dashes
        result_label.config(text=f"💡 Hint: Letter '{reveal_letter}' revealed!", fg="#81B29A")
        update_display()

    if "_" not in dashes:
        result_label.config(text="🎉 YOU WIN!", fg="#81B29A")
        disable_game()


def restart_game():
    """Resets the game"""
    global name_, list1, lives, dashes, wrong_guesses
    name_ = random.choice(names)
    list1 = []
    lives = 5
    wrong_guesses = []
    dashes = "_" * len(name_)
    entry.config(state="normal")
    guess_btn.config(state="normal")
    hint_btn.config(state="normal")
    result_label.config(text="")
    update_display()


def disable_game():
    """Disables inputs after win/lose"""
    entry.config(state="disabled")
    guess_btn.config(state="disabled")
    hint_btn.config(state="disabled")


# --- GUI ---
root = tk.Tk()
root.title("Word Guessing Game")
root.geometry("700x500")
root.configure(bg="#F4F1DE")  # Nude pastel background

title_label = tk.Label(root, text="✨ Word Guessing Game ✨",
                    font=("Helvetica", 22, "bold"),
                    bg="#F4F1DE", fg="#3D405B")
title_label.pack(pady=10)

# Show names list
names_label = tk.Label(root, text=f"Possible words: {', '.join(names)}",
                    font=("Helvetica", 12),
                    bg="#F4F1DE", fg="#6D597A")
names_label.pack()

rules_label = tk.Label(root, text="You have 5 lives. Guess one letter at a time!",
                    font=("Helvetica", 12),
                    bg="#F4F1DE", fg="#E07A5F")
rules_label.pack(pady=5)

word_label = tk.Label(root, text=" ".join(dashes),
                    font=("Helvetica", 28, "bold"),
                    bg="#F4F1DE", fg="#3D405B")
word_label.pack(pady=20)

entry = tk.Entry(root, font=("Helvetica", 16), justify="center")
entry.pack()

# Fancy Guess button
guess_btn = tk.Button(root, text="🔥 Guess 🔥", command=check_guess,
                    font=("Helvetica", 14, "bold"),
                    bg="#81B29A", fg="white", width=12, relief="flat",background="#81B29A")
guess_btn.pack(pady=10)

# Extra buttons
btn_frame = tk.Frame(root, bg="#F4F1DE")
btn_frame.pack(pady=10)

hint_btn = tk.Button(btn_frame, text="💡 Hint", command=give_hint,
                     font=("Helvetica", 12, "bold"),
                     bg="#F2CC8F", fg="#3D405B", width=8, relief="flat")
hint_btn.grid(row=0, column=0, padx=10)

restart_btn = tk.Button(btn_frame, text="🔄 Restart", command=restart_game,
                        font=("Helvetica", 12, "bold"),
                        bg="#E07A5F", fg="white", width=10, relief="flat")
restart_btn.grid(row=0, column=1, padx=10)

lives_label = tk.Label(root, text=f"Lives left: {lives}",
                       font=("Helvetica", 14),
                       bg="#F4F1DE", fg="#3D405B")
lives_label.pack()

wrong_label = tk.Label(root, text="Wrong guesses: ",
                    font=("Helvetica", 12),
                    bg="#F4F1DE", fg="#6D597A")
wrong_label.pack()

result_label = tk.Label(root, text="",
                        font=("Helvetica", 14, "bold"),
                        bg="#F4F1DE", fg="#3D405B")
result_label.pack(pady=20)

update_display()
root.mainloop()