from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, JSONField, ValidationError

from materials.models import Section, Lesson, Examination, Answer, Question, Choice


class SectionSerializer(ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class SectionDetailsSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")

    class Meta:
        model = Section
        fields = "__all__"


class ChoiceSerializer(ModelSerializer):
    percent = SerializerMethodField()

    class Meta:
        model = Choice
        fields = ['pk', 'percent', 'title', 'points', 'lock_other']

    def get_percent(self, obj):
        total = Answer.objects.filter(question=obj.question).count()
        current = Answer.objects.filter(question=obj.question, choice=obj).count()
        if total != 0:
            return float(current * 100 / total)
        else:
            return float(0)


class QuestionSerializer(ModelSerializer):
    choices = ChoiceSerializer(many=True, source="choice_set",)

    class Meta:
        model = Question
        fields = ['pk', 'text', 'choices', 'max_points']


class AnswerSerializer(ModelSerializer):
    answers = JSONField()

    class Meta:
        model = Answer
        fields = "__all__"

    def validate_answers(self, answers):
        if not answers:
            raise ValidationError("Answers field cannot be empty")
        return answers

    def save(self):
        answers = self.data['answers']
        user = self.context.user
        for question_id in answers:
            question = Question.objects.get(pk=question_id)
            choices = answers[question_id]
            for choice_id in choices:
                choice = Choice.objects.get(pk=choice_id)
                Answer(user=user, question=question, choice=choice).save()
                user.is_answer = True
                user.save()
