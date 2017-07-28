import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question
from django.urls import reverse
# Create your tests here.


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_qusetion = Question(pub_date=time)
        self.assertIs(recent_qusetion.was_published_recently(), True)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_questions(self):
        create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past question>'])

    def test_futuer_question(self):
        create_question(question_text="futuer question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_and_futuer_question(self):
        create_question(question_text="futuer question", days=30)
        create_question(question_text="past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: past question>'])

    def test_two_past_question(self):
        create_question(question_text="past question 1", days=-30)
        create_question(question_text="past question 2", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: past question 2>', '<Question: past question 1>'])

class QuestionDetailViewTests(TestCase):
    def test_futuer_question(self):
        futuer_question = create_question(question_text="Futuer Question",days=5)
        url = reverse("polls:detail",args=(futuer_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

    def test_old_question(self):
        old_question = create_question(question_text="Old Quesetion",days=-5)
        url = reverse("polls:detail",args=(old_question.id,))
        response = self.client.get(url)
        self.assertContains(response,old_question.question_text)

    def test_recent_question(self):
        recent_question = create_question(question_text="Recent Question",days=0)
        url = reverse('polls:detail',args=(recent_question.id,))
        response = self.client.get(url)
        self.assertContains(response,recent_question.question_text)