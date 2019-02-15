from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver


GENDERS = (
          ('male', 'Male'),
          ('female', 'Female'),
)

LB = "LB"
KG = "KG"

WEIGHT_UNITS = [(KG, "Kilograms"), (LB, "Pounds")]

ACTIVITY_LEVELS = (
                   (1.25, 'Sedentary'),
                   (1.3, 'Lightly Active'),
                   (1.5, 'Moderately Active'),
                   (1.7, 'Very Active'),
                   (2.0, 'Extremely Active'),
)

SERVING_TYPES = (
                 ('ounce', 'Ounce'),
                 ('cup', 'Cup'),
                 ('pound', 'Pound'),
                 ('pint', 'Pint'),
                 ('tablespoon', 'Tablespoon'),
                 ('teaspoon', 'Teaspoon'),
                 ('gram', 'Gram'),
                 ('CUSTOM', 'CUSTOM'),
)

YES_NO_FLAGS = (
                ('Y', 'Y'),
                ('N', 'N'),
)



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    gender = models.CharField(max_length=7, choices=GENDERS)
    birthdate = models.DateField(null=True, blank=True)
    height_in_meters = models.FloatField(null=True)
    favorite_fitness_hobby = models.CharField(max_length=50, help_text="Basketball, Yoga, Dancing", blank=True)
    profile_image = models.ImageField(upload_to="user_profile", null=True, blank=True, height_field=None,
    width_field=None)
    goal = models.CharField(null=True, max_length=30, help_text="ex: Increase Lean Muscle, Lower Bodyfat, Improve Strength")

    def __unicode__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


class UserWeight(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField()
    weight = models.FloatField()
    unit = models.CharField(max_length=32, choices=WEIGHT_UNITS, default=KG)
    
    class Meta:
        unique_together = (("user", "date"),)
        ordering = ['user', '-date']

    def __unicode__(self):
        return self.user.username + ", " + self.date.strftime("%Y-%m-%d") + ", " + str(self.pounds)


class Food(models.Model):
    name = models.CharField(max_length=50)
    default_serving_type = models.CharField(max_length=20, choices=SERVING_TYPES)
    serving_type_qty = models.FloatField()
    calories = models.IntegerField()
    fat = models.FloatField()
    saturated_fat = models.FloatField()
    carbs = models.FloatField()
    fiber = models.FloatField()
    sugar = models.FloatField()
    protein = models.FloatField()
    sodium = models.FloatField()

    class Meta:
        db_table = 'foods'
        ordering = ['name']

    def __unicode__(self):
        return self.name + " - " + str(self.serving_type_qty) + " " + self.default_serving_type

class FoodEaten(models.Model):
    user = models.ForeignKey(User)
    food = models.ForeignKey(Food)
    date = models.DateField()
    serving_type = models.CharField(max_length=20, choices=SERVING_TYPES)
    serving_qty = models.FloatField()

    
    class Meta:
        verbose_name = "Food eaten"
        verbose_name_plural = "Foods eaten"
        unique_together = (("user", "food", "date"),)
        ordering = ['user', '-date']
    
    def __unicode__(self):
        return self.user.username + ", " + self.date.strftime("%Y-%m-%d") + " - " + self.food.name + " " + str(self.serving_qty) + " " + self.serving_type 
        

class Muscle(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Exercise(models.Model):
    name = models.CharField(max_length=250, unique=True)
    muscle_group = models.ManyToManyField(Muscle, blank=True)
    description = models.TextField(blank=True)
    upper_body = models.BooleanField(default=False, help_text="ex: Bench Press, Shoulder Press, Shrugs")
    lower_body = models.BooleanField(default=False, help_text="ex: Squats, Lunges, Deadlifts")
    is_explosive = models.BooleanField(default=False, help_text="ex: Hang Cleans, Box Jumps, Hang Snatch")
    is_cardio = models.BooleanField(default=False, help_text="ex: Jogging, Cycling, 110s")

    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

        
class ExercisePerformed(models.Model):
    user = models.ForeignKey(User)
    exercise = models.ForeignKey(Exercise)
    date = models.DateField()
    minutes = models.IntegerField(default=0, blank=True)
    repetitions = models.PositiveIntegerField(default=0, blank=True)
    weight = models.PositiveIntegerField(default=0, blank=True)
    unit = models.CharField(max_length=32, choices=WEIGHT_UNITS, default=KG)
    bodyweight = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Exercise performed"
        verbose_name_plural = "Exercises performed"
        unique_together = (("user", "exercise", "date"),)
        ordering = ['user', '-date']
    
    def __unicode__(self):
        return self.user.username + ", " + self.date.strftime("%Y-%m-%d") + " - " + self.exercise.name

