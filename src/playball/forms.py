from __future__ import unicode_literals

import re

from django import forms
from django.forms import TextInput
from django.utils.translation import ugettext_lazy as _

from .models import Entry


only_letters = re.compile(r'^[a-z A-Z \']{2,}$')


class EntryForm(forms.ModelForm):
    """
    Handles ensuring that the exceptable inputs are valid. First name and 
    last name are first letter capitalized only and not unique together 
    duplicated names. Verify the first 5 numbers range from 1-69 without 
    duplicates and the 6th number range from 1-26.
    """

    class Meta:
        model = Entry
        fields = (
            'first_name', 
            'last_name', 
            'first_favorite',
            'second_favorite', 
            'third_favorite', 
            'fourth_favorite',
            'fifth_favorite', 
            'power_ball_number'
        )

    def __init__(self, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        self.initial_list = []
        self.correction_needed = False

    def check_dups_and_range(self, clean_d_entry, initial_input=False):
        """
        Handles checking for duplicated entries numbers 1 - 5.
        """
        if not 1 <= clean_d_entry <= 69:
            self.correction_needed = True
            raise forms.ValidationError(_(
                "Enter a valid number between 1 through 69.")
        )
        if initial_input:
            self.initial_list = []
            self.initial_list.append(clean_d_entry)
        else:
            if clean_d_entry not in self.initial_list:
                self.initial_list.append(clean_d_entry)
            else:
                self.correction_needed = True
                raise forms.ValidationError(_(
                    "No duplicates. Enter another number that you haven't \
                    already chosen.")
            )
        return clean_d_entry

    def check_name(self, name, title):
        """
        Handles ensuring entry uses only letter and is capitalized.
        """
        if not only_letters.search(name):
            self.correction_needed = True
            raise forms.ValidationError(_(
                'Enter a valid {} name. This value must contain only \
                letters.'.format(title))
        )
        return name.capitalize()

    def clean_first_name(self):
        """
        Handles validation.
        """
        return self.check_name(
            self.cleaned_data["first_name"], 
            "first"
        )

    def clean_last_name(self):
        """
        Handles validation.
        """
        return self.check_name(
            self.cleaned_data["last_name"], 
            "last"
        )

    def clean_first_favorite(self):
        """
        Handles ensuring entry is a number and verifies entry agianst 
        duplication.
        """
        return self.check_dups_and_range(
            self.cleaned_data["first_favorite"],
            initial_input=True
        )

    def clean_second_favorite(self):
        """
        Handles ensuring entry is a number and verifies entry agianst 
        duplication.
        """
        return self.check_dups_and_range(
            self.cleaned_data["second_favorite"]
        )

    def clean_third_favorite(self):
        """
        Handles ensuring entry is a number and verifies entry agianst 
        duplication.
        """
        return self.check_dups_and_range(
            self.cleaned_data["third_favorite"]
        )

    def clean_fourth_favorite(self):
        """
        Handles ensuring entry is a number and verifies entry agianst 
        duplication.
        """
        return self.check_dups_and_range(
            self.cleaned_data["fourth_favorite"]
        )

    def clean_fifth_favorite(self):
        """Handles ensuring entry is a number and verifies entry agianst 
        duplication.
        """
        return self.check_dups_and_range(
            self.cleaned_data["fifth_favorite"]
        )

    def clean_power_ball_number(self):
        """
        Handles ensuring entry is a number.
        """
        power_ball = self.cleaned_data["power_ball_number"]
        if not 1 <= power_ball <= 26:
            self.correction_needed = True
            raise forms.ValidationError(_(
                'Enter a valid number between 1 through 26.')
        )
        return power_ball

    def clean(self):
        cleaned_data = super(EntryForm, self).clean()
        if self.correction_needed:
            raise forms.ValidationError(_(
                'There are errors in the form, please correct and re-submit'
                )
            )
