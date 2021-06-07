from django.core.checks import messages
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Book, Review
import bcrypt

def root(request):
    return render(request,'welcome.html')
def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(
        name= request.POST['name'],
        alias=request.POST['alias'],
        email=request.POST['email'],
        password=hashed
    )
    request.session['user_id']= new_user.id
    return redirect('/home')
def login(request):
    errors=User.objects.login_validator(request.POST)
    if len(errors)>0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/')
    this_user=User.objects.filter(email=request.POST['email'])
    request.session['user_id']=this_user[0].id
    return redirect('/home')
def home(request):
    if 'user_id' not in request.session:
        messages.error(request,"Please log on.")
        return redirect('/')
    context ={
        'user':User.objects.get(id=int(request.session['user_id'])),
        'books':Book.objects.all(),
        'reviews':Review.objects.all().order_by('-created_at')[:3]
    }
    return render(request,'home.html',context)
def logout(request):
    request.session.clear()
    return redirect('/')
def newBook(request):
    if 'user_id' not in request.session:
        messages.error(request,"Please log on.")
        return redirect('/')
    context={
        'authors':Book.objects.values('author').distinct()
    }
    print(context)
    return render(request,'newBook.html',context)
def createBook(request):
    errors = Book.objects.book_validator(request.POST)
    errors.update(Review.objects.review_validator(request.POST))
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/newBook')
    if request.POST['author'] !='':
        author = request.POST['author']
    else:
        author = request.POST['selectAuthor']
    new_Book = Book.objects.create(
        title=request.POST['title'],
        author=author,
    )
    user= User.objects.get(id=int(request.session['user_id']))
    new_Review= Review.objects.create(
        content= request.POST['content'],
        rating= request.POST['rating'],
        by_user = user,
        for_book=new_Book,
    )
    return redirect('/home')

def viewUser(request, user_id):
    if 'user_id' not in request.session:
        messages.error(request,"Please log on.")
        return redirect('/')
    context={
        'user':User.objects.get(id=int(user_id))
    }
    return render(request,'viewUser.html',context)

def viewBook(request, book_id):
    if 'user_id' not in request.session:
        messages.error(request,"Please log on.")
        return redirect('/')
    context={
        'book':Book.objects.get(id=int(book_id)),
        'user':User.objects.get(id=int(request.session['user_id']))
    }
    print(book_id)
    return render(request,'viewBook.html',context)

def newReview(request, book_id):
    errors=Review.objects.review_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/book/'+str(book_id))
    user= User.objects.get(id=int(request.session['user_id']))
    book= Book.objects.get(id=int(book_id))
    new_review = Review.objects.create(
        content=request.POST['content'],
        rating=request.POST['rating'],
        by_user=user,
        for_book=book,
    )
    return redirect('/home')
def deleteReview(request, review_id):
    review = Review.objects.get(id=review_id)
    review.delete()
    return redirect('/home')