import pdb
import sqlite3
import bcrypt

connection = sqlite3.connect('capstone_data.db', timeout=10)
cursor = connection.cursor()


class AssesmentResults:
    def __init__(self):
        self.assessment_id = None
        self.user_id = None
        self.score = None
        self.date_taken = None

    def set_all(self, assessment_id, user_id, score, date_taken='2021-11-18 08:30:00'):
        self.assessment_id = assessment_id,
        self.user_id = user_id,
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
        print(params)
        print(self.user_id)
        assessment = Assessments()
        user = User()
        if assessment.get_assessment(self.assessment_id[0], cursor) and user.get_user(self.user_id[0], cursor):

            # params = (self.user_id, self.assessment_id,
            #           self.score, self.date_taken,)
            print(params)
            cursor.execute(insert_sql, params)
            cursor.connection.commit()

            # new_user_id = cursor.execute('SELECT user_id FROM Users WHERE email=?',(self.email,)).fetchone()
            new_assessment_id = cursor.execute(
                'SELECT last_insert_rowid()').fetchone()
            print("----------------------", new_assessment_id)
            self.new_assessment_id = new_assessment_id[0]

        else:
            print(
                f"The User_id with id {self.user_id} and {self.assessment_id} does not exist")


class Assessments:
    def __init__(self):
        self.assessment_id = None
        self.competency_id = None
        self.name = None
        self.date_taken = None

    def set_all(self, name, competency_id, date_created='2021-11-18 08:30:00'):
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
            print(params)
            cursor.execute(insert_sql, params)
            cursor.connection.commit()

            # new_user_id = cursor.execute('SELECT user_id FROM Users WHERE email=?',(self.email,)).fetchone()
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


class Competency:
    def __init__(self):
        self.competency_id = None
        self.name = None
        self.date_created = None

    def set_all(self, name, date_created='2021-11-18 08:30:00'):
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

        # new_user_id = cursor.execute('SELECT user_id FROM Users WHERE email=?',(self.email,)).fetchone()
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

    def set_all(self, first_name, last_name, email, phone, password, active, user_type, date_created='2021-11-18 08:30:00', hire_date='2021-11-18 08:30:00'):
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
        new_password = bcrypt.hashpw(new_password.encode('utf-8'), self.salt)
        select_sql = '''
         SELECT email FROM Users WHERE password=? AND email=?
        ;'''

        row = cursor.execute(select_sql, (new_password, email)).fetchone()

        return row

    def change_email(self, new_email):
        self.email = new_email

    def print_me(self):
        print(f'{self.user_id} {self.last_name}, {self.first_name}')
        print(f'  {self.city}, {self.state}')
        print(f'  {self.email}')
        print(f'  {self.__password}')
        print(f'  Created: {self.date_created}')

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
        print(params)
        cursor.execute(insert_sql, params)
        cursor.connection.commit()

        new_user_id = cursor.execute('SELECT last_insert_rowid()').fetchone()
        self.user_id = new_user_id[0]

    def update(self, cursor):
        print("---------", self.__password)
        insert_sql = '''
          UPDATE Users
           SET first_name = ?, last_name = ?, email = ?, phone = ?, password = ?,
             active = ?, date_created = ?, hire_date = ?, user_type = ?
            WHERE user_id = ?
          ;'''
        params = (self.first_name, self.last_name, self.email,
                  self.phone, self.__password, self.active,
                  self.date_created, self.hire_date, self.user_type, self.user_id)
        print(params)
        cursor.execute(insert_sql, params)
        cursor.connection.commit()

    def loadByEmail(self, email, cursor):
        select_sql = '''
          SELECT user_id, first_name, last_name, phone, email, date_created, user_type, password, active, hire_date
          FROM Users
          WHERE email=?;
        '''

        print(email)
        print(select_sql)
        row = cursor.execute(select_sql, (email,)).fetchone()
        print(row)
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

        print(email)
        print(select_sql)
        row = cursor.execute(select_sql, (self.user_id,)).fetchone()
        print(row)
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

    first_name = input("Name: ")
    last_name = input("Last Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    password = input("Password: ")
    user_type = input("user_type user/manager: ")

    user = User()
    user.set_all(first_name, last_name, email, phone, password, 1, user_type,
                 date_created='2021-11-18', hire_date='2021-11-18')
    user.save(cursor)
    print(f"SUCCESS: '{first_name}' Successfully added!")


def create_competency(cursor):

    competency_name = input("Compentcy: ")

    competency = Competency()
    competency.set_all(competency_name, date_created='2021-11-18')
    competency.save(cursor)
    # hard coding date for now


def create_assessment(cursor):

    competency_id = input("Competency Id: ")
    assessment_name = input("Assessment Name: ")

    assessment = Assessments()
    assessment.set_all(assessment_name, competency_id,
                       date_created='2021-11-18')
    assessment.save(cursor)


def create_assessment_results(cursor):
    user_id = input("User Id: ")
    assessment_id = input("Assessment Id: ")
    score = input("Score: ")

    # date_taken = input("Date Taken: ")
    assesment_results = AssesmentResults()
    assesment_results.set_all(assessment_id, user_id,
                              score, date_taken="2021-11-18")
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
     WHERE user_type = 'user';
''').fetchall()

    print(f'{"ID":<14} {"First Name":<22} {"Last Name":<20} {"Email":<40} {"active":<15} {"Date Created":<15} {"Hire Date":<15} {"User Type":<30}')

    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for row in rows:
        print(f'{row[0]!s:<15} {row[1]!s:<25} {row[2]!s:<18} {row[3]!s:<40} {row[4]!s:<16} {row[5]!s:<16} {row[6]!s:<16} {row[7]!s:<20}')


def searh_users(cursor):
    search_by = input("Search User by first or last name:  ")

    rows = cursor.execute("SELECT user_id, first_name, last_name, email, active, date_created, hire_date, user_type FROM Users WHERE first_name LIKE ? OR last_name LIKE ? ",
                          ('%'+search_by+'%', '%'+search_by+'%',)).fetchall()

    print(f'{"ID":<14} {"First Name":<22} {"Last Name":<20} {"Email":<40} {"active":<15} {"Date Created":<15} {"Hire Date":<15} {"User Type":<30}')

    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for row in rows:
        print(f'{row[0]!s:<15} {row[1]!s:<25} {row[2]!s:<18} {row[3]!s:<40} {row[4]!s:<16} {row[5]!s:<16} {row[6]!s:<16} {row[7]!s:<20}')


def all_user_competency(cursor):
    search_by_id = input("Search by ID ")

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
     FROM Compentencies
''').fetchall()

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
on u1.user_id = u2.user_id;''',
                          (competency_id,)).fetchall()

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
  WHERE c.competency_id = ? u.user_id = ?''',
                          (search_by_compid, search_by_userid,)).fetchall()

    print(f'{"First Name":<14} {"Last Name":<18} {"Email":<30} {"Score":<18} {"Competency Name":<40} {"Assessments":<15} {"Date Taken":<15} {"Average Score":<15}')
    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

    for row in rows:
        print(
            f'{row[0]!s:<15} {row[1]!s:<18} {row[2]!s:<30} {row[3]!s:<18} {row[4]!s:<40} {row[5]!s:<16} {row[6]!s:<16}  {row[7]!s:<16} ')


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

    user_input = input("What field do you want to change?: ")
    change_to = input(f"What do you want to change {user_input} to: ")

    if user_input == "First Name":
        user.first_name = change_to
    elif user_input == "Last Name":
        user.last_name = change_to
    else:
        user.change_password(change_to)

    user.update(cursor)


def view_data():
    pass


def edit_users_info(cursor):
    view_all_users(cursor)

    user_id = input("What user do you want to edit?: ")

    user_to_edit = User()
    user_to_edit.user_id = user_id
    user_to_edit.load(cursor)

    print(
        f' {"ID"}: {user_to_edit.user_id!s:<15}\n {"First name"}: {user_to_edit.first_name!s:<15}\n {"Last name"}: {user_to_edit.last_name!s:<15}\n {"phone"}: {user_to_edit.phone!s:<15}\n {"email"}: {user_to_edit.email!s:<15} \n {"active"}: {user_to_edit.active!s:<15} \n {"date_created"}: {user_to_edit.date_created!s:<15} \n {"hire_date"}: {user_to_edit.hire_date!s:<15} \n {"user_type"}: {user_to_edit.user_type!s:<15} \n  ')
    user_input = input("What field do you want to change?: ")
    change_to = input(f"What do you want to change {user_input} to: ")

    if user_input == "First Name":
        user_to_edit.first_name = change_to
    elif user_input == "Last Name":
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
     FROM Compentencies
''').fetchall()

    print(f'{"ID":<14} {"Name":<26}{"Date Created":<15} ')

    print("-----------------------------------------------------------")
    for row in rows:
        print(f'{row[0]!s:<15} {row[1]!s:<27} {row[2]!s:<18} ')

    competency_id = input("What Competency do you want to edit?: ")

    comp_to_edit = Competency()
    comp_to_edit.competency_id = competency_id
    comp_to_edit.load(cursor)

    print(
        f' {"ID"}: {comp_to_edit.competency_id!s:<15}\n {"Name"}: {comp_to_edit.name!s:<15}\n {"Date Created"}: {comp_to_edit.date_created!s:<15}\n    ')
    user_input = input("What field do you want to change?: ")
    change_to = input(f"What do you want to change {user_input} to: ")

    if user_input == "Name":
        comp_to_edit.name = change_to
    elif user_input == "Date Created":
        comp_to_edit.date_created = change_to
    comp_to_edit.update(cursor)


def edit_assessment():
    pass


def exportReport(cursor):
    csvRows = report_users_competency(cursor)
    with open('report.csv', 'w', encoding='utf-8') as f:

        for row in csvRows:
            f.write(row + '\n')


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
        # view a list of assessments for a given user
        list_of_assessments(cursor)
    elif(user_input == "7A"):
        create_user_record(cursor)
    elif(user_input == "7B"):
        create_competency(cursor)
    elif(user_input == "7C"):
        create_assessment(cursor)
    elif(user_input == "7D"):
        create_assessment_results(cursor)
    elif(user_input == "8A"):
        edit_users_info(cursor)
    elif(user_input == "8B"):
        edit_competency(cursor)
    elif(user_input == "8B"):
        edit_assessment(cursor)
    elif(user_input == "9"):
        exportReport(cursor)
    # elif(user_input == "8C"):
    #     # create_assessment_results(cursor)
    # elif(user_input == "8D"):
    #     # create_assessment_results(cursor)


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
            "Welcome\nEnter 'Login' if you already have an account, else enter 'Register'. Or type 'Q' to quit: ").lower()

        if query.lower() == "register":
            create_user_record(cursor)
        elif query.lower() == "login":
            email = input("Email: ")
            password = input("Password: ")
            user = loginUser(email, password, cursor)
    else:
        # query = input('Which command do you want to run: ')
        if user.user_type == "manager":
            query = input('''
                [1] You can view all users in a list\n
                [2] Search for users by first name or last name\n
                [3] View all user competencies by user\n
                [4] View a report of all users and their competency levels for a given competency\n
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
                [9] Report
                [Logout] Logout of session
            ''')
            manager_commands(query, cursor)
        elif user.user_type == "user":
            query = input(
                '''[1] Edit personal information.
                   [2] View Competency and Assessment Data
                   [Logout] Logout of session
                 ''')
            user_commands(query, cursor, user)
        if query.lower() == 'logout':
            user = User()
            print('You successfully logged out.')
