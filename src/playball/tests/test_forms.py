from django.test import TestCase

from playball.forms import EntryForm
from playball.models import Entry


class EntryTests(TestCase):
    def test_entry(self):
        form_data={
	              'first_name': 'george',
	              'last_name': 'jakey',
	              'first_favorite': '1',
	              'second_favorite': '20',
	              'third_favorite': '56',
	              'fourth_favorite': '23',
	              'fifth_favorite': '43',
	              'power_ball_number': '12',
		}
        form = EntryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_entry_1(self):
        form_data={
	              'first_name': 'George',
	              'last_name': 'Jakey',
	              'first_favorite': 1,
	              'second_favorite': 20,
	              'third_favorite': 56,
	              'fourth_favorite': 23,
	              'fifth_favorite': 43,
	              'power_ball_number': 23,
		}
        form = EntryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_entry_2(self):
        form_data={
	              'first_name': 'George',
	              'last_name': 'Jakey',
	              'first_favorite': 0,
	              'second_favorite': 20,
	              'third_favorite': 56,
	              'fourth_favorite': 23,
	              'fifth_favorite': 43,
	              'power_ball_number': 23,
		}
        form = EntryForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_entry_3(self):
        form_data={
	              'first_name': 'George',
	              'last_name': 'Jakey',
	              'first_favorite': 70,
	              'second_favorite': 20,
	              'third_favorite': 56,
	              'fourth_favorite': 23,
	              'fifth_favorite': 43,
	              'power_ball_number': 23,
		}
        form = EntryForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_entry_4(self):
        form_data={
	              'first_name': 'George',
	              'last_name': 'Jakey',
	              'first_favorite': 7,
	              'second_favorite': 20,
	              'third_favorite': 56,
	              'fourth_favorite': 23,
	              'fifth_favorite': 43,
	              'power_ball_number': 27,
		}
        form = EntryForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_entry_5(self):
        form_data={
	              'first_name': 'George',
	              'last_name': 'Jakey',
	              'first_favorite': 7,
	              'second_favorite':"george",
	              'fourth_favorite': 23,
	              'fifth_favorite': 43,
	              'power_ball_number': 27,
		}
        form = EntryForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_entry_6(self):
        form_data={
	              'first_name': '32',
	              'last_name': 'Jakey',
	              'first_favorite': 7,
	              'second_favorite':41,
	              'fourth_favorite': 23,
	              'fifth_favorite': 43,
	              'power_ball_number': 27,
		}
        form = EntryForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_entry_7(self):
        form_data={
	              'first_name': 'George',
	              'last_name': 'Jakey',
	              'first_favorite': 7,
	              'second_favorite':41,
	              'fourth_favorite': 41,
	              'fifth_favorite': 43,
	              'power_ball_number': 27,
		}
        form = EntryForm(data=form_data)
        self.assertFalse(form.is_valid())
