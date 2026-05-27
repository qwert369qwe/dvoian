# hamster_quiz.py - ПОЛНАЯ РАБОЧАЯ ВИКТОРИНА
import tkinter as tk
from tkinter import messagebox
import json
import os
from pathlib import Path

STATUS_FILE = Path(os.getenv('APPDATA')) / "hamster_unlock.json"

def mark_test_passed():
    try:
        with open(STATUS_FILE, 'w') as f:
            json.dump({"passed": True}, f)
    except:
        pass

# Вопросы
questions = [
    ("Сколько часов в день спит хомяк?", ["2-4 часа", "6-8 часов", "10-14 часов", "18-20 часов"], 2, "Хомяки спят 10-14 часов!"),
    ("Что НЕЛЬЗЯ давать хомяку?", ["Семечки", "Яблоко", "Шоколад", "Огурец"], 2, "Шоколад ядовит для хомяков!"),
    ("Как называются щёки хомяка для еды?", ["Сумки", "Защёчные мешки", "Карманы", "Кладовки"], 1, "Защёчные мешки!"),
    ("Сколько зубов у хомяка?", ["4", "8", "16", "32"], 2, "У хомяков 16 зубов!"),
    ("Какой длины сирийский хомяк?", ["3-5 см", "7-10 см", "13-18 см", "25-30 см"], 2, "13-18 см!")
]

score = 0
current = 0
root = None
option_btns = []

def on_closing():
    """Блокирует закрытие окна"""
    messagebox.showwarning("⚠ ЗАКРЫТЬ НЕЛЬЗЯ ⚠", 
                          "Ты не можешь закрыть окно!\n"
                          "Пройди тест до конца, чтобы разблокировать компьютер.")

def check_answer(idx):
    global score, current
    
    q_text, opts, correct, fact = questions[current]
    
    if idx == correct:
        score += 1
        feedback.config(text=f"✅ Правильно! {fact}", fg='lightgreen')
    else:
        feedback.config(text=f"❌ Неправильно! Правильно: {opts[correct]}\n{fact}", fg='#ff8888')
    
    for btn in option_btns:
        btn.config(state='disabled')
    
    next_btn.config(state='normal')

def next_question():
    global current
    
    current += 1
    
    if current < len(questions):
        update_question()
    else:
        end_test()

def update_question():
    q_text, opts, correct, fact = questions[current]
    q_label.config(text=q_text)
    
    for i, btn in enumerate(option_btns):
        btn.config(text=opts[i], state='normal', bg='#555')
    
    feedback.config(text="🤔 Выбери ответ...", fg='yellow')
    next_btn.config(state='disabled')
    progress.config(text=f"Вопрос {current + 1} из {len(questions)}")

def end_test():
    global root
    
    percent = (score / len(questions)) * 100
    
    for widget in root.winfo_children():
        widget.destroy()
    
    root.configure(bg='#1a3d1a')
    
    if percent >= 80:
        mark_test_passed()
        
        tk.Label(root, text="🎉 ПОЗДРАВЛЯЮ! 🎉", 
                font=("Arial", 20, "bold"), bg='#1a3d1a', fg='gold').pack(pady=40)
        
        tk.Label(root, text=f"Результат: {score} из {len(questions)} ({int(percent)}%)",
                font=("Arial", 14), bg='#1a3d1a', fg='white').pack()
        
        tk.Label(root, text="\nВирус уничтожен! Компьютер разблокирован.",
                font=("Arial", 12), bg='#1a3d1a', fg='lightgreen').pack(pady=20)
        
        tk.Button(root, text="✨ ВЫЙТИ ✨", font=("Arial", 12, "bold"),
                 bg='green', fg='white', padx=30, pady=10, command=root.destroy).pack(pady=30)
    else:
        tk.Label(root, text="😭 ТЕСТ НЕ СДАН! 😭", 
                font=("Arial", 18, "bold"), bg='#1a3d1a', fg='red').pack(pady=30)
        
        tk.Label(root, text=f"Результат: {score} из {len(questions)} ({int(percent)}%)\n"
                "Нужно 80% (4 из 5) для разблокировки.\n\n"
                "Нажми кнопку, чтобы пройти тест заново.",
                font=("Arial", 11), bg='#1a3d1a', fg='yellow', justify='center').pack(pady=20)
        
        tk.Button(root, text="🔄 ПРОЙТИ ЗАНОВО 🔄", 
                 font=("Arial", 12, "bold"), bg='orange', fg='black',
                 padx=20, pady=10, command=restart_test).pack(pady=20)

def restart_test():
    global score, current, root
    score = 0
    current = 0
    root.destroy()
    show_hamster_test()

def show_hamster_test():
    global root, q_label, option_btns, feedback, next_btn, progress
    
    root = tk.Tk()
    root.title("🐹 ВИРУС-ХОМЯК 🐹")
    root.geometry("600x550")
    root.configure(bg='#2d2d2d')
    root.resizable(False, False)
    
    # БЛОКИРУЕМ ЗАКРЫТИЕ
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    tk.Label(root, text="🤣 ХА-ХА-ХА! ТЫ ПОПАЛСЯ! 🤣", 
            font=("Arial", 18, "bold"), bg='#2d2d2d', fg='red').pack(pady=15)
    
    tk.Label(root, text="Твой компьютер заражён!\nПройди тест о хомяках, чтобы разблокировать.",
            font=("Arial", 11), bg='#2d2d2d', fg='white', justify='center').pack()
    
    frame = tk.Frame(root, bg='#3d3d3d', relief='ridge', bd=2)
    frame.pack(pady=15, padx=20, fill='both', expand=True)
    
    q_label = tk.Label(frame, text="", font=("Arial", 12, "bold"), 
                       bg='#3d3d3d', fg='white', wraplength=500)
    q_label.pack(pady=20)
    
    option_btns = []
    for i in range(4):
        btn = tk.Button(frame, text="", font=("Arial", 10), bg='#555', fg='white',
                       padx=15, pady=5, width=45, cursor='hand2')
        btn.pack(pady=4)
        option_btns.append(btn)
        btn.config(command=lambda i=i: check_answer(i))
    
    feedback = tk.Label(frame, text="🤔 Выбери ответ...", 
                        font=("Arial", 10), bg='#3d3d3d', fg='yellow')
    feedback.pack(pady=10)
    
    next_btn = tk.Button(root, text="Следующий вопрос →", font=("Arial", 11, "bold"), 
                         bg='#444', fg='white', state='disabled', command=next_question)
    next_btn.pack(pady=10)
    
    progress = tk.Label(root, text="", bg='#2d2d2d', fg='gray', font=("Arial", 9))
    progress.pack(pady=5)
    
    tk.Label(root, text="⚠ НЕ ПЫТАЙСЯ ЗАКРЫТЬ ОКНО! ⚠", 
            font=("Arial", 9, "bold"), bg='#2d2d2d', fg='red').pack(pady=10)
    
    update_question()
    root.mainloop()

if __name__ == "__main__":
    show_hamster_test()
