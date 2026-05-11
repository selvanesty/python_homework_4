CREATE DATABASE IF NOT EXISTS my_database;
USE my_database;

CREATE TABLE IF NOT EXISTS titanic (
    PassengerId INT PRIMARY KEY,
    Survived INT,
    Pclass INT,
    Name VARCHAR(255),
    Sex VARCHAR(10),
    Age FLOAT,
    SibSp INT,
    Parch INT,
    Ticket VARCHAR(50),
    Fare FLOAT,
    Cabin VARCHAR(50),
    Embarked VARCHAR(10)
);

--Завантаження даних
LOAD DATA INFILE '/var/lib/mysql-files/titanic.csv'
INTO TABLE titanic
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(PassengerId, Survived, Pclass, Name, Sex, @Age, SibSp, Parch, Ticket, Fare, @Cabin, @Embarked)
SET
    --Якщо поле порожнє, записуємо справжній NULL
    Age = NULLIF(@Age, ''),
    Cabin = NULLIF(@Cabin, ''),
    --TRIM прибирає можливі приховані символи переносу каретки (\r) з кінця рядка
    Embarked = NULLIF(TRIM(@Embarked), '');