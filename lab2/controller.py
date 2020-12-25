import os
import datetime
import time

from model import GROUP_TABLE
from model import GRADE_TABLE
from model import STUDENT_TABLE
from model import SUBJECT_TABLE
from model import TEACHER_TABLE
from model import TEACHER_SUBJECT_TABLE
from model import STUDENT_SUBJECT_TABLE
from model import SUBJECT_GROUP_TABLE
from model import Model
from view import View


class Controller(object):
    MAIN_M = -1
    # GRADE_M = 5
    STUDENT_M = 1
    TEACHER_M = 2
    SUBJECT_M = 3
    GROUP_M = 4
    SUBJECT_GROUP_M = 5
    TEACHER_SUBJECT_M = 6
    STUDENT_SUBJECT_M = 7
    SEARCH_MENU = 8

    def __init__(self):
        self.view = View()
        self.model = Model()

    def start(self):
        current_menu = self.MAIN_M

        while current_menu == self.MAIN_M:
            menu_option = self.view.show_main_menu()
            if menu_option.isdigit():

                while int(menu_option) == self.GROUP_M:
                    group_option = self.view.show_group_menu()
                    if group_option.isdigit():
                        current_menu = self.handle_common_inner_menu(int(group_option), GROUP_TABLE, self.GROUP_M)
                        menu_option = current_menu
                    else:
                        self.view.show_number_exception(group_option)

                while int(menu_option) == self.STUDENT_M:
                    option = self.view.show_student_menu()
                    if option.isdigit():
                        current_menu = self.handle_common_inner_menu(int(option), STUDENT_TABLE, self.STUDENT_M)
                        menu_option = current_menu
                    else:
                        self.view.show_number_exception(option)

                while int(menu_option) == self.TEACHER_M:
                    option = self.view.show_teacher_menu()
                    if option.isdigit():
                        current_menu = self.handle_common_inner_menu(int(option), TEACHER_TABLE, self.TEACHER_M)
                        menu_option = current_menu
                    else:
                        self.view.show_number_exception(option)

                while int(menu_option) == self.SUBJECT_M:
                    option = self.view.show_subject_menu()
                    if option.isdigit():
                        current_menu = self.handle_common_inner_menu(int(option), SUBJECT_TABLE, self.SUBJECT_M)
                        menu_option = current_menu
                    else:
                        self.view.show_number_exception(option)

                while int(menu_option) == self.SUBJECT_GROUP_M:
                    option = self.view.show_subject_group_menu()
                    if option.isdigit():
                        current_menu = self.handle_common_inner_menu(int(option), SUBJECT_GROUP_TABLE,
                                                                     self.SUBJECT_GROUP_M)
                        menu_option = current_menu
                    else:
                        self.view.show_number_exception(option)

                while int(menu_option) == self.STUDENT_SUBJECT_M:
                    option = self.view.show_student_subject_menu()
                    if option.isdigit():
                        current_menu = self.handle_common_inner_menu(int(option), STUDENT_SUBJECT_TABLE,
                                                                     self.STUDENT_SUBJECT_M)
                        menu_option = current_menu
                    else:
                        self.view.show_number_exception(option)

                while int(menu_option) == self.TEACHER_SUBJECT_M:
                    option = self.view.show_teacher_subject_menu()
                    if option.isdigit():
                        current_menu = self.handle_common_inner_menu(int(option), TEACHER_SUBJECT_TABLE,
                                                                     self.TEACHER_SUBJECT_M)
                        menu_option = current_menu
                    else:
                        self.view.show_number_exception(option)

                while int(menu_option) == self.SEARCH_MENU:
                    option = self.view.show_search_menu()
                    if option.isdigit():
                        current_menu = self.handle_search_menu(int(option), self.SEARCH_MENU)
                        menu_option = current_menu
                    else:
                        self.view.show_number_exception(option)

                if int(menu_option) == 0:
                    current_menu = 0
            else:
                self.view.show_number_exception(menu_option)
        exit(0)

    # handle menu options

    def handle_common_inner_menu(self, option, table_name, parent_menu):
        if option == 1:
            self.show_many(table_name)

        elif option == 2:
            self.show_option(table_name)

        elif option == 3:
            self.add_option(table_name)

        elif option == 4:
            self.update_option(table_name)

        elif option == 5:
            self.delete_option(table_name)

        elif option == 6:
            self.generate_option(table_name)

        elif option == 7:
            self.add_option_subject(table_name)

        elif option == 8:
            self.add_option_subject_student(table_name)

        elif option == 0:
            return self.MAIN_M

        else:
            self.view.no_such_menu()

        return parent_menu

    def handle_search_menu(self, option, parent_menu):
        if option == 1:
            self.search_students()

        elif option == 2:
            self.search_teachers()

        elif option == 3:
            self.search_students_by_teacher_and_group()

        elif option == 0:
            return self.MAIN_M

        else:
            self.view.no_such_menu()

        return parent_menu

    # show options

    def show_option(self, table_name):
        id = self.get_id(table_name)
        self.show_one(id, table_name)

    def show_many(self, table_name):
        items = self.model.get_many(table_name)
        self.view.show_items(items, table_name)

    def show_one(self, id, table_name):
        grade = self.model.get_one(id, table_name)
        self.view.show_item(grade, 0, table_name)

    # adding options

    def add_option(self, table_name):
        if table_name == TEACHER_TABLE:
            self.add_teacher_option()
        elif table_name == STUDENT_TABLE:
            self.add_student_option()
        elif table_name == GRADE_TABLE:
            self.add_grade_option()
        elif table_name == GROUP_TABLE:
            self.add_group_option()
        elif table_name == SUBJECT_TABLE:
            self.add_subject_option()
        elif table_name == TEACHER_SUBJECT_TABLE:
            self.add_teacher_subject_option()
        elif table_name == STUDENT_SUBJECT_TABLE:
            self.add_student_subject_option()
        elif table_name == SUBJECT_GROUP_TABLE:
            self.add_subject_group_option()

    def add_option_subject(self, table_name):
        if table_name == STUDENT_TABLE:
            self.add_option(STUDENT_SUBJECT_TABLE)
        elif table_name == GROUP_TABLE:
            self.add_option(SUBJECT_GROUP_TABLE)
        elif table_name == TEACHER_TABLE:
            self.add_option(TEACHER_SUBJECT_TABLE)
        elif table_name == SUBJECT_TABLE:
            self.add_option(TEACHER_SUBJECT_TABLE)

    def add_option_subject_student(self, table_name):
        if table_name == SUBJECT_TABLE:
            self.add_option(STUDENT_SUBJECT_TABLE)

    def add_grade_option(self):
        number = self.view.get_field(GRADE_TABLE, 'number')
        number = self.check_values(number, number.isnumeric(), GRADE_TABLE, 'number')
        data_to_add = ['', number]
        self.add_item(data_to_add, GRADE_TABLE)

    def add_group_option(self):
        name = self.view.get_field(GROUP_TABLE, 'name')
        name = self.check_values(name, True, GROUP_TABLE, 'name')
        data_to_add = ['', name]
        self.add_item(data_to_add, GROUP_TABLE)

    def add_subject_option(self):
        name = self.view.get_field(SUBJECT_TABLE, 'name')
        name = self.check_values(name, True, SUBJECT_TABLE, 'name')
        time_ = self.view.get_field(SUBJECT_TABLE, 'time')
        time_ = self.check_values(time_, time_.isnumeric(), SUBJECT_TABLE, 'time')
        data_to_add = ['', name, time_]
        self.add_item(data_to_add, SUBJECT_TABLE)

    def add_student_option(self):
        first_name = self.view.get_field(STUDENT_TABLE, 'first name')
        first_name = self.check_values(first_name, True, STUDENT_TABLE, 'first name')

        last_name = self.view.get_field(STUDENT_TABLE, 'last name')
        last_name = self.check_values(last_name, True, STUDENT_TABLE, 'last name')

        sex = self.view.get_field(STUDENT_TABLE, 'sex')
        sex = self.check_values(sex, True, STUDENT_TABLE, 'sex')

        id_group = self.get_id('group')
        dat_of_birth = self.get_date()

        data_to_add = ['', first_name, last_name, sex, dat_of_birth, id_group]
        self.add_item(data_to_add, STUDENT_TABLE)

    def add_teacher_option(self):
        first_name = self.view.get_field(TEACHER_TABLE, 'first name')
        first_name = self.check_values(first_name, True, TEACHER_TABLE, 'first name')

        last_name = self.view.get_field(TEACHER_TABLE, 'last name')
        last_name = self.check_values(last_name, True, TEACHER_TABLE, 'last name')

        phone = self.view.get_field(TEACHER_TABLE, 'phone number')
        phone = self.check_values(phone, self.valid_number(phone), TEACHER_TABLE, 'phone number')

        data_to_add = ['', first_name, last_name, phone]
        self.add_item(data_to_add, TEACHER_TABLE)

    def add_teacher_subject_option(self):
        id_teacher = self.get_id("teacher")
        id_subject = self.get_id("subject")
        data_to_add = ['', id_teacher, id_subject]
        self.add_item(data_to_add, TEACHER_SUBJECT_TABLE)

    def add_student_subject_option(self):
        id_student = self.get_id("student")
        id_subject = self.get_id("subject")
        data_to_add = ['', id_student, id_subject]
        self.add_item(data_to_add, STUDENT_SUBJECT_TABLE)

    def add_subject_group_option(self):
        id_group = self.get_id("group")
        id_subject = self.get_id("subject")
        data_to_add = ['', id_subject, id_group]
        self.add_item(data_to_add, SUBJECT_GROUP_TABLE)

    def add_item(self, data_to_add, table_name):
        try:
            item = self.model.add_row(data_to_add, table_name)
            if item is not None:
                self.view.show_item(item, 0, table_name)
            else:
                self.view.display_fk_exception()

        except Exception as e:
            self.view.display_item_already_stored_error(table_name, table_name, e)

    # delete options

    def delete_option(self, table):
        id = self.get_id(table)
        self.delete(id, table)

    def delete(self, id, table):
        try:
            item = self.model.delete_one(id, table)
            self.view.display_item_deletion(item, table)
        except Exception as e:
            self.view.display_exception(table, e)

    # update options

    def update_option(self, table_name):
        if table_name == TEACHER_TABLE:
            self.update_teacher_option()
        elif table_name == STUDENT_TABLE:
            self.update_student_option()
        elif table_name == GROUP_TABLE:
            self.update_group_option()
        elif table_name == SUBJECT_TABLE:
            self.update_subject_option()
        elif table_name == TEACHER_SUBJECT_TABLE:
            self.update_teacher_subject_option()
        elif table_name == SUBJECT_GROUP_TABLE:
            self.update_subject_group_option()
        elif table_name == STUDENT_SUBJECT_TABLE:
            self.update_student_subject_option()

    def update_teacher_option(self):
        menu = True

        id = self.get_id(TEACHER_TABLE)

        teacher = self.model.get_one(id, TEACHER_TABLE)

        if teacher is not None:
            self.view.show_item(teacher, 0, TEACHER_TABLE)
            while menu:
                option = self.view.show_update_teacher_options()
                if option.isdigit():
                    if int(option) == 1:
                        first_name = self.view.get_field(TEACHER_TABLE, 'First name')
                        first_name = self.check_values(first_name, True, TEACHER_TABLE, 'First name')
                        teacher.first_name = first_name
                    elif int(option) == 2:
                        last_name = self.view.get_field(TEACHER_TABLE, 'Last name')
                        last_name = self.check_values(last_name, True, TEACHER_TABLE, 'Last name')
                        teacher.last_name = last_name
                    elif int(option) == 3:
                        phone_number = self.view.get_field(TEACHER_TABLE, 'Phone number')
                        phone_number = self.check_values(phone_number, True, TEACHER_TABLE, 'Phone number')
                        teacher.phone_number = phone_number
                    elif int(option) == 0:
                        menu = False
                    else:
                        self.view.no_such_menu()
                else:
                    self.view.show_number_exception(option)
            try:
                self.update(teacher, TEACHER_TABLE)
            except Exception as e:
                self.view.display_exception(TEACHER_TABLE, e)

        else:
            self.view.display_item_not_yet_stored_error('teacher with id - ' + id, TEACHER_TABLE, None)

    def update_student_option(self):
        menu = True
        id = self.get_id(STUDENT_TABLE)

        student = self.model.get_one(id, STUDENT_TABLE)
        if student is not None:
            self.view.show_item(student, 0, STUDENT_TABLE)
            while menu:
                option = self.view.show_update_student_options()
                if option.isdigit():
                    if int(option) == 1:
                        first_name = self.view.get_field(STUDENT_TABLE, 'First name')
                        first_name = self.check_values(first_name, True, STUDENT_TABLE, 'First name')
                        student.first_name = first_name
                    elif int(option) == 2:
                        last_name = self.view.get_field(STUDENT_TABLE, 'Last name')
                        last_name = self.check_values(last_name, True, STUDENT_TABLE, 'Last name')
                        student.last_name = last_name
                    elif int(option) == 3:
                        sex = self.view.get_field(STUDENT_TABLE, 'Sex')
                        sex = self.check_values(sex, True, STUDENT_TABLE, 'Sex')
                        student.sex = sex
                    elif int(option) == 4:
                        dof = self.get_date()
                        student.date_of_birth = dof
                    elif int(option) == 5:
                        id = self.get_id("group")
                        if self.model.get_one(id, GROUP_TABLE) is not None:
                            student.id_group = id
                        else:
                            self.view.display_missing_item_error('group with id ' + id, None)
                    elif int(option) == 0:
                        menu = False
                    else:
                        self.view.no_such_menu()
                else:
                    self.view.show_number_exception(option)
            try:
                self.update(student, STUDENT_TABLE)
            except Exception as e:
                self.view.display_exception(STUDENT_TABLE, e)
        else:
            self.view.display_item_not_yet_stored_error(STUDENT_TABLE, STUDENT_TABLE, None)

    def update_group_option(self):
        menu = True
        id = self.get_id(GROUP_TABLE)

        group = self.model.get_one(id, GROUP_TABLE)
        if group is not None:
            self.view.show_item(group, 0, GROUP_TABLE)
            while menu:
                option = self.view.show_update_group_options()
                if option.isdigit():
                    if int(option) == 1:
                        name = self.view.get_field(GROUP_TABLE, 'Group name')
                        name = self.check_values(name, True, GROUP_TABLE, 'Group name')
                        group.name = name
                    elif int(option) == 0:
                        menu = False
                    else:
                        self.view.no_such_menu()
                else:
                    self.view.show_number_exception(option)
            try:
                self.update(group, GROUP_TABLE)
            except Exception as e:
                self.view.display_exception(GROUP_TABLE, e)
        else:
            self.view.display_item_not_yet_stored_error(GROUP_TABLE, GROUP_TABLE, None)

    def update_subject_option(self):
        menu = True
        id = self.get_id(SUBJECT_TABLE)

        subject = self.model.get_one(id, SUBJECT_TABLE)
        if subject is not None:
            self.view.show_item(subject, 0, SUBJECT_TABLE)
            while menu:
                option = self.view.show_update_subject_options()
                if option.isdigit():
                    if int(option) == 1:
                        name = self.view.get_field(GROUP_TABLE, 'Subject name')
                        name = self.check_values(name, True, SUBJECT_TABLE, 'Subject name')
                        subject.name = name
                    elif int(option) == 2:
                        credits = self.view.get_field(GROUP_TABLE, 'Credits amount')
                        credits = self.check_values(credits, credits.isnumeric(), SUBJECT_TABLE, 'Credits amount')
                        subject.time = credits
                    elif int(option) == 0:
                        menu = False
                    else:
                        self.view.no_such_menu()
                else:
                    self.view.show_number_exception(option)
            try:
                self.update(subject, SUBJECT_TABLE)
            except Exception as e:
                self.view.display_exception(SUBJECT_TABLE, e)
        else:
            self.view.display_item_not_yet_stored_error(SUBJECT_TABLE, SUBJECT_TABLE, None)

    def update_student_subject_option(self):
        menu = True
        id = self.get_id(STUDENT_SUBJECT_TABLE)

        subject = self.model.get_one(id, STUDENT_SUBJECT_TABLE)
        if subject is not None:
            self.view.show_item(subject, 0, STUDENT_SUBJECT_TABLE)
            while menu:
                option = self.view.show_update_student_subject_options()
                if option.isdigit():
                    if int(option) == 1:
                        id_subject = self.get_id('Subject')
                        subject.subject.id = id_subject
                    if int(option) == 2:
                        id_student = self.get_id('Student')
                        subject.student.id = id_student
                    elif int(option) == 0:
                        menu = False
                    else:
                        self.view.no_such_menu()
                else:
                    self.view.show_number_exception(option)
            try:
                self.update(subject, STUDENT_SUBJECT_TABLE)
            except Exception as e:
                self.view.display_exception(STUDENT_SUBJECT_TABLE, e)
        else:
            self.view.display_item_not_yet_stored_error(STUDENT_SUBJECT_TABLE, STUDENT_SUBJECT_TABLE, None)

    def update_teacher_subject_option(self):
        menu = True
        id =  self.get_id(TEACHER_SUBJECT_TABLE)

        subject = self.model.get_one(id, TEACHER_SUBJECT_TABLE)
        if subject is not None:
            self.view.show_item(subject, 0, TEACHER_SUBJECT_TABLE)
            while menu:
                option = self.view.show_update_teacher_subject_options()
                if option.isdigit():
                    if int(option) == 1:
                        id_subject = self.get_id('Subject')
                        subject.subject.id = id_subject
                    if int(option) == 2:
                        id_teacher = self.get_id('Teacher')
                        subject.teacher.id = id_teacher
                    elif int(option) == 0:
                        menu = False
                    else:
                        self.view.no_such_menu()
                else:
                    self.view.show_number_exception(option)
            try:
                self.update(subject, TEACHER_SUBJECT_TABLE)
            except Exception as e:
                self.view.display_exception(TEACHER_SUBJECT_TABLE, e)
        else:
            self.view.display_item_not_yet_stored_error(TEACHER_SUBJECT_TABLE, TEACHER_SUBJECT_TABLE, None)

    def update_subject_group_option(self):
        menu = True
        id = self.get_id(SUBJECT_GROUP_TABLE)

        subject = self.model.get_one(id, SUBJECT_GROUP_TABLE)
        if subject is not None:
            self.view.show_item(subject, 0, SUBJECT_GROUP_TABLE)
            while menu:
                option = self.view.show_update_subject_group_options()
                if option.isdigit():
                    if int(option) == 1:
                        id_subject = self.get_id('Subject')
                        subject.subject.id = id_subject
                    if int(option) == 2:
                        id_teacher = self.get_id('Group')
                        subject.group.id = id_teacher
                    elif int(option) == 0:
                        menu = False
                    else:
                        self.view.no_such_menu()
                else:
                    self.view.show_number_exception(option)
            try:
                self.update(subject, SUBJECT_GROUP_TABLE)
            except Exception as e:
                self.view.display_exception(SUBJECT_GROUP_TABLE, e)
        else:
            self.view.display_item_not_yet_stored_error(SUBJECT_GROUP_TABLE, SUBJECT_GROUP_TABLE, None)

    def update(self, item, table_name):
        try:
            res = self.model.update_row(item, table_name)
            if res is not None:
                self.view.show_item(res, 0, table_name)
            else:
                self.view.display_fk_exception()
        except Exception as e:
            self.view.display_item_not_yet_stored_error(item.id, table_name, e)

    def generate_option(self, table_name):
        data_count = self.view.get_field(table_name, 'Amount of generated data')
        data_count = self.check_values(data_count, data_count.isnumeric(), table_name,
                                       'Amount of generated data')
        try:
            res = self.model.generate_data(data_count, table_name)

            if res is None:
                self.view.display_generation_error(table_name)
            else:
                self.view.show_items(res, table_name)
        except Exception as e:
            self.view.display_exception(table_name, e)

    # searches
    def search_students(self):
        first_name = self.view.get_field(STUDENT_TABLE, 'first name')
        first_name = self.check_values(first_name, True, STUDENT_TABLE, 'first name')

        sex = self.view.get_field(STUDENT_TABLE, 'sex')
        sex = self.check_values(sex, True, STUDENT_TABLE, 'sex')

        print("Enter start date")
        start_date = self.get_date()
        print("Enter end date")
        end_date = self.get_date()

        data_to_add = [first_name, sex, start_date, end_date]
        try:
            start_t = time.time()
            res = self.model.search_students(data_to_add)
            end_t = time.time()
            self.view.show_student_search_result(res, end_t - start_t)
        except Exception as e:
            self.view.display_exception('student, group', e)

    def search_teachers(self):
        first_name = self.view.get_field(TEACHER_TABLE, 'first name')
        first_name = self.check_values(first_name, True, TEACHER_TABLE, 'first name')

        subject_name = self.view.get_field(TEACHER_TABLE, 'Subject name')
        subject_name = self.check_values(subject_name, True, TEACHER_TABLE, 'Subject name')

        max_credits = self.view.get_field('subject', 'max credits')
        max_credits = self.check_values(max_credits, max_credits.isnumeric(), 'subject', 'max credits')

        min_credits = self.view.get_field('subject', 'min credits')
        min_credits = self.check_values(min_credits, min_credits.isnumeric(), 'subject', 'min credits')

        data_to_add = [first_name, subject_name, max_credits, min_credits]
        try:
            start_t = time.time()
            res = self.model.search_teachers(data_to_add)
            end_t = time.time()
            self.view.show_teachers_search_result(res, end_t - start_t)
        except Exception as e:
            self.view.display_exception('teacher, subject', e)

    def search_students_by_teacher_and_group(self):
        first_name = self.view.get_field(TEACHER_TABLE, 'first name')
        first_name = self.check_values(first_name, True, TEACHER_TABLE, 'first name')

        group_name = self.view.get_field(TEACHER_TABLE, 'Group name')
        group_name = self.check_values(group_name, True, TEACHER_TABLE, 'Group name')

        print("Enter start date")
        start_date = self.get_date()
        print("Enter end date")
        end_date = self.get_date()

        data_to_add = [first_name, group_name, start_date, end_date]
        try:
            start_t = time.time()
            res = self.model.search_students_by_teacher_and_group(data_to_add)
            end_t = time.time()
            self.view.show_students_teachers_search_result(res, end_t - start_t)
        except Exception as e:
            self.view.display_exception('student, teacher, group, subject', e)

    def valid_number(self, phone_number):
        if len(phone_number) != 12:
            return False
        for i in range(12):
            if not phone_number[i].isalnum():
                return False
        return True

    def check_values(self, value, condition, name, field):
        val = value
        while len(val) == 0 or not condition:
            self.view.display_value_exception(field)
            val = self.view.get_field(name, field)
        return val

    def get_id(self, name):
        id = self.view.get_id(name)
        while not id.isnumeric():
            self.view.show_number_exception(id)
            id = self.view.get_id(name)
        return id

    def get_date(self):
        while True:
            try:
                year = int(self.view.get_field('year', ''))
                month = int(self.view.get_field('month', ''))
                day = int(self.view.get_field('day', ''))
                date = datetime.date(year, month, day)
                return date
            except ValueError:
                self.view.display_date_error()
