"""
🎓 СИСТЕМА УПРАВЛЕНИЯ СТУДЕНТАМИ
===========================================================
Программа для автоматической обработки студенческих данных,
регистрации в базе данных и управления доступом.
"""

import re
import os
import json
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# КОНФИГУРАЦИЯ
# ─────────────────────────────────────────────────────────────

DATABASE_FILE = 'students_database.json'

# ─────────────────────────────────────────────────────────────
# ФУНКЦИИ РАБОТЫ С БАЗОЙ ДАННЫХ
# ─────────────────────────────────────────────────────────────

def load_database():
    """📂 Загружает базу данных студентов из JSON файла."""
    if os.path.exists(DATABASE_FILE):
        try:
            with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_database(data):
    """💾 Сохраняет базу данных студентов в JSON файл."""
    try:
        with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"❌ Ошибка при сохранении базы данных: {e}")
        return False

def find_student_in_database(name, group, id):
    """🔍 Ищет студента в базе данных по комбинации имени, группы и ID."""
    database = load_database()
    for student in database:
        if (student.get('name') == name and 
            student.get('group') == group and 
            student.get('id') == id):
            return student
    return None

def add_student_to_database(college, course, name, group, id):
    """👨‍🎓 Добавляет нового студента в базу данных с проверкой на дубликаты."""
    database = load_database()
    
    # Проверка на дубликаты
    for student in database:
        if (student.get('name') == name and 
            student.get('group') == group and 
            student.get('id') == id):
            print("❌ Этот студент уже есть в базе данных!")
            return False
    
    # Создание новой записи
    new_student = {
        'college': college,
        'course': course,
        'name': name,
        'group': group,
        'id': id,
        'registration_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 'новый студент'
    }
    
    database.append(new_student)
    
    if save_database(database):
        print("✅ Новый студент успешно добавлен в базу данных!")
        return True
    else:
        print("❌ Ошибка при добавлении в базу данных!")
        return False

# ─────────────────────────────────────────────────────────────
# ФУНКЦИИ АНАЛИЗА ФАЙЛОВ
# ─────────────────────────────────────────────────────────────

def parse_file(file_path):
    """📄 Анализирует текстовый файл и извлекает информацию о студенте."""
    college = course = name = group = id = None
    
    try:
        # Попытка чтения с разными кодировками
        encodings = ['utf-8', 'cp1251', 'koi8-r', 'iso-8859-1', 'windows-1251']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    content = file.read()
                    print(f"✅ Файл успешно прочитан с кодировкой: {encoding}")
                    break
            except UnicodeDecodeError:
                continue
        else:
            print("❌ Не удалось прочитать файл с доступными кодировками")
            return college, course, name, group, id
            
        # Регулярные выражения для извлечения данных
        patterns = {
            'college': [
                r'Колледж[:\s]*([^\n]+)', 
                r'College[:\s]*([^\n]+)', 
                r'Учебное заведение[:\s]*([^\n]+)'
            ],
            'course': [r'Курс[:\s]*([^\n]+)', r'Course[:\s]*([^\n]+)'],
            'name': [
                r'ФИ[:\s]*([^\n]+)', 
                r'ФИО[:\s]*([^\n]+)', 
                r'Name[:\s]*([^\n]+)', 
                r'Имя[:\s]*([^\n]+)'
            ],
            r'Имя[:\s]*([^\n]+)'
        'group': [
                r'Команда[:\s]*([^\n]+)', 
                r'Группа[:\s]*([^\n]+)', 
                r'Group[:\s]*([^\n]+)', 
                r'Team[:\s]*([^\n]+)'
            ],
        'id': [
                r'ID[:\s]*([^\n]+)', 
                r'ИД[:\s]*([^\n]+)', 
                r'Номер[:\s]*([^\n]+)', 
                r'№[:\s]*([^\n]+)'
            ]
        }
        
        # Поиск данных в содержимом файла
        for field_name, field_patterns in patterns.items():
            for pattern in field_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    value = match.group(1).strip()
                    if field_name == 'college': college = value
                    elif field_name == 'course': course = value
                    elif field_name == 'name': name = value
                    elif field_name == 'group': group = value
                    elif field_name == 'id': id = value
                    break
                
        # Вывод результатов анализа
        print("\n📋 Найденные данные в файле:")
        print("═" * 50)
        if college:    print(f"🏫 Колледж: {college}")
        if course:     print(f"📚 Курс: {course}")
        if name:       print(f"👤 ФИО: {name}")
        if group:      print(f"👥 Группа/Команда: {group}")
        if id:         print(f"🔢 ID: {id}")
        
        # Полное содержимое файла
        print("\n📄 Полное содержимое файла:")
        print("═" * 50)
        print(content)
        print("═" * 50)
                
    except FileNotFoundError:
        print(f"❌ Ошибка: Файл '{file_path}' не найден.")
    except Exception as e:
        print(f"❌ Ошибка при чтении файла: {e}")
    
    return college, course, name, group, id

# ─────────────────────────────────────────────────────────────
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ─────────────────────────────────────────────────────────────

def manual_input_missing_data(college, course, name, group, id):
    """⌨️ Запрашивает ручной ввод недостающих данных."""
    print("\n🔄 Заполнение недостающих данных вручную:")
    print("─" * 50)
    
    if not college:  college = input("Введите название колледжа: ").strip()
    if not course:   course = input("Введите курс: ").strip()
    if not name:     name = input("Введите ФИО студента: ").strip()
    if not group:    group = input("Введите группу/команду: ").strip()
    if not id:       id = input("Введите ID: ").strip()
    
    return college, course, name, group, id

def show_database_stats():
    """📊 Показывает статистику базы данных."""
    database = load_database()
    print(f"\n📊 Статистика базы данных:")
    print(f"Всего студентов: {len(database)}")
    
    if database:
        print("\nПоследние добавленные студенты:")
        for i, student in enumerate(database[-3:], 1):
            print(f"{i}. {student['name']} ({student['group']}) - {student['registration_date']}")

def register_new_student(college, course, name, group, id):
    """🎯 Процедура регистрации нового студента."""
    print("\n❌ ОШИБКА: СТУДЕНТ НЕ НАЙДЕН В БАЗЕ ДАННЫХ!")
    print("═" * 60)
    print("🚫 Доступ запрещен!")
    print("📋 Для получения доступа необходимо зарегистрироваться")
    print("═" * 60)
    
    print(f"\n📝 Проверьте данные для регистрации:")
    print(f"🏫 Колледж: {college}")
    print(f"📚 Курс: {course}")
    print(f"👤 ФИО: {name}")
    print(f"👥 Группа: {group}")
    print(f"🔢 ID: {id}")
    print("═" * 60)
    
    # Подтверждение данных
    confirm = input("✅ Все данные верны? (да/нет): ").strip().lower()
    if confirm not in ['да', 'yes', 'y', 'д']:
        print("\n🔄 Давайте исправим данные:")
        college, course, name, group, id = manual_input_missing_data(college, course, name, group, id)
    
    # Процесс регистрации
    print(f"\n🎯 РЕГИСТРАЦИЯ НОВОГО СТУДЕНТА")
    print("═" * 60)
    answer = input("📝 Хотите зарегистрировать этого студента? (да/нет): ").strip().lower()
    
    if answer in ['да', 'yes', 'y', 'д']:
        if add_student_to_database(college, course, name, group, id):
            print("\n🎉 РЕГИСТРАЦИЯ УСПЕШНА!")
            print("═" * 60)
            print(f"👤 {name}")
            print(f"🏫 {college}")
            print(f"📚 Курс {course}")
            print(f"👥 Группа {group}")
            print(f"🔢 ID: {id}")
            print("═" * 60)
            print("✅ Теперь вам доступны все функции системы!")
            print("🎓 Добро пожаловать в нашу образовательную систему!")
            return True
    else:
        print("❌ Регистрация отменена. Доступ запрещен.")
    
    return False

# ─────────────────────────────────────────────────────────────
# ГЛАВНАЯ ФУНКЦИЯ
# ─────────────────────────────────────────────────────────────

def main():
    """🎮 Главная функция программы - точка входа."""
    print("🎓 Программа для чтения и анализа файлов студентов")
    print("═" * 60)
    
    # Показываем статистику при запуске
    show_database_stats()
    
    while True:
        print("\n📝 Выберите действие:")
        print("1. Анализировать файл студента")
        print("2. Показать статистику базы данных")
        print("3. Выйти")
        
        choice = input("➡️  Ваш выбор (1-3): ").strip()
        
        if choice == '3':
            print("\n👋 До свидания!")
            break
            
        if choice == '2':
            show_database_stats()
            continue
            
        if choice == '1':
            print("\n📁 Выберите источник файла:")
            print("1. Ввести путь к файлу")
            print("2. Использовать файл по умолчанию (README002.md)")
            
            file_choice = input("➡️  Ваш выбор (1-2): ").strip()
            
            if file_choice == '1':
                file_path = input("📂 Введите полный путь к файлу: ").strip()
            elif file_choice == '2':
                file_path = 'README002.md'
            else:
                print("❌ Неверный выбор.")
                continue
        else:
            print("❌ Неверный выбор. Попробуйте снова.")
            continue
        
        if not os.path.exists(file_path):
            print(f"❌ Файл '{file_path}' не существует.")
            continue
        
        print(f"\n📖 Чтение файла: {file_path}")
        print("─" * 50)
        
        # Анализ файла
        college, course, name, group, id = parse_file(file_path)
        
        # Проверка полноты данных
        if not all([college, course, name, group, id]):
            print("\n⚠️  Не все данные найдены в файле.")
            answer = input("❓ Хотите ввести недостающие данные вручную? (да/нет): ").strip().lower()
            if answer in ['да', 'yes', 'y', 'д']:
                college, course, name, group, id = manual_input_missing_data(college, course, name, group, id)
            else:
                print("❌ Отмена операции. Не все данные доступны.")
                continue
        
        # Поиск студента в базе
        existing_student = find_student_in_database(name, group, id)
        
        if existing_student:
            print("\n✅ СТУДЕНТ НАЙДЕН В БАЗЕ ДАННЫХ!")
            print("═" * 50)
            print(f"👤 ФИО: {existing_student['name']}")
            print(f"🏫 Колледж: {existing_student['college']}")
            print(f"📚 Курс: {existing_student['course']}")
            print(f"👥 Группа: {existing_student['group']}")
            print(f"🔢 ID: {existing_student['id']}")
            print(f"📅 Дата регистрации: {existing_student['registration_date']}")
            print(f"📊 Статус: {existing_student.get('status', 'активный')}")
            print("═" * 50)
            print("🎉 Добро пожаловать в систему!")
            print("✅ Доступ разрешен!")
        else:
            # Регистрация нового студента
            register_new_student(college, course, name, group, id)
        
        # Предложение продолжить
        another = input("\n🔄 Хотите проанализировать другой файл? (да/нет): ").strip().lower()
        if another not in ['да', 'yes', 'y', 'д']:
            print("👋 До свидания!")
            break

#─────────────────────────────────────────────────────────────
# ЗАПУСК ПРОГРАММЫ
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()