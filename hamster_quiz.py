# hamster_quiz.py - Викторина про хомяков (С ЗАЩИТОЙ ОТ ЗАКРЫТИЯ)
import tkinter as tk
from tkinter import messagebox
import json
import os
from pathlib import Path

# Путь для сохранения статуса прохождения теста
STATUS_FILE = Path(os.getenv('APPDATA')) / "hamster_unlock.json"

def mark_test_passed():
    """Отмечает, что тест пройден"""
    try:
        with open(STATUS_FILE, 'w') as f:
            json.dump({"passed": True}, f)
        return True
    except:
        return False

def show_hamster_test():
    root = tk.Tk()
    root.title("🐹 ТЕСТ О ХОМЯКАХ 🐹")
    root.geometry("600x500")
    root.configure(bg='#2d2d2d')
    
    # ЗАЩИТА ОТ ЗАКРЫТИЯ ОКНА
    def on_closing():
        messagebox.showwarning(
            "⚠ ДОСТУП ЗАБЛОКИРОВАН ⚠",
            "НЕЛЬЗЯ ЗАКРЫТЬ ОКНО!\n\n"
            "Твой компьютер заражён вирусом-хомяком!\n"
            "Единственный способ выйти — ПРОЙТИ ВЕСЬ ТЕСТ до конца!\n"
            "Вирус будет возвращаться при каждой перезагрузке, пока тест не будет пройден."
        )
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Вопросы (5 штук, как просил учитель)
    questions = [
        {
            "q": "Сколько часов в день спит хомяк?",
            "options": ["2-4 часа", "6-8 часа", "10-14 часов", "18-20 часов"],
            "correct": 2,
            "fact": "🐹 Хомяки спят 10-14 часов в сутки!"
        },
        {
            "q": "Что НЕЛЬЗЯ давать хомяку?",
            "options": ["Семечки", "Яблоко", "Шоколад", "Огурец"],
            "correct": 2,
            "fact": "🍫 Шоколад ядовит для хомяков!"
        },
        {
            "q": "Как называются щёки хомяка для еды?",
            "options": ["Сумки", "Защёчные мешки", "Карманы", "Кладовки"],
            "correct": 1,
            "fact": "👜 Защёчные мешки могут растягиваться до размера самого хомяка!"
        },
        {
            "q": "Сколько зубов у хомяка?",
            "options": ["4", "8", "16", "32"],
            "correct": 2,
            "fact": "🦷 У хомяков 16 зубов, и они растут всю жизнь!"
        },
        {
            "q": "Какой длины сирийский хомяк?",
            "options": ["3-5 см", "7-10 см", "13-18 см", "25-30 см"],
            "correct": 2,
            "fact": "📏 Сирийские хомяки вырастают до 13-18 см!"
        }
    ]
    
    score = 0
    current = 0
    
    # Интерфейс
    title_frame = tk.Frame(root, bg='#2d2d2d')
    title_frame.pack(fill='x', pady=15)
    
    tk.Label(title_frame, text="🤣 ХА-ХА-ХА! ТЫ ПОПАЛСЯ! 🤣", 
             font=("Arial", 16, "bold"), bg='#2d2d2d', fg='red').pack()
    
    tk.Label(title_frame, text="ТВОЙ КОМПЬЮТЕР ЗАРАЖЁН ВИРУСОМ-ХОМЯКОМ!", 
             font=("Arial", 11, "bold"), bg='#2d2d2d', fg='orange').pack(pady=5)
    
    tk.Label(title_frame, text="Единственный способ разблокировки — пройти тест о хомяках!\n"
             "Окно НЕЛЬЗЯ ЗАКРЫТЬ до завершения теста.",
             font=("Arial", 9), bg='#2d2d2d', fg='yellow').pack(pady=5)
    
    # Рамка для вопросов
    frame = tk.Frame(root, bg='#3d3d3d', relief='ridge', bd=3)
    frame.pack(pady=15, padx=20, fill='both', expand=True)
    
    q_label = tk.Label(frame, text="", font=("Arial", 12, "bold"), 
                       bg='#3d3d3d', fg='white', wraplength=500)
    q_label.pack(pady=20)
    
    option_btns = []
    for i in range(4):
        btn = tk.Button(frame, text="", font=("Arial", 10), bg='#555', fg='white',
                       padx=15, pady=5, width=40, cursor='hand2')
        btn.pack(pady=4)
        option_btns.append(btn)
        btn.config(command=lambda i=i: check_answer(i))
    
    feedback = tk.Label(frame, text="🤔 Выбери правильный ответ...", 
                        font=("Arial", 10), bg='#3d3d3d', fg='lightgreen', wraplength=500)
    feedback.pack(pady=10)
    
    next_btn = tk.Button(root, text="Следующий вопрос →", font=("Arial", 11, "bold"), 
                         bg='#444', fg='white', padx=20, pady=6, state='disabled',
                         command=next_question)
    next_btn.pack(pady=10)
    
    progress_label = tk.Label(root, text="", bg='#2d2d2d', fg='gray', font=("Arial", 9))
    progress_label.pack(pady=5)
    
    warning_label = tk.Label(root, text="⚠ НЕ ПЫТАЙСЯ ЗАКРЫТЬ ОКНО — ЭТО НЕ ПОМОЖЕТ! ⚠", 
                             font=("Arial", 8, "bold"), bg='#2d2d2d', fg='red')
    warning_label.pack(pady=10)
    
    def check_answer(idx):
        nonlocal score
        q = questions[current]
        
        if idx == q["correct"]:
            score += 1
            feedback.config(text=f"✅ ПРАВИЛЬНО! {q['fact']}", fg='#88ff88')
        else:
            correct_text = q["options"][q["correct"]]
            feedback.config(text=f"❌ НЕПРАВИЛЬНО! Правильно: {correct_text}\n{q['fact']}", fg='#ff8888')
        
        # Блокируем кнопки после ответа
        for btn in option_btns:
            btn.config(state='disabled')
        
        next_btn.config(state='normal')
    
    def next_question():
        nonlocal current
        current += 1
        
        if current < len(questions):
            update_question()
        else:
            end_test()
    
    def update_question():
        q = questions[current]
        q_label.config(text=q["q"])
        
        for i, btn in enumerate(option_btns):
            btn.config(text=q["options"][i], state='normal', bg='#555')
        
        feedback.config(text="🤔 Выбери ответ...", fg='lightgreen')
        next_btn.config(state='disabled')
        progress_label.config(text=f"Вопрос {current + 1} из {len(questions)}")
    
    def end_test():
        percent = (score / len(questions)) * 100
        
        # Очищаем окно
        for widget in root.winfo_children():
            widget.destroy()
        
        root.configure(bg='#1a3d1a')
        
        if percent >= 80:  # Нужно 4 из 5 правильных (80%)
            # Помечаем, что тест пройден
            mark_test_passed()
            
            tk.Label(root, text="🎉 ПОЗДРАВЛЯЮ! 🎉", 
                    font=("Arial", 24, "bold"), bg='#1a3d1a', fg='gold').pack(pady=40)
            
            tk.Label(root, text=f"Ты набрал {score} из {len(questions)} ({int(percent)}%)",
                    font=("Arial", 14), bg='#1a3d1a', fg='white').pack()
            
            tk.Label(root, text="\nТеперь ты достаточно знаешь о хомяках!\n"
                    "Вирус уничтожен! Компьютер разблокирован.\n"
                    "Нажми 'Выйти' для завершения.\n\n"
                    "PS: Вирус больше не побеспокоит тебя даже после перезагрузки!",
                    font=("Arial", 11), bg='#1a3d1a', fg='lightgreen', justify='center').pack(pady=20)
            
            # Кнопка выхода теперь работает (вирус уничтожен)
            def exit_and_unlock():
                root.destroy()
            
            tk.Button(root, text="✨ ВЫЙТИ (КОМПЬЮТЕР РАЗБЛОКИРОВАН) ✨", 
                     font=("Arial", 12, "bold"), bg='green', fg='white', 
                     padx=25, pady=10, command=exit_and_unlock).pack(pady=30)
        else:
            # Не прошёл тест — начинаем заново
            tk.Label(root, text="😭 ВЫ НЕ СДАЛИ ТЕСТ! 😭", 
                    font=("Arial", 20, "bold"), bg='#1a3d1a', fg='red').pack(pady=30)
            
            tk.Label(root, text=f"Твой результат: {score} из {len(questions)} ({int(percent)}%)\n"
                    "Нужно набрать 80% (4 из 5) для разблокировки.\n\n"
                    "ВИРУС ОСТАЁТСЯ В СИСТЕМЕ!\n"
                    "При перезагрузке компьютера вирус запустится снова.\n\n"
                    "Попробуй ещё раз и ВНИМАТЕЛЬНО читай вопросы!",
                    font=("Arial", 11), bg='#1a3d1a', fg='yellow', justify='center').pack(pady=20)
            
            # Кнопка перезапуска теста
            tk.Button(root, text="🔄 ПРОЙТИ ТЕСТ ЗАНОВО 🔄", 
                     font=("Arial", 12, "bold"), bg='orange', fg='black', 
                     padx=20, pady=8, command=restart_test).pack(pady=20)
    
    def restart_test():
        """Перезапускает тест"""
        root.destroy()
        show_hamster_test()
    
    update_question()
    root.mainloop()

if __name__ == "__main__":
    show_hamster_test()
