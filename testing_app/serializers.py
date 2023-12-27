from rest_framework import serializers
from .models import Test, Question, StudentTest, AnswerOption
from django.db.models import JSONField

class SubmitStudentTestSerializer(serializers.Serializer):
    answers = serializers.JSONField()

    def update(self, instance, validated_data):
        instance.answers = validated_data.get('answers', instance.answers)
        instance.save()
        return instance
class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id', 'text', 'correct']

class QuestionSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'test', 'options']

    def to_representation(self, instance):
        user = self.context['request'].user
        is_admin = user.is_authenticated and user.is_staff
        is_student = user.is_authenticated and not user.is_staff

        data = super(QuestionSerializer, self).to_representation(instance)

        if is_student:
            data['options'] = [
                {key: value for key, value in option.items() if key != 'correct'}
                for option in data['options']
            ]

        return data

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'name', 'description', 'questions']


class StudentTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentTest
        fields = ['id', 'student', 'test', 'answers', 'completed', 'score']

