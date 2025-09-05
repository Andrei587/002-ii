# main.py

def read_hello_format_from_readme():
    """
    Функция читает файл README.md и ищет строку, начинающуюся с 'Формат приветствия:'.
    Если находит, возвращает шаблон строки для приветствия.
    """
    try:
        # Открываем файл README.md в той же папке, что и скрипт
        with open('README.md', 'r', encoding='utf-8') as file:
            readme_content = file.readlines()
        
        # Ищем строку, которая содержит формат приветствия
        for line in readme_content:
            if line.startswith('Формат приветствия:'):
                # Извлекаем часть строки после двоеточия и очищаем её от лишних пробелов и кавычек
                format_string = line.split(':', 1)[1].strip()
                # Убираем возможные кавычки в начале и конце (если они есть)
                format_string = format_string.strip('"').strip("'")
                return format_string
        
        # Если строка не найдена, возвращаем значение по умолчанию
        return "Привет, {}!"
    
    except FileNotFoundError:
        print("Ошибка: Файл README.md не найден в директории проекта.")
        return "Привет, {}!"

def main():
    # Получаем шаблон приветствия из README
    hello_format = read_hello_format_from_readme()
    
    # Запрашиваем имя пользователя
    user_name = input("Пожалуйста, введите ваше имя: ")
    
    # Форматируем и выводим приветствие согласно шаблону из README
    greeting_message = hello_format.format(user_name)
    print(greeting_message, greeting_message, greeting_message, greeting_message, greeting_message,)

# Точка входа в программу
if __name__ == "__main__":
    main()