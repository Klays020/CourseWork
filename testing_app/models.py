from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField

class Test(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Question(models.Model):
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class AnswerOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class StudentTest(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    score = models.IntegerField(null=True, blank=True)
    answers = JSONField(null=True)

    def update_student_answers(self, provided_answers):
        print("update_student_answers: Before Update - answers:", self.answers)

        if self.answers:
            self.answers.update(provided_answers)
        else:
            self.answers = provided_answers

        print("update_student_answers: After Update - answers:", self.answers)
        self.save()


    def save_student_answers(self, provided_answers):
        print("Saving student answers")
        # Обработка и сохранение ответов студента
        self.answers = provided_answers
        self.completed = True  # Помечаем тест как завершенный
        self.save()