CREATE DATABASE calorie_diary_db
USE calorie_diary_db

CREATE TABLE Users (
    [id] INT PRIMARY KEY IDENTITY,
    [email] VARCHAR(100) NOT NULL UNIQUE,
    [password] VARCHAR(100) NOT NULL
);

CREATE TABLE Logs_reg_aut (
    [id] INT IDENTITY PRIMARY KEY,
    [email] VARCHAR(255),
    [action_type] VARCHAR(20),
    [action_time] DATETIME DEFAULT GETDATE()
);

CREATE TRIGGER trg_register_log
ON Users
AFTER INSERT
AS
BEGIN
    INSERT INTO logs_reg_aut (email, action_type)
    SELECT email, 'register' FROM inserted;
END;

SELECT * FROM Logs_reg_aut

CREATE TABLE UserInfo (
    [id] INT IDENTITY PRIMARY KEY,
    [email] VARCHAR(100) FOREIGN KEY REFERENCES Users(email),
    [name] VARCHAR(100),
    [gender] VARCHAR(10),
    [birthdate] DATE,
    [weight] INT,
    [height] INT,
    [goal] VARCHAR(50)
);

SELECT * FROM UserInfo

CREATE TABLE CalorieHistory (
    [id] INT PRIMARY KEY IDENTITY,
    [email] VARCHAR(100) FOREIGN KEY REFERENCES Users(email),
    [calories] INT,
    [timestamp] DATETIME DEFAULT GETDATE()
);