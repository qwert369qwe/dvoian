# hamster_quiz.py - Викторина про хомяков (РАБОЧАЯ ВЕРСИЯ)
import tkinter as tk
from tkinter import messagebox
import json
import os
from pathlib import Path

# Путь для сохранения статуса
STATUS_FILE = Path(os.getenv('APPDATA')) / "hamster_unlock.json"

def mark_test_passed():
    try:
        with open(STATUS_FILE, 'w') as f:
            json.dump({"passed": True}, f)
        return True
    except:
        return False

# Вопросы
questions = [
    {
        "q": "Сколько часов в день спит хомяк?",
        "options": ["2-4 часа", "6-8 часов", "10-14 часов", "18-20 часов"],
        "correct": 2,
        "fact": "Хомяки спят 10-14 часов в сутки!"
    },
    {
        "q": "Что НЕЛЬЗЯ давать хомяку?",
        "options": ["Семечки", "Яблоко", "Шоколад", "Огурец"],
        "correct": 2,
        "fact": "Шоколад ядовит для хомяков!"
    },
    {
        "q": "Как называются щёки хомяка для еды?",
        "options": ["Сумки", "Защёчные мешки", "Карманы", "Кладовки"],
        "correct": 1,
        "fact": "Защёчные мешки могут растягиваться до размера самого хомяка!"
    },
    {
        "q": "Сколько зубов у хомяка?",
        "options": ["4", "8", "16", "32"],
        "correct": 2,
        "fact": "У хомяков 16 зубов, и они растут всю жизнь!"
    },
    {
        "q": "Какой длины сирийский хомяк?",
        "options": ["3-5 см", "7-10 см", "13-18 см", "25-30 см"],
        "correct": 2,
        "fact": "Сирийские хомяки вырастают до 13-18 см!"
    }
]

score = 0
current = 0
root = None

def show_warning():
    """Предупреждение при попытке закрыть окно"""
    messagebox.showwarning(
        "⚠ НЕЛЬЗЯ ЗАКРЫТЬ! ⚠",
        "Твой компьютер заражён вирусом-хомяком!\n"
        "Единственный способ выйти — ПРОЙТИ ВЕСЬ ТЕСТ!\n\n"
        "Попробуй закрыть снова — ничего не изменится."
    )

def check_answer(idx):
    global score, current
    
    q = questions[current]
    
    if idx == q["correct"]:
        score += 1
        feedback.config(text=f"✅ ПРАВИЛЬНО! {q['fact']}", fg='lightgreen')
    else:
        correct_text = q["options"][q["correct"]]
        feedback.config(text=f"❌ НЕПРАВИЛЬНО! Правильно: {correct_text}\n{q['fact']}", fg='#ff8888')
    
    # Блокируем кнопки
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
    q = questions[current]
    q_label.config(text=q["q"])
    
    for i, btn in enumerate(option_btns):
        btn.config(text=q["options"][i], state='normal', bg='#555555')
    
    feedback.config(text="🤔 Выбери ответ...", fg='yellow')
    next_btn.config(state='disabled')
    progress_label.config(text=f"Вопрос {current + 1} из {len(questions)}")

def end_test():
    global root
    
    percent = (score / len(questions)) * 100
    
    # Очищаем окно
    for widget in root.winfo_children():
        widget.destroy()
    
    root.configure(bg='#1a3d1a')
    
    if percent >= 80:
        # Тест пройден
        mark_test_passed()
        
        tk.Label(root, text="🎉 ПОЗДРАВЛЯЮ! 🎉", 
                font=("Arial", 20, "bold"), bg='#1a3d1a', fg='gold').pack(pady=40)
        
        tk.Label(root, text=f"Ты набрал {score} из {len(questions)} ({int(percent)}%)",
                font=("Arial", 14), bg='#1a3d1a', fg='white').pack()
        
        tk.Label(root, text="\nВирус уничтожен! Компьютер разблокирован.\n"
                "Теперь можно закрыть окно.",
                font=("Arial", 11), bg='#1a3d1a', fg='lightgreen').pack(pady=20)
        
        # Разрешаем закрыть окно
        root.protocol("WM_DELETE_WINDOW", root.destroy)
        
        tk.Button(root, text="✨ ВЫЙТИ ✨", font=("Arial", 12, "bold"),
                 bg='green', fg='white', padx=30, pady=10,
                 command=root.destroy).pack(pady=30)
    else:
        tk.Label(root, text="😭 ТЕСТ НЕ СДАН! 😭", 
                font=("Arial", 18, "bold"), bg='#1a3d1a', fg='red').pack(pady=30)
        
        tk.Label(root, text=f"Твой результат: {score} из {len(questions)} ({int(percent)}%)\n"
                "Нужно 80% (4 из 5) для разблокировки.\n\n"
                "Вирус остаётся в системе! Начни тест заново.",
                font=("Arial", 11), bg='#1a3d1a', fg='yellow', justify='center').pack(pady=20)
        
        tk.Button(root, text="🔄 ПРОЙТИ ТЕСТ ЗАНОВО 🔄", 
                 font=("Arial", 12, "bold"), bg='orange', fg='black',
                 padx=20, pady=10, command=restart_test).pack(pady=20)

def restart_test():
    """Перезапускает тест"""
    global score, current, root
    score = 0
    current = 0
    root.destroy()
    show_hamster_test()

def show_hamster_test():
    global root, q_label, option_btns, feedback, next_btn, progress_label
    
    root = tk.Tk()
    root.title("🐹 ВИРУС-ХОМЯК 🐹")
    root.geometry("600520")
    root.configure(bg='#2d2d2d')
    root.resizable(False, False)
    
    # Блокируем кнопку закрытия (крестик)
    root.protocol("WM_DELETE_WINDOW", show_warning)
    
    # Заголовок
    tk.Label(root, text="🤣 ХА-ХА-ХА! ТЫ ПОПАЛСЯ! 🤣", 
            font=("Arial", 16, "bold"), bg='#2d2d2d', fg='red').pack(pady=15)
    
    tk.Label(root, text="Твой компьютер заражён вирусом-хомяком!\n"
            "Пройди тест, чтобы разблокировать компьютер.",
            font=("Arial", 10), bg='#2d2d2d', fg='white', justify='center').pack()
    
    # Рамка для вопросов
    frame = tk.Frame(root, bg='#3d3d3d', relief='ridge', bd=2)
    frame.pack(pady=15, padx=20, fill='both', expand=True)
    
    q_label = tk.Label(frame, text="", font=("Arial", 12, "bold"), 
                       bg='#3d3d3d', fg='white', wraplength=500)
    q_label.pack(pady=20)
    
    option_btns = []
    for i in range(4):
        btn = tk.Button(frame, text="", font=("Arial", 10), bg='#555555', fg='white',
                       padx=15, pady=5, width=45, cursor='hand2')
        btn.pack(pady=4)
        option_btns.append(btn)
        btn.config(command=lambda i=i: check_answer(i))
    
    feedback = tk.Label(frame, text="🤔 Выбери правильный ответ...", 
                        font=("Arial", 10), bg='#3d3d3d', fg='yellow')
    feedback.pack(pady=10)
    
    next_btn = tk.Button(root, text="Следующий вопрос →", font=("Arial", 11, "bold"), 
                         bg='#444444', fg='white', state='disabled',
                         command=next_question)
    next_btn.pack(pady=10)
    
    progress_label = tk.Label(root, text="", bg='#2d2d2d', fg='gray', font=("Arial", 9))
    progress_label.pack(pady=5)
    
    tk.Label(root, text="⚠ НЕ ПЫТАЙСЯ ЗАКРЫТЬ ОКНО — ТЕСТ НУЖНО ПРОЙТИ! ⚠", 
            font=("Arial", 8, "bold"), bg='#2d2d2d', fg='red').pack(pady=10)
    
    update_question()
    root.mainloop()

if __name__ == "__main__":
    show_hamster_test()
