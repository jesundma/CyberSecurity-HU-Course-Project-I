from django.contrib.auth.models import User
from django.db import transaction
from .models import Book, Loan


@transaction.atomic
def create_initial_data():
    desired_users = [
        {"username": "Hupu", "password": "hupu123"},
        {"username": "Tupu", "password": "tupu123"},
        {"username": "Lupu", "password": "lupu123"},
        {"username": "admin", "password": "admin123"},
    ]

    desired_usernames = {u["username"] for u in desired_users}

    # Create or update users
    for user_data in desired_users:
        user, created = User.objects.get_or_create(username=user_data["username"])
        user.set_password(user_data["password"])  # hashes password correctly
        user.save()

    # Delete users not present in desired seed
    User.objects.exclude(username__in=desired_usernames).delete()

    desired_books = [
        {
            "title": "Dune",
            "author": "Frank Herbert",
            "description": "Spice Must Flow",
            "active": 1,
        },
        {
            "title": "Neuromancer",
            "author": "William Gibson",
            "description": "Word Up: Cyberpunk",
            "active": 1,
        },
        {
            "title": "Foundation",
            "author": "Isaac Asimov",
            "description": "The Mule",
            "active": 1,
        },
        {
            "title": "Do Androids Dream of Electric Sheep?",
            "author": "Philip K. Dick",
            "description": (
                "I've seen things you people wouldn't believe. "
                "Attack ships on fire off the shoulder of Orion. "
                "I watched C-beams glitter in the dark near the Tannhäuser Gate. "
                "All those moments will be lost in time, like tears in rain. Time to die."
            ),
            "active": 1,
        },
        {
            "title": "The Left Hand of Darkness",
            "author": "Ursula K. Le Guin",
            "description": "Genly Ai on Gethen.",
            "active": 1,
        },
        {
            "title": "Snow Crash",
            "author": "Neal Stephenson",
            "description": "Metaverse.",
            "active": 1,
        },
        {
            "title": "The War of the Worlds",
            "author": "H. G. Wells",
            "description": (
                "It never was a war, any more than there's war between man and ants."
            ),
            "active": 1,
        },
        {
            "title": "I, Robot",
            "author": "Isaac Asimov",
            "description": "Three Laws of Robotics.",
            "active": 1,
        },
        {
            "title": "Stranger in a Strange Land",
            "author": "Robert A. Heinlein",
            "description": (
                "A science fiction novel often considered controversial due to "
                "its treatment of religion, society, and sexuality."
            ),
            "active": 0,
        },
    ]

    desired_book_keys = {(b["title"], b["author"]) for b in desired_books}

    # Create or update books
    for book_data in desired_books:
        book, created = Book.objects.update_or_create(
            title=book_data["title"],
            author=book_data["author"],
            defaults={
                "description": book_data["description"],
                "active": book_data["active"],
            },
        )

    # Delete books not present in desired seed
    for book in Book.objects.all():
        key = (book.title, book.author)
        if key not in desired_book_keys:
            book.delete()

    # Create three loans to demonstrate IDOR so full loan functionality is not required
    hupu = User.objects.get(username="Hupu")
    tupu = User.objects.get(username="Tupu")

    dune = Book.objects.get(
        title = "Dune",
        author = "Frank Herbert"
    )

    neuromancer = Book.objects.get(
        title = "Neuromancer",
        author = "William Gibson"
    )

    snow = Book.objects.get(
        title = "Snow Crash",
        author = "Neal Stephenson"
    )

    Loan.objects.update_or_create(
        user = hupu,
        book = dune,
        defaults = {"returned": False},
    )

    Loan.objects.update_or_create(
        user = hupu,
        book = snow,
        defaults = {"returned": False},
    )


    Loan.objects.update_or_create(
        user = tupu,
        book = neuromancer,
        defaults = {"returned": False},
    )