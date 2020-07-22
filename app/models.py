from django.db import models
from django.contrib.auth import get_user_model


class ReviewManager(models.Manager):
    def validator(self, postData):
        errors = {}

        # Title validations
        if len(postData['title']) < 3:
            errors['title'] = 'Title must be 2 or more characters'

        # Author validations
        if 'author-input' not in postData or 'author-select' not in postData:
            errors['author'] = 'Need to select or input an author.'
        elif len(postData['author-input']) < 2:
            errors['author'] = 'Author name must be 3 or more characters'

        # Review validations
        if len(postData['review']) < 10:
            errors['review'] = 'Review must be 10 or more characters'
        if postData['rating'] < 1 or postData['rating'] > 5:
            errors['rating'] = 'Rating must be between 1 and 5'

        return errors


class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Author,
        related_name='books',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Reviews(models.Model):
    review = models.TextField()
    rating = models.SmallIntegerField()
    book = models.ForeignKey(
        Book,
        related_name='reviews',
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        get_user_model(),
        related_name='reviews',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ReviewManager()
