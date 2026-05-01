from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Category,Blog

def posts_by_category(request,category_id):
    posts=Blog.objects.filter(status='Published',category=category_id)
    # category=Category.objects.get(id=category_id)
    # try except when we want to do some action if category does not exist
    try:
        category=Category.objects.get(id=category_id)
    except:
        return redirect('home')

#    when you want to 404 error page if category does not exist
    # category=get_object_or_404(Category,id=category_id)


    context={
        'posts':posts,
        'category':category,
    }
    return render(request,"posts_by_category.html",context)
# Create your views here.
