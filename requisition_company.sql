-- Для подключения к БД
--\conn requisition_company

-- Удаление таблицы
--DROP TABLE cpmpany CASCADE;
--DROP TABLE requisition CASCADE;
--DROP TABLE requisitioncompany CASCADE;
--DROP TABLE users CASCADE;

-- Создание таблицы КОМПАНИЯ
CREATE TABLE company (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    ticker VARCHAR NOT NULL,
    industry VARCHAR NOT NULL,
    capital FLOAT NOT NULL,
    enterprise_value FLOAT NOT NULL,
    revenue FLOAT NOT NULL,
    net_profit FLOAT NOT NULL,
    pe FLOAT NOT NULL,
    ps FLOAT NOT NULL,
    pb FLOAT NOT NULL,
    ev_ebitda FLOAT NOT NULL,
    ebitda_margin FLOAT NOT NULL,
    debt_ebitda FLOAT NOT NULL,
    report VARCHAR NOT NULL,
    year INT NOT NULL,
    status BOOLEAN NOT NULL,
    image VARCHAR NOT NULL
);

-- Создание таблицы ВАКАНСИЯ
CREATE TABLE requisition (
  id SERIAL PRIMARY KEY,
  name_requisition VARCHAR NOT NULL,
  date_create DATE NOT NULL,
  date_form DATE NULL,
  date_close DATE NULL,
  status_requisition VARCHAR NOT NULL,
  id_employer INT NULL,
  id_moderator INT NULL
);

-- Создание таблицы ПОЛЬЗОВАТЕЛЬ
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    admin BOOLEAN NOT NULL
);

-- Создание таблицы ВАКАНСИИКОМПАНИИ
CREATE TABLE requisitioncompany (
  id SERIAL PRIMARY KEY,
  id_company INT NOT NULL,
  id_requisition INT NOT NULL
);

-- Связывание БД внешними ключами
ALTER TABLE requisitioncompany
ADD CONSTRAINT FR_requisitioncompany_of_company
    FOREIGN KEY (id_company) REFERENCES company (id);

ALTER TABLE requisitioncompany
ADD CONSTRAINT FR_requisitioncompany_of_requisition
    FOREIGN KEY (id_requisition) REFERENCES requisition (id);

ALTER TABLE requisition
ADD CONSTRAINT FR_requisition_of_employer
    FOREIGN KEY (id_employer) REFERENCES users (id);

ALTER TABLE requisition
ADD CONSTRAINT FR_requisition_of_moderator
    FOREIGN KEY (id_moderator) REFERENCES users (id);

-- ПОЛЬЗОВАТЕЛЬ (Авторизация)
INSERT INTO users (email, password, admin) VALUES
    ('user1@user.com', '1234', false),
    ('user2@user.com', '1234', false),
    ('user3@user.com', '1234', false),
    ('root@root.com', '1234', true);
-- Вывод таблицы пользователя
SELECT * FROM users;

-- КОМПАНИЯ (Услуга)
INSERT INTO company (
    name, ticker, industry, capital, enterprise_value, revenue, net_profit, pe, ps, pb, ev_ebitda, ebitda_margin, debt_ebitda, report, year, status, image
) VALUES
    ('Роснефть', 'ROSN', 'Нефтегаз', 3206, 8170, 4988, 181.0, 17.7, 0.6, 1.1, 6.4, 0.3, 3.9, '2016-МСФО', 2016, true, 'companies/1.jpg'),
    ('Газпром', 'GAZP', 'Нефтегаз', 2827, 4760, 6111, 951.6, 3.0, 0.5, 0.2, 3.4, 0.2, 1.4, '2016-МСФО', 2016, true, 'companies/2.jpg'),
    ('Лукойл', 'LKOH', 'Нефтегаз', 2299, 2736, 5227, 206.8, 11.1, 0.4, 0.7, 3.7, 0.1, 0.6, '2016-МСФО', 2016, true, 'companies/3.jpg'),
    ('НОВАТЭК', 'NVTK', 'Нефтегаз', 1869, 2034, 537, 132.5, 14.1, 3.5, 2.8, 8.4, 0.4, 0.7, '2016-МСФО', 2016, true, 'companies/4.jpg'),
    ('ГМК Норникель', 'GMKN', 'Металургия цвет', 1237, 1513, 549, 149.3, 8.3, 2.3, 5.9, 5.9, 0.5, 1.1, '2016-МСФО', 2016, true, 'companies/5.jpg');
-- Вывод таблицы компании
SELECT * FROM company;

-- ЗАЯВКА (Заявки)
INSERT INTO requisition (name_requisition, date_create, date_form, date_close, status_requisition, id_employer, id_moderator) VALUES
    ('Заявка №1', '01-01-2023', '10-01-2023', '01-03-2023', 'Введён', 1, 4),
    ('Заявка №2', '20-05-2023', '01-06-2023', '01-08-2023', 'В работе', 2, 4),
    ('Заявка №3', '24-09-2023', '05-10-2023', '30-11-2023', 'Завершён', 3, 4),
    ('Заявка №4', '20-09-2023', '30-09-2023', '30-11-2023', 'Отменен', 1, 4),
    ('Заявка №5', '20-09-2023', '30-09-2023', '30-11-2023', 'Удалён', 2, 4);
-- Вывод таблицы заявка
SELECT * FROM requisition;

-- ЗАЯВКИКОМПАНИИ (вспомогательная таблица М-М услуга-заявка)
INSERT INTO requisitioncompany (id_company, id_requisition) VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5);
-- Вывод таблицы ЗаявкиКомпании
SELECT * FROM requisitioncompany;