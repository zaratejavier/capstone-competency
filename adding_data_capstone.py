import sqlite3


# def adding_users():
#     connection = sqlite3.connect('capstone_data.db')
#     cursor = connection.cursor()

#     the_users = [
#         ('Susan', ' Minnis', '325-203-0307', 'susan.minnis@gmail.com',
#          '12343', '1', '2021-11-15', '2020-01-20', 'manager'),
#         ('Margaret', 'Bacon', '678-637-5010', 'Margaret.Bacon@gmail.com',
#             '12938234', '1', '2021-11-15', '2020-02-21', 'manager'),
#         ('Barry', 'Mills', '845-219-5462', 'Barry.Mills@gmail.com',
#             '162348234', '1', '2021-11-15', '2020-03-22', 'manager'),
#         ('Harold', 'Runyon', '918-319-6605', 'Harold.Runyon@gmail.com',
#             '293471', '1', '2021-11-15', '2020-04-23', 'manager'),
#         ('Elizabeth', 'Koon', '818-202-2931', 'Elizabeth.Koon@gmail.com',
#          '0072341', '1', '2021-11-15', '2020-05-24', 'manager'),
#         ('Elizabeth', 'Rickey', '301-509-9707', 'Elizabeth.Rickey@gmail.com',
#          '2397487234', '1', '2021-11-15', '2020-06-25', 'manager'),
#         ('Max', 'Salerno', ' 508-204-3564', 'Max.Salerno@gmail.com',
#          '9147829384', '1', '2021-11-15', '2020-07-26', "manager"),
#         ('Stacey', 'Edward', '541-321-3807', 'Stacey.Edward@gmail.com',
#          '07234', '1', '2021-11-15', '2020-08-27', 'user'),
#         ('Kimberly', 'Gonzalez', '302-981-5850', 'Kimberly.Gonzalez@gmail.com',
#          '64532', '1', '2021-11-15', '2020-09-28', 'user'),
#         ('Tricia', 'Olson', '561-234-1952', 'Tricia.Olson@gmail.com',
#          '76543', '1', '2021-11-15', '2020-10-29', 'user'),
#         ('Elizabeth', 'Wade', '919-244-7638', 'Elizabeth.Wade@gmail.com',
#          '2312', '1', '2021-11-15', '2020-11-30', 'user'),
#         ('Johnna', 'Schwab', '616-498-8697', 'Johnna.Schwab@gmail.com',
#          '4532', '1', '2021-11-15', '2020-12-05', 'user'),
#         ('James', 'Kimball', '352-361-3426', 'James.Kimball@gmail.com',
#          '12343', '1', '2021-11-15', '2020-02-09', 'user'),
#         ('Pearl', 'Hurst', '267-600-1142', 'Pearl.Hurst@gmail.com',
#          '12322', '1', '2021-11-15', '2020-02-10', 'user'),
#     ]
#     insert_sql = "INSERT INTO Users (first_name, last_name, phone, email, password, active, date_created, hire_date, user_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

#     for user in the_users:
#         cursor.execute(insert_sql, user)

#     connection.commit()


# def adding_compentencies():
#     connection = sqlite3.connect('capstone_data.db')
#     cursor = connection.cursor()

#     the_competency = [
#         ('Data Types', '2021-12-02'),
#         ('Variables', '2021-12-02'),
#         ('Boolean Logic', '2021-12-02'),
#         ('Conditionals', '2021-12-02'),
#         ('Loops', '2021-12-02'),
#         ('Data Structures', '2021-12-02'),
#         ('Lists', '2021-12-02'),
#         ('Dictionaries', '2021-12-02'),
#         ('Working with Files', '2021-12-02'),
#         ('Quality Assurance (QA)', '2021-12-02'),
#         ('Object-Oriented Programming', '2021-12-02'),
#         ('Recursion', '2021-12-02'),
#         ('Databases', '2021-12-02')
#     ]
#     insert_sql = "INSERT INTO Compentencies (name, date_created) VALUES (?, ?)"

#     for competency in the_competency:
#         cursor.execute(insert_sql, competency)

#     connection.commit()


# def adding_assessments():
#     connection = sqlite3.connect('capstone_data.db')
#     cursor = connection.cursor()

#     the_assessments = [
#         (1, 'Data Structures Competency Measurement', '2021-12-02'),
#         (10, 'Quality Assurance Competency Measurement', '2021-12-02'),
#         (13, 'DataBases Competency Measurement', '2021-12-02'),
#     ]
#     insert_sql = "INSERT INTO Assessments (competency_id, name, date_created) VALUES (?, ?, ?)"

#     for assessment in the_assessments:
#         cursor.execute(insert_sql, assessment)

#     connection.commit()


def adding_assessment_results():
    connection = sqlite3.connect('capstone_data.db')
    cursor = connection.cursor()

    the_assessment_results = [
        (8, 1, 4, '2021-12-03'),
        (8, 1, 3, '2021-11-03'),
        (8, 1, 2, '2021-10-03'),
        (8, 1, 1, '2021-09-03'),
        (10, 2, 2, '2021-08-03'),
        (10, 2, 3, '2021-12-03'),
        (10, 2, 1, '2021-11-03'),
    ]
    insert_sql = "INSERT INTO Assessment_results (user_id, assessment_id, score, date_taken) VALUES (?, ?, ?, ?)"

    for results in the_assessment_results:
        cursor.execute(insert_sql, results)

    connection.commit()


# adding_users()
# adding_compentencies()
# adding_assessments()
adding_assessment_results()
