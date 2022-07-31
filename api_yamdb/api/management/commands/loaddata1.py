from csv import DictReader
from django.core.management import BaseCommand
import os

# Import the model
from users.models import User
from reviews.models import Category, Genre


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from users.csv"

    def handle(self, *args, **options):
    
        # Show this if the data already exist in the database
        if User.objects.exists():
            print('User data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
        else:   
            # Show this before loading the data into the database
            print("Loading User data")

            #Code to load the data into database
            for row in DictReader(open('static/data/users.csv')):
                user=User(
                    username=row['username'], 
                    email=row['email'], 
                    role=row['role']
                )
                user.save()

        if Category.objects.exists():
            print('User data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
        else:   
            # Show this before loading the data into the database
            print("Loading Category data")

            #Code to load the data into database
            for row in DictReader(open('static/data/category.csv')):
                category=Category(name=row['name'], slug=row['slug'])
                category.save()

        if Genre.objects.exists():
            print('User data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
        else:   
            # Show this before loading the data into the database
            print("Loading Genre data")

            #Code to load the data into database
            for row in DictReader(open('static/data/genre.csv')):
                genre=Genre(name=row['name'], slug=row['slug'])
                genre.save()
