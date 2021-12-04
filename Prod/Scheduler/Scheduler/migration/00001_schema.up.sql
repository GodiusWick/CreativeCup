CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE satellites(
    id SERIAL PRIMARY KEY,
    gz TEXT NOT NULL
);

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    login VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);



CREATE TABLE statuses(
    id SERIAL PRIMARY KEY,
    alias VARCHAR(255) NOT NULL
);

INSERT INTO statuses(id, alias) VALUES(1, 'В работе');
INSERT INTO statuses(id, alias) VALUES(2, 'Завершено с ошибкой');
INSERT INTO statuses(id, alias) VALUES(3, 'Чисто');
INSERT INTO statuses(id, alias) VALUES(4, 'Загрязнение');
INSERT INTO statuses(id, alias) VALUES(5, 'Отправлено на определение');

CREATE TABLE images(
    uuid uuid DEFAULT uuid_generate_v4 () PRIMARY KEY,
    src VARCHAR(255) NOT NULL,
    region VARCHAR(255) NOT NULL,
    persent NUMERIC(5,2) NOT NULL,
    status VARCHAR(255) NOT NULL,
    lon float NOT NULL,
    lan float NOT NULL,
    dateOfGet TIMESTAMP NOT NULL
);

CREATE TABLE imports(
    uuid uuid DEFAULT uuid_generate_v4 () PRIMARY KEY,
    status INTEGER REFERENCES statuses(id) NOT NULL,
    timeupdate TIMESTAMP NOT NULL,
    timestart TIMESTAMP NOT NULL,
    timeend TIMESTAMP,
    id_image uuid REFERENCES images(uuid)
);

CREATE TABLE reestr(
    id SERIAL NOT NULL,
    coordinates TEXT NOT NULL,
    resolution integer NOT NULL,
    dates TEXT NOT NULL
);