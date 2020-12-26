import psycopg2

from psycopg2.extras import RealDictCursor

DB_NAME = "postgres2"
DB_USER = "postgres"
DB_PASSWORD = "7770"
HOST = "localhost"
PORT = 5432


def connect_db(db_name=DB_NAME):
    connection = psycopg2.connect(database=db_name, user=DB_USER,
                                  password=DB_PASSWORD, host=HOST, port=PORT)
    connection.autocommit = True
    # Create a cursor connection object to a PostgreSQL instance and print the connection properties.
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    print(connection.get_dsn_parameters(), "\n")
    return cursor


from psycopg2 import OperationalError, IntegrityError, ProgrammingError


def connect(func):
    def inner_func(conn, *args, **kwargs):
        try:
            # I don't know if this is the simplest and fastest query to try
            conn.execute(
                'SELECT name FROM sqlite_temp_master WHERE type="table";')
        except (AttributeError, ProgrammingError):
            conn = connect_db(DB_NAME)
        return func(conn, *args, **kwargs)

    return inner_func


def disconnect_from_db(db=None, cursor=None):
    if db is not DB_NAME:
        print("You are trying to disconnect from a wrong DB")
    if cursor is not None:
        cursor.close()


def select_from_table_by_id(cur, item_id, table_name):
    sql = 'SELECT * FROM {} WHERE id={}'.format(table_name, item_id)
    cur.execute(sql)
    return cur.fetchone()


def select_all_from_table(cur, table_name):
    sql = 'SELECT * FROM {}'.format(table_name)
    cur.execute(sql)
    results = cur.fetchall()
    if cur.rowcount == 0:
        return None
    return results


def select_all_from_teacher_subject_table(cur):
    sql = 'SELECT ts.id as ts_id, t.first_name, t.last_name, s.name from teacher as t ' \
          'INNER JOIN teacher_subject as ts ' \
          'ON t.id = ts.id_teacher ' \
          'INNER JOIN subject as s ' \
          'ON ts.id_subject = s.id'
    cur.execute(sql)
    results = cur.fetchall()
    if cur.rowcount == 0:
        return None
    return results


def select_all_from_subject_group_table(cur):
    sql = 'SELECT sg.id as sg_id, s.id as s_id, s.name as s_name, s.time as s_time, g.id as g_id, g.name as g_name from subject as s ' \
          'INNER JOIN subject_group as sg ' \
          'ON s.id = sg.id_subject ' \
          'INNER JOIN "group" as g ' \
          'ON sg.id_group = g.id'
    cur.execute(sql)
    results = cur.fetchall()
    if cur.rowcount == 0:
        return None
    return results


def select_from_teacher_subject_table_by_id(cur, item_id):
    sql = 'SELECT ts.id as ts_id, t.first_name, t.last_name, s.name from teacher as t ' \
          'INNER JOIN teacher_subject as ts ' \
          'ON t.id = ts.id_teacher ' \
          'INNER JOIN subject as s ' \
          'ON ts.id_subject = s.id' \
          'WHERE ts.id={}'.format(item_id)
    cur.execute(sql)
    results = cur.fetchall()
    if cur.rowcount == 0:
        return None
    return results


def select_from_subject_group_table_by_id(cur, item_id):
    sql = 'SELECT sg.id as sg_id, s.id as s_id, s.name as s_name, s.time as s_time, g.id as g_id, g.name as g_name from subject as s ' \
          'INNER JOIN subject_group as sg ' \
          'ON s.id = sg.id_subject ' \
          'INNER JOIN "group" as g ' \
          'ON sg.id_group = g.id' \
          'WHERE sg.id={}'.format(scrub(item_id))
    cur.execute(sql)
    results = cur.fetchall()
    if cur.rowcount == 0:
        return None
    return results


def delete_student(cur, item_id):

    sql_delete_grade = 'DELETE FROM {} WHERE id_student={}'.format('grade_student', item_id)
    sql_delete_subject = 'DELETE FROM {} WHERE id_student={}'.format('student_subject', item_id)

    cur.execute(sql_delete_grade)
    cur.execute(sql_delete_subject)

    return delete_by_id(cur, item_id, 'student')


def delete_teacher(cur, item_id):

    sql_delete_grade = 'DELETE FROM {} WHERE id_teacher={}'.format('grade_teacher', item_id)
    sql_delete_subject = 'DELETE FROM {} WHERE id_teacher={}'.format('teacher_subject', item_id)

    cur.execute(sql_delete_grade)
    cur.execute(sql_delete_subject)

    return delete_by_id(cur, item_id, 'teacher')


def delete_group(cur, item_id):

    sql_delete_group = 'DELETE FROM {} WHERE id_group={}'.format('subject_group', item_id)
    sql_delete_group_from_student = 'DELETE FROM {} WHERE id_group={}'.format('student', item_id)
    cur.execute(sql_delete_group)
    cur.execute(sql_delete_group_from_student)

    return delete_by_id(cur, item_id, '\"group\"')


def delete_subject(cur, item_id):

    sql_delete_subject = 'DELETE FROM {} WHERE id_subject={}'.format('subject_group', item_id)
    sql_delete_student = 'DELETE FROM {} WHERE id_subject={}'.format('student_subject', item_id)
    sql_delete_teacher = 'DELETE FROM {} WHERE id_subject={}'.format('teacher_subject', item_id)

    cur.execute(sql_delete_subject)
    cur.execute(sql_delete_student)
    cur.execute(sql_delete_teacher)

    return delete_by_id(cur, item_id, 'subject')


def delete_by_id(cur, item_id, table_name):
    item_id = scrub(item_id)
    sql_check = 'SELECT EXISTS(SELECT 1 FROM {} WHERE id={} LIMIT 1)' \
        .format(table_name, item_id)
    sql_delete = 'DELETE FROM {} WHERE id={} RETURNING *'.format(table_name, item_id)
    cur.execute(sql_check)
    result = cur.fetchone()
    if result['exists']:
        cur.execute(sql_delete)
        return cur.fetchone()
    else:
        return None


def insert_data(cur, item, table_name):
    sql_check = get_check_insert_possibility_sql(item, table_name)
    sql = get_inserting_sql_for_table(item, table_name)

    if sql_check is None:
        cur.execute(sql)
        return cur.fetchone()
    else:
        cur.execute(sql_check)
        result = cur.fetchone()
        if result['exists']:
            cur.execute(sql)
            return cur.fetchone()
        else:
            return None


def update_data(cur, item, table_name):
    sql_check = get_check_insert_possibility_sql(item, table_name)
    sql = get_updating_sql_for_table(item, table_name)

    if sql_check is None:
        cur.execute(sql)
        return cur.fetchone()
    else:
        cur.execute(sql_check)
        result = cur.fetchone()
        if result['exists']:
            cur.execute(sql)
            return cur.fetchone()
        else:
            return None


# randomizing data
def random_group(cur, count):
    sql = "INSERT into \"group\" (name) " \
          "SELECT chr(trunc(65 + random() * 25)::int) " \
          "|| chr(trunc(65 + random() * 25)::int) " \
          "|| '-' " \
          "|| (random() * 100)::int as name " \
          "from GENERATE_SERIES(1, {}) as seq " \
          "RETURNING *".format(count)
    cur.execute(sql)
    return cur.fetchall()


def random_subject(cur, count):
    sql = "INSERT into subject (name, time) " \
          "SELECT " \
          "(case (random() * 8)::int " \
          "when 0 then 'Oop' " \
          "when 1 then 'Database' " \
          "when 2 then 'Physics' " \
          "when 3 then 'Philosophy' " \
          "when 4 then 'Web programing' " \
          "when 5 then 'Java' " \
          "when 6 then 'Math' " \
          "when 7 then 'English' " \
          "when 8 then 'Ukrainian language' " \
          "end) as name, " \
          "(random() * 100) as time " \
          "from GENERATE_SERIES(1, {}) as seq " \
          "RETURNING *".format(count)
    cur.execute(sql)
    return cur.fetchall()


def random_student(cur, count):
    sql = "INSERT into student (first_name, last_name, sex, id_group, date_of_birth) " \
          "SELECT " \
          "(case (random() * 3)::int " \
          "when 0 then 'Katya' " \
          "when 1 then 'Dima' " \
          "when 2 then 'Andrey' " \
          "when 3 then 'Olya' " \
          "end) || seq as first_name, " \
          "(case (random() * 3)::int " \
          "when 0 then 'Lopatkina' " \
          "when 1 then 'Lahno' " \
          "when 2 then 'Kulish' " \
          "when 3 then 'Shupik' " \
          "end) as last_name , " \
          "(case (random() * 1)::int " \
          "when 0 then 'Female'  " \
          "when 1 then 'Male' end) " \
          "as sex, " \
          "get_group_id() as id_group, " \
          "((NOW() + (random() * (NOW() - INTERVAL '20 years' - NOW())))::date) as date_of_birth " \
          "from GENERATE_SERIES(1, {}) as seq " \
          "RETURNING *".format(count)
    cur.execute(sql)
    return cur.fetchall()


def random_teacher(cur, count):
    sql = "INSERT into teacher (first_name, last_name, phone_number) " \
          "SELECT " \
          "(case (random() * 3)::int " \
          "when 0 then 'Oleg' " \
          "when 1 then 'Dmytro' " \
          "when 2 then 'Pavel' " \
          "when 3 then 'Olya' " \
          "end) || (random() * seq)::int as first_name, " \
          "(case (random() * 3)::int " \
          "when 0 then 'Melnik' " \
          "when 1 then 'Malyutin' " \
          "when 2 then 'Nazarenko' " \
          "when 3 then 'Legeza' " \
          "end) as last_name, " \
          "('380' " \
          "|| (RANDOM() * 9)::INT " \
          "|| (RANDOM() * 9)::INT " \
          "|| (RANDOM() * 9)::INT " \
          "|| (RANDOM() * 9)::INT " \
          "|| (RANDOM() * 9)::INT " \
          "|| (RANDOM() * 9)::INT " \
          "|| (RANDOM() * 9)::INT " \
          "|| (RANDOM() * 9)::INT " \
          "|| (RANDOM() * 9)::INT) as phone_number " \
          "from GENERATE_SERIES(1, {}) as seq " \
          "RETURNING *".format(count)
    cur.execute(sql)
    return cur.fetchall()


def random_teacher_subject(cur, count):
    sql = "insert into teacher_subject (id_teacher, id_subject) " \
          "select get_teacher_id(), get_subject_id() " \
          "FROM generate_series(1, '{}') ON CONFLICT DO NOTHING RETURNING *".format(count)
    cur.execute(sql)
    return cur.fetchall()


def random_student_subject(cur, count):
    sql = "insert into student_subject (id_student, id_subject) " \
          "select get_student_id(), get_subject_id() " \
          "FROM generate_series(1, '{}') ON CONFLICT DO NOTHING RETURNING *".format(count)
    cur.execute(sql)
    return cur.fetchall()


def random_subject_group(cur, count):
    sql = "insert into subject_group (id_subject, id_group) " \
          "select get_subject_id(), get_group_id() " \
          "FROM generate_series(1, '{}') ON CONFLICT DO NOTHING RETURNING *".format(count)
    cur.execute(sql)
    return cur.fetchall()


def search_students(cur, first_name, sex, star_date, end_date):
    sql = "SELECT s.id, first_name, last_name, sex, date_of_birth, gr.name as group_name, gr.id as group_id " \
          "from student as s " \
          "inner join \"group\" as gr ON gr.id = s.id_group " \
          "where first_name like '%{}%' " \
          "and sex like '{}' " \
          "and date_of_birth >= '{}' " \
          "and date_of_birth <= '{}' " \
          "order by s.id ASC".format(scrub(first_name), scrub(sex), star_date, end_date)
    cur.execute(sql)
    return cur.fetchall()


def search_teachers(cur, first_name, subject_name, max_credits, min_credits):
    sql = "SELECT teacher.id, first_name, last_name, phone_number, s.name as subject_name, s.time as credits, s.id as id_subject " \
          "from teacher " \
          "inner join teacher_subject as ts ON teacher.id = ts.id_teacher " \
          "inner join subject as s ON s.id = ts.id_subject " \
          "where first_name like '%{}%' " \
          "and s.name like '%{}%' " \
          "and s.time >= '{}' " \
          "and s.time <= '{}' " \
          "order by s.id ASC" \
        .format(scrub(first_name), scrub(subject_name), min_credits, max_credits)
    cur.execute(sql)
    return cur.fetchall()


def search_students_by_teacher_and_group(cur, first_name, group_name, start_date, end_date):
    sql = "SELECT DISTINCT s.id as id_student, s.first_name as first_name_s, s.last_name as last_name_s, s.date_of_birth, gr.name as group_name, " \
          "gr.id as id_group, sb.id as id_subject, sb.name as sb_name, teach.id as id_teacher, teach.first_name as first_name_t, " \
          "teach.last_name as last_name_t " \
          "from " \
          "student as s " \
          "inner join \"group\" as gr on s.id_group = gr.id " \
          "inner join subject_group as sg on sg.id_group = gr.id " \
          "inner join subject as sb on sg.id_subject = sb.id " \
          "inner join teacher_subject as ts on ts.id_subject = sb.id " \
          "inner join teacher as teach on teach.id = ts.id_teacher " \
          "where teach.first_name like '%{}%' " \
          "and gr.name like '%{}%' " \
          "and s.date_of_birth >= '{}' " \
          "and s.date_of_birth <= '{}' " \
          "order by s.id asc" \
        .format(scrub(first_name), group_name, start_date, end_date)
    cur.execute(sql)
    return cur.fetchall()


def get_check_insert_possibility_sql(item, table_name):
    sql_check = 'SELECT EXISTS(SELECT 1 FROM "{}" WHERE id={} LIMIT 1)'
    sql_check2 = ' AND EXISTS(SELECT 1 FROM "{}" WHERE id={} LIMIT 1) as exists'

    if table_name == '\"group\"':
        sql_check = None
    elif table_name == 'subject':
        sql_check = None
    elif table_name == 'student':
        sql_check = sql_check.format('group', item.id_group)
    elif table_name == 'teacher':
        sql_check = None
    elif table_name == 'teacher_subject':
        sql_check = sql_check.format('teacher', item.teacher.id) + sql_check2.format('subject', item.subject.id)
    elif table_name == 'student_subject':
        sql_check = sql_check.format('student', item.student.id) + sql_check2.format('subject',
                                                                                            item.subject.id)
    elif table_name == 'subject_group':
        sql_check = sql_check.format('subject', item.subject.id) + sql_check2.format('group',
                                                                                            item.group.id)

    return sql_check


def get_updating_sql_for_table(item, table_name):
    if table_name == '\"group\"':
        return "UPDATE \"group\" SET name = '{}' where id = '{}' RETURNING *".format(item.name, item.id)
    elif table_name == 'subject':
        return "UPDATE subject SET name = '{}', time = '{}' where id = '{}' RETURNING *" \
            .format(item.name, item.time, item.id)
    elif table_name == 'student':
        return "UPDATE student SET first_name = '{}', last_name = '{}',  sex= '{}', date_of_birth = '{}', id_group = " \
               "'{}' where id = '{}' RETURNING *" \
            .format(item.first_name, item.last_name, item.sex, item.date_of_birth, item.id_group, item.id)
    elif table_name == 'teacher':
        return "UPDATE teacher SET first_name = '{}', last_name = '{}', phone_number = '{}' where id = '{}' RETURNING *" \
            .format(item.first_name, item.last_name, item.phone_number, item.id)
    elif table_name == 'teacher_subject':
        return "UPDATE teacher_subject SET id_teacher = '{}', id_subject = '{}' where id = '{}' RETURNING *" \
            .format(item.teacher.id, item.subject.id, item.id)
    elif table_name == 'student_subject':
        return "UPDATE student_subject SET id_student = '{}', id_subject = '{}' where id = '{}' RETURNING *" \
            .format(item.student.id, item.subject.id, item.id)
    elif table_name == 'subject_group':
        return "UPDATE subject_group SET id_subject = '{}', id_group = '{}' where id = '{}' RETURNING *" \
            .format(item.subject.id, item.group.id, item.id)


def get_inserting_sql_for_table(item, table_name):
    if table_name == 'grade':
        return "INSERT INTO grade (number) VALUES ('{}') RETURNING *".format(item.number)
    elif table_name == '\"group\"':
        return "INSERT INTO \"group\" (name) VALUES ('{}') RETURNING *".format(item.name)
    elif table_name == 'subject':
        return "INSERT INTO subject (name, time) VALUES ('{}', '{}') RETURNING *".format(item.name, item.time)
    elif table_name == 'student':
        return "INSERT INTO student (first_name, last_name, sex, date_of_birth, id_group) VALUES ('{}', '{}', '{}', '{}', '{}') RETURNING *" \
            .format(item.first_name, item.last_name, item.sex, item.date_of_birth, item.id_group)
    elif table_name == 'teacher':
        return "INSERT INTO teacher (first_name, last_name, phone_number) VALUES ('{}', '{}', '{}') RETURNING *" \
            .format(item.first_name, item.last_name, item.phone_number)
    elif table_name == 'teacher_subject':
        return "INSERT INTO teacher_subject (id_teacher, id_subject) VALUES ('{}', '{}') RETURNING *" \
            .format(item.teacher.id, item.subject.id)
    elif table_name == 'subject_group':
        return "INSERT INTO subject_group (id_subject, id_group) VALUES ('{}', '{}') RETURNING *" \
            .format(item.subject.id, item.group.id)
    elif table_name == 'student_subject':
        return "INSERT INTO student_subject (id_subject, id_student) VALUES ('{}', '{}') RETURNING *" \
            .format(item.subject.id, item.student.id)


def scrub(input_string):
    return ''.join(k for k in input_string if k.isalnum())
