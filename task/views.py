from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm



def home(request):
    return render(request, 'task_list.html')
# ---------------------- REGISTER ----------------------
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.success(request, 'Account created successfully! Please login.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')

    return render(request, 'register.html')


# ---------------------- LOGIN ----------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back {user.username}!')
            return redirect('task_list')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')


# ---------------------- LOGOUT ----------------------
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')


# ---------------------- TASK VIEWS ----------------------
@login_required
def taskview(request):
    """Show all tasks with optional filter (Pending/Completed)."""
    filter_option = request.GET.get('filter')
    tasks = Task.objects.filter(user=request.user)

    if filter_option == 'completed':
        tasks = tasks.filter(status=True)
    elif filter_option == 'pending':
        tasks = tasks.filter(status=False)

    return render(request, 'task_list.html', {'task': tasks})


@login_required
def task_add(request):
    """Add new task with status dropdown (Pending/Completed)."""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status') == 'True'  

        Task.objects.create(user=request.user, title=title, description=description, status=status)
        return redirect('task_list')

    return render(request, 'task_list.html')

@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.status = request.POST.get('status') == 'True'
        task.save()
        messages.success(request, 'Task updated successfully!')
        return redirect('task_list')

    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task_list.html', {'task': tasks, 'edit_task': task})



@login_required
def delete_task(request, task_id):
    """Delete a task."""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    messages.success(request, 'Task deleted successfully!')
    return redirect('task_list')

