import os
import random

import psycopg2
from dotenv import load_dotenv
from faker import Faker


load_dotenv()

fake = Faker()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}


def seed_database():
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    try:
        statuses = [
            ("new",),
            ("in progress",),
            ("completed",),
        ]

        cursor.executemany(
            "INSERT INTO status (name) VALUES (%s)",
            statuses,
        )

        users = [
            (
                fake.name(),
                fake.unique.email(),
            )
            for _ in range(10)
        ]

        cursor.executemany(
            """
            INSERT INTO users (fullname, email)
            VALUES (%s, %s)
            """,
            users,
        )

        cursor.execute("SELECT id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT id FROM status")
        status_ids = [row[0] for row in cursor.fetchall()]

        tasks = [
            (
                fake.sentence(nb_words=5),
                fake.text(max_nb_chars=200),
                random.choice(status_ids),
                random.choice(user_ids),
            )
            for _ in range(20)
        ]

        cursor.executemany(
            """
            INSERT INTO tasks (title, description, status_id, user_id)
            VALUES (%s, %s, %s, %s)
            """,
            tasks,
        )

        connection.commit()

        print("Database seeded successfully.")

    except Exception as error:
        connection.rollback()
        print(f"Error: {error}")

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    seed_database()