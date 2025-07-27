from fastapi import FastAPI, HTTPException
from models import Student, Course, Professor, Enrollment
from database import students, courses, professors, enrollments
from logic import calculate_gpa, is_course_full, already_enrolled
from datetime import date

app = FastAPI()

# --- Students ---

@app.post("/students")
def create_student(student: Student):
    if student.id in students:
        raise HTTPException(status_code=400, detail="Student already exists")
    students[student.id] = student.dict()
    return student

@app.get("/students")
def get_students():
    return list(students.values())

@app.get("/students/{id}")
def get_student(id: int):
    if id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[id]

@app.put("/students/{id}")
def update_student(id: int, student: Student):
    students[id] = student.dict()
    return student

@app.delete("/students/{id}")
def delete_student(id: int):
    students.pop(id, None)
    global enrollments
    enrollments = [e for e in enrollments if e['student_id'] != id]
    return {"detail": "Student deleted"}

@app.get("/students/{id}/courses")
def student_courses(id: int):
    return [e for e in enrollments if e['student_id'] == id]

# --- Courses ---

@app.post("/courses")
def create_course(course: Course):
    if course.professor_id not in professors:
        raise HTTPException(status_code=404, detail="Professor not found")
    if course.id in courses:
        raise HTTPException(status_code=400, detail="Course already exists")
    courses[course.id] = course.dict()
    return course

@app.get("/courses")
def get_courses():
    return list(courses.values())

@app.get("/courses/{id}")
def get_course(id: int):
    return courses.get(id)

@app.put("/courses/{id}")
def update_course(id: int, course: Course):
    courses[id] = course.dict()
    return course

@app.delete("/courses/{id}")
def delete_course(id: int):
    courses.pop(id, None)
    global enrollments
    enrollments = [e for e in enrollments if e['course_id'] != id]
    return {"detail": "Course deleted"}

@app.get("/courses/{id}/students")
def course_students(id: int):
    return [e for e in enrollments if e['course_id'] == id]

# --- Professors ---

@app.post("/professors")
def create_professor(professor: Professor):
    if professor.id in professors:
        raise HTTPException(status_code=400, detail="Professor exists")
    professors[professor.id] = professor.dict()
    return professor

@app.get("/professors")
def get_professors():
    return list(professors.values())

@app.get("/professors/{id}")
def get_professor(id: int):
    return professors.get(id)

@app.put("/professors/{id}")
def update_professor(id: int, professor: Professor):
    professors[id] = professor.dict()
    return professor

@app.delete("/professors/{id}")
def delete_professor(id: int):
    professors.pop(id, None)
    # Optionally remove their courses
    global courses, enrollments
    to_remove = [cid for cid, c in courses.items() if c['professor_id'] == id]
    for cid in to_remove:
        del courses[cid]
    enrollments[:] = [e for e in enrollments if e['course_id'] not in to_remove]
    return {"detail": "Professor and related courses deleted"}

# --- Enrollments ---

@app.post("/enrollments")
def enroll(enrollment: Enrollment):
    if is_course_full(enrollment.course_id):
        raise HTTPException(status_code=400, detail="Course is full")
    if already_enrolled(enrollment.student_id, enrollment.course_id):
        raise HTTPException(status_code=400, detail="Already enrolled")
    enrollments.append(enrollment.dict())
    return enrollment

@app.get("/enrollments")
def get_enrollments():
    return enrollments

@app.put("/enrollments/{student_id}/{course_id}")
def update_grade(student_id: int, course_id: int, grade: float):
    for e in enrollments:
        if e['student_id'] == student_id and e['course_id'] == course_id:
            e['grade'] = grade
            students[student_id]['gpa'] = calculate_gpa(student_id)
            return e
    raise HTTPException(status_code=404, detail="Enrollment not found")

@app.delete("/enrollments/{student_id}/{course_id}")
def drop_course(student_id: int, course_id: int):
    global enrollments
    enrollments = [e for e in enrollments if not (e['student_id'] == student_id and e['course_id'] == course_id)]
    students[student_id]['gpa'] = calculate_gpa(student_id)
    return {"detail": "Dropped course"}