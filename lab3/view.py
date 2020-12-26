from model import GRADE_TABLE
from model import GROUP_TABLE
from model import SUBJECT_TABLE
from model import STUDENT_TABLE
from model import TEACHER_TABLE
from model import TEACHER_SUBJECT_TABLE
from model import STUDENT_SUBJECT_TABLE
from model import SUBJECT_GROUP_TABLE


class View(object):

    @staticmethod
    def show_main_menu():
        return input("Main menu:\n"
                     "\t1. Student\n"
                     "\t2. Teacher;\n"
                     "\t3. Subject;\n"
                     "\t4. Group;\n"
                     "\t5. Subject Group;\n"
                     "\t6. Teacher Subject;\n"
                     "\t7. Student Subject;\n"
                     "\t8. Search menu;\n"
                     "\t0. Exit\n")

    @staticmethod
    def show_search_menu():
        return input("Search menu:\n"
                     "\t1. Search students\n"
                     "\t2. Search teachers;\n"
                     "\t3. Search students by teacher and group;\n"
                     "\t0. Exit\n")

    @staticmethod
    def show_group_menu() -> str:
        return input("Group menu:\n"
                     "\t1. Show all groups;\n"
                     "\t2. Display group by id\n"
                     "\t3. Add group;\n"
                     "\t4. Update group\n"
                     "\t5. Delete group;\n"
                     "\t6. Generate groups;\n"
                     "\t7. Add subject to group;\n"
                     "\t0. Exit\n")

    @staticmethod
    def show_student_menu() -> str:
        return input("Student menu:\n"
                     "\t1. Show all students;\n"
                     "\t2. Display student by id\n"
                     "\t3. Add student;\n"
                     "\t4. Update student\n"
                     "\t5. Delete student;\n"
                     "\t6. Generate students;\n"
                     "\t7. Add subject to student;\n"
                     "\t0. Exit\n")

    @staticmethod
    def show_teacher_menu() -> str:
        return input("Teacher menu:\n"
                     "\t1. Show all teachers;\n"
                     "\t2. Display teacher by id\n"
                     "\t3. Add teacher;\n"
                     "\t4. Update teacher\n"
                     "\t5. Delete teacher;\n"
                     "\t6. Generate teachers;\n"
                     "\t7. Add subject to teacher;\n"
                     "\t0. Exit\n")

    @staticmethod
    def show_subject_menu() -> str:
        return input("Subject menu:\n"
                     "\t1. Show all subjects;\n"
                     "\t2. Display subject by id\n"
                     "\t3. Add subject;\n"
                     "\t4. Update subject\n"
                     "\t5. Delete subject;\n"
                     "\t6. Generate subjects;\n"
                     "\t7. Add subject to teacher;\n"
                     "\t8. Add subject to student;\n"
                     "\t0. Exit\n")

    @staticmethod
    def show_subject_group_menu() -> str:
        return input("Subject group menu:\n"
                     "\t1. Show all subject groups;\n"
                     "\t2. Display subject group by id\n"
                     "\t3. Add subject to group;\n"
                     "\t4. Update subject group connection\n"
                     "\t5. Delete subject group connection;\n"
                     "\t6. Generate subjects group connections;\n"
                     "\t0. Exit\n")

    @staticmethod
    def show_teacher_subject_menu() -> str:
        return input("Teacher Subject menu:\n"
                     "\t1. Show all teacher subjects;\n"
                     "\t2. Display teacher subjects by id\n"
                     "\t3. Add subject to teacher;\n"
                     "\t4. Update teacher subject connection\n"
                     "\t5. Delete teacher subject connection;\n"
                     "\t6. Generate teachers subjects connections;\n"
                     "\t0. Exit\n")

    @staticmethod
    def show_student_subject_menu() -> str:
        return input("Student Subject menu:\n"
                     "\t1. Show all student subjects;\n"
                     "\t2. Display student subjects by id\n"
                     "\t3. Add subject to student;\n"
                     "\t4. Update student subject connection\n"
                     "\t5. Delete student subject connection;\n"
                     "\t6. Generate student subjects connections;\n"
                     "\t0. Exit\n")

    @staticmethod
    def show_update_teacher_options():
        return input("Select field to update:\n"
                     "\t1. First name;\n"
                     "\t2. Last name\n"
                     "\t3. Phone number;\n"
                     "\t0. Save and exit.\n")

    @staticmethod
    def show_update_student_options() -> str:
        return input("Select field to update:\n"
                     "\t1. First name;\n"
                     "\t2. Last name\n"
                     "\t3. Sex;\n"
                     "\t4. Date of birth;\n"
                     "\t5. Id group;\n"
                     "\t0. Save and exit.\n")

    @staticmethod
    def show_update_group_options() -> str:
        return input("Select field to update:\n"
                     "\t1. Group name;\n"
                     "\t0. Save and exit.\n")

    @staticmethod
    def show_update_subject_options() -> str:
        return input("Select field to update:\n"
                     "\t1. Subject name;\n"
                     "\t2. Credits;\n"
                     "\t0. Save and exit.\n")

    @staticmethod
    def show_update_student_subject_options() -> str:
        return input("Select field to update:\n"
                     "\t1. Subject id;\n"
                     "\t2. Student id;\n"
                     "\t0. Save and exit.\n")

    @staticmethod
    def show_update_teacher_subject_options() -> str:
        return input("Select field to update:\n"
                     "\t1. Subject id;\n"
                     "\t2. Teacher id;\n"
                     "\t0. Save and exit.\n")

    @staticmethod
    def show_update_subject_group_options() -> str:
        return input("Select field to update:\n"
                     "\t1. Subject id;\n"
                     "\t2. Group id;\n"
                     "\t0. Save and exit.\n")

    @staticmethod
    def display_missing_item_error(item, err):
        print('**************************************************************')
        print('We are sorry, we have no {}!'.format(item.upper()))
        if err is not None:
            print('{}'.format(err.args[0]))
        print('**************************************************************')

    @staticmethod
    def display_item_already_stored_error(item, item_type, err):
        print('**************************************************************')
        print('Hey! We already have {} in our {} list!'
              .format(item.upper(), item_type))
        if err is not None:
            print('{}'.format(err.args[0]))
        print('**************************************************************')

    @staticmethod
    def display_item_not_yet_stored_error(item, item_type, err):
        print('**************************************************************')
        print('We don\'t have any {} in our {} list. Please insert it first!'
              .format(item, item_type))
        if err is not None:
            print('{}'.format(err.args[0]))
        print('**************************************************************')

    @staticmethod
    def display_item_stored(item, item_type):
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('Hooray! We have just added some {} to our {} list!'
              .format(item.upper(), item_type))
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

    @staticmethod
    def display_change_item_type(older, newer):
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
        print('Change item type from "{}" to "{}"'.format(older, newer))
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')

    @staticmethod
    def display_item_updated(item, o_price, o_quantity, n_price, n_quantity):
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
        print('Change {} price: {} --> {}'
              .format(item, o_price, n_price))
        print('Change {} quantity: {} --> {}'
              .format(item, o_quantity, n_quantity))
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')

    @staticmethod
    def no_such_menu():
        print('--------------------------------------------------------------')
        print('There is no such menu option')
        print('--------------------------------------------------------------')

    # some actions
    @staticmethod
    def get_id(name):
        return input("Enter {} id : ".format(name))

    @staticmethod
    def get_field(name, field):
        return input("Enter {} {} : ".format(name, field))

    # showing models
    def show_items(self, items, table_name):
        print('--- {}S LIST ---'.format(table_name.upper()))
        if items is not None:
            for i, item in enumerate(items):
                self.show_item(item, i, table_name)
        else:
            print('There is no items in this table - {}'.format(table_name))

    # show model

    @staticmethod
    def show_item(item, i, name):
        if item is not None:
            if name == GRADE_TABLE:
                print('* {}. id - {}, number - {}'.format(i + 1, item.id, item.number))
            elif name == GROUP_TABLE:
                print('* {}. id - {}, name - {}'.format(i + 1, item.id, item.name))
            elif name == SUBJECT_TABLE:
                print('* {}. id - {}, name - {}, time - {}'
                      .format(i + 1, item.id, item.name, item.time))
            elif name == STUDENT_TABLE:
                print('* {}. id - {}, first name - {}, last name - {}, sex - {}, id_group - {}'
                      .format(i + 1, item.id, item.first_name, item.last_name, item.sex, item.id_group))
            elif name == TEACHER_TABLE:
                print('* {}. id - {}, first name - {}, last name - {}, phone number - {}'
                      .format(i + 1, item.id, item.first_name, item.last_name, item.phone_number))

            elif name == TEACHER_SUBJECT_TABLE:
                for j, subject in enumerate(item.subjects):
                    print('* {}.  id_teacher - {}, id_subject - {}'
                          .format(j + 1,  item.id, subject.id))

            elif name == STUDENT_SUBJECT_TABLE:
                for j, subject in enumerate(item.subjects):
                    print('* {}.  id_student - {}, id_subject - {}'
                          .format(j + 1, item.id, subject.id))

            elif name == SUBJECT_GROUP_TABLE:
                for j, group in enumerate(item.groups):
                    print('* {}. id_group - {}, id_subject - {}'
                          .format(j + 1, group.id, item.id))

            elif name == TEACHER_SUBJECT_TABLE + "old":
                print('* {}. id - {}, id_subject - {}, id_teacher- {}'
                      .format(i + 1, item.id, item.subject.id, item.teacher.id))

            elif name == STUDENT_SUBJECT_TABLE + "old":
                print('* {}. id - {}, id_subject - {}, id_student- {}'
                      .format(i + 1, item.id, item.subject.id, item.student.id))

            elif name == SUBJECT_GROUP_TABLE + "old":
                print('* {}. id - {}, id_subject - {}, id_group- {}'
                      .format(i + 1, item.id, item.subject.id, item.group.id))
        else:
            print('There is no such {}.'.format(name))

    @staticmethod
    def show_number_exception(num):
        print('Entered value - {} is not a NUMBER'.format(num))

    def display_item_deletion(self, item, name):
        if item is not None:
            print('--------------------------------------------------------------')
            print('We have just removed {} from our database'.format(name))
            self.show_item(item, 0, name)
            print('--------------------------------------------------------------')
        else:
            print('There is no element to delete.')

    def display_deletion_result(self, result, name):
        if result.rowcount != 0:
            print('--------------------------------------------------------------')
            print('We have just removed {} from our database'.format(name))
            print('--------------------------------------------------------------')
        else:
            print('There is no element to delete.')

    @staticmethod
    def display_value_exception():
        print('--------------------------------------------------------------')
        print('Your provided value is empty or not a number')
        print('--------------------------------------------------------------')

    @staticmethod
    def display_fk_exception():
        print('--------------------------------------------------------------')
        print('Your provided foreign ids are incorrect ')
        print('--------------------------------------------------------------')

    @staticmethod
    def display_date_error():
        print('--------------------------------------------------------------')
        print('Your provided value is not a date')
        print('--------------------------------------------------------------')

    def display_generation_error(self, table_name):
        print('--------------------------------------------------------------')
        print("Error generating data for - {} table".format(table_name))
        print('--------------------------------------------------------------')

    def display_exception(self, table_name, exception):
        print('--------------------------------------------------------------')
        print("Error occurred while performing operation on table - {}".format(table_name))
        print("Error - {}".format(exception.args[0]))
        print('--------------------------------------------------------------')

    def show_student_search_result(self, res, execution_time):
        print('--- STUDENTS LIST ---')
        if res is not None:
            for i, item in enumerate(res):
                print('* {}. id - {}, first name - {}, last name - {}, sex - {}' \
                      'date of birth - {}, group name - {}, group id - {}'
                      .format(i + 1, item['id'], item['first_name'], item['last_name'], item['sex'],
                              item['date_of_birth'], item['group_name'], item['group_id']))
            print('Search duration - {}'.format(execution_time))
        else:
            print('Search result is empty')

    def show_teachers_search_result(self, res, execution_time):
        print('--- TEACHERS LIST ---')
        if res is not None:
            for i, item in enumerate(res):
                print('* {}. id - {}, first name - {}, last name - {}, phone number - {}' \
                      'subject name - {}, subject credits - {}, subject id - {}'
                      .format(i + 1, item['id'], item['first_name'], item['last_name'], item['phone_number'],
                              item['subject_name'], item['credits'], item['id_subject']))
            print('Search duration - {}'.format(execution_time))
        else:
            print('Search result is empty')

    def show_students_teachers_search_result(self, res, execution_time):
        print('--- STUDENTS LIST WITH TEACHER, GROUP and SUBJECT ---')
        if res is not None:
            for i, item in enumerate(res):
                print('* {}. id - {}, student first name - {}, student last name - {}, student date of birth - {}' \
                      'group name - {}, group id - {}, subject id - {}, subject name - {}, teacher id - {}, '
                      ' teacher first name - {}, teacher last name - {},'
                      .format(i + 1, item['id_student'], item['first_name_s'], item['last_name_s'],
                              item['date_of_birth'],
                              item['group_name'], item['id_group'], item['id_subject'], item['sb_name'],
                              item['id_teacher'], item['first_name_t'], item['last_name_t']))
            print('Search duration - {}'.format(execution_time))
        else:
            print('Search result is empty')
