from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.insecure_login, name="login"),
    path("change_password/", views.insecure_change_password, name="change_password"),
    path("logout/", views.insecure_logout, name="logout"),

    path("books/", views.book_list, name="book_list"),
    path("books/<int:book_id>/", views.book_detail, name="book_detail"),
    path("search/", views.search_books, name="search_books"),

    path("borrow/<int:book_id>/", views.borrow_book, name="borrow_book"),
    path("return/<int:loan_id>/", views.return_book, name="return_book"),
    path("loans/", views.my_loans, name="my_loans"),
    path("loan/<int:loan_id>/", views.loan_detail, name="loan_detail"),

    path("comment/<int:book_id>/", views.add_comment, name="add_comment"),
    path("internal-info/", views.internal_info, name="internal_info"),
]