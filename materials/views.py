from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView, GenericAPIView,
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from materials.models import Section, Lesson, Question
from materials.paginators import BasePagination
from users.permissions import IsAdmin, IsOwner, IsTeacher
from materials.serializers import (
    SectionSerializer,
    SectionDetailsSerializer,
    LessonSerializer, QuestionSerializer, AnswerSerializer,
)


class SectionViewSet(ModelViewSet):
    queryset = Section.objects.all()
    pagination_class = BasePagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SectionDetailsSerializer
        return SectionSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]
        elif self.action == "retrieve":
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsOwner | IsAdmin]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = BasePagination


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsAdmin]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsAdmin]


class GetQuestion(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer

    def get(self, request, format=None):
        questions = Question.objects.filter(visible=True,)
        last_point = QuestionSerializer(questions, many=True)
        return Response(last_point.data)


class QuestionAnswer(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AnswerSerializer

    def post(self, request, format=None):
        answer = AnswerSerializer(data=request.data, context=request)
        if answer.is_valid(raise_exception=True):
            answer.save()
            return Response({'result': 'OK'})
