from django.shortcuts import render
from blogs.models import Category,Blog
from assignments.models import About


def home(request):
    categories = Category.objects.all()
    feature_post = Blog.objects.filter(is_featured=True ,status = 'Published').order_by('updated_at')
    posts=Blog.objects.filter(is_featured=False ,status = 'Published')
    try:
        about=About.objects.get()
    except:
        about=None
    context={
        'categories':categories,
        'feature_post':feature_post,
        'posts':posts,
        'about':about
    }
    return render(request, 'home.html',context)