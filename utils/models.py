from django.db import models


class Vacancy(models.Model):
    """Модель вакансии для парсинга данных с площадок."""

    title = models.CharField('Вакансия', max_length=200)  # noqa: WPS432
    description = models.TextField('Описание', blank=True)
    published_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    employer_type = models.CharField('Тип работодателя', max_length=200, blank=True)  # noqa: WPS432
    employer_name = models.CharField('Наименование работодателя', max_length=200, blank=True)  # noqa: WPS432
    location_city = models.CharField('Город', max_length=200, blank=True)  # noqa: WPS432
    location_country = models.CharField('Страна', max_length=200, blank=True)  # noqa: WPS432
    salary_currency = models.CharField('Валюта', max_length=200, blank=True)  # noqa: WPS432
    salary_value = models.DecimalField('Доход', max_digits=9, decimal_places=2, null=True, blank=True)
    salary_left_value = models.DecimalField('Доход мин', max_digits=9, decimal_places=2, null=True, blank=True)
    salary_right_value = models.DecimalField('Доход макс', max_digits=9, decimal_places=2, null=True, blank=True)
    job_format = models.CharField('Формат работы', max_length=200, blank=True)  # noqa: WPS432
    candidate_level = models.TextField('Уровень кандидата', blank=True)
    specialization = models.TextField('Специализация', blank=True)
    branch = models.TextField('Сфера применения', blank=True)
    source = models.TextField('Url', blank=True)
    source_id = models.CharField('ID вакансии', max_length=200, null=True, blank=True, unique=True)  # noqa: WPS432

    def __str__(self):
        """Вывод в админку."""
        return self.title

    class Meta:  # noqa: WPS306
        """Сортировка."""

        ordering = ['-published_at']
        verbose_name = 'вакансия'
        verbose_name_plural = 'вакансии'
