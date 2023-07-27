from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone

# Create your models here.


class User(models.Model):
    gender_choices = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, default="None")
    password = models.TextField()
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=gender_choices)
    profile_picture = models.ImageField(upload_to="media/profile_pictures/")
    verification_code = models.CharField(max_length=6, blank=True)
    verification_status = models.BooleanField(default=False)


class FriendRequests(models.Model):
    user_email = models.EmailField()
    friend_email = models.EmailField()
    approval_status = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user_email", "friend_email")


class Message(models.Model):
    sender = models.EmailField()
    receiver = models.EmailField()
    message = models.TextField()
    time = models.DateTimeField()


class TextPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField()
    comments = GenericRelation("TextPostComment")
    likes = GenericRelation("TextLike")


class MediaPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.FileField(
        upload_to="media/posts/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "gif", "mp4"]
            )
        ],
    )
    caption = models.TextField(default="")
    time = models.DateTimeField()
    comments = GenericRelation("MediaPostComment")
    likes = GenericRelation("MediaLike")


class TextPostComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(TextPost, on_delete=models.CASCADE)
    comment = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    time = models.DateTimeField()
    content_object = GenericForeignKey("content_type", "object_id")


class MediaPostComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(MediaPost, on_delete=models.CASCADE)
    comment = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    time = models.DateTimeField()
    content_object = GenericForeignKey("content_type", "object_id")


class TextLike(models.Model):
    post = models.ForeignKey(TextPost, on_delete=models.CASCADE)
    friend = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")


class MediaLike(models.Model):
    post = models.ForeignKey(MediaPost, on_delete=models.CASCADE)
    friend = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")


class TextStory(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField()
    comments = GenericRelation("TextStoryComment")
    likes = GenericRelation("TextStoryLike")


class MediaStory(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.FileField(
        upload_to="media/posts/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "gif", "mp4"]
            )
        ],
    )
    caption = models.TextField(default="")
    time = models.DateTimeField()
    comments = GenericRelation("MediaStoryComment")
    likes = GenericRelation("MediaStoryLike")


class TextStoryComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(TextStory, on_delete=models.CASCADE)
    comment = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    time = models.DateTimeField()
    content_object = GenericForeignKey("content_type", "object_id")


class MediaStoryComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(MediaStory, on_delete=models.CASCADE)
    comment = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    time = models.DateTimeField()
    content_object = GenericForeignKey("content_type", "object_id")


class TextStoryLike(models.Model):
    story = models.ForeignKey(TextStory, on_delete=models.CASCADE)
    friend = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")


class MediaStoryLike(models.Model):
    story = models.ForeignKey(MediaStory, on_delete=models.CASCADE)
    friend = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
