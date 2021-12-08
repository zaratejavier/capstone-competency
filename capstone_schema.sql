CREATE TABLE IF NOT EXISTS Users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  phone TEXT,
  email TEXT NOT NULL,
  password TEXT NOT NULL,
  active DEFAULT 1,
  date_created TEXT,
  hire_date TEXT,
  user_type TEXT,
  UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS Compentencies (
  competency_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  date_created TEXT
);

CREATE TABLE IF NOT EXISTS Assessment_results (
  assessment_results_id INTEGER PRIMARY Key AUTOINCREMENT,
  user_id INTEGER,
  assessment_id INTEGER,
  score INTEGER,
  date_taken TEXT NOT NULL,
  FOREIGN KEY (user_id)
      REFERENCES Users (user_id),
  FOREIGN KEY (assessment_id)
      REFERENCES Assessments (assessment_id)
);

CREATE TABLE IF NOT EXISTS Assessments (
  assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
  competency_id INTEGER,
  name TEXT,
  date_created TEXT,
  FOREIGN KEY (competency_id)
    REFERENCES Compentencies (competency_id)
);

