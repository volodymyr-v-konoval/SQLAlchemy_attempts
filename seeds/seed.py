import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from conf.db import session
from conf.models import Group, Student, Teacher, Subject, Grade

fake = Faker('uk-UA')


# class Group(Base):
#     __tablename__ = 'groups'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), nullable=False)
def insert_groups():
    for _ in range(3):
        group = Group(name=fake.unique.word())
        session.add(group)
    session.commit()


# class Student(Base):
#     __tablename__ = 'students'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(150), nullable=False)
#     group_id = Column('group_id', 
#                       ForeignKey('groups.id', 
#                                  ondelete='CASCADE',
#                                  onupdate='CASCADE'))
#     group = relationship('Group', backref='students')
def insert_students():
    groups = session.query(Group).all()
    for _ in range(50):
        group = random.choice(groups)
        student = Student(name=fake.name(), group=group)
        session.add(student)
    session.commit()


# class Teacher(Base):
#     __tablename__ = 'teachers'
#     id = Column(Integer, primary_key=True)
#     fullname = Column(String(150), nullable=False)
def insert_teachers():
    for _ in range(5):
        teacher = Teacher(fullname=fake.name())
        session.add(teacher)
    session.commit()


# class Subject(Base):
#     __tablename__ = 'subjects'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(175), nullable=False)
#     teacher_id = Column('teacher_id', 
#                         ForeignKey('teachers.id', 
#                                    ondelete='CASCADE',
#                                    onupdate='CASCADE'))
#     teacher = relationship('Teacher', backref='subject')
def insert_subjects():
    teachers = session.query(Teacher).all()
    for _ in range(8):
        teacher = random.choice(teachers)
        subject = Subject(name=fake.unique.job(), teacher=teacher)
        session.add(subject)
    session.commit()


# class Grade(Base):
#     __tablename__ = 'grades'
#     id = Column(Integer, primary_key=True)
#     grade = Column(Integer, nullable=False)
#     date_of = Column('date_of', Date, nullable=True)
#     student_id = Column('student_id', 
#                         ForeignKey('students.id', 
#                                    ondelete='CASCADE',
#                                    onupdate='CASCADE'))
#     subject_id = Column('subject_id', 
#                          ForeignKey('subjects.id', 
#                                     ondelete='CASCADE',
#                                     onupdate='CASCADE'))
#     student = relationship('Student', backref='grade')
#     subject = relationship('Subject', backref='grade')
def insert_grades():
    students = session.query(Student).all()
    for student in students:
        subjects = session.query(Subject).all()
        for subject in subjects:
            num_grades = random.randint(0, 20)
            for _ in range(num_grades):
                grade_value = random.randint(1, 100)
                grade = Grade(
                    grade = grade_value,
                    date_of=fake.date_this_year(),
                    student_id=student.id,
                    subject_id=subject.id
                )
                session.add(grade)
    session.commit()


if __name__ == '__main__':
    try:
        insert_groups()
        insert_students()
        insert_teachers()
        insert_subjects()
        insert_grades()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()
