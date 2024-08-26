from django.db import models

from users.models import User


class Section(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Создатель",
        help_text="Введите создателя раздела",
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название раздела",
        help_text="Введите название раздела",
    )
    description = models.TextField(
        verbose_name="Описание раздела",
        help_text="Введите описание раздела",
        blank=True,
        null=True,
    )
    img = models.ImageField(
        upload_to="materials/Section",
        blank=True,
        null=True,
        verbose_name="Превью раздела",
        help_text="Добавьте превью раздела",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"


class Lesson(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Создатель",
        help_text="Введите создателя урока",
        null=True,
        blank=True,
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        verbose_name="Раздел",
        help_text="Введите к какому разделу относится урок",
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        verbose_name="Описание урока",
        help_text="Введите описание урока",
        blank=True,
        null=True,
    )
    img = models.ImageField(
        upload_to="materials/Lesson",
        blank=True,
        null=True,
        verbose_name="Превью урока",
        help_text="Добавьте превью урока",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Examination(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Создатель",
        help_text="Введите создателя теста",
        null=True,
        blank=True,
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Урок",
        help_text="Введите к какому уроку относится тестирование знаний",
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название тестирования",
        help_text="Введите название тестирования",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тестирование знаний"
        verbose_name_plural = "Тестирования знаний"


class Question(models.Model):
    examination = models.ForeignKey(
        Examination,
        on_delete=models.CASCADE,
        verbose_name="Тестирование знаний",
        help_text="Введите к какому тестированию знаний относится вопрос",
    )
    text = models.TextField(
        verbose_name="Вопрос",
        help_text="Введите вопрос",
    )
    max_points = models.FloatField()
    visible = models.BooleanField(default=False)

    def __str__(self):
        return f"Question: {self.text}"

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255)
    points = models.FloatField()
    lock_other = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Выбор"
        verbose_name_plural = "Выборы"


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    choice = models.ForeignKey(Choice, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.choice.title

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
