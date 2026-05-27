# hamster_quiz.py - Викторина про хомяков
import tkinter as tk

def show_hamster_test():
    root = tk.Tk()
    root.title("🐹 ТЕСТ О ХОМЯКАХ 🐹")
    root.geometry("550x450")
    root.configure(bg='#2d2d2d')
    
    # Вопросы
    questions = [
        ("Сколько часов в день спит хомяк?", ["2-4 часа", "6-8 часов", "10-14 часов", "18-20 часов"], 2, "Хомяки спят 10-14 часов!"),
        ("Что НЕЛЬЗЯ давать хомяку?", ["Семечки", "Яблоко", "Шоколад", "Огурец"], 2, "Шоколад ядовит для хомяков!"),
        ("Как называются щёки хомяка для еды?", ["Сумки", "Защёчные мешки", "Карманы", "Кладовки"], 1, "Защёчные мешки!"),
    ]
    
    score = 0
    current = 0
    
    def check_answer(idx):
        nonlocal score
        if idx == questions[current][2]:
            score += 1
            feedback.config(text=f"✅ Правильно! {questions[current][3]}", fg='lightgreen')
        else:
            correct = questions[current][1][questions[current][2]]
            feedback.config(text=f"❌ Неправильно! Правильно: {correct}\n{questions[current][3]}", fg='#ff8888')
        
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
        q_label.config(text=q[0])
        for i, btn in enumerate(option_btns):
            btn.config(text=q[1][i], state='normal')
        feedback.config(text="🤔 Выбери ответ...")
        next_btn.config(state='disabled')
        progress_label.config(text=f"Вопрос {current+1} из {len(questions)}")
    
    def end_test():
        for w in root.winfo_children():
            w.destroy()
        percent = (score / len(questions)) * 100
        tk.Label(root, text="🐹 РЕЗУЛЬТАТ ТЕСТА 🐹", font=("Arial", 16, "bold"), 
                bg='#2d2d2d', fg='yellow').pack(pady=40)
        tk.Label(root, text=f"Ты набрал {score} из {len(questions)} ({int(percent)}%)", 
                font=("Arial", 14), bg='#2d2d2d', fg='white').pack(pady=20)
        
        if percent == 100:
            msg = "🌟 Ты эксперт по хомякам! 🌟"
        elif percent >= 66:
            msg = "🎉 Неплохо! Но можно лучше! 🎉"
        else:
            msg = "📚 Почитай о хомяках и возвращайся! 🐹"
        
        tk.Label(root, text=msg, font=("Arial", 12), bg='#2d2d2d', fg='lightblue').pack(pady=20)
        tk.Button(root, text="Выйти", command=root.destroy, font=("Arial", 11), 
                 bg='red', fg='white', padx=20, pady=8).pack(pady=30)
    
    # Интерфейс
    tk.Label(root, text="🤣 ХА-ХА-ХА! ТЫ ПОПАЛСЯ! 🤣", font=("Arial", 16, "bold"), 
            bg='#2d2d2d', fg='red').pack(pady=15)
    tk.Label(root, text="Пройди тест на знание повадок хомяков!", 
            font=("Arial", 11), bg='#2d2d2d', fg='white').pack()
    
    frame = tk.Frame(root, bg='#3d3d3d', relief='groove', bd=2)
    frame.pack(pady=20, padx=20, fill='both', expand=True)
    
    q_label = tk.Label(frame, text="", font=("Arial", 12, "bold"), 
                       bg='#3d3d3d', fg='white', wraplength=450)
    q_label.pack(pady=20)
    
    option_btns = []
    for i in range(4):
        btn = tk.Button(frame, text="", font=("Arial", 10), bg='#555', fg='white',
                       padx=15, pady=5, width=35, cursor='hand2')
        btn.pack(pady=4)
        option_btns.append(btn)
        btn.config(command=lambda i=i: check_answer(i))
    
    feedback = tk.Label(frame, text="", font=("Arial", 10), bg='#3d3d3d', fg='yellow')
    feedback.pack(pady=10)
    
    next_btn = tk.Button(root, text="Следующий вопрос →", font=("Arial", 11), 
                         bg='#555', fg='white', padx=20, pady=6, command=next_question)
    next_btn.pack(pady=10)
    
    progress_label = tk.Label(root, text="", bg='#2d2d2d', fg='gray')
    progress_label.pack(pady=5)
    
    update_question()
    root.mainloop()

if __name__ == "__main__":
    show_hamster_test()
