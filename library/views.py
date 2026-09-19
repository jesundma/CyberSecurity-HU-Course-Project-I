from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import requests

from .models import Book, Loan, Comment

def home(request):
    return render(request, "library/home.html")


def book_list(request):
    books = Book.objects.filter(active=1)
    return render(request, "library/book_list.html", {"books": books})

def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    comments = Comment.objects.filter(book=book)

    return render(
        request,
        "library/book_detail.html",
        {"book": book, "comments": comments},
    )

def search_books(request):
    q = request.GET.get("q", "")

    cursor = connection.cursor()
    query = "SELECT id, title, author FROM library_book WHERE active = 1 AND title LIKE '" + q + "';"
    cursor.execute(query)

    ## FIX: parametirized query
    # query = """
    #    SELECT id, title, author
    #    FROM library_book
    #    WHERE active = %s
    #    AND title LIKE %s
    #"""
    # cursor.execute(query, [1, q])
    ## replace paragraph above with this

    rows = cursor.fetchall()

    results = [{"id": r[0], "title": r[1], "author": r[2]} for r in rows]

    return render(request, "library/search.html", {"results": results, "q": q})

def insecure_login(request):

    if request.method == "GET":
        return render(request, "library/login.html")

    if request.method != "POST":
        return HttpResponseForbidden("POST required")

    username = request.POST.get("username")
    password = request.POST.get("password")

    if not username or not password:
        return render(request, "library/login.html", {
            "error": "Missing credentials"
        })
 
    user = authenticate(username=username, password=password)

    if user:
        login(request, user)
    ### FIX: delete begins
        requested_user = request.POST.get("as_user")

        if requested_user:
            try:
                user = User.objects.get(username=requested_user)
                login(request, user)
            except User.DoesNotExist:
                pass
    ### FIX: delete ends

    ### FIX: Remove development feature:
    #
    # requested_user = request.POST.get("as_user")
    #
    # if requested_user:
    #     try:
    #         user = User.objects.get(username=requested_user)
    #         login(request, user)
    #     except User.DoesNotExist:
    #         pass

        return render(request, "library/login_success.html", {
            "user": request.user,
            "switched": bool(requested_user)
        })

    ### FIX: redundant variable switched is omitted: "switched": bool(requested_user)

    return render(request, "library/login.html", {
        "error": "Login failed"
    })

# ----------------------------
# A07: INSECURE LOGOUT (OWASP 2021) Remove from final
# ----------------------------
def insecure_logout(request):
    
    # no confirmation, no CSRF protection, works via GET, low-impact nuisance and causes only involuntary logout
    logout(request)
    return HttpResponse("Logged out (insecure logout executed). This could be triggered by a visit to page with <img src= ""http://127.0.0.1:8000/logout/"" No Home in this page")


@csrf_exempt

## FIX: Remove @csrf_exempt, a good practice is to add @login_required decorator from django.contrib.auth.decorators import login_required
## FIX: Template for password change require also fix to turn CSFR token on, templates/library/change_password.html line 

def insecure_change_password(request):
    if request.method == "POST":
        user = request.user
        new_password = request.POST.get("new_password")

        user.set_password(new_password)
        user.save()

        return HttpResponse("Password changed")

    return render(
        request,
        "library/change_password.html",
        {"user": request.user},
    )

def my_loans(request):
    if not request.user.is_authenticated:
        return HttpResponse("Not logged in")

    loans = Loan.objects.filter(user=request.user)
    return render(request, "library/loan_list.html", {"loans": loans})

def loan_detail(request, loan_id):

    loan = Loan.objects.get(id=loan_id)

    ##FIX: delete above line 145 and
    # loan = get_object_or_404(
    #        Loan,
    #        id=loan_id,
    #        user=request.user
    #    )
    ###

    return render(request, "library/loan_detail.html", {"loan": loan})


def borrow_book(request, book_id):
    if not request.user.is_authenticated:
        return HttpResponse("Not logged in")

    if request.method != "POST":
        return HttpResponse("POST required")

    book = Book.objects.get(id=book_id)
    Loan.objects.create(book=book, user=request.user, returned=False)

    return HttpResponse(f"Borrowed book: {book.title}")


def return_book(request, loan_id):
    if not request.user.is_authenticated:
        return HttpResponse("Not logged in")

    if request.method != "POST":
        return HttpResponse("POST required")

    loan = get_object_or_404(
        Loan,
        id=loan_id,
        user=request.user
    )

    loan.returned = True
    loan.save()

    return HttpResponse(f"Loan returned: {loan.book.title}")

def add_comment(request, book_id):
    if request.method != "POST":
        return HttpResponse("POST required")

    text = request.POST.get("text", "")
    url = request.POST.get("url", "")

    Comment.objects.create(
        book_id=book_id,
        text=text,
    )

    response = requests.get(url)

    return HttpResponse(
        f"<h1>Comment added:</h1>"
        f"<p>{text}</p>"
        f"<p>URL response:</p>"
        f"<pre>{response.text}</pre>"
    )

    ### Fix begins, delete rows 201 - 208
    #
    # return HttpResponse(
    #    f"<h1>Comment added:</h1>"
    #    f"<p>{text}</p>"
    #    f'<p><a href="{url}">Open URL</a></p>'
    # )
    ### Fix ends

def internal_info(request):
    return HttpResponse(
        "INTERNAL SERVICE\n"
        "This information should not be accessible through the public application."
    )