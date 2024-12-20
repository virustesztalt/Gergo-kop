import customtkinter as ctk
from tkinter import messagebox, Listbox, END, ACTIVE
from PIL import Image
import random
import json
import os


class StudentHelper:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Helper")

        # Fullscreen Window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")

        # Background Image with CTkImage
        self.bg_image = Image.open("BG.jpg")
        self.bg_ctk_image = ctk.CTkImage(light_image=self.bg_image, size=(screen_width, screen_height))
        self.bg_label = ctk.CTkLabel(self.root, image=self.bg_ctk_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Style settings
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.score = 0
        self.total_questions = 0
        self.quizzes = {}  # To store quiz data

        self.create_main_menu()

    def create_main_menu(self):
        """Creates the main menu with options."""
        self.clear_frame()

        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = ctk.CTkLabel(self.main_frame, text="Főmenü", font=("Arial", 40, "bold"), bg_color="transparent")
        title_label.pack(pady=30)

        button_font = ("Arial", 20, "bold")
        button_options = {
            "width": 300,
            "height": 60,
            "fg_color": "#4CAF50",
            "text_color": "white",
            "corner_radius": 0
        }

        ctk.CTkButton(self.main_frame, text="Tananyagok", command=self.create_materials_menu, font=button_font,
                      **button_options).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Quiz Készítő", command=self.create_quiz_menu, font=button_font,
                      **button_options).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Beállítások", command=self.create_settings_menu, font=button_font,
                      **button_options).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Kilépés", command=self.exit_program, font=button_font,
                      **button_options).pack(pady=10)

    def create_materials_menu(self):
        """Displays the Materials Menu."""
        self.clear_frame()

        self.materials_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.materials_frame.pack(fill="both", expand=True)

        title_label = ctk.CTkLabel(self.materials_frame, text="Tananyagok", font=("Arial", 30, "bold"))
        title_label.pack(pady=20)

        ctk.CTkButton(self.materials_frame, text="Vissza a főmenübe", command=self.create_main_menu,
                      font=("Arial", 14)).pack(pady=20)

    def create_quiz_menu(self):
        """Displays the Quiz Creator interface."""
        self.clear_frame()

        self.quiz_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.quiz_frame.pack(fill="both", expand=True)

        title_label = ctk.CTkLabel(self.quiz_frame, text="Quiz Készítő", font=("Arial", 30, "bold"))
        title_label.pack(pady=20)

        self.quiz_name_entry = ctk.CTkEntry(self.quiz_frame, width=400, placeholder_text="Quiz neve")
        self.quiz_name_entry.pack(pady=10)

        self.question_entry = ctk.CTkEntry(self.quiz_frame, width=400, placeholder_text="Kérdés")
        self.question_entry.pack(pady=10)

        self.answers_frame = ctk.CTkFrame(self.quiz_frame)
        self.answers_frame.pack(pady=10)

        self.answer_entries = []
        for i in range(4):
            label = ctk.CTkLabel(self.answers_frame, text=f"Válasz {chr(65 + i)}:")
            label.grid(row=i, column=0, padx=10, pady=5)
            entry = ctk.CTkEntry(self.answers_frame, width=300)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.answer_entries.append(entry)

        self.correct_answer_entry = ctk.CTkEntry(self.quiz_frame, width=50, placeholder_text="Helyes válasz (A, B, C, D)")
        self.correct_answer_entry.pack(pady=10)

        ctk.CTkButton(self.quiz_frame, text="Kérdés hozzáadása", command=self.add_question,
                      font=("Arial", 14), fg_color="#4CAF50", text_color="white").pack(pady=10)

        ctk.CTkButton(self.quiz_frame, text="Teszt elmentése", command=self.save_quiz,
                      font=("Arial", 14), fg_color="#4CAF50", text_color="white").pack(pady=10)

        ctk.CTkButton(self.quiz_frame, text="Kész quizek", command=self.load_quizzes,
                      font=("Arial", 14), fg_color="#4CAF50", text_color="white").pack(pady=10)

        ctk.CTkButton(self.quiz_frame, text="Vissza a főmenübe", command=self.create_main_menu,
                      font=("Arial", 14)).pack(pady=20)

        self.questions = []  # Reset the questions list

    def add_question(self):
        """Adds a question to the quiz."""
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
        """Saves the quiz to a file."""
        quiz_name = self.quiz_name_entry.get()
        if quiz_name and self.questions:
            self.quizzes[quiz_name] = self.questions
            with open("quizzes.json", "w", encoding="utf-8") as f:
                json.dump(self.quizzes, f)
            messagebox.showinfo("Siker", "Teszt elmentve!")
        else:
            messagebox.showwarning("Hiba", "Kérjük, add meg a kvíz nevét és legalább egy kérdést!")

    def load_quizzes(self):
        """Loads existing quizzes."""
        if os.path.exists("quizzes.json"):
            with open("quizzes.json", "r", encoding="utf-8") as f:
                self.quizzes = json.load(f)
            self.show_quizzes()
        else:
            messagebox.showwarning("Hiba", "Nincs elmentett teszt!")

    def show_quizzes(self):
        """Displays saved quizzes."""
        self.clear_frame()

        self.quiz_list_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.quiz_list_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(self.quiz_list_frame, text="Elérhető tesztek", font=("Arial", 24, "bold")).pack(pady=20)

        self.quiz_listbox = Listbox(self.quiz_list_frame)
        self.quiz_listbox.pack(fill=ctk.BOTH, expand=True, padx=20, pady=10)

        for quiz_name in self.quizzes.keys():
            self.quiz_listbox.insert(END, quiz_name)

        ctk.CTkButton(self.quiz_list_frame, text="Vissza a főmenübe", command=self.create_main_menu,
                      font=("Arial", 14)).pack(pady=10)

    def create_settings_menu(self):
        """Displays the settings menu."""
        self.clear_frame()
        ctk.CTkLabel(self.root, text="Beállítások még nincsenek implementálva.", font=("Arial", 24)).pack(pady=20)
        ctk.CTkButton(self.root, text="Vissza a főmenübe", command=self.create_main_menu,
                      font=("Arial", 14)).pack(pady=20)

    def clear_frame(self):
        """Utility function to clear the current frame."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def exit_program(self):
        """Exit the program."""
        self.root.quit()


if __name__ == "__main__":
    root = ctk.CTk()
    app = StudentHelper(root)
    root.mainloop()
