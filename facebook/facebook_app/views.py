from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import *
from .forms import *
from django.core.mail import send_mail
from django.conf import settings
import secrets
import string
import bcrypt
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from datetime import datetime

# Create your views here.

#to generate verification code which will be used for authentication after signup
def generate_verification_code(length):
    alphabet = string.ascii_letters + string.digits
    code = "".join(secrets.choice(alphabet) for _ in range(length))
    return code

#this function will be used to send verification code email to user
def send_email(verification_code, email):
    subject = "Verification Code for Facebook"
    message = "Your verification code is: " + verification_code
    from_email = "facebook.clone.project123@gmail.com"
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

#this function will render signup.html page and after signup will redirect to authenticate
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            name = form.cleaned_data["name"]
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]
            date_of_birth = form.cleaned_data["date_of_birth"]
            gender = form.cleaned_data["gender"]
            profile_picture = form.cleaned_data["profile_picture"]
            if password == confirm_password:
                verification_code = generate_verification_code(6)
                #generating hashed_password to save in db for security
                hashed_password = bcrypt.hashpw(
                    password.encode("utf-8"), bcrypt.gensalt()
                )
                hashed_password = hashed_password.decode("utf-8")
                user = User(
                    email=email,
                    name=name,
                    password=hashed_password,
                    date_of_birth=date_of_birth,
                    gender=gender,
                    profile_picture=profile_picture,
                    verification_code=verification_code,
                )
                user.save()
                send_email(verification_code, email)
                return redirect("authenticate", email=email)
    else:
        form = SignUpForm()

    return render(request, "facebook/signup.html", {"form": form})

#this function will render authenticate.html and if user is authenticated it will redirect to login
def authenticate(request, email):
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=email)
            if user.verification_code == form.cleaned_data["verification_code"]:
                user.verification_status = True
                user.save()
                return redirect("login")
            else:
                return redirect("authenticate", email)
    else:
        form = AuthenticationForm()
    return render(request, "facebook/authenticate.html", {"form": form})


#this function will render login.html and if user is not authenticated yet it will redirect to authenticate otherwise home 
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.get(email=email)
            if user.verification_status == True:
                user_password = user.password.encode("utf-8")
                if bcrypt.checkpw(password.encode("utf-8"), user_password):
                    request.session["user_email"] = email
                    return redirect("home")
                else:
                    return render(request, "facebook/login.html", {"form": form})
            else:
                return redirect("authenticate", user.email)

    else:
        form = LoginForm()
    return render(request, "facebook/login.html", {"form": form})

#this function will help user to search other users based on a search_term
def search(request):
    current_user = request.session.get("user_email")
    user = User.objects.get(email=current_user)
    users = {}
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data["search"]
            users = User.objects.filter(name__icontains=search_term)

    else:
        form = SearchForm()

    return render(
        request, "facebook/search.html", {"form": form, "users": users, "user": user}
    )



def add_friend(request, email):
    current_user = request.session.get("user_email")
    friend_email = email
    user = User.objects.get(email=current_user)
    friend_request = FriendRequests(user_email=user.email, friend_email=friend_email)
    friend_request.save()
    return redirect("add_friend")


def view_requests(request):
    current_user = request.session.get("user_email")
    user = User.objects.get(email=current_user)
    requests = FriendRequests.objects.filter(friend_email=current_user)
    email_ids = []
    for req in requests:
        if req.approval_status == False:
            email_ids.append(req.user_email)
    users = []
    for email_id in email_ids:
        users.append(User.objects.get(email=email_id))

    return render(
        request, "facebook/view_requests.html", {"users": users, "user": user}
    )


def accept_request(request, email):
    current_user = request.session.get("user_email")
    requests = FriendRequests.objects.get(friend_email=current_user, user_email=email)
    requests.approval_status = True
    requests.save()
    return redirect("view_requests")

#on logout user session is cleared after this. Now to access any page user has to login first
def logout(request):
    request.session.clear()
    return redirect("login")


def reject_request(request, email):
    current_user = request.session.get("user_email")
    requests = FriendRequests.objects.get(friend_email=current_user, user_email=email)
    requests.delete()
    return redirect("view_requests")


def view_friends(request):
    current_user = request.session.get("user_email")
    user = User.objects.get(email=current_user)
    #users are friends if either user email or friend is same as current user 
    friends = FriendRequests.objects.filter(
        Q(user_email=current_user) | Q(friend_email=current_user)
    )

    email_ids = []
    for friend in friends:
        if friend.approval_status == True:
            if friend.user_email == current_user:
                email_ids.append(friend.friend_email)
            else:
                email_ids.append(friend.user_email)
    users = []
    for email_id in email_ids:
        users.append(User.objects.get(email=email_id))

    return render(request, "facebook/view_friends.html", {"users": users, "user": user})


def view_profile(request, email):
    current_user = request.session.get("user_email")
    current_user = User.objects.get(email=current_user)
    user = User.objects.filter(email=email)
    return render(
        request, "facebook/view_profile.html", {"users": user, "user": current_user}
    )


def view_user_profile(request, email):
    current_user = request.session.get("user_email")
    current_user = User.objects.get(email=current_user)
    user = User.objects.filter(email=email)
    return render(
        request, "facebook/user_profile.html", {"users": user, "user": current_user}
    )

"""this funtion will redirect to chat.html and when a message is sent
from user side it will redirect to chat so user will not have to refresh
page again and again to check whether message is sent or not but friend 
have to refresh to check new messages"""

def chat(request, email):
    user = request.session.get("user_email")
    friend = User.objects.get(email=email)
    sender = User.objects.get(email=user)
    messages = Message.objects.filter(
        (Q(sender=user) & Q(receiver=email)) | (Q(sender=email) & Q(receiver=user))
    ).order_by("time")
    sent = []
    received = []
    for message in messages:
        if message.sender == user:
            sent.append(message)
        else:
            received.append(message)

    if request.method == "POST":
        form = ChatForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            msg = Message(
                sender=user, receiver=email, message=message, time=datetime.now()
            )
            msg.save()
            return redirect("chat", email)
    else:
        form = ChatForm()
    return render(
        request,
        "facebook/chat.html",
        {
            "messages": messages,
            "form": form,
            "sent": sent,
            "received": received,
            "friend": friend,
            "sender": sender,
        },
    )


def text_post(request):
    user = request.session.get("user_email")
    post = {}
    user = User.objects.get(email=user)
    if request.method == "POST":
        form = TextPostForm(request.POST)
        if form.is_valid():
            post = TextPost(
                author=user, content=form.cleaned_data["content"], time=datetime.now()
            )
            post.save()
            return redirect("your_posts")
    else:
        form = TextPostForm()
    return render(
        request,
        "facebook/create_text_post.html",
        {"form": form, "post": post, "user": user},
    )


def media_post(request):
    user = request.session.get("user_email")
    post = {}
    user = User.objects.get(email=user)
    if request.method == "POST":
        form = MediaPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = MediaPost(
                author=user,
                content=form.cleaned_data["content"],
                caption=form.cleaned_data["caption"],
                time=datetime.now(),
            )
            post.save()
            return redirect("your_posts")
    else:
        form = MediaPostForm()
    return render(
        request,
        "facebook/create_media_post.html",
        {"form": form, "post": post, "user": user},
    )


def your_posts(request):
    user = request.session.get("user_email")
    user = User.objects.get(email=user)
    text_posts = TextPost.objects.filter(author=user)
    media_posts = MediaPost.objects.filter(author=user)
    combined_posts = list(text_posts) + list(media_posts)
    combined_posts = sorted(combined_posts, key=lambda post: post.time)
    return render(
        request,
        "facebook/your_posts.html",
        {
            "text_posts": text_posts,
            "media_posts": media_posts,
            "combined_posts": combined_posts,
            "user": user,
        },
    )

#this function will render home.html and contains all the posts from friends which are sorted on the basis of time
def home(request):
    current_user = request.session.get("user_email")
    user = User.objects.get(email=current_user)
    friends = FriendRequests.objects.filter(
        Q(user_email=current_user) | Q(friend_email=current_user)
    )

    email_ids = []
    for friend in friends:
        if friend.approval_status == True:
            if friend.user_email == current_user:
                email_ids.append(friend.friend_email)
            else:
                email_ids.append(friend.user_email)
    friends = []
    for email_id in email_ids:
        friends.append(User.objects.get(email=email_id))

    text_posts = []
    media_posts = []
    for friend in friends:
        text_posts = TextPost.objects.filter(author=friend)
        media_posts = MediaPost.objects.filter(author=friend)
    combined_posts = list(text_posts) + list(media_posts)
    combined_posts = sorted(combined_posts, key=lambda post: post.time)
    return render(
        request,
        "facebook/home.html",
        {
            "text_posts": text_posts,
            "media_posts": media_posts,
            "combined_posts": combined_posts,
            "user": user,
        },
    )


def text_post_like(request, id):
    current_user = request.session.get("user_email")
    user = User.objects.get(email=current_user)
    post = TextPost.objects.get(id=id)
    like = TextLike.objects.create(
        friend=user,
        post=post,
        content_type=ContentType.objects.get_for_model(post),
        object_id=id,
    )
    like.save()
    return redirect("home")


def media_post_like(request, id):
    current_user = request.session.get("user_email")
    user = User.objects.get(email=current_user)
    post = MediaPost.objects.get(id=id)
    like = MediaLike.objects.create(
        friend=user,
        post=post,
        content_type=ContentType.objects.get_for_model(post),
        object_id=id,
    )
    like.save()
    return redirect("home")


def text_post_comment(request, id):
    current_user = request.session.get("user_email")
    user = User.objects.get(email=current_user)
    post = TextPost.objects.get(id=id)
    text_post_comments = post.comments.all()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = TextPostComment.objects.create(
                author=user,
                post=post,
                comment=form.cleaned_data["comment"],
                time=datetime.now(),
                content_type=ContentType.objects.get_for_model(post),
                object_id=id,
            )
            comment.save()
    else:
        form = CommentForm()
    return render(
        request,
        "facebook/comment.html",
        {"form": form, "comments": text_post_comments, "user": user},
    )


def media_post_comment(request, id):
    current_user = request.session.get("user_email")
    user = User.objects.get(email=current_user)
    post = MediaPost.objects.get(id=id)
    text_post_comments = post.comments.all()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = MediaPostComment.objects.create(
                author=user,
                post=post,
                comment=form.cleaned_data["comment"],
                time=datetime.now(),
                content_type=ContentType.objects.get_for_model(post),
                object_id=id,
            )
            comment.save()
    else:
        form = CommentForm()
    return render(
        request,
        "facebook/comment.html",
        {"form": form, "comments": text_post_comments, "user": user},
    )


def view_text_comments(request, id):
    current_user = request.session.get("user_email")
    user = User.objects.get(email=current_user)
    post = TextPost.objects.get(id=id)
    text_post_comments = post.comments.all()
    return render(
        request,
        "facebook/view_comments.html",
        {"comments": text_post_comments, "user": user},
    )


def view_media_comments(request, id):
    current_user = request.session.get("user_email")
    user = User.objects.get(email=current_user)
    post = MediaPost.objects.get(id=id)
    media_post_comments = post.comments.all()
    return render(
        request,
        "facebook/view_comments.html",
        {"comments": media_post_comments, "user": user},
    )


def view_text_likes(request, id):
    current_user = request.session.get("user_email")
    user = User.objects.get(email=current_user)
    post = TextPost.objects.get(id=id)
    text_post_likes = post.likes.all()
    return render(
        request, "facebook/view_likes.html", {"likes": text_post_likes, "user": user}
    )


def view_media_likes(request, id):
    current_user = request.session.get("user_email")
    user = User.objects.get(email=current_user)
    post = MediaPost.objects.get(id=id)
    media_post_likes = post.likes.all()
    return render(
        request, "facebook/view_likes.html", {"likes": media_post_likes, "user": user}
    )


def update_profile(request):
    email = request.session.get("user_email")
    user = User.objects.get(email=email)
    if request.method == "POST":
        name = request.POST.get("name")
        profile_picture = request.FILES.get("picture")
        if profile_picture:
            user.profile_picture = profile_picture
            user.save()
        if name:
            user.name = name
            user.save()

    return redirect("view_user_profile", email)


def text_story(request):
    user = request.session.get("user_email")
    post = {}
    user = User.objects.get(email=user)
    if request.method == "POST":
        form = TextStoryForm(request.POST)
        if form.is_valid():
            post = TextStory(
                author=user, content=form.cleaned_data["content"], time=datetime.now()
            )
            post.save()
            return redirect("your_stories")
    else:
        form = TextPostForm()
    return render(
        request,
        "facebook/add_text_story.html",
        {"form": form, "post": post, "user": user},
    )


def media_story(request):
    user = request.session.get("user_email")
    post = {}
    user = User.objects.get(email=user)
    if request.method == "POST":
        form = MediaStoryForm(request.POST, request.FILES)
        if form.is_valid():
            post = MediaStory(
                author=user,
                content=form.cleaned_data["content"],
                caption=form.cleaned_data["caption"],
                time=datetime.now(),
            )
            post.save()
            return redirect("your_stories")
    else:
        form = MediaPostForm()
    return render(
        request,
        "facebook/add_media_story.html",
        {"form": form, "post": post, "user": user},
    )


def your_stories(request):
    user = request.session.get("user_email")
    user = User.objects.get(email=user)
    text_posts = TextStory.objects.filter(author=user)
    media_posts = MediaStory.objects.filter(author=user)
    combined_posts = list(text_posts) + list(media_posts)
    combined_posts = sorted(combined_posts, key=lambda post: post.time)
    return render(
        request,
        "facebook/your_stories.html",
        {
            "text_posts": text_posts,
            "media_posts": media_posts,
            "combined_posts": combined_posts,
            "user": user,
        },
    )


def view_text_story_comments(request, id):
    current_user = request.session.get("user_email")
    user = User.objects.get(email=current_user)
    story = TextStory.objects.get(id=id)
    text_story_comments = story.comments.all()
    return render(
        request,
        "facebook/view_comments.html",
        {"comments": text_story_comments, "user": user},
    )


def view_media_story_comments(request, id):
    current_user = request.session.get("user_email")
    user = User.objects.get(email=current_user)
    story = MediaStory.objects.get(id=id)
    media_story_comments = story.comments.all()
    return render(
        request,
        "facebook/view_comments.html",
        {"comments": media_story_comments, "user": user},
    )


def view_text_story_likes(request, id):
    current_user = request.session.get("user_email")
    user = User.objects.get(email=current_user)
    story = TextStory.objects.get(id=id)
    text_story_likes = story.likes.all()
    return render(
        request, "facebook/view_likes.html", {"likes": text_story_likes, "user": user}
    )


def view_media_story_likes(request, id):
    current_user = request.session.get("user_email")
    user = User.objects.get(email=current_user)
    story = MediaStory.objects.get(id=id)
    media_story_likes = story.likes.all()
    return render(
        request, "facebook/view_likes.html", {"likes": media_story_likes, "user": user}
    )


def text_story_comment(request, id):
    current_user = request.session.get("user_email")
    user = User.objects.get(email=current_user)
    story = TextStory.objects.get(id=id)
    text_story_comments = story.comments.all()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = TextStoryComment.objects.create(
                author=user,
                story=story,
                comment=form.cleaned_data["comment"],
                time=datetime.now(),
                content_type=ContentType.objects.get_for_model(story),
                object_id=id,
            )
            comment.save()
    else:
        form = CommentForm()
    return render(
        request,
        "facebook/comment.html",
        {"form": form, "comments": text_story_comments, "user": user},
    )


def media_story_comment(request, id):
    current_user = request.session.get("user_email")
    user = User.objects.get(email=current_user)
    story = MediaStory.objects.get(id=id)
    media_story_comments = story.comments.all()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = MediaStoryComment.objects.create(
                author=user,
                story=story,
                comment=form.cleaned_data["comment"],
                time=datetime.now(),
                content_type=ContentType.objects.get_for_model(story),
                object_id=id,
            )
            comment.save()
    else:
        form = CommentForm()
    return render(
        request,
        "facebook/comment.html",
        {"form": form, "comments": media_story_comments, "user": user},
    )


def text_story_like(request, id, email):
    current_user = request.session.get("user_email")
    user = User.objects.get(email=current_user)
    story = TextStory.objects.get(id=id)
    like = TextStoryLike.objects.create(
        friend=user,
        story=story,
        content_type=ContentType.objects.get_for_model(story),
        object_id=id,
    )
    like.save()
    return redirect("view_story", email)


def media_story_like(request, id, email):
    current_user = request.session.get("user_email")
    user = User.objects.get(email=current_user)
    story = MediaStory.objects.get(id=id)
    like = MediaStoryLike.objects.create(
        friend=user,
        story=story,
        content_type=ContentType.objects.get_for_model(story),
        object_id=id,
    )
    like.save()
    return redirect("view_story", email)


def view_story(request, email):
    user = request.session.get("user_email")
    user = User.objects.get(email=user)
    friend = User.objects.get(email=email)
    text_posts = TextStory.objects.filter(author=friend)
    media_posts = MediaStory.objects.filter(author=friend)
    combined_posts = list(text_posts) + list(media_posts)
    combined_posts = sorted(combined_posts, key=lambda post: post.time)
    return render(
        request,
        "facebook/view_story.html",
        {
            "text_posts": text_posts,
            "media_posts": media_posts,
            "combined_posts": combined_posts,
            "user": user,
        },
    )


def remove_text_story(request, id):
    story = TextStory.objects.get(id=id)
    story.delete()
    user = request.session.get("user_email")
    return redirect("your_stories")


def remove_media_story(request, id):
    story = MediaStory.objects.get(id=id)
    story.delete()
    user = request.session.get("user_email")
    return redirect("your_stories")


def remove_text_post(request, id):
    post = TextPost.objects.get(id=id)
    post.delete()
    user = request.session.get("user_email")
    return redirect("your_posts")


def remove_media_post(request, id):
    post = MediaPost.objects.get(id=id)
    post.delete()
    user = request.session.get("user_email")
    return redirect("your_posts")
