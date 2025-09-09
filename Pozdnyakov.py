import re


def create_user(): #def — это ключевое слово в Python, которое используется для объявления функций.
#Таким образом, def позволяет 
#структурировать код и создавать повторно используемые блоки действий,
# улучшая читаемость и организацию программы.
    """
    Функция для создания нового пользователя.
    """
    print("\nСоздание нового пользователя")
    print("=" * 40)
    
    college = input("Введите название колледжа: ").strip()
    course = input("Введите название курса: ").strip()
    name = input("Введите ФИО: ").strip()
    group = input("Введите группу/команду: ").strip()
    user_id = input("Введите ID: ").strip()
    
    # Создаем содержимое файла
    content = f"""Колледж: {college}
Курс: {course}
ФИО: {name}
Команда: {group}
ID: {user_id}"""
    
    # Сохраняем в файл
    file_path = 'README002.md'
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Пользователь создан! Данные сохранены в файл: {file_path}")
        return college, course, name, group, user_id
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
        return None, None, None, None, None

def find_user_in_file(file_path, target_name):
    """
    Функция для поиска пользователя в файле по ФИО.
    Возвращает данные пользователя если найден, иначе None.
    """
    try:
        # Пробуем разные кодировки
        encodings = ['utf-8']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    content = file.read()
                    break
            except UnicodeDecodeError:
                continue
        else:
            return None

              # Ищем пользователя по ФИО с помощью регулярных выражений
        name_patterns = [r'ФИО[:\s]*([^\n]+)', r'Name[:\s]*([^\n]+)', r'Имя[:\s]*([^\n]+)']
        
        for pattern in name_patterns:  # Перебираем каждый шаблон из списка
            matches = re.findall(pattern, content, re.IGNORECASE)  # Ищем ВСЕ совпадения с шаблоном в тексте
            for match in matches:  # Перебираем найденные совпадения
                if target_name.lower() in match.lower():  # Если искомое имя (в нижнем регистре) есть в найденной строке
                    return extract_user_data(content) 
        
        return None  # Если ни одно совпадение не подошло, возвращаем None (не найдено)
                
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

def extract_user_data(content):
    # Словарь, где ключ - название поля, значение - список шаблонов для его поиска
    patterns = {
        'college': [r'Колледж[:\s]*([^\n]+)', r'College[:\s]*([^\n]+)', r'Учебное заведение[:\s]*([^\n]+)'],
        'course': [r'Курс[:\s]*([^\n]+)', r'Course[:\s]*([^\n]+)'],
        'name': [r'ФИО[:\s]*([^\n]+)', r'Name[:\s]*([^\n]+)', r'Имя[:\s]*([^\n]+)'],
        'group': [r'Команда[:\s]*([^\n]+)', r'Группа[:\s]*([^\n]+)', r'Group[:\s]*([^\n]+)', r'Team[:\s]*([^\n]+)'],
        'id': [r'ID[:\s]*([^\n]+)', r'ИД[:\s]*([^\n]+)', r'Номер[:\s]*([^\n]+)', r'№[:\s]*([^\n]+)']
    }
    
    found_data = {}  # Создаем пустой словарь для хранения найденных данных
    for field_name, field_patterns in patterns.items():  # Проходим по каждому полю и его шаблонам
        for pattern in field_patterns:  # Для каждого шаблона в списке шаблонов для этого поля
            match = re.search(pattern, content, re.IGNORECASE)  # Ищем ПЕРВОЕ совпадение в тексте
            if match:  # Если нашли
                found_data[field_name] = match.group(1).strip()  # Сохраняем найденное значение в словарь
                break  # Прерываем цикл по шаблонам для этого поля, переходим к следующему полю
    
    # Проверяем, что все данные найдены
    if all(key in found_data for key in ['college', 'course', 'name', 'group', 'id']):
        return (  # Возвращаем кортеж, доставая значения из словаря по ключам
            found_data['college'],
            found_data['course'],
            found_data['name'],
            found_data['group'],
            found_data['id']
        )
    
    return None  # Если хотя бы одного ключа нет в словаре

def main():
    """
    Главная функция программы.
    """
    print("Программа для работы с пользовательскими данными")
    print("=" * 50)
    
    file_path = 'README002.md'
    
    while True:
        print("\nВыберите действие:")
        print("1. Поиск пользователя по ФИО")
        print("2. Создать нового пользователя")
        print("3. Показать всех пользователей в файле")
        print("4. Выйти")
        
        choice = input("Ваш выбор (1-4): ").strip()
        
        if choice == '4':
            print("До свидания!")
            break
            
        elif choice == '1':
            target_name = input("Введите ФИО для поиска: ").strip()
            
            if not target_name:
                print("ФИО не может быть пустым!")
                continue
            
            # Ищем пользователя в файле
            user_data = find_user_in_file(file_path, target_name)
            
            if user_data:
                college, course, name, group, user_id = user_data
                print(f"\nПользователь найден!")
                print_user_greeting(college, course, name, group, user_id)
            else:
                print(f"\nПользователь '{target_name}' не найден в файле.")
                create_new = input("Хотите создать нового пользователя? (да/нет): ").strip().lower()
                if create_new in ['да', 'yes', 'y', 'д']:
                    college, course, name, group, user_id = create_user()
                    if all([college, course, name, group, user_id]):
                        print_user_greeting(college, course, name, group, user_id)
        
        elif choice == '2':
            college, course, name, group, user_id = create_user()
            if all([college, course, name, group, user_id]):
                print_user_greeting(college, course, name, group, user_id)
        
        elif choice == '3':
            print("\nВсе пользователи в файле:")
            print("=" * 50)
            show_all_users(file_path)
        
        else:
            print("Неверный выбор. Попробуйте снова.")
            continue
        
        # Предложение продолжить работу
        another = input("\nХотите продолжить работу? (да/нет): ").strip().lower()
        if another not in ['да', 'yes', 'y', 'д']:
            print("До свидания!")
            break

def show_all_users(file_path):
    """
    Показывает всех пользователей из файла.
    """
    try:
        # Пробуем разные кодировки
        encodings = ['utf-8', 'cp1251', 'koi8-r', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    content = file.read()
                    break
            except UnicodeDecodeError:
                continue
        else:
            print("Не удалось прочитать файл")
            return
        
        # Ищем все записи с ФИО
        name_patterns = [r'ФИО[:\s]*([^\n]+)', r'Name[:\s]*([^\n]+)', r'Имя[:\s]*([^\n]+)']
        all_names = []
        
        for pattern in name_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            all_names.extend(matches)
        
        if all_names:
            for i, name in enumerate(set(all_names), 1):
                print(f"{i}. {name.strip()}")
        else:
            print("В файле нет записей о пользователях")
            
    except FileNotFoundError:
        print("Файл не существует")
    except Exception as e:
        print(f"Ошибка: {e}")

def print_user_greeting(college, course, name, group, user_id):
    """
    Функция для вывода приветствия пользователя.
    """
    print("\nВсе данные успешно получены!")
    print("=" * 50)
    print(f"ФИО: {name}")
    print(f"Колледж: {college}")
    print(f"Курс: {course}")
    print(f"Группа/Команда: {group}")
    print(f"ID: {user_id}")
    print("=" * 50)
    print("Добро пожаловать!")

# Запуск программы
if __name__ == "__main__":
    main()
   ''' import re  # Для работы с регулярными выражениями (поиск шаблонов в тексте)

def create_user(): #Объявление функции с именем create_user
    # Запрос данных у пользователя
    # Форматирование данных в структурированный текст
    # Сохранение в файл README002.md
    # Возврат данных для дальнейшего использования

    def find_user_in_file(file_path, target_name):
    # Попытка чтения файла с разными кодировками
    # Поиск по шаблонам ФИО с помощью регулярных выражений
    # Извлечение полных данных при нахождении совпадения

    def extract_user_data(content):
    # Использование словаря шаблонов для разных полей
    # Поиск данных с помощью регулярных выражений
    # Проверка полноты найденных данных

    def main():
    # Организация бесконечного цикла меню
    # Обработка выбора пользователя
    # Координация работы всех функций
Import — команда, это ключевое слово в языках программирования,
которое позволяет использовать код из одного модуля (файла) в другом модуле.
Проще говоря, это способ "взять" уже готовые функции,
классы или переменные из одного файла и "перенести" их в другой, чтобы не писать один и тот же код заново.

def — это ключевое слово в Python, которое используется для объявления функций.
Таким образом, def позволяет 
структурировать код и создавать повторно используемые блоки действий,
 улучшая читаемость и организацию программы.

 операторы break и return

 content - содержание структуры данных

encoding это способ представления символов текста в двоичном формате. 

UTF-8: Наиболее распространённая схема кодирования Unicode,
поддерживающая почти все языки мира и специальные символы.

except в Python — это ключевая часть конструкции обработки исключений вместе с try

name_patterns или patterns - шаблоны именования

re.IGNORECASE делает регулярные выражения более гибкими и удобными для работы
 с реальными данными, где регистр часто непоследователен!'''