import postgres_backend

from models.student import Student
from models.subject import Subject
from models.grade import Grade
from models.group import Group
from models.teacher import Teacher
from models.teacher_subject import TeacherSubject
from models.subject_group import SubjectGroup
from models.student_subject import StudentSubject

GROUP_TABLE = "\"group\""
STUDENT_TABLE = "student"
TEACHER_TABLE = "teacher"
SUBJECT_TABLE = "subject"
GRADE_TABLE = "grade"
SUBJECT_GROUP_TABLE = "subject_group"
TEACHER_SUBJECT_TABLE = "teacher_subject"
STUDENT_SUBJECT_TABLE = "student_subject"


def get_value_if_exists(res, key):
    if key in res:
        return res[key]
    else:
        return None


class Model(object):

    def __init__(self):
        self._cursor = postgres_backend.connect_db()

    @property
    def connection(self):
        return self._cursor

    # reading from tables
    def get_one(self, id, table_name):
        res = postgres_backend.select_from_table_by_id(self.connection, id, table_name)
        if res is not None:
            return self.dict_to_model_data(res, table_name)
        else:
            return None

    def get_many(self, table_name):

        if table_name == SUBJECT_GROUP_TABLE:
            res = postgres_backend.select_all_from_table(self.connection, table_name)
        elif table_name == TEACHER_SUBJECT_TABLE:
            res = postgres_backend.select_all_from_table(self.connection, table_name)
        else:
            res = postgres_backend.select_all_from_table(self.connection, table_name)

        if res is not None:
            return list(map(lambda r: self.dict_to_model_data(r, table_name), res))
        else:
            return None

    # deleting data from tables
    def delete_one(self, id, table_name):
        if table_name == STUDENT_TABLE:
            return self.delete_student(id)
        elif table_name == TEACHER_TABLE:
            return self.delete_teacher(id)
        elif table_name == GROUP_TABLE:
            return self.delete_group(id)
        elif table_name == SUBJECT_TABLE:
            return self.delete_subject(id)
        else:
            res = postgres_backend.delete_by_id(self.connection, id, table_name)
            if res is not None:
                return self.dict_to_model_data(res, table_name)
            else:
                return None

    def delete_student(self, id):
        res = postgres_backend.delete_student(self.connection, id)
        if res is not None:
            return self.dict_to_model_data(res, STUDENT_TABLE)
        else:
            return None

    def delete_teacher(self, id):
        res = postgres_backend.delete_teacher(self.connection, id)
        if res is not None:
            return self.dict_to_model_data(res, TEACHER_TABLE)
        else:
            return None

    def delete_group(self, id):
        res = postgres_backend.delete_group(self.connection, id)
        if res is not None:
            return self.dict_to_model_data(res, GROUP_TABLE)
        else:
            return None

    def delete_subject(self, id):
        res = postgres_backend.delete_subject(self.connection, id)
        if res is not None:
            return self.dict_to_model_data(res, SUBJECT_TABLE)
        else:
            return None

    # inserting data to table
    def add_row(self, data_to_add, table):
        data = self.array_to_model_data(data_to_add, table)
        res = postgres_backend.insert_data(self.connection, data, table)
        if res is not None:
            return self.dict_to_model_data(res, table)
        else:
            return None

    # updating data in table
    def update_row(self, data, table):
        res = postgres_backend.update_data(self.connection, data, table)
        if res is not None:
            return self.dict_to_model_data(res, table)
        else:
            return None

    # generating data in table
    def generate_data(self, data_count, table_name):
        res = None
        if table_name == STUDENT_TABLE:
            res = postgres_backend.random_student(self.connection,data_count)
        elif table_name == TEACHER_TABLE:
            res = postgres_backend.random_teacher(self.connection,data_count)
        elif table_name == GROUP_TABLE:
            res = postgres_backend.random_group(self.connection,data_count)
        elif table_name == SUBJECT_TABLE:
            res = postgres_backend.random_subject(self.connection,data_count)
        elif table_name == SUBJECT_GROUP_TABLE:
            res = postgres_backend.random_subject_group(self.connection,data_count)
        elif table_name == TEACHER_SUBJECT_TABLE:
            res = postgres_backend.random_teacher_subject(self.connection,data_count)
        elif table_name == STUDENT_SUBJECT_TABLE:
            res = postgres_backend.random_student_subject(self.connection,data_count)

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
        elif item_type == GRADE_TABLE:
            return Grade(res['id'], res['number'])
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

    @staticmethod
    def array_to_model_data(res, item_type):
        if item_type == STUDENT_TABLE:
            return Student(res[0], res[1], res[2], res[3], res[4], res[5])
        elif item_type == GRADE_TABLE:
            return Grade(res[0], res[1])
        elif item_type == SUBJECT_TABLE:
            return Subject(res[0], res[1], res[2])
        elif item_type == GROUP_TABLE:
            return Group(res[0], res[1])
        elif item_type == TEACHER_TABLE:
            return Teacher(res[0], res[1], res[2], res[3])
        elif item_type == TEACHER_SUBJECT_TABLE:
            return TeacherSubject(res[0], Teacher(res[1], None, None, None), Subject(res[2], None, None))
        elif item_type == SUBJECT_GROUP_TABLE:
            return SubjectGroup(res[0], Subject(res[1], None, None), Group(res[2], None))
        elif item_type == STUDENT_SUBJECT_TABLE:
            return StudentSubject(res[0], Student(res[1], None, None, None, None, None), Subject(res[2], None, None))
        else:
            return None
