CREATE DATABASE calorie_diary_db
USE calorie_diary_db

CREATE TABLE Users (
    [ID] INT PRIMARY KEY IDENTITY,
    [Email] VARCHAR(100) NOT NULL UNIQUE,
    [Password] VARCHAR(100) NOT NULL
);
