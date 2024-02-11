import tkinter as tk
from tkinter import messagebox

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz App")

        self.create_widgets()
    def create_widgets(self):
        self.start_button = tk.Button(self.master, text="Start Quiz", command=self.start_quiz)
        self.start_button.pack()

        self.question_label = tk.Label(self.master, text="What is your favorite programming language?")
        self.question_label.pack()

        self.options_var = tk.StringVar()
        self.options_var.set(None)

        options = [("Option 1", "1"), ("Option 2", "2"), ("Option 3", "3"), ("Option 4", "4")]

        for text, value in options:
            option_radio = tk.Radiobutton(self.master, text=text, variable=self.options_var, value=value)
            option_radio.pack()

        self.submit_button = tk.Button(self.master, text="Submit", command=self.check_answer)
        self.submit_button.pack()

    def start_quiz(self):
        self.start_button.pack_forget()
        self.question_label.pack()
        self.submit_button.pack()
        for widget in self.master.winfo_children():
            if widget not in [self.start_button, self.question_label, self.options_var, self.submit_button]:
                widget.pack()

    def check_answer(self):
        selected_option = self.options_var.get()

        if selected_option == "1":
            messagebox.showinfo("Congratulations", "You got it right!")
            self.reset_quiz()
        else:
            response = messagebox.askquestion("Try Again", "Oops! That's incorrect. Would you like to try again?")
            if response == 'no':
                self.master.destroy()
            else:
                self.reset_quiz()

    def reset_quiz(self):
        self.start_button.pack()
        self.question_label.pack_forget()
        self.submit_button.pack_forget()
        for widget in self.master.winfo_children():
            if widget not in [self.start_button]:
                widget.pack_forget()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
