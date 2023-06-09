
from enums.sort_mode import SortMode
from repository.course_repository import add_rating, bulk_import, get_available_courses_by_order, get_course_by_id, insert_course


def get_chapter_information(course_id, chapter_id):
    course = get_course_by_id(course_id)
    chapter_id = chapter_id-1
    try:
        if course:
            chapters = course.chapters
            chapter_rating = (chapters[chapter_id]['rating_sum'] / chapters[chapter_id]['rating_count'])
            chapters[chapter_id]['rating'] = round(chapter_rating)
            return chapters[chapter_id]
    except:
        return "Invalid course or chapter id"

    return None

def get_course_overview(cid):
    course = get_course_by_id(cid)
    total_rating = 0
    for chapter in course.chapters:
        if(chapter['rating_sum'] == 0 and chapter['rating_sum'] == 0 ):
            pass
        chapter_rating = (chapter['rating_sum'] / chapter['rating_count'])
        total_rating += chapter_rating
        chapter['rating'] = round(chapter_rating)
    if total_rating != 0:
        rating = total_rating/ len(course.chapters)
    rating = 0
    total_rating = 0
    course.rating = round(rating)
    return course

# def get_course_description(id):
#     course = get_course_by_id(id)
#     if course:
#         description = course.get('description', '')
#         return description
#     return None

def get_available_course(sort_mode:SortMode, domain:str):
    courses =  get_available_courses_by_order(sort_mode,domain)
    total_rating = 0
    for course in courses:
        for chapter in course.chapters:
            if(chapter['rating_count'] != 0 ):
                chapter_rating = (chapter['rating_sum'] / chapter['rating_count'])
                total_rating += chapter_rating
                chapter['rating'] = round(chapter_rating)
        if total_rating != 0:
            rating = total_rating/ len(course.chapters)
        total_rating = 0
        rating = 0
        course.rating = round(rating)
    return courses
    
    

def post_course(course):
    try:
        insert_course(course)
    except:
        return "Error posting course"
    return "Success"

def post_bulk_courses(courses):
    try:
        bulk_import(courses)
    except:
        return "Error importing courses"
    return "Success"
    
def add_rating_chapter(course_id,chapter_id,rating):
    if rating > 0 and rating <= 10:
        add_rating(course_id,chapter_id,rating)
        return "Success"
    return "Rating range should be in between 0 to 10"