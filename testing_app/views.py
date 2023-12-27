from django.contrib.auth.views import LogoutView
from django.urls import get_resolver
from django.views import View
from rest_framework import generics, permissions
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from testing_app.models import StudentTest, Question, Test
from testing_app.serializers import StudentTestSerializer, SubmitStudentTestSerializer, QuestionSerializer, \
    TestSerializer

class ListAllUrlsView(View):
    def get(self, request, *args, **kwargs):
        url_patterns = get_resolver().url_patterns
        url_list = [pattern.pattern for pattern in url_patterns]
        return render(request, 'list_all_urls.html', {'url_list': url_list})

class TestAPIView(generics.RetrieveAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class SubmitTestAPIView(generics.UpdateAPIView):
    queryset = StudentTest.objects.all()
    serializer_class = StudentTestSerializer

    def update(self, request, *args, **kwargs):
        student_test = self.get_object()
        provided_answers = request.data.get('answers')
        student_test.evaluate_test(provided_answers)

        return Response({'score': student_test.score, 'completed': student_test.completed}, status=status.HTTP_200_OK)

class TestList(generics.ListCreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]

class TestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]

class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

class StudentTestList(generics.ListCreateAPIView):
    queryset = StudentTest.objects.all()
    serializer_class = StudentTestSerializer
    permission_classes = [IsAuthenticated]

class StudentTestDetail(generics.RetrieveUpdateAPIView):
    queryset = StudentTest.objects.all()
    serializer_class = StudentTestSerializer
    permission_classes = [IsAuthenticated]

class SubmitStudentTestView(generics.UpdateAPIView):
    queryset = StudentTest.objects.all()
    serializer_class = SubmitStudentTestSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentTestDeleteView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        try:
            student_test = StudentTest.objects.get(pk=pk)
            student_test.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except StudentTest.DoesNotExist:
            return Response({"detail": "StudentTest not found"}, status=status.HTTP_404_NOT_FOUND)


class TestDeleteView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        try:
            test = Test.objects.get(pk=pk)
            test.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Test.DoesNotExist:
            return Response({"detail": "Test not found"}, status=status.HTTP_404_NOT_FOUND)

class UserDeleteView(APIView):
    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        # Ваша логика перед удалением токена, если необходимо
        response = super().post(request, *args, **kwargs)
        # Ваш код после удаления токена, если необходимо
        return response

class TestDetailView(RetrieveAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]