from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import Category,Blog,Comment
from django.db.models import Q

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

def blogs(request,slug):
    single_blog = get_object_or_404(Blog , slug=slug, status='Published')
    if request.method=='POST':
        comment=Comment()
        comment.user=request.user
        comment.blog=single_blog
        comment.comment=request.POST['comment']
        comment.save()
        return HttpResponseRedirect(request.path_info)
    comments=Comment.objects.filter(blog=single_blog)
    comments_count = comments.count()
    context={
        'single_blog':single_blog,
        'comments':comments,
        'comments_count':comments_count,
    }

    return render(request,'blogs.html',context)

def search(request):
    keyword=request.GET.get('keyword')
    blogs= Blog.objects.filter(Q(title__icontains = keyword)|Q(short_description__icontains = keyword)|Q( blog_body__icontains = keyword) , status='Published',)
    context={
        'keyword':keyword,
        'blogs':blogs,
    }
    return render(request , 'search.html',context)