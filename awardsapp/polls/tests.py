from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question

class QuestionModelTests(TestCase):
    
    def setUp(self):
        self.question = Question(question_text = "¿Quien es el mejor Course Director de Platzi?")
    
    def test_was_published_recently_with_future_questions(self):
        """
        was_published_recently returns False for questions whose pub_date is in the future
        """
        time = timezone.now() + timedelta(days=30)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)
        
    def test_was_published_recently_with_present_questions(self):
        """
        was_published_recently returns True for questions whose pub_date is in the last 24hrs
        """
        time = timezone.now() - timedelta(hours=23)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), True)
        
    def test_was_published_recently_with_past_questions(self):
        """
        was_published_recently returns False for questions whose pub_date is older than 24hrs
        """
        time = timezone.now() - timedelta(days=1, minutes=1)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)


def create_question(questionText, days = 0, hours = 0, minutes = 0, seconds = 0):
    """_summary_
    Create a question with the given "question_text", and published the given number of
    days offset to now (negative for questions published in the past, positive for 
    questions that have yet to be published)
    
    Args:
        questionText (_type_): _description_ str question text
        days (_type_): _description_ days offset
    """
    time = timezone.now() + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    return Question.objects.create(question_text=questionText, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropiate message is displayed
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
        
    def test_no_future_questions_are_displayed(self):
        """
        If a future question is created in the database, this questions isn't shown until his pub_date is equal to the present time
        """
        create_question("Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
        
    def test_past_questions(self):
        """
        Questions with a pub_date in the past are displayed in the index page.
        """
        past_question = create_question("Past question", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question])
        
    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions are displayed
        """
        pastQuestion = create_question(questionText="Past Question", days=-30)
        futureQuestion = create_question(questionText="Future Question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [pastQuestion]
        )
    

    def test_two_past_questions(self):
        past_question1 = create_question(questionText="Past 1", days=-30)
        past_question2 = create_question(questionText="Past 2", days=-40)
        
        response = self.client.get(reverse("polls:index"))
        
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1, past_question2]
        )
        
        
    def test_two_future_questions(self):
        future_question1 = create_question(questionText="Future 1", days=30)
        future_question2 = create_question(questionText="Future 2", days=40)
        
        response = self.client.get(reverse("polls:index"))
        
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            []
        )
        
        
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pubdate in the future returns a 404 error not found
        """
        futureQuestion = create_question(questionText="Future Question", days=30)
        url = reverse("polls:detail", args=(futureQuestion.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past displays the question's text
        """
        pastQuestion = create_question(questionText="Past Question", days=-30)
        url = reverse("polls:detail", args=(pastQuestion.id,))
        response = self.client.get(url)
        self.assertContains(response, pastQuestion.question_text)