"""
Hashcode 2020 data structures and parsing helpers
"""

import logging
from typing import List, Set, TextIO, Dict


class Library:  # pylint: disable=too-few-public-methods
    """Library"""

    def __init__(self, id_: int,  # pylint: disable=too-many-arguments
                 n_books: int, signup_delay: int, books_per_day: int, books: Set[int]):
        self.id_ = id_
        self.n_books = n_books
        self.signup_delay = signup_delay  # days
        self.books_per_day = books_per_day  # books/day
        self.books = books  # books id set


class InputDataSet:  # pylint: disable=too-few-public-methods
    """Input Data"""

    def __init__(self, n_books,  # pylint: disable=too-many-arguments
                 n_libraries, n_days, book_scores, libraries):
        self.n_books = n_books
        self.n_libraries = n_libraries
        self.n_days = n_days
        self.book_scores: List[int] = book_scores  # book i score = book_scores[i]
        self.libraries: List[Library] = libraries  # List[Library]

    def __str__(self):
        return f"B: {self.n_books} L: {self.n_libraries} D: {self.n_days}"


class LibraryOrder:  # pylint: disable=too-few-public-methods
    """Library Order"""

    def __init__(self, id_: int, n_books: int, books: List[int]):
        self.id_ = id_
        self.n_books = n_books
        self.books = books  # book id list (ordered)


class OutputDataSet:  # pylint: disable=too-few-public-methods
    """Output Data"""

    def __init__(self, n_libraries, library_orders: List[LibraryOrder]):
        self.n_libraries = n_libraries
        self.library_orders = library_orders  # List[LibraryOrder]

    def __str__(self):
        return f"L: {self.n_libraries}"


def parse_input_file(input_file) -> InputDataSet:
    """
    Parse input file and return an initialized InputDataSet struct
    :param input_file: file for parsing
    :return: InputDataSet
    """
    # B, L, D
    (total_books, total_libraries, total_days) = map(int, input_file.readline().split(' '))
    book_scores = list(map(int, input_file.readline().split(' ')))
    libraries = []
    for id_ in range(total_libraries):
        (n_books, signup_delay, books_per_day) = map(int, input_file.readline().split(' '))
        books = set(map(int, input_file.readline().split(' ')))
        libraries.append(Library(id_, n_books, signup_delay, books_per_day, books))
    return InputDataSet(total_books, total_libraries, total_days, book_scores, libraries)


def parse_output_file(output_file, n_libraries, n_books) -> (bool, OutputDataSet):
    """
    Parse output file and return an initialized OutputDataSet struct
    :param output_file: file for parsing
    :param n_libraries: number of libraries from input file
    :param n_books: number of books from input file
    :return: OutputDataSet
    """
    n_orders = int(output_file.readline())  # L
    library_orders = []
    library_found: Dict[int, int] = {}  # library, line 1st definition
    books_found: Dict[int, int] = {}  # book, line 1st definition
    for line in range(n_orders):
        current_line = 2 * line + 2
        library_definition = output_file.readline()
        try:
            (id_, lib_n_books) = map(int, library_definition.split(' '))
            if id_ < 0 or id_ >= n_libraries:
                logging.warning(f"line {current_line}: library id {id_} is invalid should be >= 0 and < {n_libraries}")
                continue
            if lib_n_books == 0:
                logging.warning(f"line {current_line}: library books sent {lib_n_books} == 0")
            if id_ in library_found:
                logging.warning(f"line {current_line}: library {id_} previously defined line {library_found[id_]}")
                continue
            else:
                library_found[id_] = current_line
        except ValueError as _:
            logging.warning(
                f"line {current_line}: invalid content: '{library_definition}' should be <library_id> <books>")
            continue
        current_line = 2 * line + 3
        library_books = output_file.readline()
        try:
            books = list(map(int, library_books.split(' ')))
            for book in books:
                if book < 0 or book >= n_books:
                    logging.warning(f"line {current_line}: book id {book} is invalid should be >= 0 and < {n_books}")
                if book in books_found:
                    logging.debug(f"line {current_line}: book {book} previously defined line {books_found[book]}")
                else:
                    books_found[book] = current_line
        except ValueError as _:
            logging.warning(f"line {current_line}: invalid content: '{library_books}' should be <books>...")
            continue
        if len(books) != lib_n_books:
            logging.warning(f"line {current_line}: number of books ({len(books)}) does not match declaration at line {current_line - 1} ({lib_n_books})")
        library_orders.append(LibraryOrder(id_, lib_n_books, books))
    return OutputDataSet(n_orders, library_orders)


def write_output_file(output_data: OutputDataSet, output_file: TextIO):
    """
    Dump output data (solution) to output file
    :param output_data: solution
    :param output_file: file for dumping
    """
    output_file.write(f"{output_data.n_libraries}\n")
    for library_order in output_data.library_orders:
        output_file.write(f"{library_order.id_} {library_order.n_books}\n")
        output_file.write(" ".join(str(lib) for lib in library_order.books) + "\n")


def build_signup_schedule(input_data_set: InputDataSet, output_data_set: OutputDataSet):
    """
    Return signup schedule i.e (day signup complete, library id) list

    Note: returned list in arbitrary order
    :param input_data_set:
    :param output_data_set:
    :return: (day signup complete, library id) list
    """
    day = 0
    signup_schedule = []
    for library_order in output_data_set.library_orders:
        library = input_data_set.libraries[library_order.id_]
        day += library.signup_delay
        signup_schedule.append((day, library.id_))
    return signup_schedule
