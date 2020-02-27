import argparse
import logging

from parser import InputDataSet, OutputDataSet, parse_input_file, parse_output_file, build_signup_schedule


def compute_score(input_data_set: InputDataSet, output_data_set: OutputDataSet):
    score = 0
    books_already_sent = set()
    signup_schedule = build_signup_schedule(input_data_set, output_data_set)
    library_orders = {library_order.id_: library_order for library_order in output_data_set.library_orders}
    for (signup_day, signup_finished_id) in signup_schedule:
        logging.debug(f"day {signup_day}: library {signup_finished_id} signup is finished")
        days_left = input_data_set.n_days - signup_day
        if days_left <= 0:
            continue
        library_order = library_orders[signup_finished_id]
        books_per_day = input_data_set.libraries[signup_finished_id].books_per_day
        n_books_sent = days_left * books_per_day
        n_books_sent = min(n_books_sent, library_order.n_books)
        books_sent = library_order.books[:n_books_sent]
        logging.debug(f"day {signup_day}: {n_books_sent} books sent: {books_sent}")
        for book in books_sent:
            if book not in books_already_sent:
                book_score = input_data_set.book_scores[book]
                score += book_score
                books_already_sent.add(book)
    return score


def main():
    parser = argparse.ArgumentParser(description="hashcode-2020 score")
    parser.add_argument("input", help="input file")
    parser.add_argument("output", help="output file")
    parser.add_argument("--debug", action="store_true", help="enable debug logs")
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    with open(args.input) as input_file:
        input_data_set = parse_input_file(input_file)
    with open(args.output) as output_file:
        output_data_set = parse_output_file(output_file)

    score = compute_score(input_data_set, output_data_set)
    print(f"score: {score:,}")


if __name__ == "__main__":
    main()
