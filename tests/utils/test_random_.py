from string import ascii_lowercase

from faker import Faker

from src.utils.random_ import rand_int, rand_word, rand_letter


def test_rand_int_should_return_value_in_range_of_start_and_end():
    start = Faker().pyint()
    end = Faker().pyint(min_value=start + 1)

    assert start <= rand_int(start, end) < end


def test_rand_word_should_return_value_in_list():
    fake = Faker()
    words = {fake.word() for _ in range(10)}
    assert rand_word(words) in words


def test_rand_letter_should_return_lowercase_char():
    assert rand_letter() in list(ascii_lowercase)
