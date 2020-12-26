import postgres_backend
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, func, and_, update, case, select
from sqlalchemy.orm import sessionmaker

from models.student import Student
from models.subject import Subject
from models.group import Group
from models.teacher import Teacher
from models.teacher_subject import TeacherSubject
from models.subject_group import SubjectGroup
from models.student_subject import StudentSubject
from models.student import student_subject_links
from models.teacher import teacher_subject_links
from models.subject import subject_group_links

from postgres_backend import DB_NAME, DB_PASSWORD, DB_USER, PORT

GROUP_TABLE = "\"group\""
STUDENT_TABLE = "student"
TEACHER_TABLE = "teacher"
SUBJECT_TABLE = "subject"
GRADE_TABLE = "grade"
SUBJECT_GROUP_TABLE = "subject_group"
TEACHER_SUBJECT_TABLE = "teacher_subject"
STUDENT_SUBJECT_TABLE = "student_subject"

DATABASE_URI = 'postgres+psycopg2://{}:{}@localhost:{}/{}'.format(DB_USER, DB_PASSWORD, PORT, DB_NAME)

Base = declarative_base()


def get_value_if_exists(res, key):
    if key in res:
        return res[key]
    else:
        return None


def get_table(table_name):
    if table_name == STUDENT_TABLE:
        return Student
    elif table_name == TEACHER_TABLE:
        return Teacher
    elif table_name == SUBJECT_TABLE:
        return Subject
    elif table_name == GROUP_TABLE:
        return Group
    elif table_name == TEACHER_SUBJECT_TABLE:
        return Teacher
    elif table_name == STUDENT_SUBJECT_TABLE:
        return Student
    elif table_name == SUBJECT_GROUP_TABLE:
        return Subject


def get_data_table(table_name, data):
    if table_name == STUDENT_TABLE:
        return {
            Student.first_name: data.first_name,
            Student.last_name: data.last_name,
            Student.sex: data.sex,
            Student.date_of_birth: data.date_of_birth,
            Student.id_group: data.id_group,
        }
    elif table_name == TEACHER_TABLE:
        return {
            Teacher.first_name: data.first_name,
            Teacher.last_name: data.last_name,
            Teacher.phone_number: data.phone_number
        }
    elif table_name == SUBJECT_TABLE:
        return {
            Subject.name: data.name,
            Subject.time: data.time
        }
    elif table_name == GROUP_TABLE:
        return {
            Group.name: data.name
        }


class Model(object):

    def __init__(self):
        self.engine = create_engine(DATABASE_URI, echo=True)
        Base.metadata.clear()
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self._cursor = postgres_backend.connect_db()

    @property
    def connection(self):
        return self._cursor

    # reading from tables
    def get_one(self, id_q, table_name):
        return self.session.query(get_table(table_name)).filter_by(id=id_q).first()

    def get_one_by_ids(self, id1, id2, table_name1):

        if table_name1 == SUBJECT_GROUP_TABLE:
            res = self.session.query(subject_group_links) \
                .filter(and_(subject_group_links.c.id_group == id2,
                             subject_group_links.c.id_subject == id1)).first()
            if res is not None:
                group = Group(res.id_group, None)
                groups = [group]
                s = Subject(res.id_subject, None, None)
                s.groups = groups
                return [s]
            else:
                return [None]
        elif table_name1 == STUDENT_SUBJECT_TABLE:
            res = self.session.query(student_subject_links) \
                .filter(and_(student_subject_links.c.id_student == id2,
                             student_subject_links.c.id_subject == id1)).first()
            if res is not None:
                student = Student(res.id_student, None, None, None, None, None)
                s = Subject(res.id_subject, None, None)
                subjects = [s]
                student.subjects = subjects
                return [student]
            else:
                return [None]

        elif table_name1 == TEACHER_SUBJECT_TABLE:
            res = self.session.query(teacher_subject_links) \
                .filter(and_(teacher_subject_links.c.id_teacher == id2,
                             teacher_subject_links.c.id_subject == id1)).first()
            if res is not None:
                s = Subject(res.id_subject, None, None)
                subjects = [s]
                teacher = Teacher(res.id_teacher, None, None, None)
                teacher.subjects = subjects
                return [teacher]
            else:
                return [None]

    def get_many(self, table_name):
        return self.session.query(get_table(table_name)).all()

    # deleting data from tables
    def delete_one(self, id, table_name):
        req = self.session.query(get_table(table_name)).get(id)
        self.session.delete(req)
        self.session.commit()
        return req

    def delete_by_ids(self, id1, id2, table_name):
        if table_name == TEACHER_SUBJECT_TABLE:
            req = teacher_subject_links.delete() \
                .where(and_(teacher_subject_links.c.id_subject == id1,
                            teacher_subject_links.c.id_teacher == id2))
            res = self.session.execute(req)
            self.session.commit()
            return res
        elif table_name == STUDENT_SUBJECT_TABLE:
            req = student_subject_links.delete() \
                .where(and_(student_subject_links.c.id_subject == id1,
                            student_subject_links.c.id_student == id2))
            res = self.session.execute(req)
            self.session.commit()
            return res
        elif table_name == SUBJECT_GROUP_TABLE:
            req = subject_group_links.delete() \
                .where(and_(subject_group_links.c.id_subject == id1,
                            subject_group_links.c.id_group == id2))
            res = self.session.execute(req)
            self.session.commit()
            return res

    # inserting data to table
    def add_row(self, data_to_add, table):
        data = self.array_to_model_data(data_to_add, table)
        if data is not None:
            self.session.add(data)
            self.session.commit()
        return data

    # updating data in table
    def update_row(self, data, table):

        if table == SUBJECT_GROUP_TABLE:
            req = subject_group_links.update() \
                .where(and_(subject_group_links.c.id_subject == data[1],
                            subject_group_links.c.id_group == data[0])) \
                .values(id_subject=data[3], id_group=data[2])
            self.session.execute(req)
            self.session.commit()
            return self.get_one_by_ids(data[3], data[2], table)[0]
        elif table == TEACHER_SUBJECT_TABLE:
            req = teacher_subject_links.update() \
                .where(and_(teacher_subject_links.c.id_subject == data[1],
                            teacher_subject_links.c.id_teacher == data[0])) \
                .values(id_subject=data[3], id_teacher=data[2])
            self.session.execute(req)
            self.session.commit()
            return self.get_one_by_ids(data[3], data[2], table)[0]
        elif table == STUDENT_SUBJECT_TABLE:
            req = student_subject_links.update() \
                .where(and_(student_subject_links.c.id_subject == data[1],
                            student_subject_links.c.id_student == data[0])) \
                .values(id_subject=data[3], id_student=data[2])
            self.session.execute(req)
            self.session.commit()
            return self.get_one_by_ids(data[3], data[2], table)[0]
        else:
            self.session.query(get_table(table)) \
                .filter(get_table(table).id == data.id) \
                .update(
                get_data_table(table, data)
            )
            self.session.commit()
            item = self.get_one(data.id, table)
            return item

    # generating data in table
    def generate_data(self, data_count, table_name):
        res = None
        if table_name == STUDENT_TABLE:
            res = postgres_backend.random_student(self.connection, data_count)
        elif table_name == TEACHER_TABLE:
            res = postgres_backend.random_teacher(self.connection, data_count)
        elif table_name == GROUP_TABLE:
            res = postgres_backend.random_group(self.connection, data_count)
        elif table_name == SUBJECT_TABLE:
            res = postgres_backend.random_subject(self.connection, data_count)
        elif table_name == SUBJECT_GROUP_TABLE:
            res = postgres_backend.random_subject_group(self.connection, data_count)
        elif table_name == TEACHER_SUBJECT_TABLE:
            res = postgres_backend.random_teacher_subject(self.connection, data_count)
        elif table_name == STUDENT_SUBJECT_TABLE:
            res = postgres_backend.random_student_subject(self.connection, data_count)

        if res is not None:
            return list(map(lambda r: self.dict_to_model_data(r, table_name), res))
        else:
            return None

    # searches
    def search_students(self, data):
        res = postgres_backend.search_students(self.connection, data[0], data[1], data[2], data[3])
        if res is not None:
            return res
        else:
            return None

    def search_teachers(self, data):
        res = postgres_backend.search_teachers(self.connection, data[0], data[1], data[2], data[3])
        if res is not None:
            return res
        else:
            return None

    def search_students_by_teacher_and_group(self, data):
        res = postgres_backend.search_students_by_teacher_and_group(self.connection, data[0], data[1], data[2], data[3])
        if res is not None:
            return res
        else:
            return None

    @staticmethod
    def dict_to_model_data(res, item_type):
        if item_type == STUDENT_TABLE:
            return Student(res['id'], res['first_name'], res['last_name'], res['sex'], res['date_of_birth'],
                           res['id_group'])
        elif item_type == SUBJECT_TABLE:
            return Subject(res['id'], res['name'], res['time'])
        elif item_type == GROUP_TABLE:
            return Group(res['id'], res['name'])
        elif item_type == TEACHER_TABLE:
            return Teacher(res['id'], res['first_name'], res['last_name'], res['phone_number'])

        elif item_type == TEACHER_SUBJECT_TABLE:
            return TeacherSubject(
                res['id'],
                Teacher(get_value_if_exists(res, 'id_teacher'), get_value_if_exists(res, 'first_name'),
                        get_value_if_exists(res, 'last_name'), get_value_if_exists(res, 'phone_number')),
                Subject(get_value_if_exists(res, 'id_subject'), get_value_if_exists(res, 'name'),
                        get_value_if_exists(res, 'time')))

        elif item_type == SUBJECT_GROUP_TABLE:
            return SubjectGroup(
                res['id'],
                Subject(get_value_if_exists(res, 'id_subject'), get_value_if_exists(res, 'name'),
                        get_value_if_exists(res, 'time')),
                Group(get_value_if_exists(res, 'id_group'), get_value_if_exists(res, 'name')))

        elif item_type == STUDENT_SUBJECT_TABLE:
            return StudentSubject(
                res['id'],
                Student(get_value_if_exists(res, 'id_student'), get_value_if_exists(res, 'first_name'),
                        get_value_if_exists(res, 'last_name'), get_value_if_exists(res, 'sex'),
                        get_value_if_exists(res, 'date_of_birth'), get_value_if_exists(res, 'id_group')),
                Subject(get_value_if_exists(res, 'id_subject'), get_value_if_exists(res, 'name'),
                        get_value_if_exists(res, 'time')))
        else:
            return None

    def array_to_model_data(self, res, item_type):
        if item_type == STUDENT_TABLE:
            return Student(res[0], res[1], res[2], res[3], res[4], res[5])
        elif item_type == SUBJECT_TABLE:
            return Subject(res[0], res[1], res[2])
        elif item_type == GROUP_TABLE:
            return Group(res[0], res[1])
        elif item_type == TEACHER_TABLE:
            return Teacher(res[0], res[1], res[2], res[3])
        elif item_type == TEACHER_SUBJECT_TABLE:
            new_teacher = self.get_one(res[1], TEACHER_TABLE)
            if new_teacher is None:
                return None

            new_subject = self.get_one(res[2], SUBJECT_TABLE)
            if new_subject is None:
                return None

            new_teacher.subjects.append(new_subject)
            return new_teacher
        elif item_type == SUBJECT_GROUP_TABLE:
            new_group = self.get_one(res[2], GROUP_TABLE)
            if new_group is None:
                return None

            new_subject = self.get_one(res[1], SUBJECT_TABLE)
            if new_subject is None:
                return None

            new_subject.groups.append(new_group)

            return new_subject

        elif item_type == STUDENT_SUBJECT_TABLE:
            new_student = self.get_one(res[1], STUDENT_TABLE)
            if new_student is None:
                return None

            new_subject = self.get_one(res[2], SUBJECT_TABLE)
            if new_subject is None:
                return None

            new_student.subjects.append(new_subject)
            return new_student
        else:
            return None
