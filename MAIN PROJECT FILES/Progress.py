import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

class StudentHelper:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Helper")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")

        self.bg_image = Image.open("BG.jpg")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image.resize((screen_width, screen_height)))

        self.bg_label = ctk.CTkLabel(self.root, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.score = 0
        self.total_questions = 0

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

        ctk.CTkButton(self.main_frame, text="Tananyagok", command=self.create_materials_menu, font=button_font, **button_options).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Quiz Készítő", command=self.show_wip_message, font=button_font, **button_options).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Nagy Teszt", command=self.show_wip_message, font=button_font, **button_options).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Beállítások", command=self.create_settings_menu, font=button_font, **button_options).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Kilépés", command=self.exit_program, font=button_font, **button_options).pack(pady=10)

    def create_settings_menu(self):
        """Displays a basic settings menu."""
        self.clear_frame()

        self.settings_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.settings_frame.pack(fill="both", expand=True)

        title_label = ctk.CTkLabel(self.settings_frame, text="Beállítások", font=("Arial", 30, "bold"), bg_color="transparent")
        title_label.pack(pady=40)

        ctk.CTkLabel(self.settings_frame, text="Itt beállíthatsz néhány alapvető opciót.", font=("Arial", 16), bg_color="transparent").pack(pady=20)

        back_button = ctk.CTkButton(self.settings_frame, text="Vissza a főmenübe", command=self.create_main_menu, font=("Arial", 14))
        back_button.pack(pady=20)

    def create_materials_menu(self):
        """Shows the list of materials available to study."""
        self.clear_frame()

        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)

        label = ctk.CTkLabel(self.main_frame, text="Válassz tananyagot:", font=("Arial", 24, "bold"), bg_color="transparent")
        label.grid(row=0, column=0, columnspan=3, pady=20)

        materials = [
            ("Ókori irodalom.txt", True),
            ("Középkori irodalom.txt", True),
            ("Magyar középkori irodalom.txt", False),
            ("Reneszánsz.txt", False),
            ("Magyar reneszánsz.txt", False),
            ("Barokk.txt", False),
            ("Klasszicizmus és felvilágosodás.txt", False),
            ("Magyar klasszicimus és felvilágosodás.txt", False),
            ("Csokonai Vitéz Mihály.txt", False),
            ("Romantika - világirodalom.txt", False),
            ("Katona József.txt", False),
            ("Reformkor.txt", False),
            ("Vörösmarty Mihály.txt", False),
            ("Jókai Mór.txt", False),
            ("Realizmus - világirodalom.txt", False),
            ("Arany János.txt", False),
            ("Madách Imre.txt", False),
            ("Mikszáth Kálmán.txt", False),
            ("1945 utáni irodalom.txt", False),
            ("1945 utáni magyar líra.txt", False),
            ("1945 utáni magyar próza.txt", False),
            ("Ady Endre.txt", False),
            ("Határon túli irodalom.txt", False),
            ("Móricz Zsigmond.txt", False),
            ("Nyugat nemzedékei.txt", False),
            ("Petőfi Sándor.txt", False),
            ("Radnóti Miklós.txt", False),
            ("Huszadik századi drámairodalom.txt", False),
            ("Huszadik századi világirodalom.txt", False)
        ]

        for i, (filename, has_quiz) in enumerate(materials):
            row = (i // 3) + 1
            col = i % 3

            button = ctk.CTkButton(
                self.main_frame,
                text=filename.split('.')[0],
                command=lambda f=filename, q=has_quiz: self.show_material(f, q),
                font=("Arial", 14),
                width=250,
                height=40,
                corner_radius=10,
                fg_color="#4CAF50",
                text_color="white"
            )
            button.grid(row=row, column=col, padx=20, pady=10, sticky="nsew")

        for col in range(3):
            self.main_frame.grid_columnconfigure(col, weight=1)

        back_button = ctk.CTkButton(self.main_frame, text="Vissza a főmenübe", command=self.create_main_menu, font=("Arial", 14))
        back_button.grid(row=row + 1, column=0, columnspan=3, pady=20)

    def show_material(self, filename, has_quiz):
        """Displays the selected material from a text file with the option to start a quiz."""
        self.clear_frame()

        self.lesson_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.lesson_frame.pack(fill="both", expand=True)

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                material_content = file.read()
        except FileNotFoundError:
            material_content = "A fájl nem található!"

        ctk.CTkLabel(self.lesson_frame, text=filename.split('.')[0].capitalize(), font=("Arial", 24, "bold"), bg_color="transparent").pack(pady=20)
        
        material_text = ctk.CTkTextbox(self.lesson_frame, width=1400, height=550)
        material_text.pack(pady=10)
        material_text.insert("0.0", material_content)
        material_text.configure(state="disabled")

        ctk.CTkButton(self.lesson_frame, text="Kilépés", command=self.create_materials_menu, font=("Arial", 16)).pack(pady=10)

        if has_quiz:
            quiz_file = "okori_teszt.txt" if "Ókori" in filename else "Középkori irodalom quiz.txt"
            ctk.CTkButton(self.lesson_frame, text="Tovább a teszthez", command=lambda: self.start_quiz(quiz_file), font=("Arial", 16)).pack(pady=20)

    def start_quiz(self, quiz_file):
        """Starts the quiz for the given file."""
        self.clear_frame()
        self.score = 0  

        try:
            with open(quiz_file, 'r', encoding='utf-8') as file:
                questions = file.read().split("\n\n")
        except FileNotFoundError:
            messagebox.showerror("Hiba", "A tesztfájl nem található!")
            return

        self.quiz_data = []
        for q in questions:
            lines = q.split("\n")
            if len(lines) >= 6:
                question = lines[0]
                options = lines[1:5]
                answer = lines[5].strip()
                self.quiz_data.append((question, options, answer))

        self.total_questions = len(self.quiz_data)
        random.shuffle(self.quiz_data)
        self.current_question_index = 0
        self.show_next_question()

    def show_next_question(self):
        """Shows the next question in the quiz."""
        if self.current_question_index < self.total_questions:
            question, options, answer = self.quiz_data[self.current_question_index]
            self.current_answer = answer  

            self.clear_frame()

            self.quiz_frame = ctk.CTkFrame(self.root)
            self.quiz_frame.pack(fill="both", expand=True)

            ctk.CTkLabel(self.quiz_frame, text=question, font=("Arial", 18)).pack(pady=20)

            for option in options:
                option_btn = ctk.CTkButton(self.quiz_frame, text=option, command=lambda o=option: self.check_answer(o), font=("Arial", 14))
                option_btn.pack(pady=10)

            self.current_question_index += 1
        else:
            self.show_result()

    def check_answer(self, selected_option):
        """Check if the selected answer is correct and update the score."""
        if selected_option[0] == self.current_answer:
            self.score += 1  
        self.root.after(500, self.show_next_question)  

    def show_result(self):
        """Display the quiz result."""
        percentage = (self.score / self.total_questions) * 100
        result_message = f"Eredmény: {self.score}/{self.total_questions} ({percentage:.2f}%)"

        if percentage >= 80:
            result_message += "\nGratulálunk, sikeres teszt!"
        else:
            result_message += "\nSajnos nem sikerült."

        messagebox.showinfo("Teszt eredmény", result_message)
        self.create_materials_menu()

    def clear_frame(self):
        """Utility function to clear the current frame."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def exit_program(self):
        """Exit the program."""
        self.root.quit()

    def show_wip_message(self):
        """Display a 'work in progress' message."""
        messagebox.showinfo("Fejlesztés alatt", "Ez a funkció még fejlesztés alatt áll.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = StudentHelper(root)
    root.mainloop()
