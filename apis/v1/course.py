from typing import List, Optional
from fastapi import APIRouter
from enums.sort_mode import SortMode
from models.course import Course
from bloc.course_bloc import add_rating_chapter, get_available_course, get_chapter_information, get_course_overview, post_bulk_courses, post_course


router = APIRouter()


@router.post("/insert")
async def post_course_api(course:Course):
    return post_course(course)

@router.post("/import")
async def post_bulk_courses_api(courses: List[Course]):
    return post_bulk_courses(courses)

@router.post("/rate_chapter")
async def add_rating_chapter_api(course_id:int,chapter_id:int,rating:int):
    return add_rating_chapter(course_id,chapter_id,rating)

@router.get("/course_overview")
async def get_course_overview_api(course_id:int):
    return get_course_overview(course_id)

@router.get("/available_courses")
async def get_available_course_api(sort_mode:SortMode,domain:Optional[str] = None):
    return get_available_course(sort_mode,domain)

@router.get("/chapter_info")
async def get_chapter_information_api(course_id:int,chapter_id:int):
    return get_chapter_information(course_id,chapter_id)


