import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
import uuid


# Instructor model
class Instructor(models.Model):
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.username


# Learner model
class Learner(models.Model):
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'dba'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin')
    ]
    occupation = models.CharField(
    null=False,
    max_length=20,
    choices=OCCUPATION_CHOICES,
    default=STUDENT
    )
    social_link = models.URLField(max_length=200)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.username + "," + \
            self.occupation


# Course model
class Course(models.Model):
    name = models.CharField(null=False, max_length=30, default='online course')
    image = models.ImageField(upload_to='course_images/')
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='Enrollment')
    total_enrollment = models.IntegerField(default=0)
    is_enrolled = False

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


# Course instructors model
Class Course_instructor(models.Model)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor_id = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    
    def __str__(self):
        return "Course: " + self.course_id + "," + \
               "Instructor: " + self.instructor_id


# Lesson model
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    content = models.TextField()
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __str__(self):
        return "Lesson name: " + self.title


# Enrollment model
# <HINT> Once a user enrolled a class, an enrollment entry should be created between the user and course
# And we could use the enrollment to track information such as exam submissions
class Enrollment(models.Model):
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)
    AUDIT = 'audit'
    HONOR = 'honor'
    BETA = 'BETA'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
        (BETA, 'BETA')
    ]
    rating = models.FloatField(default=5.0)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    

class Question(models.Model):
    lesson_id = models.ManyToManyField(Lesson, through='Course')
    question_text = models.CharField(null=False,max_length=500)
    grade = models.IntegerField()
    choice = models.ManyToManyField(choice_id, through='submission_choices')

    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        if all_answers == selected_correct:
            return True
        else:
            return False


class Choice(models.Model):
    choice_text = models.CharField(null=False,max_length=100)
    is_correct = models.BooleanField()
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.enrollment)


class Submission_choices(models.Model):
    choice_id = models.ForeignKey(Choice)
    submission_id = models.ForeignKey(Submission)
    
    def __str__(self):
        return self.choice_id + self.submission_id
