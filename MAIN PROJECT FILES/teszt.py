import customtkinter as ctk
from tkinter import messagebox, Menu, Listbox, END, ACTIVE
import os
import json

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("800x600")
        self.questions = []
        self.quizzes = {}

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Menü", menu=self.file_menu)
        self.file_menu.add_command(label="Quiz készítése", command=self.create_quiz)
        self.file_menu.add_command(label="Kész quizek", command=self.load_quizzes)

    def create_widgets(self):
        self.quiz_name_label = ctk.CTkLabel(self.root, text="Kvíz neve:")
        self.quiz_name_label.pack(pady=10)

        self.quiz_name_entry = ctk.CTkEntry(self.root, width=400)
        self.quiz_name_entry.pack(pady=10)

        self.question_label = ctk.CTkLabel(self.root, text="Kérdés:")
        self.question_label.pack(pady=10)

        self.question_entry = ctk.CTkEntry(self.root, width=400)
        self.question_entry.pack(pady=10)

        self.answers_frame = ctk.CTkFrame(self.root)
        self.answers_frame.pack(pady=10)

        self.answer_entries = []
        for i in range(4):
            label = ctk.CTkLabel(self.answers_frame, text=f"Válasz {chr(65 + i)}:")
            label.grid(row=i, column=0, padx=10, pady=5)
            entry = ctk.CTkEntry(self.answers_frame, width=300)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.answer_entries.append(entry)

        self.correct_answer_label = ctk.CTkLabel(self.root, text="Helyes válasz (A, B, C, D):")
        self.correct_answer_label.pack(pady=10)

        self.correct_answer_entry = ctk.CTkEntry(self.root, width=50)
        self.correct_answer_entry.pack(pady=10)

        self.add_question_button = ctk.CTkButton(self.root, text="Kérdés hozzáadása", command=self.add_question)
        self.add_question_button.pack(pady=10)

        self.save_quiz_button = ctk.CTkButton(self.root, text="Teszt elmentése", command=self.save_quiz)
        self.save_quiz_button.pack(pady=10)

    def create_quiz(self):
        self.questions = []
        self.quiz_name_entry.delete(0, ctk.END)
        self.question_entry.delete(0, ctk.END)
        for entry in self.answer_entries:
            entry.delete(0, ctk.END)
        self.correct_answer_entry.delete(0, ctk.END)

    def add_question(self):
        question = self.question_entry.get()
        answers = [entry.get() for entry in self.answer_entries]
        correct_answer = self.correct_answer_entry.get().upper()

        if question and all(answers) and correct_answer in ['A', 'B', 'C', 'D']:
            self.questions.append((question, answers, correct_answer))
            self.question_entry.delete(0, ctk.END)
            for entry in self.answer_entries:
                entry.delete(0, ctk.END)
            self.correct_answer_entry.delete(0, ctk.END)
            messagebox.showinfo("Siker", "Kérdés hozzáadva!")
        else:
            messagebox.showwarning("Hiba", "Kérjük, töltsd ki az összes mezőt és add meg a helyes választ!")

    def save_quiz(self):
        quiz_name = self.quiz_name_entry.get()
        if quiz_name and self.questions:
            self.quizzes[quiz_name] = self.questions
            with open("quizzes.json", "w") as f:
                json.dump(self.quizzes, f)
            messagebox.showinfo("Siker", "Teszt elmentve!")
        else:
            messagebox.showwarning("Hiba", "Kérjük, add meg a kvíz nevét és legalább egy kérdést!")

    def load_quizzes(self):
        if os.path.exists("quizzes.json"):
            with open("quizzes.json", "r") as f:
                self.quizzes = json.load(f)
            self.show_quizzes()
        else:
            messagebox.showwarning("Hiba", "Nincs elmentett teszt!")

    def show_quizzes(self):
        self.quiz_list_window = ctk.CTkToplevel(self.root)
        self.quiz_list_window.title("Kész tesztek")
        self.quiz_list_window.geometry("400x300")

        self.quiz_listbox = Listbox(self.quiz_list_window)
        self.quiz_listbox.pack(fill=ctk.BOTH, expand=True)

        for quiz_name in self.quizzes.keys():
            self.quiz_listbox.insert(END, quiz_name)

        self.start_quiz_button = ctk.CTkButton(self.quiz_list_window, text="Kvíz indítása", command=self.start_quiz)
        self.start_quiz_button.pack(pady=10)

    def start_quiz(self):
        selected_quiz = self.quiz_listbox.get(ACTIVE)
        if selected_quiz:
            self.questions = self.quizzes[selected_quiz]
            self.quiz_list_window.destroy()
            self.quiz_window = ctk.CTkToplevel(self.root)
            self.quiz_window.title("Kvíz")
            self.quiz_window.geometry("800x600")

            self.current_question = 0
            self.correct_answers = 0

            self.show_question()
        else:
            messagebox.showwarning("Hiba", "Kérjük, válassz egy kvízt!")

    def show_question(self):
        if self.current_question < len(self.questions):
            question, answers, correct_answer = self.questions[self.current_question]

            self.question_label = ctk.CTkLabel(self.quiz_window, text=question)
            self.question_label.pack(pady=10)

            self.answer_vars = []
            for answer in answers:
                var = ctk.StringVar()
                ctk.CTkRadioButton(self.quiz_window, text=answer, variable=var, value=answer).pack(pady=5)
                self.answer_vars.append(var)

            self.next_button = ctk.CTkButton(self.quiz_window, text="Következő", command=self.next_question)
            self.next_button.pack(pady=10)
        else:
            self.show_result()

    def next_question(self):
        selected_answer = None
        for var in self.answer_vars:
            if var.get():
                selected_answer = var.get()
                break

        if selected_answer:
            question, answers, correct_answer = self.questions[self.current_question]
            if selected_answer == answers[ord(correct_answer) - 65]:
                self.correct_answers += 1

        self.current_question += 1
        for widget in self.quiz_window.winfo_children():
            widget.destroy()

        self.show_question()

    def show_result(self):
        score = (self.correct_answers / len(self.questions)) * 100
        messagebox.showinfo("Eredmény", f"A pontszámod: {score:.2f}%")
        self.quiz_window.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    app = QuizApp(root)
    root.mainloop()
