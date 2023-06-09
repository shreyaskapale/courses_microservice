from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apis.v1.course import router as course_v1

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.middleware("http")(auth_middleware)
# app.middleware("http")(logging_middleware)

app.include_router(course_v1, prefix="/v1/course")
