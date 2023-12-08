import datetime
import pytest
from unittest.mock import patch
from librarySystem import Library, get_checkout_input, get_return_input


@pytest.fixture
def library():
    return Library("test_books.txt")


def test_checkout_books_success(library):
    with patch('builtins.input', side_effect=['1', '2', '3', '0', 'no']):
        selections = get_checkout_input(library)
    assert selections == [{'index': 0, 'quantity': 1}, {'index': 1, 'quantity': 1}, {'index': 2, 'quantity': 1}]


def test_checkout_books_invalid_index(library):
    with patch('builtins.input', side_effect=['10', '0', 'no']):
        selections = get_checkout_input(library)
    assert selections == -1


def test_return_books_success(library):
    with patch('builtins.input', side_effect=['1', '1', '2023-01-01', '0', 'no']):
        return_details = get_return_input(library)
    assert return_details == [{'index': 0, 'quantity': 1, 'due_date': '2023-01-01'}]


def test_return_books_invalid_index(library):
    with patch('builtins.input', side_effect=['10', '0', 'no']):
        return_details = get_return_input(library)
    assert return_details == -1


def test_calculate_late_fee_overdue(library):
    due_date = (datetime.datetime.now() - datetime.timedelta(days=5)).strftime("%Y-%m-%d")
    late_fee = library.calculate_late_fee(due_date)
    assert late_fee == 5


def test_calculate_late_fee_on_time(library):
    due_date = (datetime.datetime.now() + datetime.timedelta(days=5)).strftime("%Y-%m-%d")
    late_fee = library.calculate_late_fee(due_date)
    assert late_fee == 0