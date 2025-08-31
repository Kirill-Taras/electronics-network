from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Кастомный менеджер для пользователя.
    Отвечает за создание обычных юзеров и суперпользователей.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Создаём обычного пользователя.
        Email и пароль обязательны.
        """
        if not email:
            raise ValueError("У пользователя должен быть email")
        if not password:
            raise ValueError("Пароль обязателен")

        email = self.normalize_email(email)  # приведение email к нижнему регистру
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # шифруем пароль
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Создаём суперпользователя.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя.
    Основная авторизация идёт через email.
    """

    email = models.EmailField(unique=True, verbose_name="Почта")
    first_name = models.CharField(max_length=50, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=50, blank=True, verbose_name="Фамилия")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")

    # флаги для админки и прав
    is_active = models.BooleanField("Активен", default=True)
    is_staff = models.BooleanField("Доступ в админку", default=False)
    is_superuser = models.BooleanField("Суперпользователь", default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"  # вход по email
    REQUIRED_FIELDS = []  # обязательные при создании суперюзера кроме email/пароля

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
