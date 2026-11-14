import unittest

from pluralize_py import is_plural, pluralize, singularize


class TestPluralize(unittest.TestCase):
    def test_regular_s(self):
        self.assertEqual(pluralize("cat"), "cats")

    def test_regular_es(self):
        self.assertEqual(pluralize("box"), "boxes")
        self.assertEqual(pluralize("church"), "churches")
        self.assertEqual(pluralize("dish"), "dishes")

    def test_consonant_y(self):
        self.assertEqual(pluralize("city"), "cities")
        self.assertEqual(pluralize("baby"), "babies")

    def test_vowel_y(self):
        self.assertEqual(pluralize("boy"), "boys")
        self.assertEqual(pluralize("day"), "days")

    def test_f_to_ves(self):
        self.assertEqual(pluralize("leaf"), "leaves")
        self.assertEqual(pluralize("knife"), "knives")

    def test_irregular(self):
        self.assertEqual(pluralize("child"), "children")
        self.assertEqual(pluralize("person"), "people")
        self.assertEqual(pluralize("mouse"), "mice")

    def test_uncountable(self):
        self.assertEqual(pluralize("sheep"), "sheep")
        self.assertEqual(pluralize("information"), "information")

    def test_count_one(self):
        self.assertEqual(pluralize("cat", 1), "cat")
        self.assertEqual(pluralize("child", 1), "child")

    def test_count_zero_rejected(self):
        with self.assertRaises(ValueError):
            pluralize("cat", 0)

    def test_count_negative_rejected(self):
        with self.assertRaises(ValueError):
            pluralize("cat", -1)

    def test_empty_word_rejected(self):
        with self.assertRaises(ValueError):
            pluralize("")

    def test_non_string_word_rejected(self):
        with self.assertRaises(ValueError):
            pluralize(None)  # type: ignore[arg-type]

    def test_capitalisation_preserved(self):
        self.assertEqual(pluralize("Cat"), "Cats")
        self.assertEqual(pluralize("CHILD"), "CHILDREN")


class TestSingularize(unittest.TestCase):
    def test_regular(self):
        self.assertEqual(singularize("cats"), "cat")
        self.assertEqual(singularize("boxes"), "box")

    def test_ies(self):
        self.assertEqual(singularize("cities"), "city")

    def test_ves(self):
        self.assertEqual(singularize("leaves"), "leaf")
        self.assertEqual(singularize("knives"), "knife")

    def test_irregular(self):
        self.assertEqual(singularize("children"), "child")
        self.assertEqual(singularize("people"), "person")

    def test_uncountable(self):
        self.assertEqual(singularize("sheep"), "sheep")

    def test_already_singular(self):
        self.assertEqual(singularize("cat"), "cat")

    def test_capitalisation_preserved(self):
        self.assertEqual(singularize("Children"), "Child")


class TestIsPlural(unittest.TestCase):
    def test_plural(self):
        self.assertTrue(is_plural("cats"))
        self.assertTrue(is_plural("boxes"))
        self.assertTrue(is_plural("children"))

    def test_singular(self):
        self.assertFalse(is_plural("cat"))
        self.assertFalse(is_plural("child"))

    def test_uncountable_neither(self):
        self.assertFalse(is_plural("sheep"))

    def test_empty_rejected(self):
        with self.assertRaises(ValueError):
            is_plural("")


if __name__ == "__main__":
    unittest.main()
