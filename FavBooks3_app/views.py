from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Book
from time import gmtime, strftime
from django.contrib.auth.hashers import check_password
import bcrypt

def Index(request):
    return render(request, "index.html")

def Registration(request):
    form = request.POST
    errors = User.objects.basic_validator_reg(form)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")    
    else:
        pw_hash = bcrypt.hashpw(form["password"].encode(), bcrypt.gensalt()).decode()

    user = User.objects.create(first_name = request.POST['first_name'], last_name= request.POST['last_name'] , email = request.POST['email'] , password = pw_hash)

    return redirect("/")

def Login(request):
    form = request.POST
    errors = User.objects.basic_validator_log(form)
    print("********PRINTING THE LOGIN ERRORS",errors)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/") 
    else: 
        user = User.objects.filter(email = request.POST['email'])
        if user:
            user_id = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user_id.password.encode()):
                same_email = User.objects.filter(email = form['email'])
                request.session['user_id'] = same_email[0].id 
                return redirect('/books')

def User_Logged_In(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to view the news feed")
        return redirect("/")

    context = {
        'userid': User.objects.get(id = request.session['user_id']),
        'favbookslist': Book.objects.all(),
        "time": strftime("%Y-%m-%d %H:%M %p", gmtime())
    }
    return render(request, "fav_books_homepage.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")

def Add_Book_To_Site(request):
    form = request.POST
    errors = Book.objects.basic_validator(form)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/books")
    this_user = User.objects.get(id = request.session['user_id'])
    this_user.readers.add(Book.objects.create(title = form['title'], description = form['description'], uploaded_by = User.objects.get(id=request.session['user_id'])))
    return redirect("/books")
    
def Edit_FavBook(request, bookid):
    form = request.POST
    errors = Book.objects.basic_validator(form)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/books")
    return redirect(f"/books/{bookid}")

def Details_Read(request, bookid):
    context = {
        'userid': User.objects.get(id = request.session['user_id']),
        'book_details': Book.objects.get(id=bookid),
        "time": strftime("%Y-%m-%d %H:%M %p", gmtime())
    }
    return render(request, "fav_details.html", context)

def delete_atag(request, bookid):
    e = Book.objects.get(id=bookid)
    e.delete() 
    return redirect("/books")

def update_book(request, bookid):
    errors_from_basic_validator = Book.objects.basic_validator(request.POST)
    if len(errors_from_basic_validator)>0:
        for key, value in errors_from_basic_validator.items():
            messages.error(request, value)
        return redirect(f'books/{bookid}')

    b = Book.objects.get(id = bookid)
    this_user = User.objects.get(id = request.session['user_id'])
    b.users_who_favorited.add(this_user)

    b = Book.objects.get(id = bookid)
    b.title = request.POST['title']
    b.description = request.POST['description']
    b.save()
    return redirect('/books')

def add_to_fav_book_list(request, bookid):
    b = Book.objects.get(id = bookid)
    this_user = User.objects.get(id = request.session['user_id'])
    b.users_who_favorited.add(this_user)
    return redirect(f"/books/{bookid}")

def remove_from_book_list(request, bookid):
    b = Book.objects.get(id = bookid)
    this_user = User.objects.get(id = request.session['user_id'])
    b.users_who_favorited.remove(this_user)
    return redirect(f"/books/{bookid}")

def back(request):
    return redirect('/books')






# def add_book_to_fav_list(request, userid, bookid):
#     this_user = User.objects.get(id=userid)
#     this_book = Book.objects.get(id=bookid)
#     book = Book.objects.get(id = request.POST['book_id'])
#     this_user.readers.add(book)
#     return redirect(f'/books/{bookid}')








