import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse

from .models import Question

# Testing.
# Models
# Views

def create_question(question_text, days):
    """
    Create a question with the given question_text and published at the given numbers of days 
    offset to now (negative for questions in the past, positive for the ones in the future)
    """
    time              = timezone.now() + datetime.timedelta(days = days)
    question          = Question.objects.create(question_text    = question_text)
    question.pub_date = time
    return question

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

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """If no question exist, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])




    def test_questions_with_no_future_pub_date(self):
        """Questions with date greater to timezone.now shouldn't be displayed"""

        future_question = create_question("¿Quién es el mejor Course Director de Platzi?", days=30)

        response = self.client.get(reverse('polls:index'))

        self.assertContains(response, "No polls are available")
        # self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_two_future_questions(self):
            """ The questions arent displayed in the index view"""
            future_question1 = create_question("Future Question 1", 25)
            future_question2 = create_question("Future Question 2", 15)
            response = self.client.get(reverse("polls:index"))
            self.assertContains(response, "No polls are available.")
            self.assertQuerysetEqual(
                response.context["latest_question_list"], [])
            



class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        return a 404 error not found
        """
        future_question = create_question(question_text="Future question", days=30)
        url = reverse("polls:detail", args=[future_question.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displayed the question's text
        """
        past_question = create_question(question_text="past question", days=-30)
        url = reverse("polls:detail", args=[past_question.id])
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)