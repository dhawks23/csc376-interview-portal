BEGIN TRANSACTION;

CREATE TABLE Users (
  user_id    INTEGER     UNIQUE NOT NULL,
  user_name  TEXT        UNIQUE NOT NULL,
  user_perms INTEGER     NOT NULL,

  CONSTRAINT pk_user_id PRIMARY KEY (user_id),
  CONSTRAINT fk_user_perms FOREIGN KEY (user_perms) REFERENCES UserPermissions (perms_id)
);

CREATE TABLE UserPermissions
(
  perms_id     INTEGER     UNIQUE NOT NULL,
  perms_alias  TEXT UNIQUE NOT NULL,
  perms_create BOOLEAN     NOT NULL,
  perms_delete BOOLEAN     NOT NULL,
  perms_edit   BOOLEAN     NOT NULL,
  perms_answer BOOLEAN     NOT NULL,
  perms_review BOOLEAN     NOT NULL,
  CONSTRAINT pk_perms_id PRIMARY KEY (perms_id)
);

INSERT INTO UserPermissions (perms_id, perms_alias, perms_create, perms_delete, perms_edit, perms_answer, perms_review)
VALUES
  (0, 'sysadmin',    1,  1,  1,  1,  1),
  (1, 'attorney',    1,  1,  1,  0, 1),
  (2, 'staff',       0, 0, 1,  0, 1),
  (3, 'interviewee', 0, 0, 0, 1,  0);

CREATE TABLE Interviews
(
  interview_id INTEGER UNIQUE NOT NULL,
  interview_name TEXT NOT NULL,
  interview_description TEXT NOT NULL,
  CONSTRAINT pk_interview_id PRIMARY KEY (interview_id)
);

CREATE TABLE Questions
(
  question_id INTEGER UNIQUE NOT NULL,
  question_interview INTEGER NOT NULL,
  question_kind INTEGER NOT NULL,
  CONSTRAINT pk_question_id PRIMARY KEY (question_id),
  CONSTRAINT fk_question_interview FOREIGN KEY (question_interview) REFERENCES Interviews (interview_id)
);

CREATE TABLE QuestionKinds
(
  qkind_id INTEGER UNIQUE NOT NULL,
  qkind_name TEXT UNIQUE NOT NULL
);

INSERT INTO QuestionKinds (qkind_id, qkind_name)
VALUES
  (0, 'text'),
  (1, 'radio'),
  (2, 'check');

CREATE TABLE PredefinedAnswers
(
  predef_id INTEGER UNIQUE NOT NULL,
  predef_question INTEGER NOT NULL,
  predef_text TEXT NOT NULL,

  CONSTRAINT pk_predef_id PRIMARY KEY (predef_id),
  CONSTRAINT fk_predef_question FOREIGN KEY (predef_question) REFERENCES Questions (question_id)
);

CREATE TABLE Answers
(
  answer_id INTEGER UNIQUE NOT NULL,
  answer_user INTEGER NOT NULL,
  answer_question INTEGER NOT NULL,

  CONSTRAINT pk_answer_id PRIMARY KEY (answer_id),
  CONSTRAINT fk_answer_user FOREIGN KEY (answer_user) REFERENCES Users (user_id),
  CONSTRAINT fk_answer_question FOREIGN KEY (answer_question) REFERENCES Questions (question_id)
);

COMMIT TRANSACTION;