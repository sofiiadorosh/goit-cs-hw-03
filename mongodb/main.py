import os
import certifi

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.server_api import ServerApi

from cats import cats


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(
    MONGO_URI,
    server_api=ServerApi("1"),
    tlsCAFile=certifi.where()
)

db = client.neoversity
cats_collection = db.cats


def add_cats():
    """Add 20 cats to the collection."""
    try:
        result = cats_collection.insert_many(cats)

        print(f"Added {len(result.inserted_ids)} cats.")

        return result

    except PyMongoError as e:
        print(f"Error adding cats: {e}")
        return None


def get_cats():
    """Return all cats from the collection."""
    try:
        return cats_collection.find({})

    except PyMongoError as e:
        print(f"Error getting cats: {e}")
        return []


def get_cat_by_name(name):
    """Return a cat by its name."""
    try:
        return cats_collection.find_one(
            {"name": {"$regex": f"^{name}$", "$options": "i"}}
        )

    except PyMongoError as e:
        print(f"Error getting cat: {e}")
        return None


def update_cat_age_by_name(name, age):
    """Update the age of a cat by its name."""
    try:
        result = cats_collection.update_one(
            {"name": {"$regex": f"^{name}$", "$options": "i"}},
            {"$set": {"age": age}}
        )

        if not result.matched_count:
            print(f"Cat '{name}' not found.")
            return None

        return cats_collection.find_one(
            {"name": {"$regex": f"^{name}$", "$options": "i"}}
        )

    except PyMongoError as e:
        print(f"Error updating cat age: {e}")
        return None


def update_cat_feature_by_name(name, feature):
    """Add a new feature to a cat by its name."""
    try:
        result = cats_collection.update_one(
            {"name": {"$regex": f"^{name}$", "$options": "i"}},
            {"$push": {"features": feature}}
        )

        if not result.matched_count:
            print(f"Cat '{name}' not found.")
            return None

        return cats_collection.find_one(
            {"name": {"$regex": f"^{name}$", "$options": "i"}}
        )

    except PyMongoError as e:
        print(f"Error adding cat feature: {e}")
        return None


def delete_cat_by_name(name):
    """Delete a cat by its name."""
    try:
        result = cats_collection.delete_one(
            {"name": {"$regex": f"^{name}$", "$options": "i"}}
        )

        if not result.deleted_count:
            print(f"Cat '{name}' not found.")
        else:
            print(f"Cat '{name}' was deleted.")

        return result

    except PyMongoError as e:
        print(f"Error deleting cat: {e}")
        return None


def delete_cats():
    """Delete all cats from the collection."""
    try:
        result = cats_collection.delete_many({})

        print(f"Deleted {result.deleted_count} cats.")

        return result

    except PyMongoError as e:
        print(f"Error deleting cats: {e}")
        return None


def get_valid_age():
    """Ask the user for a valid non-negative age."""
    while True:
        try:
            age = int(input("Enter new age: "))

            if age < 0:
                print("Age cannot be negative.")
                continue

            return age

        except ValueError:
            print("Age must be a valid number.")


def main():
    try:
        client.admin.command("ping")
        print("Successfully connected to MongoDB!")

    except PyMongoError as e:
        print(f"MongoDB connection error: {e}")
        return

    add_cats()

    print()
    print("All cats:")

    cats_cursor = get_cats()

    for cat in cats_cursor:
        print(cat)

    print()
    print("Find cat by name:")

    name = input("Enter cat name: ")

    cat = get_cat_by_name(name)

    if cat:
        print(cat)
    else:
        print("Cat not found.")

    print()
    print("Update cat age:")

    name = input("Enter cat name: ")
    age = get_valid_age()

    updated_cat = update_cat_age_by_name(name, age)

    if updated_cat:
        print("Updated cat:")
        print(updated_cat)

    print()
    print("Add cat feature:")

    name = input("Enter cat name: ")
    feature = input("Enter new feature: ")

    updated_cat = update_cat_feature_by_name(name, feature)

    if updated_cat:
        print("Updated cat:")
        print(updated_cat)

    print()
    print("Delete cat:")

    name = input("Enter cat name: ")

    delete_cat_by_name(name)

    print()
    print("Delete all cats:")

    delete_cats()


if __name__ == "__main__":
    main()