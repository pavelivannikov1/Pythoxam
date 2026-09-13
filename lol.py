# Глобальные хранилища
books = []          # книги: список словарей
readers = []        # читатели: список словарей {"reader_id": int, "name": str}
loans = []          # выдачи: список словарей {"book": dict, "reader": dict, "loan_id": int}

next_reader_id = 1
next_loan_id = 1


# --- Вспомогательные функции поиска --- книги Эта функция ищет книгу в списке по названию и возращает найденную книгу (словарь) или None если нечиго не нашлось

def _find_book_by_title(title: str): # Объявление функции
    title_lower = title.lower() # Приводим искомое название к нижнему регистру. Это нужно, чтобы поиск был нечувствителен к регистру: это нужно чтобы Название книги пример "Руслан и Людмила", руслан и людмила считались одинаковыми
    for b in books:
        if b["title"].lower() == title_lower: # сравниваем название текущей книги с исковым 
            return b # сразу возварщаем найденый словарь с книгой как только return срабатывает функция завершается
    return None # эта строка выполняется только если цикл закончился а совподений не было ////

#  Эта функция Ищет в глобальном списке books все книги заданного автора и возваращает их в виде списка#
def _find_books_by_author(author: str):  #приводит переданное имя автора к нижнему регистру, чтобы поиск не зависел от регистра (например, «Пушкин», «пушкин» и «ПУШКИН» будут считаться одинаковыми).
    author_lower = author.lower() # Это списковое включение проходит по всем книгам в списке  сравнивает с author_lower если совподает добовляет книгу b в результативный список 
    return [b for b in books if b["author"].lower() == author_lower] # Находит все книги , где  имя автора совпадает с запросом 


def _find_books_by_genre(genre: str): # приводится точно также к нижнему ругистру. Теперь руслан и людмила и Руслан и Людмила одно и тоже
    genre_lower = genre.lower() # Проходит по всем книгам сравнивает жанр книги с искомым и собирает совпадения в список 
    return [b for b in books if b["genre"].lower() == genre_lower] # И возвращает список если не чиго не найдено


def _find_reader_by_id(reader_id: int): # Эта функция ищет читателя по его уникальному ID  и возвращает словарь с данными читателя если находит а если нет то None 
    for r in readers: # Проходит по списку readers (который, судя по всему, глобальный).
        if r["reader_id"] == reader_id: #Для каждого читателя r проверяет, совпадает ли r["reader_id"] с переданным reader_id.
            return r # Если совпадение есть — сразу возвращает этого читателя (словарь).
    return None #Если цикл закончился, а совпадений не было — возвращает None.


def _find_loan_by_book_and_reader(book: dict, reader: dict): #  эта книга ищет в списке loans запись о выдаче конкретной книги читателю
    """Находит активную выдачу книги конкретному читателю."""
    for loan in loans:  # Перебирает все выдачи в списке loans
        if loan["book"] is book and loan["reader"] is reader: # Проверяет точное совпадение объектов книги и читателя:
            # Проверяем, что книга ещё не возвращена (простая логика: если есть в loans — значит выдана)
            return loan # возвращает если улсовие выпонено 
    return None # Если нечиго не найдено то none

# --- Основные функции библиотеки ---

def add_book(title: str, author: str, year: int, genre: str, copies: int) -> None:  # объявляем функцию с именем add_book. эта функция нужна для того чтобы пользователь мог добавить книгу
    """Добавляет книгу в библиотеку."""  
    book = {      # это аргументы по которым будет добавлятся книга
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "copies": copies,
    }
    books.append(book)
    print(f"Книга '{title}' добавлена. Экземпляров: {copies}")


def remove_book(title, str) -> bool:  #  Эта функция для удаления книги #
     
    book = _find_book_by_title(title)
    if not book:
        print(f"Книга с названием '{title}' не найдена.")
        return False #  # Нельзя удалить, если есть активные выдачи
    
    for loan in loans: 
        if loan["book"] is book:
            print(f"Не удалось удалить: книга '{title}' сейчас выдана.")
            return False
    books.remove(book) 
    print(f"Книга '{title}' удалена из библиотеки.")
    return True 
     

def register_reader(name: str) -> dict: # Обьявление функции Она принимает имя  читателя как строку str и обещает вернуть словарь dict
    """Регистрирует нового читателя и возвращает его запись.""" 
    global next_reader_id # говорит Python, что мы хотим менять глобальную переменную#
    reader = {
        "reader_id": next_reader_id,
        "name": name,
    }
    readers.append(reader) # добавляет нового читателя в глобальный список 
    next_reader_id += 1   # увеличивает счётчик ID на 1, чтобы следующий читатель получил новый номер.#
    print(f"Читатель '{name}' зарегистрирован. ID: {reader['reader_id']}") # выводит что новый читатель зарегистрирован
    return reader 


def lend_book(book_title: str, reader_id: int) -> bool:  # Принимает название книги (book_title) и ID читателя (reader_id).
    """Выдаёт книгу читателю, если есть свободные экземпляры """
    book = _find_book_by_title(book_title) #Вызывается вспомогательная функция _find_book_by_title, которая ищет книгу по названию.#
    if not book: 
        print(f"Книга '{book_title}' не найдена в библиотеке.")
        return False     # если книга не найдена 

    if book["copies"] <= 0:   # берется значение по ключу copies из словаря book количество экземпляров И проверяется если свободных копий 0 Если ключ отсутсвует здесь возникает ошибка keyError В текущей архитектуре предполагается что у всех книг есть это ключ
        print(f"Нет свободных экземпляров книги '{book_title}'.") # сообщается что остутсвуют свободные экземпляры книги и они уже все выданы
        return False  #Берется значение по ключу "copies" из словаря book (количество экземпляров).
 
 
                                                        
    reader = _find_reader_by_id(reader_id) # Вызывается вспомогательная функция  (числовой идентификатор читателя).
    if not reader: #  Проверяет что ридер это None то есть читататель не найден 
        print(f"Читатель с ID {reader_id} не найден.") 
        return False 

    # Проверка: не выдана ли уже эта книга этому читателю
    existing_loan = _find_loan_by_book_and_reader(book, reader) # Проверка не выдана этаже книга читателю
    if existing_loan:  
        print(f"Книга '{book_title}' уже выдана читателю '{reader['name']}'.")
        return False  # если книга выдана читателю то возврощает False

    # Выдача
    global next_loan_id  #говорит, что мы хотим менять глобальную переменную next_loan_id (счётчик ID выдач) внутри функции. Без этого Python создал бы локальную переменную, а глобальная осталась бы прежней.
    loan = {
        "book": book, # ссылка на обьект книги
        "reader": reader, # сылка на обьект читателя 
        "loan_id": next_loan_id, # текущие значение счетчика next_loan_id 
    }
    loans.append(loan) # Новая запись о выдаче добавляется в глобальный список loans. Теперь она хранится как активная выдача.
    book["copies"] -= 1  # уменьшаем количество доступных экземпляров на 1 
    next_loan_id += 1
    print(f"Книга '{book_title}' выдана читателю '{reader['name']}' (ID {reader_id}).")
    return True    #  выдает книгу если она доступна по id то возвращение идет true


def return_book(book_title: str, reader_id: int) -> bool:  #  Обьявляет функции принимает название книги  и читатедя ридер айди
    """Принимает книгу обратно от читателя."""
    book = _find_book_by_title(book_title)    # вызывается вспомогательная функция которая ищет книгу по названию в списке books
    if not book:                                
        print(f"Книга '{book_title}' не найдена.") # если книга не найдена вернется false
        return False

    reader = _find_reader_by_id(reader_id)  # имя читателя по его id если читателя книги нет в базе то нельзя оформить возврат
    if not reader:
        print(f"Читатель с ID {reader_id} не найден.")
        return False

    loan = _find_loan_by_book_and_reader(book, reader) #Ищем запись о выдаче (loan) для этой пары: книга + читатель.
    if not loan:
        print(f"У читателя '{reader['name']}' нет активной выдачи книги '{book_title}'.")
        return False 

    # Возврат
    loans.remove(loan)
    book["copies"] += 1  # увеличиваем количество доступных экземпляров
    print(f"Книга '{book_title}' возвращена читателем '{reader['name']}'.")
    return True


def list_available_books() -> None:   # Обьявляем функцию без аргументов 
    #Выводит список всех книг с количеством доступных экземпляров.#
    if not books: # Проверяем пустой ли список books
        print("В библиотеке нет книг.") 
        return  # Завершаем функцию дальше код не выполняется 
    print("\n--- Доступные книги ---") # выводит доступные книги
    for b in books:
        print(f"{b['title']} ({b['author']}, {b['year']}, {b['genre']}) — экз.: {b['copies']}")
    print("-----------------------\n")


def search_books_by_title(title: str) -> None:  # обьявляется функция поиска книги по типу строки 
    book = _find_book_by_title(title)
    if not book:
        print(f"Книга с названием '{title}' не найдена.")  
        return  # возвращаемся если книгу не нашло
    print(f"Найдена книга: {book['title']} ({book['author']}, {book['year']}, {book['genre']}), экз.: {book['copies']}")
    # елси книгу нашло 

def search_books_by_author(author: str) -> None:  #Объявляем функцию search_books_by_author, которая принимает один аргумент — строку author (имя автора).
    results = _find_books_by_author(author)     # проверяем пуст ли список results
    if not results:                                       
        print(f"Книги автора '{author}' не найдены.")   # если книг не найдено то выводим сообщение с именем автора
        return
    print(f"\nКниги автора '{author}':")
    for b in results:
        print(f"- {b['title']} ({b['year']}, {b['genre']}), экз.: {b['copies']}")
    print()


def search_books_by_genre(genre: str) -> None:
    results = _find_books_by_genre(genre)
    if not results:
        print(f"Книги жанра '{genre}' не найдены.")
        return
    print(f"\nКниги жанра '{genre}':")
    for b in results:
        print(f"- {b['title']} ({b['author']}, {b['year']}), экз.: {b['copies']}")
    print()


# --- Простой консольный интерфейс (меню) ---

def show_menu():
    print("\n=== Электронная библиотека ===")
    print("1. Добавить книгу")
    print("2. Удалить книгу по названию")
    print("3. Зарегистрировать читателя")
    print("4. Выдать книгу читателю")
    print("5. Принять книгу обратно")
    print("6. Список доступных книг")
    print("7. Поиск книги по названию")
    print("8. Поиск книг по автору")
    print("9. Поиск книг по жанру")
    print("0. Выход")
    print("==============================")


def run_library_app():
    while True:
        show_menu()
        choice = input("Выберите действие (введите номер): ").strip()

        if choice == "1":
            title = input("Название книги: ").strip()
            author = input("Автор: ").strip()
            year = int(input("Год издания: ").strip())
            genre = input("Жанр: ").strip()
            copies = int(input("Количество экземпляров: ").strip())
            add_book(title, author, year, genre, copies)

        elif choice == "2":
            title = input("Название книги для удаления: ").strip()
            remove_book(title)

        elif choice == "3":
            name = input("Имя читателя: ").strip()
            register_reader(name)

        elif choice == "4":
            book_title = input("Название книги для выдачи: ").strip()
            reader_id = int(input("ID читателя: ").strip())
            lend_book(book_title, reader_id)

        elif choice == "5":
            book_title = input("Название возвращаемой книги: ").strip()
            reader_id = int(input("ID читателя: ").strip())
            return_book(book_title, reader_id)

        elif choice == "6":
            list_available_books()

        elif choice == "7":
            title = input("Название для поиска: ").strip()
            search_books_by_title(title)

        elif choice == "8":
            author = input("Автор для поиска: ").strip()
            search_books_by_author(author)

        elif choice == "9":
            genre = input("Жанр для поиска: ").strip()
            search_books_by_genre(genre)

        elif choice == "0":
            print("Выход из приложения.")
            break

        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    run_library_app()