from __future__ import unicode_literals

import random
import operator

from django.db import models
from django.db.models.signals import pre_save
from django.shortcuts import get_object_or_404
from django.utils.text import slugify


def pick_random_balls(fav_list):
    """
    Used in the event of less than 5 duplicate ball selection.
    """
    exempt_nums = [num for num in fav_list]
    while len(fav_list) < 5:
        random_num = random.choice(range(1, 70))
        if random_num not in exempt_nums:
            fav_list.append(random_num)
            exempt_nums.append(random_num)
    return fav_list


def most_popular_balls(balls):
    """
    Sorts and possibly randomly selects highest ranking duplicate balls.
    """
    luckiest_list = []
    temp_list_of_equals = []
    for num in balls:
        if num[1] > 1 and len(luckiest_list) < 5:           
            if len(temp_list_of_equals) == 0 or temp_list_of_equals[0][1] == num[1]:
                temp_list_of_equals.append(num)
            else:
                if len(temp_list_of_equals) + len(luckiest_list) <= 5:
                    luckiest_list += [ball[0] for ball in temp_list_of_equals]
                    temp_list_of_equals = []
                    temp_list_of_equals.append(num)
    if len(temp_list_of_equals) > 0:
        temp_list_of_balls = [ball[0] for ball in temp_list_of_equals]
        while len(luckiest_list) < 5:
            if temp_list_of_balls:
                random_pick = random.choice(temp_list_of_balls)
                luckiest_list.append(random_pick)
                temp_list_of_balls.remove(random_pick)
            else:
                return sorted(pick_random_balls(luckiest_list))
        return sorted(luckiest_list)
    else:
        return sorted(pick_random_balls(luckiest_list))


def most_popular_powerball(powerballs, occurences=None):
    """
    Sorts and possibly randomly selects the highest ranking duplicate 
    powerball.
    """
    popular_powerballs = []
    for ball in powerballs:
        if ball[1] > 1:
            if occurences == None or ball[1] == occurences:
                popular_powerballs.append(ball[0])
                occurences = ball[1]
    if len(popular_powerballs) > 0:
        return random.choice(popular_powerballs)
    return random.choice(range(1, 27))


class PopularSelection(models.Model):
    """
    Stores the most recently calculated popular choice. This is required 
    so that this selection is saved after each entry and not able to 
    recalculate by refreshing the browser.
    """
    current_most_popular = models.CharField(max_length=80)

    def __str__(self):
        return self.current_most_popular       


class Entry(models.Model):
    """All Entry data"""
    slug = models.SlugField()
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    first_favorite = models.PositiveSmallIntegerField()
    second_favorite = models.PositiveSmallIntegerField()
    third_favorite = models.PositiveSmallIntegerField()
    fourth_favorite = models.PositiveSmallIntegerField()
    fifth_favorite = models.PositiveSmallIntegerField()
    power_ball_number = models.PositiveSmallIntegerField(verbose_name='Powerball')


    class Meta:
        ordering = ["last_name", "first_name"]
        unique_together = ("first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super(Entry, self).__init__(*args, **kwargs)
        self.all_favorite_balls = {}
        self.all_powerballs = {}
        self.labels = [
            self.first_name,
            self.last_name,
            self.first_favorite, 
            self.second_favorite, 
            self.third_favorite, 
            self.fourth_favorite,
            self.fifth_favorite,
            self.power_ball_number
        ]

    def __str__(self):
        return "{n[0]} {n[1]}:  {d[0]} {d[1]} {d[2]} {d[3]} {d[4]} and Powerball {p[0]}".format(
                n=self.labels[:2],
                d=sorted(self.labels[2:7]),
                p=self.labels[7:]
        )

    def save(self, *args, **kwargs):
        super(Entry, self).save(*args, **kwargs)
        # now update the most popular number selection based on duplicate 
        # popularity and store it to PopularSelection
        fields=(
            'first_favorite',
            'second_favorite',
            'third_favorite',
            'fourth_favorite',
            'fifth_favorite'
        )
        for entry in Entry.objects.all():
            for identifier in fields:
                fav_selction = getattr(entry, identifier)
                if fav_selction in self.all_favorite_balls:
                    self.all_favorite_balls[fav_selction] += 1
                else:
                    self.all_favorite_balls.update({fav_selction: 1})
            if entry.power_ball_number in self.all_powerballs:
                self.all_powerballs[entry.power_ball_number] += 1
            else:
                self.all_powerballs.update({entry.power_ball_number: 1})
        balls, powerballs = (
            sorted(
                self.all_favorite_balls.items(),
                key=operator.itemgetter(1), 
                reverse=True
            ),
            sorted(
                self.all_powerballs.items(), 
                key=operator.itemgetter(1), 
                reverse=True
            )
        )
        selection = "{d[0]} {d[1]} {d[2]} {d[3]} {d[4]} and Powerball {p}".format(
            d=most_popular_balls(balls),
            p=most_popular_powerball(powerballs)
        )
        try:
            popular_selection = get_object_or_404(PopularSelection, pk=1)
        except:
            popular_selection = PopularSelection.objects.create(current_most_popular="")
        popular_selection.current_most_popular = "{}".format(selection)
        popular_selection.save()

def pre_save_entry(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.first_name + instance.last_name)

pre_save.connect(pre_save_entry, sender=Entry)
