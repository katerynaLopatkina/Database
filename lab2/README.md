# Лабораторна робота № 2.

Створення додатку бази даних, орієнтованого на взаємодію з СУБД PostgreSQL
Обрана предметна галузь - школа.

# teacher

|name|data_type|not null|PK|FK|
|--|--|--|--|--|
|id|integer|yes|yes|
|firts_name|text|yes|no|
|last_name|text|yes|no|
|phone_number|text|yes|no|

# subject

|name|data_type|not null|PK|FK|
|--|--|--|--|--|
|id|integer|yes|yes|
|name|text|yes|no|
|time|integer|yes|no|

# group

|name|data_type|not null|PK|FK|
|--|--|--|--|--|
|id|integer|yes|yes|
|name|text|yes|no|

# student

|name|data_type|not null|PK|FK|
|--|--|--|--|--|
|id|integer|yes|yes|
|firts_name|text|yes|no|
|last_name|text|yes|no|
|sex|text|yes|no|
|date_of_birth|date|yes|no|
|id_group|integer|yes|yes|


# teacher_subject

|name|data_type|not null|PK|FK|
|--|--|--|--|--|
|id|integer|yes|yes|
|id_teacher|integer|yes|yes|
|id_subject|integer|yes|yes|


# student_subject

|name|data_type|not null|PK|FK|
|--|--|--|--|--|
|id|integer|yes|yes|
|id_subject|integer|yes|yes|
|id_student|integer|yes|yes|


# subject_group

|name|data_type|not null|PK|FK|
|--|--|--|--|--|
|id|integer|yes|yes|
|id_group|integer|yes|yes|
|id_student|integer|yes|yes|