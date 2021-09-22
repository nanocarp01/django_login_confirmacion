from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, validate_comma_separated_integer_list, MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _

# Exercise
class Exercise(models.Model):
    exercise_id = models.IntegerField(default=-1, unique=True, null=False, blank=False)
    name = models.CharField(max_length=200, unique=False, null=False, blank=False)
    description = models.CharField(max_length=200, unique=False, null=False, blank=False)
    default_value = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    
    EXERCISE_CATEGORY = [
        (0, _('Shoulders')),
        (1, _('Back')),
        (2, _('Biceps')),
        (3, _('Triceps')),
        (4, _('Chest')),
        (5, _('Core')),
        (6, _('Gluteus')),
        (7, _('Quadriceps')),
        (8, _('Hamstring')),
        (9, _('Cardio')),
        (10, _('Lumbar')),
        (11, _('Grip')),
    ]
    category_id = models.PositiveSmallIntegerField(default=1, choices=EXERCISE_CATEGORY, null=False, blank=False)

    EXERCISE_LEVEL = [
        (0, 'N1'),
        (1, 'N2'),
        (2, 'RX'),
        (3, 'RX+'),
    ]
    level = models.PositiveSmallIntegerField(default=0, choices=EXERCISE_LEVEL, null=False, blank=False)
    url = models.URLField()
    is_metabolic = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        return_value = str(self.name) + ' [' + str(self.get_category_id_display()) + '] [' + str(self.get_level_display() + ']')
        return return_value


# Routine
class Routine(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    # Each routine has 10 exercises separated by ,: 1,2,3,4,5,6,7,8,9,10
    exercise_ids = models.CharField(validators=[validate_comma_separated_integer_list], max_length=512, blank=True, null=False)
    exercise_repetitions = models.CharField(validators=[validate_comma_separated_integer_list], max_length=512, blank=True, null=False)
    rounds = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(4)])
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    # There are 10 exercise categories, percentages are separated by ,: 1,2,3,4,5,6,7,8,9,10
    percentages = models.CharField(validators=[validate_comma_separated_integer_list], max_length=512, blank=False, null=False)
    level = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return str(self.date)
