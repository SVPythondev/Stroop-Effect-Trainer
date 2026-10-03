import tkinter as tk  # Import the library used to build windows and buttons
import random  # Import the library used to make random choices
import time  # Import the library used to measure time

COLORS = {"RED": "#E74C3C", "GREEN": "#2ECC71", "BLUE": "#3498DB", "YELLOW": "#F1C40F"}  # Color names and their hex codes
BG = "#1E1E2E"  # Background color of the whole window
TXT = "#CDD6F4"  # Default text color

class StroopGame:  # A class groups all game logic in one place
    def __init__(self, root):  # This runs once when the game is created
        self.root = root  # Remember the main window
        self.root.title("Stroop Effect: Attention Trainer")  # Set the window title
        self.root.geometry("450x450")  # Set the window size
        self.root.configure(bg=BG)  # Set the window background color
        self.root.resizable(False, False)  # Forbid resizing the window
        self.icon = tk.PhotoImage(width=32, height=32)  # Create an empty 32x32 picture for the window icon
        for color, (x, y) in zip(COLORS.values(), [(0, 0), (0, 16), (16, 0), (16, 16)]):  # Go through the 4 colors and 4 corner positions
            self.icon.put(color, to=(x, y, x + 12, y + 12))  # Paint one 16x16 colored square of the icon
        self.root.iconphoto(True, self.icon)  # Use the picture as the window icon
        self.mode = tk.StringVar(value="ink")  # Store the chosen mode: "ink" = text color, "word" = word meaning
        self.duration = 60  # Default round length in seconds
        self.show_start()  # Show the first (start) screen

    def clear(self):  # Remove everything from the window
        for widget in self.root.winfo_children():  # Look at every element currently in the window
            widget.destroy()  # Delete that element

    def label(self, text, size=12, color=TXT, bold=False, pady=5):  # Helper that adds a text line to the window
        lbl = tk.Label(self.root, text=text, font=("Helvetica", size, "bold" if bold else "normal"), fg=color, bg=BG)  # Create the text label
        lbl.pack(pady=pady)  # Place the label in the window
        return lbl  # Give the label back so it can be changed later

    def button(self, parent, text, command):  # Helper that adds a clickable button
        tk.Button(parent, text=text, command=command, width=8, font=("Helvetica", 11)).pack(side="left", padx=5)  # Create and place a button

    def show_start(self):  # Build the start screen
        self.clear()  # Remove anything left from a previous screen
        self.label("Stroop Effect Trainer", 20, bold=True, pady=20)  # Show the game title
        self.label("Choose a mode:")  # Ask the player to choose a mode
        for text, value in [("Pick the COLOR OF THE TEXT", "ink"), ("Pick the COLOR NAMED BY THE WORD", "word")]:  # Two available modes
            tk.Radiobutton(self.root, text=text, variable=self.mode, value=value, fg=TXT, bg=BG, selectcolor=BG, activebackground=BG, activeforeground=TXT).pack()  # Add a selectable option
        self.label("Round length:", pady=15)  # Caption for the time setting
        row = tk.Frame(self.root, bg=BG)  # Create a row to hold the time controls
        row.pack()  # Place the row in the window
        self.button(row, "- 10s", lambda: self.change_time(-10))  # Button that shortens the round by 10 seconds
        self.time_label = tk.Label(row, text=f"{self.duration}s", font=("Helvetica", 14, "bold"), fg=TXT, bg=BG, width=6)  # Label showing the current length
        self.time_label.pack(side="left")  # Place the time label between the buttons
        self.button(row, "+ 10s", lambda: self.change_time(10))  # Button that lengthens the round by 10 seconds
        tk.Button(self.root, text="START", command=self.start_game, font=("Helvetica", 14, "bold"), width=12).pack(pady=30)  # Button that starts the game

    def change_time(self, delta):  # Change the round length by the given number of seconds
        self.duration = min(300, max(30, self.duration + delta))  # Keep the length between 30 and 300 seconds
        self.time_label.config(text=f"{self.duration}s")  # Show the new length on screen

    def start_game(self):  # Prepare and start a new round
        self.correct, self.wrong, self.times = 0, 0, []  # Reset correct answers, wrong answers and reaction times
        self.end_time = time.time() + self.duration  # Calculate the moment when the round ends
        self.clear()  # Remove the start screen
        self.timer_label = self.label("", 14, bold=True, pady=10)  # Label that shows the remaining time
        hint = "Choose the color of the TEXT!" if self.mode.get() == "ink" else "Choose the color the WORD NAMES!"  # Pick the hint matching the mode
        self.label(hint, 10, "#A6ADC8")  # Show the hint to the player
        self.show_score = True  # The live score starts True = not hidden, False = hidden
        self.score_label = self.label("", 11, "#A6ADC8", pady=0)  # Label for the live score (empty while hidden)
        self.score_button = tk.Button(self.root, text="Hide score", command=self.toggle_score)  # Button that shows or hides the live score
        self.score_button.pack(side="bottom", pady=10)  # Place the button at the bottom of the window
        self.word_label = tk.Label(self.root, font=("Helvetica", 36, "bold"), bg=BG)  # Label that shows the colored word
        self.word_label.pack(pady=45)  # Place the word in the window
        frame = tk.Frame(self.root, bg=BG)  # Container for the color circles
        frame.pack(pady=20)  # Place the container in the window
        for name, hex_code in COLORS.items():  # Create one circle for each color
            canvas = tk.Canvas(frame, width=65, height=65, bg=BG, highlightthickness=0, cursor="hand2")  # Create a small drawing area
            canvas.create_oval(5, 5, 60, 60, fill=hex_code, outline="")  # Draw a colored circle in it
            canvas.bind("<Button-1>", lambda event, n=name: self.check_answer(n))  # When clicked, check the chosen color
            canvas.pack(side="left", padx=10)  # Place the circle in a row
        self.next_round()  # Show the first word
        self.update_score()  # Show the initial score
        self.tick()  # Start the countdown

    def tick(self):  # Update the countdown timer
        left = int(self.end_time - time.time())  # Calculate the whole seconds left
        if left <= 0:  # Check whether time is over
            self.show_result()  # Show the final statistics
            return  # Stop the countdown
        self.timer_label.config(text=f"Time left: {left}s")  # Display the remaining time
        self.root.after(200, self.tick)  # Run this function again in 0.2 seconds

    def next_round(self):  # Show a new random word
        word = random.choice(list(COLORS))  # Pick a random color name to display
        ink = random.choice(list(COLORS))  # Pick a random color to paint the text
        self.answer = ink if self.mode.get() == "ink" else word  # The right answer depends on the chosen mode
        self.word_label.config(text=word, fg=COLORS[ink])  # Show the word painted in the chosen color
        self.shown_at = time.time()  # Remember when the word appeared

    def check_answer(self, chosen):  # Called when the player clicks a circle
        self.times.append(time.time() - self.shown_at)  # Save how long the player took to answer
        if chosen == self.answer:  # Check if the click was correct
            self.correct += 1  # Count one more correct answer
        else:  # Otherwise the answer was wrong
            self.wrong += 1  # Count one more wrong answer
        self.update_score()  # Refresh the live score text
        self.next_round()  # Show the next word

    def toggle_score(self):  # Called when the player clicks the show/hide button
        self.show_score = not self.show_score  # Switch between shown and hidden
        self.score_button.config(text="Hide score" if self.show_score else "Show score")  # Change the button caption
        self.update_score()  # Refresh the live score text

    def update_score(self):  # Put the current score on screen, or clear it if hidden
        self.score_label.config(text=f"Correct: {self.correct}   Wrong: {self.wrong}" if self.show_score else "")  # Show the numbers only when allowed

    def show_result(self):  # Build the results screen
        total = self.correct + self.wrong  # Total number of answers given
        accuracy = 100 * self.correct / total if total else 0  # Percent of correct answers
        avg = sum(self.times) / total if total else 2.5  # Average reaction time in seconds
        speed = max(0, min(100, 100 * (2.5 - avg) / 2.0))  # Convert reaction time to 0-100 (0.5s = 100, 2.5s = 0)
        brain = round(0.6 * accuracy + 0.4 * speed)  # Brain score: 60% accuracy plus 40% speed
        level = "Excellent focus!" if brain >= 80 else "Good focus" if brain >= 60 else "Average focus" if brain >= 40 else "Needs more practice"  # Text rating
        self.clear()  # Remove the game screen
        self.label("Results", 22, bold=True, pady=15)  # Show the results title
        self.label(f"Correct answers: {self.correct}", 13, "#2ECC71")  # Show the number of correct answers
        self.label(f"Wrong answers: {self.wrong}", 13, "#E74C3C")  # Show the number of wrong answers
        self.label(f"Accuracy: {accuracy:.0f}%", 13)  # Show the accuracy percentage
        self.label(f"Average reaction time: {avg:.2f}s", 13)  # Show the average reaction speed
        self.label(f"Brain performance: {brain}/100", 16, "#F1C40F", True, 15)  # Show the overall brain score
        self.label(level, 14, "#F1C40F")  # Show the text rating
        tk.Button(self.root, text="PLAY AGAIN", command=self.show_start, font=("Helvetica", 13, "bold"), width=12).pack(pady=25)  # Button to return to the start screen

if __name__ == "__main__":  # Run the code below only when this file is started directly
    app = tk.Tk()  # Create the main window
    StroopGame(app)  # Create the game inside that window
    app.mainloop()  # Keep the window open and react to clicks
