import datetime
from django.test import TestCase
from django.utils import timezone

from .models import Question

# Testing.
# Models
# Views

class QuestionModelTests(TestCase):

    def setUp(self) -> None:
        self.question =  Question(question_text="¿Quién es el mejor arquero del mundo?")

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time                     = timezone.now() + datetime.timedelta(days = 30)
        
        future_question          = self.question
        future_question.pub_date = time

        # self.assertIs(future_question.was_published_recently(), False)
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_present_questions(self):
        time                     = timezone.now() - datetime.timedelta(hours=23)
        
        present_question          = self.question
        present_question.pub_date = time

        # self.assertIs(present_question.was_published_recently(), False)
        self.assertTrue(present_question.was_published_recently())

    def test_was_published_recently_with_past_questions(self):
        time                     = timezone.now() - datetime.timedelta(days=1, minutes=1)
        
        past_question          = self.question
        past_question.pub_date = time

        # self.assertIs(past_question.was_published_recently(), False)
        self.assertFalse(past_question.was_published_recently())


    def test_was_published_recently_with_today_questions(self):
        time                     = timezone.now()
        
        past_question          = self.question
        past_question.pub_date = time

        # self.assertIs(past_question.was_published_recently(), False)
        self.assertTrue(past_question.was_published_recently())