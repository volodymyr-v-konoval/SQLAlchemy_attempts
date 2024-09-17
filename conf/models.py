from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


    # sql_create_groups_table = """
    #     CREATE TABLE IF NOT EXISTS groups (
    #         id SERIAL PRIMARY KEY,
    #         name VARCHAR(50) NOT NULL
    #     );
    # """


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)


    # sql_create_students_table = """
    #     CREATE TABLE IF NOT EXISTS students(
    #         id SERIAL PRIMARY KEY,
    #         name VARCHAR(150) NOT NULL,
    #         group_id INTEGER REFERENCES groups(id)
    #             on delete cascade
    #     );
    # """
    

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    group_id = Column('group_id', 
                      ForeignKey('groups.id', 
                                 ondelete='CASCADE',
                                 onupdate='CASCADE'))
    group = relationship('Group', backref='students')


    # sql_create_teachers_table = """
    #     CREATE TABLE IF NOT EXISTS teachers (
    #         id SERIAL PRIMARY KEY,
    #         fullname VARCHAR(150) NOT NULL
    #     );
    # """


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)


    # sql_create_subjects_table = """
    #     CREATE TABLE IF NOT EXISTS subjects (
    #         id SERIAL PRIMARY KEY,
    #         name VARCHAR(175) NOT NULL,
    #         teacher_id INTEGER REFERENCES teachers(id)
    #             on delete cascade
    #     );
    # """


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(175), nullable=False)
    teacher_id = Column('teacher_id', 
                        ForeignKey('teachers.id', 
                                   ondelete='CASCADE',
                                   onupdate='CASCADE'))
    teacher = relationship('Teacher', backref='subject')


    # sql_create_grades_table = """
    #     CREATE TABLE IF NOT EXISTS grades (
    #         id SERIAL PRIMARY KEY,
    #         student_id INTEGER REFERENCES students(id)
    #         on delete cascade,
    #         subject_id INTEGER REFERENCES subjects(id)
    #         on delete cascade,
    #         grade INTEGER CHECK (grade >= 0 AND grade <= 100),
    #         grade_date DATE NOT NULL
    #     );
    # """


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    date_of = Column('date_of', Date, nullable=True)
    student_id = Column('student_id', 
                        ForeignKey('students.id', 
                                   ondelete='CASCADE',
                                   onupdate='CASCADE'))
    subject_id = Column('subject_id', 
                         ForeignKey('subjects.id', 
                                    ondelete='CASCADE',
                                    onupdate='CASCADE'))
    student = relationship('Student', backref='grade')
    subject = relationship('Subject', backref='grade')
    