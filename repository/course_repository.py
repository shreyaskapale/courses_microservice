import datetime
from typing import List
from pydantic import ValidationError
from pymongo import MongoClient
from enums.sort_mode import SortMode
from repository.mongodb_connection import MongoConnection
from models.course import Course


# MongoDB connection settings
connection = MongoConnection.get_instance()

def get_available_courses_by_order(sort_mode=SortMode.ALPHABETICAL, filter_domain=None):
    query = {}
    if filter_domain:
        query['domain'] = filter_domain
    # Sorting
    sort_key = 'name'  # Default sort key
    sort_direction = 1  # Default sort direction (ascending)

    if sort_mode == SortMode.DATE:
        sort_key = 'date'
        sort_direction = -1  # Sort by date in descending order
    elif sort_mode == SortMode.RATING:
        sort_key = 'rating'
        sort_direction = -1  # Sort by rating in descending order

    # Retrieve courses from MongoDB
    connection = MongoConnection.get_instance()
    courses = connection.collection.find(query).sort(sort_key, sort_direction)

    # Convert MongoDB documents to Course objects
    course_list = [Course(course_id=str(course['course_id']),
                          name=course['name'],
                          date=course['date'],
                          description=course['description'],
                          domain=course['domain'],
                          chapters=course['chapters'])
                   for course in courses]

    return course_list

def insert_course(course: Course):
    connection = MongoConnection.get_instance()
    try:
        # Generate a new course ID
        course_id = connection.collection.count_documents({}) + 1

        # Generate chapter IDs
        for i, chapter in enumerate(course.chapters):
            chapter['chapter_id'] = i + 1
            chapter['rating_count'] = 0
            chapter['rating_sum'] = 0

        # Create the document to insert
        course_doc = {
            'course_id': course_id,
            'name': course.name,
            'date': course.date,
            'description': course.description,
            'domain': course.domain,
            'chapters': course.chapters
        }

        connection.collection.insert_one(course_doc)

    except ValidationError as e:
        print(f"Validation error: {e}")

def get_course_by_id(cid):
    connection = MongoConnection.get_instance()
    course = connection.collection.find_one({'course_id': cid})
    course = Course(course_id=str(course['course_id']),
                          name=course['name'],
                          date=course['date'],
                          description=course['description'],
                          domain=course['domain'],
                          chapters=course['chapters'])
    return course

def bulk_import(courses: List[Course]):
    connection = MongoConnection.get_instance()

    # Generate course IDs
    start_course_id = connection.collection.count_documents({}) + 1

    # Generate chapter IDs
    course_docs = []
    for i, course in enumerate(courses):
        course_id = start_course_id + i
        for j, chapter in enumerate(course.chapters):
            chapter['chapter_id'] = j + 1
            chapter['rating_count'] = 0
            chapter['rating_sum'] = 0


        # Create the course document
        course_doc = {
            'course_id': course_id,
            'name': course.name,
            'date': course.date,
            'description': course.description,
            'domain': course.domain,
            'chapters': course.chapters
        }

        # Add the course document to the list
        course_docs.append(course_doc)

    # Insert the course documents into the MongoDB collection
    connection.collection.insert_many(course_docs)

def add_rating(course_id, chapter_id, rating):

    # Find the course and chapter by their IDs
    query = {"course_id": course_id, "chapters.chapter_id": chapter_id}
    projection = {"chapters.$": 1}
    course =  connection.collection.find_one(query, projection)

    # Check if the course and chapter exist
    if course:
        chapter = course["chapters"][0]

        # Update the rating_sum and rating_count fields
        chapter["rating_sum"] = chapter.get("rating_sum", 0) + rating
        chapter["rating_count"] = chapter.get("rating_count", 0) + 1

        # Update the chapter in the collection
        update_query = {"course_id": course_id, "chapters.chapter_id": chapter_id}
        update = {"$set": {"chapters.$": chapter}}
        connection.collection.update_one(update_query, update)
        print("Rating added successfully.")
    else:
        print("Course or chapter not found.")



# Example usage of insert_course
# course = Course(
    # course_id="#",
    # name='Highlights of Calculus',
    # date=datetime.now(),
    # description='This is a course on the highlights of calculus.',
    # domain=['mathematics'],
    # chapters=[
    #     {'name': 'Introduction', 'text': 'This is the introduction chapter.'},
    #     {'name': 'Derivatives', 'text': 'This is the derivatives chapter.'},
    # ]
# )

# insert_course(course)
# print(get_available_courses('alphabetical', None))
