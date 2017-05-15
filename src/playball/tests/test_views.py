import unittest

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.messages.api import get_messages
from django.core.urlresolvers import reverse
from django.test import RequestFactory
from test_plus.test import TestCase

from playball.tests.test_models import EntryTest
from playball.views import EntryCreateView, PopularSelection


class EntryViewMessageTestCase(unittest.TestCase):

    def test_get(self):       
        popular_selection = PopularSelection.objects.create(current_most_popular="trial")
        request = RequestFactory().get('/fake-path')
        view = EntryCreateView.as_view(template_name='homepage.html')
        response = view(
            request, 
            first_name="George", 
            last_name="Lane", 
            first_favorite=45, 
            second_favorite=23, 
            third_favorite=67,
            fourth_favorite=2,
            fifth_favorite=3,
            power_ball_number=25
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'homepage.html')
        self.assertEqual(response.context_data['current_most_popular'], "trial")
        self.assertEqual(get_messages(response), [])


class MyTests(TestCase):

    def test_context_data(self):
        response = self.post(
            "playball:entry_create", 
            data={
                'first_name': 'George',
                'last_name': 'Lane',
                'first_favorite': 45,
                'second_favorite': 23,
                'third_favorite': 67,
                'fourth_favorite': 2,
                'fifth_favorite': 3,
                'power_ball_number': 25
            },
            extra={
                'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'
            }
        )


class EntryViewTest(EntryTest):

    def test_form_view(self):
        w = self.create_entry()
        url = reverse("playball:entry_create")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_list_view(self):
        w = self.create_entry()
        w.save()
        another_w = self.create_entry_second()
        another_w.save()
        yet_another_w = self.create_entry_third()
        yet_another_w.save()
        url = reverse("playball:entry_list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_popular_view(self):
        w = self.create_entry()
        url = reverse("playball:popular_entry")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
