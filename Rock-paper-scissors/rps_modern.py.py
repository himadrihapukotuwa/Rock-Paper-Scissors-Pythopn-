import tkinter as tk
from tkinter import messagebox
import random
import os
from playsound import playsound

# ---------------- Game Settings ----------------
choices = ["Rock", "Paper", "Scissors"]
total_rounds = 10
high_score_file = "high_score.txt"

player_score = 0
computer_score = 0
rounds_played = 0
game_over = False

# Load high score
high_score = 0

if os.path.exists(high_score_file):
    with open(high_score_file, "r") as f:
        data = f.read().strip()
        if data.isdigit():
            high_score = int(data)
        else:
            high_score = 0

def play_sound(name):
    try:
        playsound(f"assets/{name}.wav", block=False)
    except:
        pass

def save_high_score(score):
    global high_score
    if score > high_score:
        high_score = score
        with open(high_score_file, "w") as f:
            f.write(str(high_score))

def play(user_choice):
    global player_score, computer_score, rounds_played, game_over

    if game_over:
        return

    computer_choice = random.choice(choices)
    result_text.set(f"Computer chose: {computer_choice}")

    if user_choice == computer_choice:
        outcome.set("It's a Tie 🤝")
        play_sound("tie")
    elif (
        (user_choice == "Rock" and computer_choice == "Scissors") or
        (user_choice == "Paper" and computer_choice == "Rock") or
        (user_choice == "Scissors" and computer_choice == "Paper")
    ):
        outcome.set("You Win this Round 🎉")
        play_sound("win")
        player_score += 1
    else:
        outcome.set("Computer Wins this Round 😢")
        play_sound("lose")
        computer_score += 1

    rounds_played += 1
    score_text.set(f"You: {player_score} | Computer: {computer_score} | Round: {rounds_played}/{total_rounds}")
    high_score_text.set(f"High Score: {high_score}")

    if rounds_played >= total_rounds:
        game_over = True
        save_high_score(player_score)
        high_score_text.set(f"High Score: {high_score}")

        if player_score > computer_score:
            winner.set("🏆 YOU WON THE GAME!")
        elif computer_score > player_score:
            winner.set("💻 COMPUTER WON THE GAME!")
        else:
            winner.set("🤝 GAME TIED!")

        messagebox.showinfo(
            "Game Over",
            f"Final Score\nYou: {player_score}\nComputer: {computer_score}\nHigh Score: {high_score}"
        )

def reset_game():
    global player_score, computer_score, rounds_played, game_over
    player_score = 0
    computer_score = 0
    rounds_played = 0
    game_over = False
    result_text.set("")
    outcome.set("")
    winner.set("")
    score_text.set(f"You: 0 | Computer: 0 | Round: 0/{total_rounds}")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("600x480")
root.configure(bg="#1E1E2F")
root.resizable(False, False)

tk.Label(root, text="🎮 Rock Paper Scissors 🎮",
         font=("Helvetica", 22, "bold"),
         bg="#1E1E2F", fg="#FFD700").pack(pady=15)

result_text = tk.StringVar()
outcome = tk.StringVar()
winner = tk.StringVar()
score_text = tk.StringVar(value=f"You: 0 | Computer: 0 | Round: 0/{total_rounds}")
high_score_text = tk.StringVar(value=f"High Score: {high_score}")

tk.Label(root, textvariable=result_text, font=("Arial", 14),
         bg="#1E1E2F", fg="#FAD7A0").pack()

tk.Label(root, textvariable=outcome, font=("Arial", 16, "bold"),
         bg="#1E1E2F", fg="#58D68D").pack(pady=5)

tk.Label(root, textvariable=winner, font=("Arial", 18, "bold"),
         bg="#1E1E2F", fg="#F4D03F").pack(pady=5)

tk.Label(root, textvariable=score_text, font=("Arial", 14),
         bg="#1E1E2F", fg="#85C1E9").pack()

tk.Label(root, textvariable=high_score_text, font=("Arial", 14, "bold"),
         bg="#1E1E2F", fg="#EC7063").pack(pady=5)

# Load images
rock_img = tk.PhotoImage(file="assets/rock.png").subsample(2,2)
paper_img = tk.PhotoImage(file="assets/paper.png").subsample(2,2)
scissors_img = tk.PhotoImage(file="assets/scissors.png").subsample(2,2)

btn_frame = tk.Frame(root, bg="#1E1E2F")
btn_frame.pack(pady=20)

tk.Button(btn_frame, image=rock_img, command=lambda: play("Rock"),
          bg="#1E1E2F", borderwidth=0).grid(row=0, column=0, padx=20)

tk.Button(btn_frame, image=paper_img, command=lambda: play("Paper"),
          bg="#1E1E2F", borderwidth=0).grid(row=0, column=1, padx=20)

tk.Button(btn_frame, image=scissors_img, command=lambda: play("Scissors"),
          bg="#1E1E2F", borderwidth=0).grid(row=0, column=2, padx=20)

tk.Button(root, text="Reset Game", command=reset_game,
          font=("Arial", 12, "bold"),
          bg="#E74C3C", fg="white").pack(pady=10)

root.mainloop()