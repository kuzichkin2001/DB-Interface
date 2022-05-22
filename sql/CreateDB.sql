CREATE DATABASE restaurant;

DROP TABLE users;
DROP TABLE product_list;
DROP TABLE dish_list;
DROP TABLE offer;
DROP TABLE client;
DROP TABLE dish;
DROP TABLE kitchen;
DROP TABLE officiant;
DROP TABLE discount;
DROP TABLE product;

CREATE TABLE users (
    user_id SERIAL UNIQUE,
    username VARCHAR(32) NOT NULL,
    password VARCHAR(80) NOT NULL,
    role VARCHAR(10) NOT NULL
);

CREATE TABLE kitchen (
    kitchen_id SERIAL UNIQUE,
    kitchen_name VARCHAR(255) NOT NULL
);

CREATE TABLE officiant (
    officiant_id SERIAL UNIQUE,
    name VARCHAR(255) NOT NULL,
    hiring_date DATE NOT NULL,
    level VARCHAR(45) NOT NULL,
    phone_number VARCHAR(15),
    birthdate DATE
);

CREATE TABLE discount (
    discount_id SERIAL UNIQUE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);

CREATE TABLE product (
    id_product SERIAL UNIQUE,
    product_name VARCHAR(30) NOT NULL,
    exp_time INTEGER NOT NULL,
    arrivement_date DATE NOT NULL,
    cost MONEY NOT NULL,
    supplier VARCHAR(60) NOT NULL
);

CREATE TABLE client (
    client_id SERIAL UNIQUE,
    name VARCHAR(40) NOT NULL,
    birthdate DATE,
    phone_number VARCHAR(15),
    discount_id INT NOT NULL,
    CONSTRAINT fk_discount
        FOREIGN KEY(discount_id)
            REFERENCES discount(discount_id)
);

CREATE TABLE dish (
    dish_id SERIAL UNIQUE,
    dish_name VARCHAR(40) NOT NULL,
    kitchen_id INT NOT NULL,
    cost MONEY NOT NULL,
    CONSTRAINT fk_kitchen
        FOREIGN KEY(kitchen_id)
            REFERENCES kitchen(kitchen_id)
);

CREATE TABLE product_list (
    id_dish INT NOT NULL,
    product_id INT NOT NULL,
    product_count INTEGER NOT NULL,
    cooking_type VARCHAR(20),
    CONSTRAINT fk_product_id
        FOREIGN KEY(id_dish)
            REFERENCES dish(dish_id),
    CONSTRAINT fk_product_list
        FOREIGN KEY(product_id)
            REFERENCES product(id_product)
);

CREATE TABLE offer (
    offer_id SERIAL UNIQUE,
    offer_time DATE NOT NULL,
    price MONEY NOT NULL,
    officiant_id BIGINT NOT NULL,
    client_id BIGINT NOT NULL,
    CONSTRAINT fk_officiant
        FOREIGN KEY(officiant_id)
            REFERENCES officiant(officiant_id),
    CONSTRAINT fk_client
        FOREIGN KEY(client_id)
            REFERENCES client(client_id)
);

CREATE TABLE dish_list (
    offer_id INT NOT NULL,
    dish_id INT NOT NULL,
    CONSTRAINT fk_offer
        FOREIGN KEY(offer_id)
            REFERENCES offer(offer_id),
    CONSTRAINT fk_dish
        FOREIGN KEY(dish_id)
            REFERENCES dish(dish_id)
);