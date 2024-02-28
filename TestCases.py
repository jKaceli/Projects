#testcase codes for the student class

class TestStudent(unittest.TestCase):
    def test_greater_than(self):
        student1 = Student("Alice", 3.8, 1400)
        student2 = Student("Bob", 3.5, 1300)
        self.assertTrue(student1 > student2)

    def test_less_than(self):
        student1 = Student("Alice", 3.8, 1400)
        student2 = Student("Bob", 3.9, 1500)
        self.assertTrue(student1 < student2)

    def test_equal(self):
        student1 = Student("Alice", 3.8, 1400)
        student2 = Student("Bob", 3.8, 1400)
        self.assertTrue(student1 == student2)

if __name__ == "__main__":
    unittest.main()

#Testcase for basketball class code

import unittest

class TestBasketball(unittest.TestCase):
    def test_start(self):
        basketball_game = Game.Basketball("Basketball", 10, "indoor")
        self.assertEqual(basketball_game.start(), "The Basketball game is starting with 10 players in an indoor basketball court")

    def test_end(self):
        basketball_game = Game.Basketball("Basketball", 10, "indoor")
        self.assertEqual(basketball_game.end(), "The game has ended \nThank you for playing basketball!")

    def test_str(self):
        basketball_game = Game.Basketball("Basketball", 10, "indoor")
        self.assertEqual(str(basketball_game), "Basketball is played with 10 players and it is an indoor sport")

if __name__ == "__main__":
    unittest.main()
