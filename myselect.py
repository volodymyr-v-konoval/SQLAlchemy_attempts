from sqlalchemy import func, desc
from sqlalchemy.orm import aliased
from conf.db import session
from conf.models import Grade, Group, Student, Subject, Teacher

def select1():
    result = session.query(Student.name, 
                  func.round(func.avg(Grade.grade), 2)
                  .label('avg_grade')).select_from(Grade)\
    .join(Student).group_by(Student.id)\
    .order_by(desc('avg_grade')).limit(5).all()
    return result


def select2():
    avg_grades = session.query(
        Grade.subject_id,
        Grade.student_id,
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    ).group_by(Grade.subject_id, Grade.student_id).subquery()

    StudentAlias = aliased(Student)

    max_avg_grade_per_subject = session.query(
        avg_grades.c.subject_id,
        func.max(avg_grades.c.avg_grade).label('max_avg_grade')
    ).group_by(avg_grades.c.subject_id).subquery()

    result = session.query(
        Subject.name.label('subject_name'),
        StudentAlias.name.label('student_name'),
        max_avg_grade_per_subject.c.max_avg_grade
    ).join(Subject, Subject.id == max_avg_grade_per_subject.c.subject_id)\
     .join(avg_grades, (avg_grades.c.subject_id == max_avg_grade_per_subject.c.subject_id) &
                      (avg_grades.c.avg_grade == max_avg_grade_per_subject.c.max_avg_grade))\
     .join(StudentAlias, StudentAlias.id == avg_grades.c.student_id)\
     .order_by(Subject.id)\
     .all()

    return result

def select3():
    result = session.query(
        Group.name.label('group_name'),
        Subject.name.label('subject_name'),
        func.round(func.avg(Grade.grade), 2).label('average_grade')
    ).join(Student, Student.group_id == Group.id
    ).join(Grade, Grade.student_id == Student.id
    ).join(Subject, Subject.id == Grade.subject_id
    ).group_by(Group.name, Subject.name).all()

    return result


def select4():
    average_grade = session.query(func.round(func.avg(Grade.grade), 2)).scalar()
    return average_grade    


def select5():
    results = session.query(
        Teacher.fullname.label('teacher_name'),
        Subject.name.label('subject_name')
    ).join(Subject, Subject.teacher_id == Teacher.id).all()

    teacher_subjects = {}
    for row in results:
        if row.teacher_name not in teacher_subjects:
            teacher_subjects[row.teacher_name] = []
        teacher_subjects[row.teacher_name].append(row.subject_name)
    
    return teacher_subjects


def select6():
    results = session.query(
        Group.name.label('group_name'),
        Student.name.label('student_name')
    ).join(Student, Student.group_id == Group.id).all()

    group_students = {}
    for row in results:
        if row.group_name not in group_students:
            group_students[row.group_name] = []
        group_students[row.group_name].append(row.student_name)
    
    return group_students


def select7():
    results = session.query(
        Group.name.label('group_name'),
        Subject.name.label('subject_name'),
        Student.name.label('student_name'),
        Grade.grade.label('grade')
    ).join(Student, Student.group_id == Group.id
    ).join(Grade, Grade.student_id == Student.id
    ).join(Subject, Subject.id == Grade.subject_id).all()

    group_subject_grades = {}
    for row in results:
        group_subject_key = (row.group_name, row.subject_name)
        if group_subject_key not in group_subject_grades:
            group_subject_grades[group_subject_key] = []
        group_subject_grades[group_subject_key].append((row.student_name, row.grade))
    
    return group_subject_grades


def select8():
    results = session.query(
        Teacher.fullname.label('teacher_name'),
        Subject.name.label('subject_name'),
        func.round(func.avg(Grade.grade), 2).label('average_grade')
    ).join(Subject, Subject.teacher_id == Teacher.id
    ).join(Grade, Grade.subject_id == Subject.id
    ).group_by(Teacher.fullname, Subject.name).all()
    
    teacher_subject_averages = {}
    for row in results:
        if row.teacher_name not in teacher_subject_averages:
            teacher_subject_averages[row.teacher_name] = {}
        teacher_subject_averages[row.teacher_name][row.subject_name] = row.average_grade
    
    return teacher_subject_averages


def select9():
    results = session.query(
        Student.name.label('student_name'),
        Subject.name.label('subject_name')
    ).join(Grade, Grade.student_id == Student.id
    ).join(Subject, Subject.id == Grade.subject_id).all()
    
    student_courses = {}
    for row in results:
        if row.student_name not in student_courses:
            student_courses[row.student_name] = set()
        student_courses[row.student_name].add(row.subject_name)
    
    for student in student_courses:
        student_courses[student] = list(student_courses[student])
    
    return student_courses


def select10():
    results = session.query(
        Student.name.label('student_name'),
        Teacher.fullname.label('teacher_name'),
        Subject.name.label('subject_name')
    ).join(Grade, Grade.student_id == Student.id
    ).join(Subject, Subject.id == Grade.subject_id
    ).join(Teacher, Teacher.id == Subject.teacher_id).all()
    
    student_teachers_courses = {}
    for row in results:
        if row.student_name not in student_teachers_courses:
            student_teachers_courses[row.student_name] = {}
        if row.teacher_name not in student_teachers_courses[row.student_name]:
            student_teachers_courses[row.student_name][row.teacher_name] = set()
        student_teachers_courses[row.student_name][row.teacher_name].add(row.subject_name)
    
    for student in student_teachers_courses:
        for teacher in student_teachers_courses[student]:
            student_teachers_courses[student][teacher] = list(student_teachers_courses[student][teacher])
    
    return student_teachers_courses

if __name__ == '__main__':
    print(select1())
    print(select2())
    print(select3())
    print(select4())
    print(select5())
    print(select6())
    print(select7())
    print(select8())    
    print(select9())
    print(select10())
