"""
Intermediate Result Calculator
-------------------------------
A GUI app (Tkinter) for calculating total marks, percentage and grade
for Pakistani Intermediate (11th/12th) students, supporting different
fields with their own subject lists and elective choices.

Run with: python3 result_calculator.py
"""

import tkinter as tk
from tkinter import ttk, messagebox

# ---------------------------------------------------------------------------
# Subject definitions per field
# ---------------------------------------------------------------------------
# Each field is a list of "subject slots". A slot is either:
#   ("Fixed Subject Name",)                      -> single compulsory subject
#   ("Choice Label", ["Option A", "Option B"])    -> pick one of the options
#
# This structure makes it easy to add/remove fields or subjects later.

FIELDS = {
    "ICS (Computer Science)": [
        ("English",),
        ("Urdu",),
        ("Pakistan Studies / Islamiyat", ["Pakistan Studies", "Islamiyat"]),
        ("Tarjama-tul-Quran",),
        ("Mathematics",),
        ("Computer Science",),
        ("Physics / Statistics", ["Physics", "Statistics"]),
    ],
    "FSc Pre-Engineering": [
        ("English",),
        ("Urdu",),
        ("Pakistan Studies / Islamiyat", ["Pakistan Studies", "Islamiyat"]),
        ("Tarjama-tul-Quran",),
        ("Mathematics",),
        ("Physics",),
        ("Chemistry",),
    ],
    "FSc Pre-Medical": [
        ("English",),
        ("Urdu",),
        ("Pakistan Studies / Islamiyat", ["Pakistan Studies", "Islamiyat"]),
        ("Tarjama-tul-Quran",),
        ("Biology",),
        ("Physics",),
        ("Chemistry",),
    ],
    "I.Com (Commerce)": [
        ("English",),
        ("Urdu",),
        ("Pakistan Studies / Islamiyat", ["Pakistan Studies", "Islamiyat"]),
        ("Tarjama-tul-Quran",),
        ("Principles of Accounting",),
        ("Principles of Economics",),
        ("Business Maths / Computerized Accounting", ["Business Maths", "Computerized Accounting"]),
    ],
}


def grade_for(percentage: float) -> str:
    """Return the letter grade for a given percentage."""
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    elif percentage >= 33:
        return "E"
    else:
        return "F"


# ---------------------------------------------------------------------------
# GUI Application
# ---------------------------------------------------------------------------
class ResultApp(tk.Tk):
    BG = "#f4f6f9"
    ACCENT = "#2f6feb"
    FONT = ("Segoe UI", 11)
    FONT_BOLD = ("Segoe UI", 12, "bold")
    FONT_TITLE = ("Segoe UI", 18, "bold")

    def __init__(self):
        super().__init__()
        self.title("Intermediate Result Calculator")
        self.geometry("560x640")
        self.minsize(520, 560)
        self.configure(bg=self.BG)

        # State
        self.selected_field = tk.StringVar()
        self.subject_rows = []      # list of dicts: {label, combo_var/None, total_var, obtained_var}

        self.container = tk.Frame(self, bg=self.BG)
        self.container.pack(fill="both", expand=True)

        self.show_field_selection()

    # ------------------------------------------------------------------
    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # ------------------------------------------------------------------
    # Screen 1: choose field
    # ------------------------------------------------------------------
    def show_field_selection(self):
        self.clear_container()

        tk.Label(
            self.container, text="Intermediate Result Calculator",
            font=self.FONT_TITLE, bg=self.BG, fg="#1a1a1a"
        ).pack(pady=(30, 5))

        tk.Label(
            self.container, text="Select your field to continue",
            font=self.FONT, bg=self.BG, fg="#555"
        ).pack(pady=(0, 25))

        for field_name in FIELDS:
            btn = tk.Button(
                self.container, text=field_name, font=self.FONT_BOLD,
                bg=self.ACCENT, fg="white", activebackground="#1e56c4",
                activeforeground="white", relief="flat", cursor="hand2",
                padx=10, pady=12,
                command=lambda f=field_name: self.select_field(f)
            )
            btn.pack(fill="x", padx=60, pady=8)

    def select_field(self, field_name):
        self.selected_field.set(field_name)
        self.show_marks_entry()

    # ------------------------------------------------------------------
    # Screen 2: enter marks for each subject in the chosen field
    # ------------------------------------------------------------------
    def show_marks_entry(self):
        self.clear_container()
        field_name = self.selected_field.get()
        subjects = FIELDS[field_name]

        header = tk.Frame(self.container, bg=self.BG)
        header.pack(fill="x", pady=(15, 5), padx=20)
        tk.Button(
            header, text="< Back", font=self.FONT, bg=self.BG, fg=self.ACCENT,
            relief="flat", cursor="hand2", command=self.show_field_selection
        ).pack(side="left")
        tk.Label(
            header, text=field_name, font=self.FONT_TITLE, bg=self.BG
        ).pack(side="left", padx=15)

        # Scrollable area for subject rows
        canvas = tk.Canvas(self.container, bg=self.BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.BG)

        scroll_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        # Column headers
        col_header = tk.Frame(scroll_frame, bg=self.BG)
        col_header.pack(fill="x", pady=(0, 8))
        tk.Label(col_header, text="Subject", font=self.FONT_BOLD, bg=self.BG, width=22, anchor="w").grid(row=0, column=0, sticky="w")
        tk.Label(col_header, text="Total Marks", font=self.FONT_BOLD, bg=self.BG, width=10).grid(row=0, column=1)
        tk.Label(col_header, text="Obtained", font=self.FONT_BOLD, bg=self.BG, width=10).grid(row=0, column=2)

        self.subject_rows = []

        for slot in subjects:
            row = tk.Frame(scroll_frame, bg=self.BG)
            row.pack(fill="x", pady=6)

            if len(slot) == 1:
                # Fixed subject
                label_text = slot[0]
                tk.Label(row, text=label_text, font=self.FONT, bg=self.BG, width=22, anchor="w").grid(row=0, column=0, sticky="w")
                combo_var = None
                combo_widget = None
            else:
                # Choice subject -> dropdown
                label_text, options = slot
                combo_var = tk.StringVar(value=options[0])
                combo_widget = ttk.Combobox(
                    row, textvariable=combo_var, values=options,
                    state="readonly", width=20, font=self.FONT
                )
                combo_widget.grid(row=0, column=0, sticky="w")

            total_var = tk.StringVar()
            obtained_var = tk.StringVar()

            tk.Entry(row, textvariable=total_var, width=10, font=self.FONT, justify="center").grid(row=0, column=1, padx=5)
            tk.Entry(row, textvariable=obtained_var, width=10, font=self.FONT, justify="center").grid(row=0, column=2, padx=5)

            self.subject_rows.append({
                "label": label_text,
                "combo_var": combo_var,
                "total_var": total_var,
                "obtained_var": obtained_var,
            })

        # Calculate button (outside scroll area, fixed at bottom)
        btn_frame = tk.Frame(self.container, bg=self.BG)
        btn_frame.pack(fill="x", pady=15, padx=20)
        tk.Button(
            btn_frame, text="Calculate Result", font=self.FONT_BOLD,
            bg="#1fa855", fg="white", activebackground="#178a44",
            activeforeground="white", relief="flat", cursor="hand2",
            padx=10, pady=12, command=self.calculate_result
        ).pack(fill="x")

    # ------------------------------------------------------------------
    def calculate_result(self):
        total_of_totals = 0
        total_obtained = 0
        breakdown = []

        for row in self.subject_rows:
            subject_name = row["combo_var"].get() if row["combo_var"] else row["label"]

            total_str = row["total_var"].get().strip()
            obtained_str = row["obtained_var"].get().strip()

            if not total_str or not obtained_str:
                messagebox.showerror(
                    "Missing Marks",
                    f"Please enter both total and obtained marks for:\n{subject_name}"
                )
                return

            try:
                subject_total = float(total_str)
                subject_obtained = float(obtained_str)
            except ValueError:
                messagebox.showerror(
                    "Invalid Input",
                    f"Marks for '{subject_name}' must be numbers."
                )
                return

            if subject_total <= 0:
                messagebox.showerror("Invalid Input", f"Total marks for '{subject_name}' must be greater than 0.")
                return

            if subject_obtained < 0 or subject_obtained > subject_total:
                messagebox.showerror(
                    "Invalid Input",
                    f"Obtained marks for '{subject_name}' must be between 0 and {subject_total:g}."
                )
                return

            total_of_totals += subject_total
            total_obtained += subject_obtained
            breakdown.append((subject_name, subject_total, subject_obtained))

        percentage = (total_obtained / total_of_totals) * 100
        grade = grade_for(percentage)

        self.show_result_screen(breakdown, total_of_totals, total_obtained, percentage, grade)

    # ------------------------------------------------------------------
    # Screen 3: show result
    # ------------------------------------------------------------------
    def show_result_screen(self, breakdown, total_of_totals, total_obtained, percentage, grade):
        self.clear_container()

        tk.Label(
            self.container, text="Result Summary", font=self.FONT_TITLE, bg=self.BG
        ).pack(pady=(25, 15))

        table_frame = tk.Frame(self.container, bg="white", bd=1, relief="solid")
        table_frame.pack(padx=20, fill="x")

        header_row = tk.Frame(table_frame, bg="#e8ecf3")
        header_row.pack(fill="x")
        tk.Label(header_row, text="Subject", font=self.FONT_BOLD, bg="#e8ecf3", width=24, anchor="w").pack(side="left", padx=8, pady=6)
        tk.Label(header_row, text="Total", font=self.FONT_BOLD, bg="#e8ecf3", width=8).pack(side="left")
        tk.Label(header_row, text="Obtained", font=self.FONT_BOLD, bg="#e8ecf3", width=8).pack(side="left")

        for name, tot, obt in breakdown:
            r = tk.Frame(table_frame, bg="white")
            r.pack(fill="x")
            tk.Label(r, text=name, font=self.FONT, bg="white", width=24, anchor="w").pack(side="left", padx=8, pady=4)
            tk.Label(r, text=f"{tot:g}", font=self.FONT, bg="white", width=8).pack(side="left")
            tk.Label(r, text=f"{obt:g}", font=self.FONT, bg="white", width=8).pack(side="left")

        summary_frame = tk.Frame(self.container, bg=self.BG)
        summary_frame.pack(pady=25)

        tk.Label(summary_frame, text=f"Total Marks: {total_obtained:g} / {total_of_totals:g}",
                 font=self.FONT_BOLD, bg=self.BG).pack(pady=4)
        tk.Label(summary_frame, text=f"Percentage: {percentage:.2f}%",
                 font=self.FONT_BOLD, bg=self.BG).pack(pady=4)

        grade_color = "#1fa855" if grade in ("A+", "A", "B") else ("#e0a800" if grade in ("C", "D", "E") else "#d9363e")
        tk.Label(summary_frame, text=f"Grade: {grade}", font=("Segoe UI", 22, "bold"),
                 bg=self.BG, fg=grade_color).pack(pady=10)

        btn_frame = tk.Frame(self.container, bg=self.BG)
        btn_frame.pack(pady=10)
        tk.Button(
            btn_frame, text="Edit Marks", font=self.FONT, bg="#e8ecf3",
            relief="flat", cursor="hand2", padx=15, pady=8,
            command=self.show_marks_entry
        ).pack(side="left", padx=6)
        tk.Button(
            btn_frame, text="Start Over", font=self.FONT, bg="#e8ecf3",
            relief="flat", cursor="hand2", padx=15, pady=8,
            command=self.show_field_selection
        ).pack(side="left", padx=6)


if __name__ == "__main__":
    app = ResultApp()
    app.mainloop()
