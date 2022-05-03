from django.db import models
from django.contrib.auth.models import User


class Vacancy(models.Model):

    title = models.CharField(max_length=50, verbose_name='Вакансия')
    specialty = models.ForeignKey('Specialty', on_delete=models.CASCADE, related_name="specialty",
                                  verbose_name='Специальность')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name="company", verbose_name='Компания')
    skills = models.TextField(verbose_name='Навыки')
    description = models.TextField(verbose_name='Описание')
    salary_min = models.IntegerField(verbose_name='Минимальня зарплата')
    salary_max = models.IntegerField(verbose_name='Максимальная зарплата')
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Вакансии'
        verbose_name = 'Вакансия'
        ordering = ['title']


class Company(models.Model):

    name = models.CharField(max_length=50, verbose_name='Компания')
    location = models.CharField(max_length=50, verbose_name='Город')
    logo = models.ImageField(upload_to='job_site_app/static/logo/', verbose_name='Лого')
    description = models.TextField(verbose_name='Информация о компании')
    employee_count = models.IntegerField(verbose_name='Количество сотрудников')
    owner = models.OneToOneField(User, null=True, on_delete=models.CASCADE,  related_name="owner",
                                 verbose_name='Владелец')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Компании'
        verbose_name = 'Компания'
        ordering = ['name']


class Specialty(models.Model):

    code = models.CharField(max_length=50, verbose_name='Специализация')
    title = models.CharField(max_length=50, verbose_name='Название')
    picture = models.ImageField(upload_to='job_site_app/static/picture/', verbose_name='Картинка')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Специальности'
        verbose_name = 'Специальность'
        ordering = ['title']


class Application(models.Model):

    written_username = models.CharField(max_length=50, verbose_name='Имя')
    written_phone = models.CharField(max_length=50, verbose_name='Телефон')
    written_cover_letter = models.TextField(verbose_name='Сопроводительное письмо')
    vacancy = models.ForeignKey('Vacancy', on_delete=models.CASCADE, related_name="applications",
                                verbose_name='Вакансия')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications", verbose_name='Пользователь')

    def __str__(self):
        return self.written_username

    class Meta:
        verbose_name_plural = 'Отклики'
        verbose_name = 'Отклик'
        ordering = ['written_username']


class Resume(models.Model):

    owner = models.OneToOneField(User, null=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(max_length=50, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    STATUS = (
        ('not_looking', 'Не ищу работу'),
        ('considering', 'Рассматриваю предложения'),
        ('looking', 'Ищу работу'),
    )
    GRADE = (
        ('intern', 'Стажер'),
        ('junior', 'Джуниор'),
        ('middle', 'Миддл'),
        ('senior', 'Синьор'),
        ('lead', 'Лид'),
    )
    status = models.CharField(max_length=50, choices=STATUS)
    salary = models.IntegerField(verbose_name='Вознаграждение')
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name="resumes",
                                  verbose_name='Специализация')
    grade = models.CharField(max_length=50, choices=GRADE)
    education = models.TextField(verbose_name='Образование')
    experience = models.TextField(verbose_name='Опыт работы')
    portfolio = models.URLField()
