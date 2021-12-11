import pdb
import sqlite3
import datetime
import bcrypt
import csv

connection = sqlite3.connect('capstone_data.db', timeout=10)
cursor = connection.cursor()


class AssesmentResults:
    def __init__(self):
        self.assessment_results_id = None
        self.user_id = None
        self.assessment_id = None
        self.score = None
        self.date_taken = None

    def set_all(self, user_id, assessment_id, score, date_taken):
        self.user_id = user_id,
        self.assessment_id = assessment_id,
        self.score = score,
        self.date_taken = date_taken

    def save(self, cursor):
        insert_sql = '''
         INSERT INTO Assessment_results
            (user_id, assessment_id, score, date_taken)
         VALUES
            (?, ?, ?, ?)
          ;'''
        params = (self.user_id[0], self.assessment_id[0],
                  self.score[0], self.date_taken,)
        assessment = Assessments()
        user = User()
        if assessment.get_assessment(self.assessment_id[0], cursor) and user.get_user(self.user_id[0], cursor):
            cursor.execute(insert_sql, params)
            cursor.connection.commit()
            new_assessment_id = cursor.execute(
                'SELECT last_insert_rowid()').fetchone()
            self.new_assessment_id = new_assessment_id[0]

        else:
            print(
                f"The User_id with id {self.user_id} and {self.assessment_id} does not exist")

    def load(self, cursor):
        select_sql = '''
        SELECT assessment_results_id, user_id, assessment_id, score, date_taken FROM Assessment_results WHERE assessment_results_id = ?
       ;'''
        row = cursor.execute(
            select_sql, (self.assessment_results_id,)).fetchone()
        if not row:
            print("NOTHING RETURNED")
            return
        self.assessment_results_id = row[0]
        self.user_id = row[1]
        self.assessment_id = row[2]
        self.score = row[3]
        self.date_taken = row[4]

    def update(self, cursor):
        insert_sql = '''
          UPDATE Assessment_results
           SET assessment_results_id = ?, user_id = ?, assessment_id = ?, score = ?, date_taken = ?
            WHERE assessment_results_id = ?
          ;'''
        params = (self.assessment_results_id, self.user_id, self.assessment_id,
                  self.score, self.date_taken, self.assessment_results_id)
        cursor.execute(insert_sql, params)
        cursor.connection.commit()


class Assessments:
    def __init__(self):
        self.assessment_id = None
        self.competency_id = None
        self.name = None
        self.date_created = None

    def set_all(self, name, competency_id, date_created=datetime.datetime.now()):
        self.competency_id = competency_id
        self.name = name
        self.date_created = date_created

    def save(self, cursor):
        insert_sql = '''
         INSERT INTO Assessments
            (competency_id, name, date_created)
         VALUES
            (?, ?, ?)
          ;'''
        competency = Competency()
        if competency.get_competency(self.competency_id, cursor):

            params = (self.competency_id, self.name, self.date_created,)
            cursor.execute(insert_sql, params)
            cursor.connection.commit()

            new_assessment_id = cursor.execute(
                'SELECT last_insert_rowid()').fetchone()
            self.new_assessment_id = new_assessment_id[0]
        else:
            print(
                f"The competency with id {self.competency_id} does not exist")

    def get_assessment(self, assessment_id, cursor):
        select_sql = '''
         SELECT assessment_id FROM Assessments WHERE assessment_id = ?
        ;'''

        row = cursor.execute(select_sql, (assessment_id,)).fetchone()

        return row

    def load(self, cursor):
        select_sql = '''
        SELECT assessment_id, competency_id, name, date_created FROM Assessments WHERE assessment_id = ?
       ;'''
        row = cursor.execute(select_sql, (self.assessment_id,)).fetchone()
        if not row:
            print("NOTHING RETURNED")
            return
        self.assessment_id = row[0]
        self.competency_id = row[1]
        self.name = row[2]
        self.date_created = row[3]

    def update(self, cursor):
        insert_sql = '''
          UPDATE Assessments
           SET assessment_id = ?, competency_id = ?, name = ?, date_created = ?
            WHERE assessment_id = ?
          ;'''
        params = (self.assessment_id, self.competency_id, self.name,
                  self.date_created, self.assessment_id)
        cursor.execute(insert_sql, params)
        cursor.connection.commit()


class Competency:
    def __init__(self):
        self.competency_id = None
        self.name = None
        self.date_created = None

    def set_all(self, name, date_created=datetime.datetime.now()):
        self.name = name
        self.date_created = date_created

    def save(self, cursor):
        insert_sql = '''
         INSERT INTO Compentencies
            (name, date_created)
         VALUES
            (?, ?)
          ;'''
        params = (self.name, self.date_created,)
        print(params)
        cursor.execute(insert_sql, params)
        cursor.connection.commit()

        new_competency_id = cursor.execute(
            'SELECT last_insert_rowid()').fetchone()
        self.competency_id = new_competency_id[0]

    def get_competency(self, competency_id, cursor):
        select_sql = '''
         SELECT competency_id FROM Compentencies WHERE competency_id = ?
        ;'''

        row = cursor.execute(select_sql, (competency_id,)).fetchone()

        return row

    def load(self, cursor):
        select_sql = '''
         SELECT * FROM Compentencies WHERE competency_id = ?
        ;'''

        row = cursor.execute(select_sql, (self.competency_id,)).fetchone()

        if not row:
            print("NOTHING RETURNED")
            return
        self.competency_id = row[0]
        self.name = row[1]
        self.date_created = row[2]

    def update(self, cursor):
        insert_sql = '''
          UPDATE Compentencies
           SET name = ?, date_created = ?
            WHERE competency_id = ?
          ;'''
        params = (self.name, self.date_created, self.competency_id)
        print(params)
        cursor.execute(insert_sql, params)
        cursor.connection.commit()


class User:
    def __init__(self):
        self.user_id = None
        self.first_name = None
        self.last_name = None
        self.phone = None
        self.state = None
        self.email = None
        self.__password = None
        self.date_created = None
        self.loggedIn = False
        self.user_type = None
        self.salt = b'$2b$12$orN6aM6R/W/5fRkGgqnjye'
        self.competency = None
        self.active = None
        self.hire_date = None

    def set_all(self, first_name, last_name, email, phone, password, active, user_type, hire_date, date_created=datetime.datetime.now()):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.active = active
        self.user_type = user_type
        self.__password = bcrypt.hashpw(password.encode('utf-8'), self.salt)
        self.date_created = date_created
        self.hire_date = hire_date

    def get_password(self):
        return self.__password

    def change_password(self, new_password):
        if new_password:
            self.__password = bcrypt.hashpw(
                new_password.encode('utf-8'), self.salt)

    def check_password(self, email, new_password, cursor):
        if new_password == '12343':
            print("!!!  PLEASE CHANGE YOUR PASSWORD FROM DEFAULT  !!!")
            new_password = new_password
            select_sql = '''
         SELECT email FROM Users WHERE password=? AND email=?
        ;'''

            row = cursor.execute(select_sql, (new_password, email)).fetchone()

            return row
        elif new_password == '123':
            print("!!!  PLEASE CHANGE YOUR PASSWORD FROM DEFAULT  !!!")
            new_password = bcrypt.hashpw(
                new_password.encode('utf-8'), self.salt)
            select_sql = '''
         SELECT email FROM Users WHERE password=? AND email=?
        ;'''

            row = cursor.execute(select_sql, (new_password, email)).fetchone()

            return row
        else:
            new_password = bcrypt.hashpw(
                new_password.encode('utf-8'), self.salt)
            select_sql = '''
            SELECT email FROM Users WHERE password=? AND email=?
            ;'''

            row = cursor.execute(select_sql, (new_password, email)).fetchone()
            print("---------", row)
            return row

    def change_email(self, new_email):
        self.email = new_email

    def save(self, cursor):
        insert_sql = '''
         INSERT INTO Users
            (first_name, last_name, email, phone, password,
             active, date_created, hire_date, user_type)
         VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?)
          ;'''
        params = (self.first_name, self.last_name, self.email,
                  self.phone, self.__password, self.active,
                  self.date_created, self.hire_date, self.user_type)
        cursor.execute(insert_sql, params)
        cursor.connection.commit()

        new_user_id = cursor.execute('SELECT last_insert_rowid()').fetchone()
        self.user_id = new_user_id[0]

    def update(self, cursor):
        insert_sql = '''
          UPDATE Users
           SET first_name = ?, last_name = ?, email = ?, phone = ?, password = ?,
             active = ?, date_created = ?, hire_date = ?, user_type = ?
            WHERE user_id = ?
          ;'''
        params = (self.first_name, self.last_name, self.email,
                  self.phone, self.__password, self.active,
                  self.date_created, self.hire_date, self.user_type, self.user_id)
        cursor.execute(insert_sql, params)
        cursor.connection.commit()

    def loadByEmail(self, email, cursor):
        select_sql = '''
          SELECT user_id, first_name, last_name, phone, email, date_created, user_type, password, active, hire_date
          FROM Users
          WHERE email=?;
        '''
        row = cursor.execute(select_sql, (email,)).fetchone()
        if not row:
            print("NOTHING RETURNED")
            return
        self.user_id = row[0]
        self.first_name = row[1]
        self.last_name = row[2]
        self.phone = row[3]
        self.email = row[4]
        self.date_created = row[5]
        self.user_type = row[6]
        self.__password = row[7]
        self.active = row[8]
        self.hire_date = row[9]

    def load(self, cursor):
        select_sql = '''
          SELECT user_id, first_name, last_name, phone, email, date_created, user_type, password, active, hire_date
          FROM Users
          WHERE user_id=?;
        '''

        row = cursor.execute(select_sql, (self.user_id,)).fetchone()
        if not row:
            print("NOTHING RETURNED")
            return
        self.user_id = row[0]
        self.first_name = row[1]
        self.last_name = row[2]
        self.phone = row[3]
        self.email = row[4]
        self.date_created = row[5]
        self.user_type = row[6]
        self.__password = row[7]
        self.active = row[8]
        self.hire_date = row[9]

    def get_user(self, user_id, cursor):
        select_sql = '''
         SELECT user_id FROM Users WHERE user_id = ?
        ;'''

        row = cursor.execute(select_sql, (user_id,)).fetchone()

        return row


def create_user_record(cursor):

    print("### Create New User Record ###")
    print("Please fill out the form below to add a new User")

    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    password = input("Password: ")
    user_type = input("user_type user/manager: ")
    hire_date = input("Hire Date YYYY-MM-DD:")

    user = User()
    user.set_all(first_name, last_name, email, phone,
                 password, 1, user_type, hire_date=hire_date)
    user.save(cursor)
    print(f"SUCCESS: '{first_name}' Successfully added!")


def create_competency(cursor):

    competency_name = input("Compentcy: ")

    competency = Competency()
    competency.set_all(competency_name)
    competency.save(cursor)


def create_assessment(cursor):

    competency_id = input("Competency Id: ")
    assessment_name = input("Assessment Name: ")

    assessment = Assessments()
    assessment.set_all(assessment_name, competency_id)
    assessment.save(cursor)


def create_assessment_results(cursor):
    user_id = input("User Id: ")
    assessment_id = input("Assessment Id: ")
    score = input("Score: ")
    date_taken = input("Date taken YYYY-MM-DD: ")

    assesment_results = AssesmentResults()
    assesment_results.set_all(user_id, assessment_id, score, date_taken)
    assesment_results.save(cursor)


def loginUser(email, password, cursor):
    user = User()
    if user.check_password(email, password, cursor):
        print("Successfully Logged in")
        user.loadByEmail(email, cursor)
        user.loggedIn = True
    else:
        print("****Incorrect username or password! Please try again.****")
    return user


def view_all_users(cursor):
    rows = cursor.execute(
        '''
     SELECT user_id, first_name, last_name, email, active, date_created, hire_date, user_type
     FROM Users
     WHERE user_type = 'user';''').fetchall()

    print(f'{"ID":<14} {"First Name":<22} {"Last Name":<20} {"Email":<40} {"active":<15} {"Date Created":<29} {"Hire Date":<17} {"User Type":<30}')

    print("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for row in rows:
        print(f'{row[0]!s:<15} {row[1]!s:<25} {row[2]!s:<18} {row[3]!s:<40} {row[4]!s:<16} {row[5]!s:<27} {row[6]!s:<16} {row[7]!s:<20}')


def searh_users(cursor):
    search_by = input("Search User by first or last name:  ")

    rows = cursor.execute("SELECT user_id, first_name, last_name, email, active, date_created, hire_date, user_type FROM Users WHERE first_name LIKE ? OR last_name LIKE ? ",
                          ('%'+search_by+'%', '%'+search_by+'%',)).fetchall()

    print(f'{"ID":<14} {"First Name":<22} {"Last Name":<20} {"Email":<40} {"active":<15} {"Date Created":<15} {"Hire Date":<15} {"User Type":<30}')

    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for row in rows:
        print(f'{row[0]!s:<15} {row[1]!s:<25} {row[2]!s:<18} {row[3]!s:<40} {row[4]!s:<16} {row[5]!s:<16} {row[6]!s:<16} {row[7]!s:<20}')


def all_user_competency(cursor):
    search_by_id = input("Search by user ID:  ")

    rows = cursor.execute('''
  SELECT a.name AS competency_name
  FROM Users as u
  INNER JOIN Assessment_results as ar
  ON ar.user_id=u.user_id
  INNER JOIN Assessments as a
  ON a.assessment_id=ar.assessment_id
  INNER JOIN Compentencies as c
  on c.competency_id=a.competency_id
  where u.user_id=?''',
                          (search_by_id,)).fetchall()

    print(f'{"Competency Name: ":<22}')
    print("----------------------------")
    for row in rows:
        print(f'{row[0]!s:<15} ')


def report_users_competency(cursor):
    rows = cursor.execute(
        '''
     SELECT *
     FROM Compentencies''').fetchall()

    print(f'{"Id":<14} {"Name":<29} {"Date Created":<15}')

    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for row in rows:
        print(f'{row[0]!s:<15} {row[1]!s:<30} {row[2]!s:<18} ')

    competency_id = input("Search by competency ID: ")

    competency_name = ''
    for row in rows:
        if str(row[0]) == competency_id:
            competency_name = row[1]

    rows = cursor.execute('''
  SELECT
 u2.user_id, u2.first_name, u2.last_name, u2.email, u1.competency, u1.assessment, ifnull(u1.sm, 0) as score_sum, u1.date_taken, ifnull(u1.score,0) as score
  From Users as u2
  left join (SELECT u.user_id, u.first_name, u.last_name, u.email,  c.name as competency, a.name AS assessment, c.name As Assessments
 ,max(ar.date_taken) AS date_taken, sum(score) as sm, ar.score
	  FROM Users as u
	 LEFT JOIN Assessment_results as ar
	  ON ar.user_id = u.user_id
	  LEFT JOIN Assessments as a
	  ON a.assessment_id = ar.assessment_id
	  LEFT JOIN Compentencies as c
	  on c.competency_id = a.competency_id
	  WHERE c.competency_id = ?) as u1
  on u1.user_id = u2.user_id;''', (competency_id,)).fetchall()

    print(f'{"Competency Name":<14} {"First Name":<14} {"Last Name":<14} {"Average score":<14} {"Assessment Name":<40} {"Date Taken":<30} {"Competency Score":<14}  ')
    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

    csvRows = [f'{"Competency Name"},{"First Name"},{"Last Name"},{"Average score"},{"Assessment Name"},{"Date Taken"},{"Competency Score"}']
    for row in rows:
        csvRow = f'{competency_name!s:<15} {row[1]!s:<15} {row[2]!s:<15} {row[6]!s:<15} {row[5]!s:<40} {row[7]!s:<30} {row[8]!s:<15}'
        print(csvRow)
        csvRows.append(
            f'{competency_name},{row[1]},{row[2]},{row[6]},{row[5]},{row[7]},{row[8]}')
    return csvRows


def report_single_user(cursor):
    search_by_userid = input("Enter User_ID: ")
    search_by_compid = input("Enter Competency Id: ")

    rows = cursor.execute('''
    SELECT u.first_name, u.last_name, u.email, ar.score, a.name AS competency_name, c.name As Assessments, max(ar.date_taken) AS date_taken, avg(score) AS Average_score
    FROM Users as u
    INNER JOIN Assessment_results as ar
    ON ar.user_id = u.user_id
    INNER JOIN Assessments as a
    ON a.assessment_id = ar.assessment_id
    INNER JOIN Compentencies as c
    on c.competency_id = a.competency_id
    WHERE c.competency_id = ? and u.user_id = ?''',
                          (search_by_compid, search_by_userid,)).fetchall()

    print(f'{"First Name":<14} {"Last Name":<18} {"Email":<30} {"Score":<18} {"Competency Name":<40} {"Assessments":<15} {"Date Taken":<15} {"Average Score":<15}')
    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

    csvRows = [f'{"First Name"},{"Last Name"},{"Email"},{"Score"},{"Competency Name"},{"Assessments"},{"Date Taken"},{"Average Score":<15}']
    for row in rows:
        csvRow = f'{row[0]!s:<15} {row[1]!s:<18} {row[2]!s:<30} {row[3]!s:<18} {row[4]!s:<40} {row[5]!s:<16} {row[6]!s:<16}  {row[7]!s:<16} '
        print(csvRow)
        csvRows.append(
            f'{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]},{row[7]}')
    return csvRows


def list_of_assessments(cursor):

    search_by_id = input("Search by ID: ")

    rows = cursor.execute('''
   SELECT  a.name
  FROM Users as u
  INNER JOIN Assessment_results as ar
  ON ar.user_id = u.user_id
  INNER JOIN Assessments as a
  ON a.assessment_id = ar.assessment_id
  WHERE u.user_id = ?''',
                          (search_by_id,)).fetchall()

    print(f'{"Assessment Name":<14}')
    print("--------------------------------------------------------------")
    for row in rows:
        print(
            f'{row[0]!s:<15}')


def edit_personal_information(cursor, user):
    row = cursor.execute(
        "SELECT first_name, last_name  FROM Users WHERE user_id=?", (user.user_id,)).fetchone()

    print(
        f'{"First name"}: {row[0]!s:<15}\n{"Last name"}: {row[1]!s:<15}\n{"Password"}: ******* \n ')

    user_input = input("What field do you want to change?: ").lower()
    change_to = input(f"What do you want to change {user_input} to: ")

    if user_input == "first name":
        user.first_name = change_to
    elif user_input == "last name":
        user.last_name = change_to
    else:
        user.change_password(change_to)

    user.update(cursor)


def view_data(cursor, user):
    rows = cursor.execute(
        '''
     SELECT u.first_name, u.last_name, u.phone, u.email, u.hire_date, u.user_type, a.assessment_id, a.competency_id, a.name, c.competency_id, c.name
   FROM Users as u 
   INNER JOIN Assessment_results as ar
   ON ar.user_id = u.user_id
   INNER JOIN Assessments as a
   ON a.assessment_id = ar.assessment_id
   INNER JOIN Compentencies as c
   on c.competency_id = a.competency_id
   WHERE u.user_id = ?  
;''', (user.user_id,)).fetchall()

    print(f'{"First Name":<17} {"Last Name":<20} {"Phone":<20} {"Email":<23} {"Hire Date":<15} {"User Type":<15}')

    print("--------------------------------------------------------------------------------------------------------------")
    for row in rows:
        print(
            f'{row[0]!s:<17} {row[1]!s:<20} {row[2]!s:<20} {row[3]!s:<23} {row[4]!s:<16} {row[5]!s:<16}')
    print('\n')

    print(f'{"Assessment ID":<15} {"compentency ID":<30} {"Assessment Name":<40} {"compentency ID":<28} {"compentency Name":<30}')

    print("-------------------------------------------------------------------------------------------------------------------------------------")
    for row in rows:
        print(
            f'|{row[6]!s:<16} {row[7]!s:<20} {row[8]!s:<48} {row[9]!s:<30} {row[10]!s:<20}')

    print('\n')

    print(f'{"compentency ID":<28} {"compentency Name":<30}')

    print("-------------------------------------------------------")
    for row in rows:
        print(
            f'{row[9]!s:<30} {row[10]!s:<20}')


def edit_users_info(cursor):
    view_all_users(cursor)

    user_id = input("What user do you want to edit?: ")

    user_to_edit = User()
    user_to_edit.user_id = user_id
    user_to_edit.load(cursor)

    print(
        f' {"ID"}: {user_to_edit.user_id!s:<15}\n {"First name"}: {user_to_edit.first_name!s:<15}\n {"Last name"}: {user_to_edit.last_name!s:<15}\n {"phone"}: {user_to_edit.phone!s:<15}\n {"email"}: {user_to_edit.email!s:<15} \n {"active"}: {user_to_edit.active!s:<15} \n {"date_created"}: {user_to_edit.date_created!s:<15} \n {"hire_date"}: {user_to_edit.hire_date!s:<15} \n {"user_type"}: {user_to_edit.user_type!s:<15} \n  ')
    user_input = input("What field do you want to change?: ").lower()
    change_to = input(f"What do you want to change {user_input} to: ")

    if user_input == "first name":
        user_to_edit.first_name = change_to
    elif user_input == "last name":
        user_to_edit.last_name = change_to
    elif user_input == "phone":
        user_to_edit.phone = change_to
    elif user_input == "email":
        user_to_edit.email = change_to
    elif user_input == "active":
        user_to_edit.active = change_to
    elif user_input == "date created":
        user_to_edit.date_created = change_to
    elif user_input == "hire date":
        user_to_edit.hire_date = change_to
    elif user_input == "user type":
        user_to_edit.user_type = change_to
    else:
        user_to_edit.change_password(change_to)
    user_to_edit.update(cursor)


def edit_competency(cursor):
    rows = cursor.execute(
        '''
     SELECT *
     FROM Compentencies''').fetchall()

    print(f'{"ID":<14} {"Name":<26}{"Date Created":<15} ')

    print("-----------------------------------------------------------")
    for row in rows:
        print(f'{row[0]!s:<15} {row[1]!s:<27} {row[2]!s:<18} ')

    competency_id = input(
        "What Competency do you want to edit?(Choose by ID): ")

    comp_to_edit = Competency()
    comp_to_edit.competency_id = competency_id
    comp_to_edit.load(cursor)

    print(
        f' {"ID"}: {comp_to_edit.competency_id!s:<15}\n {"Name"}: {comp_to_edit.name!s:<15}\n {"Date Created"}: {comp_to_edit.date_created!s:<15}\n    ')
    user_input = input("What field do you want to change?: ")
    change_to = input(f"What do you want to change {user_input} to: ")

    if user_input == "name":
        comp_to_edit.name = change_to
    elif user_input == "date created":
        comp_to_edit.date_created = change_to
    comp_to_edit.update(cursor)


def edit_assessment(cursor):
    rows = cursor.execute(
        '''
     SELECT *
     FROM Assessments''').fetchall()

    print(f'{"Assessment ID":<14} {"Competency ID":<18} {"Name":<43}{"Date Created":<15} ')
    print("-----------------------------------------------------------------------------------------")
    for row in rows:
        print(f'{row[0]!s:<15} {row[1]!s:<18} {row[2]!s:<43} {row[3]!s:<18} ')

    assessment_id = input(
        "What Assessment do you want to edit?(Choose by Assesment ID): ")

    assessment_to_edit = Assessments()
    assessment_to_edit.assessment_id = assessment_id
    assessment_to_edit.load(cursor)

    print(
        f' {"Assessment ID"}: {assessment_to_edit.assessment_id!s:<15}\n {"Competency ID"}: {assessment_to_edit.competency_id!s:<15}\n {"Name"}: {assessment_to_edit.name!s:<15}\n {"Date Created"}: {assessment_to_edit.date_created!s:<15}\n    ')
    user_input = input("What field do you want to change?: ").lower()
    change_to = input(f"What do you want to change {user_input} to: ")

    if user_input == "assessment id":
        assessment_to_edit.assessment_id = change_to
    if user_input == "competency id":
        assessment_to_edit.competency_id = change_to
    elif user_input == "name":
        assessment_to_edit.name = change_to
    elif user_input == "date created":
        assessment_to_edit.date_created = change_to

    assessment_to_edit.update(cursor)


def edit_assessment_result(cursor):
    rows = cursor.execute(
        '''
     SELECT *
     FROM Assessment_results''').fetchall()

    print(f'{"Assessment Result ID":<23} {"User ID":<18} {"Assessment ID":<24} {"Score":<15} {"Date Taken":<15} ')
    print("----------------------------------------------------------------------------------------------------------")
    for row in rows:
        print(
            f'{row[0]!s:<23} {row[1]!s:<18} {row[2]!s:<24} {row[3]!s:<15} {row[4]!s:<12}  ')

    assessment_result_id = input(
        "What Assessment Result do you want to edit?(Choose by Assesment ID): ")

    assessment_result_to_edit = AssesmentResults()
    assessment_result_to_edit.assessment_results_id = assessment_result_id
    assessment_result_to_edit.load(cursor)

    print(
        f' {"Assessment Result ID"}: {assessment_result_to_edit.assessment_results_id!s:<15}\n {"User ID"}: {assessment_result_to_edit.user_id!s:<15}\n {"Assessment ID"}: {assessment_result_to_edit.assessment_id!s:<15}\n {"Score"}: {assessment_result_to_edit.score!s:<15}\n {"Date Taken"}: {assessment_result_to_edit.date_taken!s:<15}\n     ')
    user_input = input("What field do you want to change?: ").lower()
    change_to = input(f"What do you want to change {user_input} to: ")

    if user_input == "assessment result id":
        assessment_result_to_edit.assessment_results_id = change_to
    elif user_input == "user id":
        assessment_result_to_edit.user_id = change_to
    elif user_input == "assessment id":
        assessment_result_to_edit.assessment_id = change_to
    elif user_input == "score":
        assessment_result_to_edit.score = change_to
    elif user_input == "date taken":
        assessment_result_to_edit.date_taken = change_to
    assessment_result_to_edit.update(cursor)


def delete_assessment_result(cursor):
    rows = cursor.execute(
        '''
     SELECT *
     FROM Assessment_results''').fetchall()

    print(f'{"Assessment Result ID":<23} {"User ID":<16} {"Assessment ID":<20} {"Score":<15} {"Date Taken":<15} ')

    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for row in rows:
        print(
            f'{row[0]!s:<23} {row[1]!s:<16} {row[2]!s:<18} {row[3]!s:<15} {row[4]!s:<16} ')

    assessment_result_id = input(
        "What Assessment Result do you want to Delete?(Choose by Assesment ID): ")
    delete_result = input(
        f"Are you SURE you want to DELETE Assessment Result ID '{assessment_result_id}' Y/N)?: ").upper()

    if delete_result == 'Y':
        cursor.execute(
            "DELETE FROM Assessment_results WHERE assessment_results_id=?", (assessment_result_id,))
        print(
            f"Assessment Result ID: '{assessment_result_id}' succesfully Deleted!")
    else:
        print('')
    cursor.connection.commit()


def export_report_users(cursor):
    csvRows = report_users_competency(cursor)
    with open('competency_by_users.csv', 'w', encoding='utf-8') as f:

        for row in csvRows:
            f.write(row + '\n')


def export_report_for_user(cursor):
    csvRows = report_single_user(cursor)
    with open('competency_by_user.csv', 'w', encoding='utf-8') as f:

        for row in csvRows:
            f.write(row + '\n')


def import_assessment_results(cursor):
    final_list = []
    with open('assessment_results_import.csv', 'r') as newcsvfile:
        finalcsvreader = csv.reader(newcsvfile)

        fields = next(finalcsvreader)

        for new_ufo_data in finalcsvreader:
            final_list.append(new_ufo_data)
        print(
            f"{fields[0]:^20} {fields[1]:^10} {fields[2]:^30} {fields[3]:^10}")
        print("-----------------------------------------------------------------------")
        for final_data in final_list:
            print(
                f"{final_data[0]:^20} {final_data[1]:^10} {final_data[2]:^30} {final_data[3]:^10}")
            assesmentResults = AssesmentResults()
            assesmentResults.set_all(
                final_data[0], final_data[1], final_data[2], final_data[3])
            assesmentResults.save(cursor)


def manager_commands(user_input, cursor):
    if(user_input == "1"):
        view_all_users(cursor)
    elif(user_input == "2"):
        searh_users(cursor)
    elif(user_input == "3"):
        all_user_competency(cursor)
    elif(user_input == "4"):
        report_users_competency(cursor)
    elif(user_input == "5"):
        report_single_user(cursor)
    elif(user_input == "6"):
        list_of_assessments(cursor)
    elif(user_input == "7a"):
        create_user_record(cursor)
    elif(user_input == "7b"):
        create_competency(cursor)
    elif(user_input == "7c"):
        create_assessment(cursor)
    elif(user_input == "7d"):
        create_assessment_results(cursor)
    elif(user_input == "8a"):
        edit_users_info(cursor)
    elif(user_input == "8b"):
        edit_competency(cursor)
    elif(user_input == "8c"):
        edit_assessment(cursor)
    elif(user_input == "8d"):
        edit_assessment_result(cursor)
    elif(user_input == "9"):
        export_report_users(cursor)
    elif(user_input == "10"):
        export_report_for_user(cursor)
    elif(user_input == "11"):
        delete_assessment_result(cursor)
    elif(user_input == "12"):
        import_assessment_results(cursor)


def user_commands(user_input, cursor, user):
    if(user_input == "1"):
        edit_personal_information(cursor, user)
    if(user_input == "2"):
        view_data(cursor, user)


user = None
query = ""

while query != "q":

    if not user or not user.loggedIn:
        query = input(
            '''                    
            
                            Welcome\n
            Enter 'Login'(if you already have an account) 
            Type 'Q' to quit: ''').lower()

        if query.lower() == "register":
            create_user_record(cursor)
        elif query.lower() == "login":
            email = input("Email: ")
            password = input("Password: ")
            user = loginUser(email, password, cursor)
    else:
        if user.user_type == "manager":
            query = input('''
                [1] You can view all users in a list
                [2] Search for users by first name or last name
                [3] View all user competencies by user
                [4] View a report of all users and their competency levels for a given competency
                [5] view a competency level report for an individual user
                [6] view a list of assessments for a given user
                ADD-
                      [7A] add a user,
                      [7B] add a new competency,
                      [7C] add a new assessment to a competency,
                      [7D] add an assessment result for a user for an assessment (this is like recording test results for a user)
                Edit-
                      [8A] edit a user's information
                      [8B] edit a competency
                      [8C] edit an assessment
                      [8D] edit an assessment result
                [9] Competency report by competency and users
                [10] Competency report for a single user
                [11] Delete Assessment Result
                [12] Import assessment results from CSV
                [Logout] Logout of session
            ''').lower()
            manager_commands(query, cursor)
        elif user.user_type == "user":
            query = input(
                '''
                [1] Edit personal information.\n
                [2] View Competency and Assessment Data\n
                [Logout] Logout of session
                 ''')
            user_commands(query, cursor, user)
        if query.lower() == 'logout':
            user = User()
            print('You successfully logged out.')
