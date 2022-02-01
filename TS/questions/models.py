from django.db import models
from users.models import User
from django.conf import settings
from django.db.models.signals import pre_save
from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator

from techsemester.utils import unique_slug_generator, unique_slug_question_generator


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


def slug_related_question(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_question_generator(instance)


class TagsQuestions(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    approval = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'TagsQuestion'
        verbose_name_plural = 'TagsQuestions'


class Question(models.Model):
    user                    = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user_questions',
                                                related_name='questions')
    tags                    = models.ManyToManyField(TagsQuestions, related_name='question_tags')
    create_date             = models.DateTimeField(auto_now_add=True)
    update_date             = models.DateTimeField(auto_now=True)
    title                   = models.CharField(max_length=255, blank=True, null=True)
    slug                    = models.CharField(max_length=255, blank=True, null=True)
    body                    = RichTextField(blank=True, null=True)
    code                    = RichTextField(blank=True, null=True)
    url                     = models.URLField(blank=True, null=True)
    imageUrl                = models.URLField(blank=True, null=True)
    audio_url               = models.URLField(blank=True, null=True)
    video_url               = models.URLField(blank=True, null=True)
    youtube_url             = models.URLField(blank=True, null=True)
    active                  = models.BooleanField(default=True)
    total_answers           = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def number_of_rating(self):
        ratings = RatingModel.objects.filter(question=self)
        return len(ratings)

    def average_rating(self):
        sum = 0
        ratings = RatingModel.objects.filter(question=self)
        for rating in ratings:
            sum += rating.stars
        if len(ratings) > 0:
            return sum / len(ratings)
        else:
            return 0


class BlogPost(models.Model):
    user                    = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user_blog_post',
                                                related_name='blog_posts')
    tags                    = models.ManyToManyField(TagsQuestions, related_name='blog_post_tags')
    create_date             = models.DateTimeField(auto_now_add=True)
    update_date             = models.DateTimeField(auto_now=True)
    title                   = models.CharField(max_length=255, blank=True, null=True)
    slug                    = models.CharField(max_length=255, blank=True, null=True)
    body                    = RichTextField(blank=True, null=True)
    code                    = RichTextField(blank=True, null=True)
    url                     = models.URLField(blank=True, null=True)
    imageUrl                = models.URLField(blank=True, null=True)
    audio_url               = models.URLField(blank=True, null=True)
    video_url               = models.URLField(blank=True, null=True)
    youtube_url             = models.URLField(blank=True, null=True)
    active                  = models.BooleanField(default=True)
    total_answers           = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'BlogPost'
        verbose_name_plural = 'BlogPosts'


class Answer(models.Model):
    user                    = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user_answers',
                                                related_name='answers')
    question                = models.ForeignKey(Question, on_delete=models.CASCADE)
    create_date             = models.DateTimeField(auto_now_add=True)
    update_date             = models.DateTimeField(auto_now=True)
    body                    = RichTextField(blank=True, null=True)
    code                    = RichTextField(blank=True, null=True)
    slug                    = models.CharField(max_length=255, blank=True, null=True)
    url                     = models.URLField(blank=True, null=True)
    imageUrl                = models.URLField(blank=True, null=True)
    audio_url               = models.URLField(blank=True, null=True)
    video_url               = models.URLField(blank=True, null=True)
    youtube_url             = models.URLField(blank=True, null=True)
    active                  = models.BooleanField(default=True)
    in_reply_to             = models.ForeignKey('self', null=True, related_name='replies', on_delete=models.CASCADE)
    chosen                  = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


class Vote(models.Model):
    user                  = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                                              verbose_name='user_vote', related_name='votes')
    question              = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True,
                                              verbose_name='question_vote', related_name='question_votes')
    answer                = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True,
                                              verbose_name='answer_vote', related_name='answers_votes')
    slug                  = models.CharField(max_length=255, blank=True, null=True)
    create_date           = models.DateTimeField(auto_now_add=True)
    update_date           = models.DateTimeField(auto_now=True)
    up                    = models.BooleanField(default=False)
    down                  = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'


class RatingModel(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True,
                                 verbose_name='rating_question',  related_name='rating_questions')
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('user', 'question'),)
        index_together = (('user', 'question'),)


pre_save.connect(slug_generator, sender=TagsQuestions)
pre_save.connect(slug_generator, sender=Question)
pre_save.connect(slug_generator, sender=BlogPost)
pre_save.connect(slug_related_question, sender=Answer)
pre_save.connect(slug_related_question, sender=Vote)

