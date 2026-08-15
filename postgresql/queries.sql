-- 1. Отримати всі завдання певного користувача

SELECT *
FROM tasks
WHERE user_id = 1;


-- 2. Вибрати завдання за певним статусом

SELECT *
FROM tasks
WHERE status_id = (
    SELECT id
    FROM status
    WHERE name = 'new'
);


-- 3. Оновити статус конкретного завдання

UPDATE tasks
SET status_id = (
    SELECT id
    FROM status
    WHERE name = 'in progress'
)
WHERE id = 1;


-- 4. Отримати користувачів, які не мають жодного завдання

SELECT *
FROM users
WHERE id NOT IN (
    SELECT user_id
    FROM tasks
);


-- 5. Додати нове завдання для конкретного користувача

INSERT INTO tasks (title, description, status_id, user_id)
VALUES (
    'New task',
    'Description of the new task',
    (SELECT id FROM status WHERE name = 'new'),
    1
);


-- 6. Отримати всі завдання, які ще не завершено

SELECT *
FROM tasks
WHERE status_id != (
    SELECT id
    FROM status
    WHERE name = 'completed'
);


-- 7. Видалити конкретне завдання

DELETE FROM tasks
WHERE id = 1;


-- 8. Знайти користувачів з певною електронною поштою

SELECT *
FROM users
WHERE email LIKE '%@example.com';


-- 9. Оновити ім'я користувача

UPDATE users
SET fullname = 'John Smith'
WHERE id = 1;


-- 10. Отримати кількість завдань для кожного статусу

SELECT
    s.name AS status,
    COUNT(t.id) AS task_count
FROM status AS s
LEFT JOIN tasks AS t ON t.status_id = s.id
GROUP BY s.id, s.name;


-- 11. Отримати завдання користувачів з певним доменом

SELECT
    t.id,
    t.title,
    t.description,
    u.fullname,
    u.email
FROM tasks AS t
INNER JOIN users AS u ON u.id = t.user_id
WHERE u.email LIKE '%@example.com';


-- 12. Отримати список завдань, що не мають опису

SELECT *
FROM tasks
WHERE description IS NULL;


-- 13. Отримати користувачів та їхні завдання зі статусом 'in progress'

SELECT
    u.fullname,
    t.title,
    t.description,
    s.name AS status
FROM users AS u
INNER JOIN tasks AS t ON t.user_id = u.id
INNER JOIN status AS s ON s.id = t.status_id
WHERE s.name = 'in progress';


-- 14. Отримати користувачів та кількість їхніх завдань

SELECT
    u.id,
    u.fullname,
    COUNT(t.id) AS task_count
FROM users AS u
LEFT JOIN tasks AS t ON t.user_id = u.id
GROUP BY u.id, u.fullname;