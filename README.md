# Electronics Network
---

## 🕹️Проект
Это веб-приложение для управления сетью продаж электроники. Проект позволяет:

- Создавать иерархическую сеть из трёх уровней: **завод → розничная сеть → индивидуальный предприниматель (ИП)**.  
- Управлять продуктами каждого звена сети.  
- Отслеживать задолженность между звеньями сети.  
- Фильтровать и сортировать данные через API.  
- Контролировать доступ к API с помощью прав пользователей.  
- Вести учет через админ-панель Django.

---

## 💻Стек технологий

- **Python 3.8+**  
- **Django 3+**  
- **Django REST Framework 3.10+**  
- **PostgreSQL 10+**  
- **JWT-аутентификация** (`djangorestframework-simplejwt`)  
- **Swagger-документация** (`drf-yasg`)  
- **Django Filters** для фильтрации данных  

Дополнительно использованы: `python-dotenv` для хранения секретов, `pytest` / `unittest` для тестирования.


## Установка и запуск

Следуйте шагам ниже для локального запуска приложения.

### 1. Клонируем репозиторий

```bash
# клонируем репозиторий
git clone https://github.com/Kirill-Taras/electronics-network.git
# переходим в папку проекта
cd electronics-network
```

### 2. Создаем виртуальное окружение и активируем его
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Устанавливаем зависимости
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
### 4. Настраиваем переменные окружения
```bash
Создайте файл .env в корне проекта и заполните его:

SECRET_KEY=<ваш_секретный_ключ>
DEBUG=True
DB_NAME=<имя_базы>
DB_USER=<пользователь>
DB_PASSWORD=<пароль>
DB_HOST=127.0.0.1
DB_PORT=5432
```

⚠️ Для работы проекта необходима локальная или удалённая PostgreSQL база.

### 5. Применяем миграции
```bash
python manage.py migrate
```
### 6. Создаём суперпользователя
```bash
python manage.py createsuperuser
```
Следуйте инструкциям (email, пароль).
### 7. Запускаем сервер
```bash
python manage.py runserver
```
Сервер будет доступен по адресу: http://127.0.0.1:8000

### 8. Доступ к API и документации
```bash

Swagger: http://127.0.0.1:8000/swagger/
Redoc: http://127.0.0.1:8000/redoc/
```

**API защищён JWT-аутентификацией. Для запросов используйте токен суперпользователя или активного сотрудника.**

Важно, чтобы пользователь имел доступ к API:
```bash
is_active = True → пользователь активен
is_staff = True → сотрудник/доступ к админке
```
Без этих флагов пользователь не сможет работать с API.

### Пример создания пользователя через Django shell
```bash
from users.models import CustomUser

user = CustomUser.objects.create_user(
    email="employee@example.com",
    password="strongpassword",
    is_active=True,
    is_staff=True
)
```

**Автор проекта** 

🧑‍💼 Разработчик Кирилл Тарасов