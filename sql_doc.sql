USE ecom

-- DML Data Manipulation Language

SELECT * FROM customer;
SELECT * FROM orders;

INSERT INTO customer (customer_name, email, phone, address)
VALUES ('Travis','travisp@codingtemple.com','1111111111','123 real street');

INSERT INTO customer (customer_name, email, phone)
VALUES ('Dylan Katina','dk@gmail.com','2223334444','123 cool street'),
('Darth Vader','darthvader@gmail.com','6667778888','890 darth street'),
('Luke Skywalker','luke@gmail.com','9998887777');

UPDATE customer 
SET customer_name = 'Anakin Skywalker', email = 'as@jedi.com'
WHERE id = 4;


INSERT INTO customer (customer_name, email, phone)

VALUES ('Peter Cottontail', 'pc@email.com', '1234567891'),

('Jungle George', 'banana@email.com', '1234567892'),

('Billy Butcher', 'supesoup@email.com', '1234567893'),

('Obi-wan Kenoibi', 'ok@jedi.com', '1234567894'),

('Django Freeman', 'whereshildi@email.com', '1234567895'),

('John Dutton', 'ranch4life@email.com', '1234567896'),

('Jeff Probst', 'jp@survivor.com', '1234567897');

INSERT INTO customer_account (username, password)
VALUES ('peterc', 'P@ssw0rdAlpha!'),
('jungleg','Beta@1234!'),
('billyb','pa33workd'),
('obiw','G@mmaPass2024!'),
('djangof','D3lt@Secure!'),
('johnd','Eps!l0nSafe#'),
('jeffp','Et@Pass987!');

SELECT * FROM customer_account;

('Jungle George', 'banana@email.com', '1234567892'),

('Billy Butcher', 'supesoup@email.com', '1234567893'),

('Obi-wan Kenoibi', 'ok@jedi.com', '1234567894'),

('Django Freeman', 'whereshildi@email.com', '1234567895'),

('John Dutton', 'ranch4life@email.com', '1234567896'),

('Jeff Probst', 'jp@survivor.com', '1234567897');

USE ecom
SELECT * FROM customer;
SELECT * FROM products;
SELECT * FROM orders;
SELECT * FROM order_products;

INSERT INTO products (product_name, price)
VALUES ('EchoSmart Wireless Earbuds','59.99'),
('LuxeLeather Laptop Bag','129.99'),
('QuantumFit', '79.99'),
('GourmetPro Blender','99.99'),
('AquaFresh Water Bottle', '24.99');

INSERT INTO orders (order_date, customer_id)

VALUES ('2023-01-18', 1),

('2023-02-24', 1),

('2023-02-28', 6),

('2023-03-04', 8),

('2023-03-12', 2),

('2023-04-16', 7),

('2023-05-19', 9),

('2023-06-02', 10),

('2023-09-04', 3),

('2023-12-23', 11),

('2024-01-18', 1);

INSERT INTO orders (order_date, customer_id)

VALUES ('2023-01-18', 1),

('2023-02-24', 1),

('2023-02-28', 6),

('2023-03-04', 8),

('2023-03-12', 2),

('2023-04-16', 7),

('2023-05-19', 9),

('2023-06-02', 10),

('2023-09-04', 3),

('2023-12-23', 11),

('2024-01-18', 1);