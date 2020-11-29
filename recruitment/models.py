from django.db import models


class Language(models.Model):
    """Модель языков."""

    name = models.CharField(max_length=200)  # noqa: WPS432
    level = models.CharField(max_length=200)  # noqa: WPS432

    def __str__(self):
        """Вывод в консоль."""
        return self.name


class Candidate(models.Model):
    """Модель кандидатов с резюме."""

    gender = models.CharField(max_length=200, blank=True)  # noqa: WPS432
    age = models.PositiveIntegerField(blank=True)
    city = models.CharField(max_length=200, blank=True)  # noqa: WPS432
    ready_to_move = models.TextField(blank=True)
    title = models.TextField()
    salary = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    branch = models.TextField(blank=True)
    spec = models.TextField(blank=True)
    type_of_work = models.TextField(blank=True)
    work_schedule = models.TextField(blank=True)
    total_work_exp = models.PositiveIntegerField(null=True, blank=True)
    last_employee = models.TextField(blank=True)
    last_job_title = models.TextField(blank=True)
    last_job_responsibilities = models.TextField(blank=True)
    last_job_time = models.PositiveIntegerField(null=True, blank=True)
    skills = models.TextField(blank=True)
    about_candidate = models.TextField(blank=True)
    education = models.TextField(blank=True)
    language = models.ManyToManyField(
        Language,  # noqa: WPS318
        related_name='candidates',
        blank=True,
    )
    source = models.TextField(blank=True)
    source_id = models.CharField(max_length=200, blank=True, unique=True)  # noqa: WPS432

    def __str__(self):
        """Вывод в консоль."""
        return self.title

    class Meta:  # noqa: WPS306
        """Сортировка."""

        ordering = ['salary']
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'


class HardRequirements(models.Model):
    """Модель хард скиллов."""

    name = models.CharField(verbose_name='Хард скилл', max_length=250)  # noqa: WPS432

    def __str__(self):
        """Вывод в консоль."""
        return self.name

    class Meta:  # noqa: WPS306
        """Сортировка и подробный вывод."""

        verbose_name = 'Хард скилл'
        verbose_name_plural = 'Хард скилы'


class SoftRequirements(models.Model):
    """Модель софтскилов."""

    name = models.CharField(verbose_name='Софт скилл', max_length=250)  # noqa: WPS432

    def __str__(self):
        """Вывод в консоль."""
        return self.name

    class Meta:  # noqa: WPS306
        """Сортировка и подробный вывод."""

        verbose_name = 'Софт скилл'
        verbose_name_plural = 'Софт скилы'


class Specialization(models.Model):
    """Модель со специализациями."""

    name = models.CharField(verbose_name='Специализация', max_length=250)  # noqa: WPS432

    def __str__(self):
        """Вывод в консоль."""
        return self.name

    class Meta:  # noqa: WPS306
        """Сортировка и подробный вывод."""

        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'


class Level(models.Model):
    """Модель уровней должности."""

    name = models.CharField(verbose_name='Уровень должности', max_length=200)  # noqa: WPS432

    def __str__(self):
        """Вывод в консоль."""
        return self.name

    class Meta:  # noqa: WPS306
        """Сортировка и подробный вывод."""

        verbose_name = 'Уровень должности'
        verbose_name_plural = 'Уровень должности'


class VacancyRequest(models.Model):
    """Модель вакансий заказчика."""

    title = models.CharField(verbose_name='Название вакансии', max_length=250)  # noqa: WPS432
    level = models.ForeignKey(
        Level,
        on_delete=models.DO_NOTHING,
        related_name='vacancies_requests',
        verbose_name='Уровень',
    )
    teaser = models.TextField(verbose_name='О компании и вакансии', blank=True)
    description = models.TextField(verbose_name='Описание вакансии', blank=True)
    location_city = models.CharField(verbose_name='Город', max_length=250, blank=True)  # noqa: WPS432
    location_country = models.CharField(verbose_name='Страна', max_length=250, blank=True)  # noqa: WPS432
    hard_requirements = models.ManyToManyField(
        HardRequirements,
        related_name='vacancies_requests',
        verbose_name='Требования',
        blank=True,
    )
    soft_requirements = models.ManyToManyField(
        SoftRequirements,
        related_name='vacancies_requests',
        verbose_name='Софт скилы',
        blank=True,
    )
    working_conditions = models.TextField(verbose_name='Условия работы', blank=True)
    salary_min = models.DecimalField(verbose_name='Доход от:', null=True, max_digits=9, decimal_places=2)
    salary_max = models.DecimalField(verbose_name='Доход до:', null=True, max_digits=9, decimal_places=2)
    job_format = models.TextField(verbose_name='Формат работы', blank=True)
    specialization = models.ManyToManyField(
        'Specialization',
        related_name='vacancies_requests',
        verbose_name='Специализация',
        blank=True,
    )
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    published_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)

    def __str__(self):
        """Вывод в консоль."""
        return self.title

    class Meta:  # noqa: WPS306
        """Сортировка и подробный вывод."""

        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
