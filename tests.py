import unittest
from unittest.mock import patch
from bloc.course_bloc import (
    get_chapter_information,
    get_course_overview,
    get_available_course,
    post_course,
    post_bulk_courses,
    add_rating_chapter
)
from enums.sort_mode import SortMode

class TestCourseFunctions(unittest.TestCase):

    def setUp(self):
        # Set up sample data
        self.course_id = 1
        self.chapter_id = 3
        self.course = {
            "name": "Highlights of Calculus",
            "date": 1530133200,
            "description": "Highlights of Calculus is a series of short videos...",
            "domain": ["mathematics"],
            "chapters": [
                {"name": "Gil Strang's Introduction to Calculus for Highlights for High School", "text": "Highlights of Calculus"},
                {"name": "Big Picture of Calculus", "text": "Highlights of Calculus"},
                {"name": "Six Functions, Six Rules, and Six Theorems", "text": "Highlights of Calculus"}
            ]
        }

    def test_get_chapter_information_valid(self):
        chapter = get_chapter_information(self.course_id, self.chapter_id)
        expected_chapter = {
            "name": "Big Picture: Derivatives",
            "text": "Highlights of Calculus",
            "rating_sum": 0,
            "rating_count": 0,
            "rating": 0
        }
        self.assertEqual(chapter, expected_chapter)

    def test_get_chapter_information_invalid_course(self):
        chapter = get_chapter_information(2, self.chapter_id)
        self.assertIsNone(chapter)

    def test_get_chapter_information_invalid_chapter(self):
        chapter = get_chapter_information(self.course_id, 2)
        self.assertIsNone(chapter)

    def test_get_course_overview(self):
        course_overview = get_course_overview(self.course_id)
        expected_course_overview = {
            "name": "Highlights of Calculus",
            "date": 1530133200,
            "description": "Highlights of Calculus is a series of short videos...",
            "domain": ["mathematics"],
            "chapters": [
                {"name": "Gil Strang's Introduction to Calculus for Highlights for High School", "text": "Highlights of Calculus", "rating_sum": 0, "rating_count": 0, "rating": 0},
                {"name": "Big Picture of Calculus", "text": "Highlights of Calculus", "rating_sum": 0, "rating_count": 0, "rating": 0},
                {"name": "Six Functions, Six Rules, and Six Theorems", "text": "Highlights of Calculus", "rating_sum": 0, "rating_count": 0, "rating": 0}
            ],
            "rating": 0
        }
        self.assertEqual(course_overview, expected_course_overview)

    @patch('bloc.course_bloc.get_available_courses_by_order')
    def test_get_available_course(self, mock_get_available_courses_by_order):
        sort_mode = SortMode.ALPHABETICAL
        domain = "mathematics"

        # Set up mock return value
        mock_courses = [
            {"name": "Course 1", "chapters": []},
            {"name": "Course 2", "chapters": []},
        ]
        mock_get_available_courses_by_order.return_value = mock_courses

        courses = get_available_course(sort_mode, domain)

        mock_get_available_courses_by_order.assert_called_once_with(sort_mode, domain)
        self.assertEqual(courses, mock_courses)

    @patch('bloc.course_bloc.insert_course')
    def test_post_course(self, mock_insert_course):
        course = {"name": "New Course", "chapters": []}

        post_course(course)

        mock_insert_course.assert_called_once_with(course)

    @patch('bloc.course_bloc.bulk_import')
    def test_post_bulk_courses(self, mock_bulk_import):
        courses = [
            {"name": "Course 1", "chapters": []},
            {"name": "Course 2", "chapters": []},
        ]

        post_bulk_courses(courses)

        mock_bulk_import.assert_called_once_with(courses)

    @patch('bloc.course_bloc.add_rating')
    def test_add_rating_chapter_valid(self, mock_add_rating):
        course_id = 1
        chapter_id = 2
        rating = 8

        result = add_rating_chapter(course_id, chapter_id, rating)

        mock_add_rating.assert_called_once_with(course_id, chapter_id, rating)
        self.assertEqual(result, mock_add_rating.return_value)

    @patch('bloc.course_bloc.add_rating')
    def test_add_rating_chapter_invalid_rating(self, mock_add_rating):
        course_id = 1
        chapter_id = 2
        rating = 15

        result = add_rating_chapter(course_id, chapter_id, rating)

        mock_add_rating.assert_not_called()
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
