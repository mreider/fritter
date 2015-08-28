SET autocommit=0;
START TRANSACTION;

INSERT INTO ITEMS (name, description, price, created_date)
VALUES ('Турка "Утро Востока"', 'Турка медная средняя "Утро Востока "TimA  0,30л (цельная) со съемной ручкой в подарочной упаковке.', 11, now());
INSERT INTO ITEMS (name, description, price, created_date)
VALUES ('Турка медная средняя', 'Турка медная средняя "Утро Востока "TimA  0,42л (цельная) со съемной ручкой в подарочной упаковке.', 10, now());
INSERT INTO ITEMS (name, description, price, created_date)
VALUES ('Турка медная средняя', 'Турка медная средняя "Утро Востока" TimA  0,30л (цельная)  со съемной ручкой', 14, now());
INSERT INTO ITEMS (name, description, price, created_date)
VALUES ('Турка мельхиоровая', 'Турка мельхиоровая "Нефертити" ООО"Станица"(г.Пятигорск) 0,3л', 4, now());
INSERT INTO ITEMS (name, description, price, created_date)
VALUES ('Турка нержавеющая сталь', 'Турка нержавеющая сталь 18/10 , REGENT inox, 0,35л ', 6, now());
INSERT INTO ITEMS (name, description, price, created_date)
VALUES ('Турка нержавеющая сталь', 'Турка нержавеющая сталь 18/10 , REGENT inox, 180мл  ', 6, now());
INSERT INTO ITEMS (name, description, price, created_date)
VALUES ('Турка нержавеющая сталь', 'Турка нержавеющая сталь 18/10 , REGENT inox, 750млVALUES', 6, now());
INSERT INTO ITEMS (name, description, price, created_date)
VALUES ('Набор для приготовления', 'Набор для приготовления кофе на песке "Восточный""Виноград" (Турция).', 40, now());
INSERT INTO ITEMS (name, description, price, created_date)
VALUES ('Набор для приготовления', 'Набор для приготовления кофе на песке "Тет-а-Тет" (Турция).', 36, now());
INSERT INTO ITEMS (name, description, price, created_date)
VALUES ('Подарочный набор', 'Подарочный набор "Кофейный гурман" из меди TimA.', 35, now());
INSERT INTO ITEMS (name, description, price, created_date)
VALUES ('Подарочный набор', 'Подарочный набор "Кофейный гурман"(тубус) из меди TimA (Россия)', 35, now());
INSERT INTO ITEMS (name, description, price, created_date)
VALUES ('Кофеварка медная ""', 'Кофеварка медная ООО"Станица"(г.Пятигорск) 0,38л в подарочной упаковке.', 6, now());
INSERT INTO ITEMS (name, description, price, created_date)
VALUES ('Турка медная  малая', 'Турка медная  малая "Утро Востока"TimA  0,18л (цельная)', 14, now());
INSERT INTO ITEMS (name, description, price, created_date)
VALUES ('Турка медная большая', 'Турка медная большая "Арабика" TimA  0,30 (цельная)  ', 15, now());
INSERT INTO ITEMS (name, description, price, created_date)
VALUES ('Турка медная большая', 'Турка медная большая "Турчанка" TimA  0,7л  со съемной ручкой.', 19, now());
INSERT INTO ITEMS (name, description, price, created_date)
VALUES ('Кофеварка медная ""', 'Кофеварка медная с узким горлом "Орел" ООО"Станица"(г.Пятигорск) 0,3л', 20, now());
INSERT INTO ITEMS (name, description, price, created_date)
VALUES ('Кофеварка медная ""', 'Кофеварка медная с узким горлом  ООО"Станица"(г.Пятигорск) 0,38л', 25, now());
INSERT INTO ITEMS (name, description, price, created_date)
VALUES ('Подставка латунная под кофеварку', 'Подставка латунная под кофеварку 18см ООО"Станица"(г.Пятигорск).', 8, now());

COMMIT;