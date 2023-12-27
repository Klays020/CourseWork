from django.contrib import admin
from django import forms
from .models import Test, Question, StudentTest, AnswerOption

class AnswerOptionForm(forms.ModelForm):
    class Meta:
        model = AnswerOption
        fields = '__all__'
        widgets = {
            'correct': forms.RadioSelect(),
        }

class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerOptionInline]

admin.site.register(Test)
admin.site.register(Question, QuestionAdmin)
admin.site.register(StudentTest)
admin.site.register(AnswerOption)
