# hamster_quiz.py - Викторина про хомяков (ПОЛНАЯ БЛОКИРОВКА ЗАКРЫТИЯ)
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

class HamsterQuiz:
    def __init__(self):
        self.root = None
        self.score = 0
        self.current = 0
        self.questions = [
            {
                "q": "Сколько часов в день спит хомяк?",
                "options": ["2-4 часа", "6-8 часов", "10-14 часов", "18-20 часов"],
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
    
    def disable_close(self):
        """Полностью блокирует все способы закрытия окна"""
        # Блокируем крестик
        self.root.protocol("WM_DELETE_WINDOW", self.show_warning)
        # Убираем кнопку "Выйти" из системного меню (Alt+F4)
        self.root.attributes('-disabled', False)
    
    def show_warning(self):
        """Показывает предупреждение при попытке закрыть"""
        messagebox.showerror(
            "🚨 ДОСТУП ЗАБЛОКИРОВАН 🚨",
            "НЕЛЬЗЯ ЗАКРЫТЬ ОКНО!\n\n"
            "Ваш компьютер заражён вирусом-хомяком!\n"
            "Единственный способ выйти — ПРОЙТИ ВЕСЬ ТЕСТ до конца!\n\n"
            "Попытка закрыть окно = вирус остаётся в системе!\n"
            "При перезагрузке ПК вирус запустится снова."
        )
    
    def create_window(self):
        """Создаёт окно с блокировкой"""
        self.root = tk.Tk()
        self.root.title("🐹 ВИРУС-ХОМЯК ЗАБЛОКИРОВАЛ КОМПЬЮТЕР 🐹")
        self.root.geometry("620x550")
        self.root.configure(bg='#2d2d2d')
        
        # Блокируем закрытие
        self.disable_close()
        
        # Запрещаем изменение размера
        self.root.resizable(False, False)
        
        # Заголовок
        tk.Label(self.root, text="🤣 ХА-ХА-ХА! ТЫ ПОПАЛСЯ! 🤣", 
                font=("Arial", 18, "bold"), bg='#2d2d2d', fg='red').pack(pady=15)
        
        tk.Label(self.root, text="🔒 ВАШ КОМПЬЮТЕР ЗАБЛОКИРОВАН ВИРУСОМ-ХОМЯКОМ 🔒", 
                font=("Arial", 12, "bold"), bg='#2d2d2d', fg='orange').pack()
        
        tk.Label(self.root, text="\nЕдинственный способ разблокировки — пройти тест на знание повадок хомяков!\n"
                "Окно НЕЛЬЗЯ ЗАКРЫТЬ! Крестик не работает, Alt+F4 не работает.\n"
                "Только ПОЛНОЕ прохождение теста спасёт ваш компьютер!\n",
                font=("Arial", 9), bg='#2d2d2d', fg='yellow', justify='center').pack(pady=10)
        
        # Рамка для теста
        self.test_frame = tk.Frame(self.root, bg='#3d3d3d', relief='ridge', bd=3)
        self.test_frame.pack(pady=15, padx=20, fill='both', expand=True)
        
        self.q_label = tk.Label(self.test_frame, text="", font=("Arial", 12, "bold"), 
                                bg='#3d3d3d', fg='white', wraptext=500)
        self.q_label.pack(pady=20)
        
        self.options_frame = tk.Frame(self.test_frame, bg='#3d3d3d')
        self.options_frame.pack(pady=10)
        
        self.option_btns = []
        for i in range(4):
            btn = tk.Button(self.options_frame, text="", font=("Arial", 10), 
                           bg='#555555', fg='white', width=45, pady=5,
                           cursor='hand2')
            btn.pack(pady=4)
            self.option_btns.append(btn)
            btn.config(command=lambda i=i: self.check_answer(i))
        
        self.feedback = tk.Label(self.test_frame, text="🤔 Выбери правильный ответ...", 
                                 font=("Arial", 10), bg='#3d3d3d', fg='lightgreen', wraplength=500)
        self.feedback.pack(pady=10)
        
        self.next_btn = tk.Button(self.root, text="Следующий вопрос →", 
                                  font=("Arial", 11, "bold"), bg='#444444', fg='white',
                                  state='disabled', command=self.next_question)
        self.next_btn.pack(pady=10)
        
        self.progress_label = tk.Label(self.root, text="", bg='#2d2d2d', fg='gray', font=("Arial", 9))
        self.progress_label.pack(pady=5)
        
        # КРАСНОЕ ПРЕДУПРЕЖДЕНИЕ
        warning_frame = tk.Frame(self.root, bg='red', height=35)
        warning_frame.pack(fill='x', pady=10)
        warning_frame.pack_propagate(False)
        
        tk.Label(warning_frame, text="⚠⚠⚠ НЕ ПЫТАЙСЯ ЗАКРЫТЬ ОКНО — ЭТО НЕ ПОМОЖЕТ! ⚠⚠⚠", 
                font=("Arial", 9, "bold"), bg='red', fg='white').pack(expand=True)
        
        self.update_question()
        self.root.mainloop()
    
    def check_answer(self, idx):
        q = self.questions[self.current]
        
        if idx == q["correct"]:
            self.score += 1
            self.feedback.config(text=f"✅ ПРАВИЛЬНО! {q['fact']}", fg='#88ff88')
        else:
            correct_text = q["options"][q["correct"]]
            self.feedback.config(text=f"❌ НЕПРАВИЛЬНО! Правильно: {correct_text}\n{q['fact']}", fg='#ff8888')
        
        for btn in self.option_btns:
            btn.config(state='disabled')
        
        self.next_btn.config(state='normal')
    
    def next_question(self):
        self.current += 1
        
        if self.current < len(self.questions):
            self.update_question()
        else:
            self.end_test()
    
    def update_question(self):
        q = self.questions[self.current]
        self.q_label.config(text=q["q"])
        
        for i, btn in enumerate(self.option_btns):
            btn.config(text=q["options"][i], state='normal', bg='#555555')
        
        self.feedback.config(text="🤔 Выбери ответ...", fg='lightgreen')
        self.next_btn.config(state='disabled')
        self.progress_label.config(text=f"Вопрос {self.current + 1} из {len(self.questions)}")
    
    def end_test(self):
        percent = (self.score / len(self.questions)) * 100
        
        # Очищаем окно
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.configure(bg='#1a3d1a')
        
        if percent >= 80:  # Нужно 4 из 5 (80%)
            # Помечаем, что тест пройден
            mark_test_passed()
            
            tk.Label(self.root, text="🎉 ПОЗДРАВЛЯЮ! 🎉", 
                    font=("Arial", 26, "bold"), bg='#1a3d1a', fg='gold').pack(pady=40)
            
            tk.Label(self.root, text=f"Твой результат: {self.score} из {len(self.questions)} ({int(percent)}%)",
                    font=("Arial", 14), bg='#1a3d1a', fg='white').pack()
            
            tk.Label(self.root, text="\n🌟 Теперь ты достаточно знаешь о хомяках! 🌟\n"
                    "Вирус уничтожен! Компьютер разблокирован.\n\n"
                    "Можешь закрыть окно — вирус больше не вернётся,\n"
                    "даже после перезагрузки компьютера!",
                    font=("Arial", 11), bg='#1a3d1a', fg='lightgreen', justify='center').pack(pady=20)
            
            # Теперь кнопка закрытия работает
            self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
            
            exit_btn = tk.Button(self.root, text="✨ ВЫЙТИ (КОМПЬЮТЕР РАЗБЛОКИРОВАН) ✨", 
                                font=("Arial", 12, "bold"), bg='green', fg='white', 
                                padx=25, pady=10, command=self.root.destroy)
            exit_btn.pack(pady=30)
        else:
            tk.Label(self.root, text="😭 ВЫ НЕ СДАЛИ ТЕСТ! 😭", 
                    font=("Arial", 20, "bold"), bg='#1a3d1a', fg='red').pack(pady=30)
            
            tk.Label(self.root, text=f"Твой результат: {self.score} из {len(self.questions)} ({int(percent)}%)\n"
                    "Нужно набрать 80% (4 из 5) для разблокировки.\n\n"
                    "❌ ВИРУС ОСТАЁТСЯ В СИСТЕМЕ! ❌\n"
                    "При перезагрузке компьютера вирус запустится снова.\n"
                    "Закрыть окно НЕЛЬЗЯ! Ты должен пройти тест.\n\n"
                    "Попробуй ещё раз и ВНИМАТЕЛЬНО читай вопросы!",
                    font=("Arial", 11), bg='#1a3d1a', fg='yellow', justify='center').pack(pady=20)
            
            retry_btn = tk.Button(self.root, text="🔄 ПРОЙТИ ТЕСТ ЗАНОВО 🔄", 
                                 font=("Arial", 12, "bold"), bg='orange', fg='black', 
                                 padx=20, pady=8, command=self.restart_test)
            retry_btn.pack(pady=20)
    
    def restart_test(self):
        """Перезапускает тест"""
        self.root.destroy()
        new_quiz = HamsterQuiz()
        new_quiz.create_window()
    
    def run(self):
        self.create_window()

if __name__ == "__main__":
    quiz = HamsterQuiz()
    quiz.run()
