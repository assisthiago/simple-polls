import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):

    def test_was_publshed_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)

        self.assertIs(old_question.was_published_recently(), False)

    def test_was_publshed_recently_with_recent_question(self):
        time = timezone.now()
        recent_question = Question(pub_date=time)

        self.assertIs(recent_question.was_published_recently(), True)

    def test_was_publshed_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nenhuma enquente disponível.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        create_question(question_text='Questão passada.', days=-30)
        response = self.client.get(reverse('polls:index'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Questão passada.>']
        )

    def test_future_question(self):
        create_question(question_text='Questão futura.', days=30)
        response = self.client.get(reverse('polls:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nenhuma enquente disponível.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_and_future_question(self):
        create_question(question_text='Questão passada.', days=-30)
        create_question(question_text='Questão futura.', days=30)
        response = self.client.get(reverse('polls:index'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Questão passada.>']
        )

    def test_two_past_question(self):
        create_question(question_text='Questão passada 1.', days=-30)
        create_question(question_text='Questão passada 2.', days=-5)
        response = self.client.get(reverse('polls:index'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Questão passada 2.>', '<Question: Questão passada 1.>']
        )


class QuestionDetailViewTests(TestCase):

    def test_past_question(self):
        past_question = create_question(question_text='Questão passada', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question)

    def test_future_question(self):
        future_question = create_question(question_text='Questão futura', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
