import re
import os

def parse_file(file_path):
    """
    Функция читает и анализирует файл, чтобы извлечь информацию.
    """
    college = None
    course = None
    name = None
    group = None
    id = None
    
    try:
        # Пробуем разные кодировки
        encodings = ['utf-8', 'cp1251', 'koi8-r', 'iso-8859-1', '002-ii']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    content = file.read()
                    print(f"Файл успешно прочитан с кодировкой: {encoding}")
                    break
            except UnicodeDecodeError:
                continue
        else:
            print("Не удалось прочитать файл с доступными кодировками")
            return college, course, name, group, id
            
        # Извлекаем данные с помощью регулярных выражений
        patterns = {
            'college': [r'Колледж[:\s]*([^\n]+)', r'College[:\s]*([^\n]+)', r'Учебное заведение[:\s]*([^\n]+)'],
            'course': [r'Курс[:\s]*([^\n]+)', r'Course[:\s]*([^\n]+)'],
            'name': [r'ФИ[:\s]*([^\n]+)', r'ФИО[:\s]*([^\n]+)', r'Name[:\s]*([^\n]+)', r'Имя[:\s]*([^\n]+)'],
            'group': [r'Команда[:\s]*([^\n]+)', r'Группа[:\s]*([^\n]+)', r'Group[:\s]*([^\n]+)', r'Team[:\s]*([^\n]+)'],
            'id': [r'ID[:\s]*([^\n]+)', r'ИД[:\s]*([^\n]+)', r'Номер[:\s]*([^\n]+)', r'№[:\s]*([^\n]+)']
        }
        
        # Поиск по всем шаблонам для каждого поля
        for field_name, field_patterns in patterns.items():
            for pattern in field_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    if field_name == 'college':
                        college = match.group(1).strip()
                    elif field_name == 'course':
                        course = match.group(1).strip()
                    elif field_name == 'name':
                        name = match.group(1).strip()
                    elif field_name == 'group':
                        group = match.group(1).strip()
                    elif field_name == 'id':
                        id = match.group(1).strip()
                    break
                
        # Выводим все найденные данные
        print("\nНайденные данные в файле:")
        print("=" * 50)
        if college:
            print(f"Колледж: {college}")
        if course:
            print(f"Курс: {course}")
        if name:
            print(f"ФИО: {name}")
        if group:
            print(f"Группа/Команда: {group}")
        if id:
            print(f"ID: {id}")
        
        # Показываем также все содержимое файла
        print("\nПолное содержимое файла:")
        print("=" * 50)
        print(content)
        print("=" * 50)
                
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.")
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
    
    return college, course, name, group, id

def main():
    """
    Главная функция программы.
    """
    print("Программа для чтения и анализа файлов")
    print("=" * 50)
    
    while True:
        print("\nВыберите действие:")
        print("1. Ввести путь к файлу")
        print("2. Использовать файл по умолчанию (README002.md)")
        print("3. Выйти")
        
        choice = input("Ваш выбор (1-3): ").strip()
        
        if choice == '3':
            print("До свидания!")
            break
            
        if choice == '1':
            file_path = input("Введите полный путь к файлу: ").strip()
        elif choice == '2':
            file_path = 'README002.md'
        else:
            print("Неверный выбор. Попробуйте снова.")
            continue
        
        if not os.path.exists(file_path):
            print(f"Файл '{file_path}' не существует.")
            continue
        
        print(f"\nЧтение файла: {file_path}")
        print("-" * 50)
        
        # Парсим данные из файла
        college, course, name, group, id = parse_file(file_path)
        
        # Если найдены все основные данные, выводим приветствие
        if all([college, course, name, group, id]):
            print("\nВсе данные успешно получены!")
            print("=" * 50)
            print(f"Здравствуйте, {name}!")
            print(f"Приветствуем студента {college}")
            print(f"Курс: {course}")
            print(f"Команда: {group}")
            print(f"ID: {id}")
            print("=" * 50)
            print("Желаем успехов в обучении!")
        else:
            print("\nНе все данные найдены в файле.")
            print("Проверьте формат файла или укажите другой файл.")
        
        # Предложение проанализировать другой файл
        another = input("\nХотите проанализировать другой файл? (да/нет): ").strip().lower()
        if another not in ['да', 'yes', 'y', 'д']:
            print("До свидания!")
            break

# Запуск программы
if __name__ == "__main__":
    main()