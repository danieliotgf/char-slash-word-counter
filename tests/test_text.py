import unittest

from counter import count_text


class WordCountTests(unittest.TestCase):
    def words(self, text):
        return count_text(text).words

    def test_empty(self):
        self.assertEqual(count_text("").to_dict(), {
            "words": 0, "characters": 0, "characters_no_spaces": 0, "paragraphs": 0,
        })

    def test_english(self):
        self.assertEqual(self.words("The quick brown fox jumps over the lazy dog."), 9)

    def test_spanish_accents_and_punctuation(self):
        self.assertEqual(self.words("¿Qué tal estás? ¡Muy bien, señor Núñez!"), 7)
        self.assertEqual(self.words("pingüino, cigüeña y año"), 4)

    def test_contractions_and_hyphens(self):
        self.assertEqual(self.words("Don't stop — it's a well-known fact."), 6)
        self.assertEqual(self.words("It’s curly"), 2)

    def test_numbers(self):
        self.assertEqual(self.words("Pi is 3.14 and a grand is 1,000"), 8)

    def test_symbols_are_not_words(self):
        self.assertEqual(self.words("hello -- world ... !!! ¿?"), 2)


class CharacterCountTests(unittest.TestCase):
    def test_spaces(self):
        c = count_text("Hola mundo")
        self.assertEqual(c.characters, 10)
        self.assertEqual(c.characters_no_spaces, 9)

    def test_composed_accent_is_one_character(self):
        # "é" written as "e" + combining acute accent
        self.assertEqual(count_text("café").characters, 4)

    def test_windows_newlines(self):
        self.assertEqual(count_text("a\r\nb").characters, 3)


class ParagraphCountTests(unittest.TestCase):
    def test_paragraphs(self):
        text = "First paragraph.\nStill first.\n\nSecond.\n\n\n  \nThird."
        self.assertEqual(count_text(text).paragraphs, 3)


if __name__ == "__main__":
    unittest.main()
