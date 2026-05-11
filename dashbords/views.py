from django.shortcuts import render,redirect
from blogs.models import Category,Blog
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm,BlogPostForm
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify

# Create your views here.
@login_required(login_url='login')
def dashbords(request):
    category_count= Category.objects.all().count()
    blog_count=Blog.objects.all().count()
    context={
        'category_count':category_count,
        'blog_count':blog_count,
    }
    return render(request,'dashbord/dashbord.html',context)


# Category crud
def categories(request):
    return render(request,'dashbord/categories.html')
def add_category(request):
    if request.method=='POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form=CategoryForm()
    context={
        'form':form
    }
    return render(request,'dashbord/add_category.html',context)
def edit_category(request,pk):
    category= get_object_or_404(Category,pk=pk)
    if request.method=='POST':
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')

    form=CategoryForm(instance=category)
    context={
        'form':form,
        'category':category
    }
    return render(request,'dashbord/edit_category.html',context)

def delete_category(request, pk):
    category=get_object_or_404(Category,pk=pk)
    category.delete()
    return redirect('categories')



# POST BLOG crud
def posts(request):
    posts=Blog.objects.all()
    context={
        'posts':posts,
    }
    return render(request,'dashbord/posts.html',context)

# def add_post(request):
#     if request.method=="POST":
#         form=BlogPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post=form.save(commit=False)
#             post.author=request.user
#             title=form.cleaned_data['title']
#             post.slug= slugify(title)
#             post.save() 
#             post.slug= f"{slugify(post.title)}-{post.id}"
#             post.save()
#             return redirect('posts')
#     else:
#         form = BlogPostForm()
#     context={
#         'form':form
#     }
#     return render(request,'dashbord/add_post.html',context)
    
from django.utils.text import slugify
import uuid

def add_post(request):

    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # temporary unique slug
            post.slug = str(uuid.uuid4())
            # first save
            post.save()
            # final readable unique slug
            post.slug = f"{slugify(post.title)}-{post.id}"
            # second save
            post.save()
            return redirect('posts')
    else:
        form = BlogPostForm()

    context = {
        'form': form
    }
    return render(request, 'dashbord/add_post.html', context)



# def edit_post(request,pk):
#     post= get_object_or_404(Blog,pk=pk)
#     if request.method=='POST':
#         form = Blog(request.POST,instance=post)
#         if form.is_valid():
#             form.save()
#             return redirect('posts')

#     form=BlogPostForm(instance=post)
#     context={
#         'form':form,
#         'post':post
#     }
#     return render(request,'dashbord/edit_post.html',context)


def edit_post(request,pk):
    post= get_object_or_404(Blog,pk=pk)
    if request.method=='POST':
        form = BlogPostForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            form.save()
            title = form.cleaned_data['title']
            post.slug= slugify(title) + '-' + str(post.id)
            post.save()
            return redirect('posts')
        

    form=BlogPostForm(instance=post)
    context={
        'form':form,
        'post':post
    }
    return render(request,'dashbord/edit_post.html',context)

def delete_post(request,pk):
    post= get_object_or_404(Blog , pk= pk)
    post.delete()
    return redirect('posts')