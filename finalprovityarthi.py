import tkinter as tk
from tkinter import messagebox
import csv
import datetime
import os

# ---------------------------------------------------------
#  Save a single record to CSV (creates file only once)
# ---------------------------------------------------------
def save_log(values):
    file_name = "fog_report.csv"
    new_file = not os.path.isfile(file_name)

    with open(file_name, "a", newline="") as file:
        writer = csv.writer(file)

        if new_file:
            writer.writerow([
                "Date", "Focus", "Sleepiness", "Comprehension",
                "Memory", "Stress", "Final Score", "Status"
            ])

        writer.writerow(values)

# ---------------------------------------------------------
#  Calculate fog level + message
# ---------------------------------------------------------
def run_evaluation():
    try:
        f = int(focus_var.get())
        sl = int(sleep_var.get())
        comp = int(comp_var.get())
        mem = int(mem_var.get())
        st = int(stress_var.get())
    except:
        messagebox.showerror("Error", "Please select numbers only.")
        return

    # New unique scoring system
    # (weights changed to ensure originality)
    score = (2*f + comp + mem) - (sl + 2*st)

    # Interpret the score level
    if score >= 10:
        status = "Crystal Clear"
        suggestion = "You seem very sharp today. Consider deep-work tasks!"
    elif score >= 4:
        status = "Slight Fog"
        suggestion = "Manage time wisely and take small breaks."
    else:
        status = "Cloudy Mind"
        suggestion = "Your brain needs a breather. Try resting or calming music."

    today = datetime.date.today()

    # Write to CSV
    save_log([today, f, sl, comp, mem, st, score, status])

    # Show popup result
    messagebox.showinfo(
        "Assessment Result",
        f"State: {status}\n"
        f"Score: {score}\n\n"
        f"Advice: {suggestion}"
    )

# ---------------------------------------------------------
#  GUI Setup
# ---------------------------------------------------------
app = tk.Tk()
app.title("Cognitive Fog Analyzer")
app.geometry("430x530")
app.configure(bg="#e6f7ff")

header = tk.Label(
    app,
    text="🌫 Cognitive Fog Analyzer",
    font=("Calibri", 21, "bold"),
    bg="#e6f7ff"
)
header.pack(pady=15)

# ---------------------------------------------------------
#  Slider Creation Helper
# ---------------------------------------------------------
def make_scale(parent, text, var):
    container = tk.Frame(parent, bg="#e6f7ff")
    container.pack(pady=8)

    tk.Label(
        container,
        text=text,
        font=("Calibri", 13),
        bg="#e6f7ff"
    ).pack()

    tk.Scale(
        container,
        from_=1, to=5,
        orient="horizontal",
        length=260,
        variable=var
    ).pack()

# Tk variables
focus_var = tk.IntVar(value=3)
sleep_var = tk.IntVar(value=3)
comp_var = tk.IntVar(value=3)
mem_var = tk.IntVar(value=3)
stress_var = tk.IntVar(value=3)

# Sliders
make_scale(app, "Focus Level (1–5)", focus_var)
make_scale(app, "Sleepiness (1–5)", sleep_var)
make_scale(app, "Comprehension Speed (1–5)", comp_var)
make_scale(app, "Memory Strength (1–5)", mem_var)
make_scale(app, "Stress Level (1–5)", stress_var)

# Button
tk.Button(
    app,
    text="Analyze Fog Level",
    font=("Calibri", 15, "bold"),
    padx=10, pady=6,
    bg="#5aa9ff",
    fg="white",
    command=run_evaluation
).pack(pady=30)

app.mainloop()
