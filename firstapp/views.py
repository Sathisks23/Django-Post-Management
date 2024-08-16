from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from firstapp.models import Category, Post
from django.core.paginator import Paginator
from .forms import PostForm, LoginForm,CategoryForm

from django.http import HttpResponse

def index(req):
    query = req.GET.get('q')
    if query:
        all_posts = Post.objects.filter(title__icontains=query)
    else:
        all_posts = Post.objects.all()

    categories = Category.objects.all()

    # Pagination
    paginator = Paginator(all_posts, 9)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(req, 'index.html', {"page_obj": page_obj, 'categories': categories, 'query': query})

def adminpage(req):
    if not req.user.is_authenticated:
        return redirect('firstapp:adminlogin')

    post_id = req.GET.get('edit')
    edit_post = None

    if post_id:
        edit_post = get_object_or_404(Post, id=post_id)
        form = PostForm(instance=edit_post)
    else:
        form = PostForm()

    if req.method == "POST":
        form = PostForm(req.POST, req.FILES, instance=edit_post)
        if form.is_valid():
            form.save()
            messages.success(req, "Post updated successfully!" if edit_post else "Post created successfully!")
            return redirect('firstapp:adminPage')
        else:
            messages.error(req, "Error in form submission. Please try again.")

    return render(req, 'admin.html', {'form': form, 'edit_post': edit_post})

def delete_post(req):
    post_id = req.GET.get('post_id')
    post = get_object_or_404(Post, id=post_id)

    if req.method == "GET" and req.user.is_authenticated:
        post.delete()
        messages.success(req, "Post deleted successfully!")
        return redirect('firstapp:index')

    return HttpResponse("Unauthorized", status=401)

# Other views remain unchanged


def categoryShort(req, post_name):
    all_posts = Post.objects.filter(category__name=post_name)
    categories = Category.objects.all()

    # pagination
    paginator = Paginator(all_posts, 9)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(req, 'index.html', {"page_obj": page_obj, 'categories': categories})


def postview(req, post_id):
    post = Post.objects.get(pk=post_id)
    return render(req, 'singlepost.html', {'post': post})
def login(req):
    if req.user.is_authenticated:
        return redirect('firstapp:index')  # Redirect if the user is already logged in

    if req.method == "POST":
        form = LoginForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(req, username=username, password=password)
            if user is not None:
                auth_login(req, user)
                return redirect('firstapp:adminPage')
            else:
                messages.error(req, "Invalid username or password")
                return redirect('firstapp:adminlogin')  # Redirect back to the login page on error
        else:
            messages.error(req, "Invalid form input")
            return redirect('firstapp:adminlogin')  # Redirect back to the login page on error
    else:
        form = LoginForm()

    return render(req, 'login.html', {'form': form})


def logout_view(req):
    auth_logout(req)
    return redirect('firstapp:index')

def add_category(req):
    if req.method == "POST":
        form = CategoryForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('firstapp:adminPage')
        else:
            # Handle the case where the form is invalid
            pass
    else:
        form = CategoryForm()

    return render(req, 'add_category.html', {'form': form})