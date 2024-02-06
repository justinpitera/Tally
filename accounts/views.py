from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .forms import RegisterForm  # Ensure this is imported
from .models import UserProfile  # Ensure this is imported
from django.utils.text import slugify
from .forms import PostForm
from django.urls import reverse
from .models import Post
def UserLogout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page

def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # This saves the User model associated with the form
            user = form.save()

            # Now, capture the role from the form. This assumes 'role' is a field in your form.
            # You might need to adjust this based on how your form is structured.
            role = form.cleaned_data.get('role', UserProfile.STUDENT)  # Default to STUDENT if not provided
            
            # Create and save the UserProfile instance
            UserProfile.objects.create(
                user=user,
                role=role,
                slug=slugify(user.username)  # Or handle slug creation in the model's save method as you already do
            )
            
            # Redirect to login page or wherever you want
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
user = 0
def UserLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Redirect to a success page
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def view_profile(request, user_id):
    # Fetch the User instance
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=user).order_by('-date_posted')  
    # Attempt to fetch the associated UserProfile instance
    # This will include the role information you want to display
    user_profile = UserProfile.objects.filter(user=user).first()
    
    # Pass both the User and UserProfile instances (or just the role, if preferred) to your template
    return render(request, 'accounts/profile.html', {
        'user': user,
        'posts': posts,
        'user_profile': user_profile  # You can also directly pass 'role': user_profile.role if you only need the role
    })

@login_required  # Ensures that only logged-in users can create posts
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # Create a Post instance but don't save it to the database yet
            post.user = request.user  # Set the user of the post to the current user
            post.save()  # Now save the Post instance to the database with the user set
            # Use the reverse function to dynamically generate the URL to redirect to, including the user ID
            return redirect(reverse('view_profile', kwargs={'user_id': request.user.id}))  # Pass the user ID correctly
    else:
        form = PostForm()
    return render(request, 'accounts/post_form.html', {'form': form})
