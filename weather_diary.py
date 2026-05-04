import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# ========== GitHub репозиторий ==========
GITHUB_URL = "https://github.com/ваш_логин/weather-diary"  # Замените на свой

class WeatherDiary:
    """
    Приложение "Дневник погоды".
    Позволяет добавлять, просматривать и фильтровать записи о погоде.
    Данные сохраняются в JSON-файл.
    """
    
    def __init__(self):
        # Создание главного окна
        self.window = tk.Tk()
        self.window.title("🌤️ Weather Diary - Дневник погоды")
        self.window.geometry("800x600")
        self.window.configure(bg="#e8f4f8")
        
        # Загрузка данных из файла
        self.entries = self.load_data()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление таблицы
        self.update_table()
        
    # ========== Работа с JSON ==========
    def load_data(self):
        """Загружает записи из JSON-файла."""
        try:
            with open("weather_data.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_data(self):
        """Сохраняет записи в JSON-файл."""
        with open("weather_data.json", "w", encoding="utf-8") as file:
            json.dump(self.entries, file, ensure_ascii=False, indent=4)
    
    # ========== Интерфейс ==========
    def create_widgets(self):
        """Создаёт все элементы интерфейса."""
        
        # ===== Заголовок =====
        title_label = tk.Label(
            self.window,
            text="🌦️ Weather Diary - Дневник погоды",
            font=("Arial", 18, "bold"),
            bg="#e8f4f8",
            fg="#2c3e50"
        )
        title_label.pack(pady=10)
        
        # ===== Фрейм для ввода данных =====
        input_frame = tk.LabelFrame(
            self.window,
            text="📝 Добавить новую запись",
            font=("Arial", 12, "bold"),
            bg="#e8f4f8",
            fg="#2c3e50",
            padx=10,
            pady=10
        )
        input_frame.pack(pady=10, padx=20, fill="x")
        
        # Дата
        tk.Label(input_frame, text="📅 Дата (ГГГГ-ММ-ДД):", bg="#e8f4f8").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.date_entry = tk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Температура
        tk.Label(input_frame, text="🌡️ Температура (°C):", bg="#e8f4f8").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.temp_entry = tk.Entry(input_frame, width=10)
        self.temp_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Описание
        tk.Label(input_frame, text="📝 Описание:", bg="#e8f4f8").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.desc_entry = tk.Entry(input_frame, width=40)
        self.desc_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="w")
        
        # Осадки
        self.precipitation_var = tk.BooleanVar()
        precip_check = tk.Checkbutton(
            input_frame,
            text="🌧️ Осадки (да/нет)",
            variable=self.precipitation_var,
            bg="#e8f4f8"
        )
        precip_check.grid(row=1, column=4, padx=5, pady=5)
        
        # Кнопка "Добавить запись"
        add_button = tk.Button(
            input_frame,
            text="➕ Добавить запись",
            command=self.add_entry,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        add_button.grid(row=2, column=0, columnspan=5, pady=10)
        
        # ===== Фрейм для фильтрации =====
        filter_frame = tk.LabelFrame(
            self.window,
            text="🔍 Фильтрация записей",
            font=("Arial", 12, "bold"),
            bg="#e8f4f8",
            fg="#2c3e50",
            padx=10,
            pady=10
        )
        filter_frame.pack(pady=10, padx=20, fill="x")
        
        # Фильтр по дате
        tk.Label(filter_frame, text="📅 Фильтр по дате:", bg="#e8f4f8").grid(row=0, column=0, padx=5, pady=5)
        self.filter_date_entry = tk.Entry(filter_frame, width=15)
        self.filter_date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.filter_date_entry.insert(0, "")
        
        # Фильтр по температуре
        tk.Label(filter_frame, text="🌡️ Фильтр по температуре (>):", bg="#e8f4f8").grid(row=0, column=2, padx=5, pady=5)
        self.filter_temp_entry = tk.Entry(filter_frame, width=10)
        self.filter_temp_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Кнопка "Применить фильтр"
        filter_button = tk.Button(
            filter_frame,
            text="🔍 Применить фильтр",
            command=self.apply_filter,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        filter_button.grid(row=0, column=4, padx=10, pady=5)
        
        # Кнопка "Сбросить фильтр"
        reset_button = tk.Button(
            filter_frame,
            text="🔄 Сбросить фильтр",
            command=self.reset_filter,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        reset_button.grid(row=0, column=5, padx=10, pady=5)
        
        # ===== Таблица для отображения записей =====
        table_frame = tk.Frame(self.window, bg="#e8f4f8")
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview (таблица)
        columns = ("date", "temperature", "description", "precipitation")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        # Настройка колонок
        self.tree.heading("date", text="📅 Дата")
        self.tree.heading("temperature", text="🌡️ Температура (°C)")
        self.tree.heading("description", text="📝 Описание")
        self.tree.heading("precipitation", text="🌧️ Осадки")
        
        self.tree.column("date", width=120)
        self.tree.column("temperature", width=120)
        self.tree.column("description", width=300)
        self.tree.column("precipitation", width=80)
        
        self.tree.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Кнопка "Удалить выбранное"
        delete_button = tk.Button(
            self.window,
            text="🗑️ Удалить выбранную запись",
            command=self.delete_entry,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        delete_button.pack(pady=5)
        
        # Строка с ссылкой на GitHub
        github_label = tk.Label(
            self.window,
            text=f"📂 GitHub: {GITHUB_URL}",
            font=("Arial", 8),
            bg="#e8f4f8",
            fg="#7f8c8d"
        )
        github_label.pack(side=tk.BOTTOM, pady=5)
    
    # ========== Логика работы ==========
    def add_entry(self):
        """Добавляет новую запись в дневник."""
        date = self.date_entry.get().strip()
        temp = self.temp_entry.get().strip()
        description = self.desc_entry.get().strip()
        precipitation = "Да" if self.precipitation_var.get() else "Нет"
        
        # Валидация
        if not date:
            messagebox.showwarning("Ошибка", "Введите дату!")
            return
        
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Ошибка", "Неверный формат даты! Используйте ГГГГ-ММ-ДД")
            return
        
        if not temp:
            messagebox.showwarning("Ошибка", "Введите температуру!")
            return
        
        try:
            temp_float = float(temp)
        except ValueError:
            messagebox.showwarning("Ошибка", "Температура должна быть числом!")
            return
        
        if not description:
            messagebox.showwarning("Ошибка", "Введите описание погоды!")
            return
        
        # Добавление записи
        new_entry = {
            "date": date,
            "temperature": temp_float,
            "description": description,
            "precipitation": precipitation
        }
        self.entries.append(new_entry)
        self.save_data()
        
        # Очистка полей
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precipitation_var.set(False)
        
        # Обновление таблицы
        self.update_table()
        
        messagebox.showinfo("Успех", "Запись добавлена!")
    
    def delete_entry(self):
        """Удаляет выбранную запись."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите запись для удаления!")
            return
        
        index = int(selected[0])
        removed = self.entries.pop(index)
        self.save_data()
        self.update_table()
        
        messagebox.showinfo("Удалено", f"Запись от {removed['date']} удалена!")
    
    def update_table(self, filtered_entries=None):
        """Обновляет таблицу записей."""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Данные для отображения
        display_entries = filtered_entries if filtered_entries is not None else self.entries
        
        # Заполнение таблицы
        for i, entry in enumerate(display_entries):
            self.tree.insert("", tk.END, iid=i, values=(
                entry["date"],
                entry["temperature"],
                entry["description"],
                entry["precipitation"]
            ))
    
    def apply_filter(self):
        """Применяет фильтрацию записей."""
        filter_date = self.filter_date_entry.get().strip()
        filter_temp_str = self.filter_temp_entry.get().strip()
        
        filtered = self.entries.copy()
        
        # Фильтр по дате
        if filter_date:
            try:
                datetime.strptime(filter_date, "%Y-%m-%d")
                filtered = [e for e in filtered if e["date"] == filter_date]
            except ValueError:
                messagebox.showwarning("Ошибка", "Неверный формат даты в фильтре!")
                return
        
        # Фильтр по температуре (>)
        if filter_temp_str:
            try:
                filter_temp = float(filter_temp_str)
                filtered = [e for e in filtered if e["temperature"] > filter_temp]
            except ValueError:
                messagebox.showwarning("Ошибка", "Температура фильтра должна быть числом!")
                return
        
        self.update_table(filtered)
        
        if filtered:
            messagebox.showinfo("Фильтр", f"Найдено {len(filtered)} записей")
        else:
            messagebox.showinfo("Фильтр", "Записей не найдено")
    
    def reset_filter(self):
        """Сбрасывает фильтрацию."""
        self.filter_date_entry.delete(0, tk.END)
        self.filter_temp_entry.delete(0, tk.END)
        self.update_table()
    
    def run(self):
        """Запускает главный цикл приложения."""
        self.window.mainloop()


# ========== Запуск программы ==========
if __name__ == "__main__":
    app = WeatherDiary()
    app.run()