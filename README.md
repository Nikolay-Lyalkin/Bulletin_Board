**Описание проекта**

Проект "Bulletin board" предназначен для размещения на сайте объявлений о продаже товаров.

Модель "user" имеет обязательные поля: username, email, first_name, last_name.
Модель "advertisement" принимает на вход: title(название товара), description(описание товара), price(цена).
Модель "comment" принимает на вход: text(cодержание отзыва), ad(товар под которым оставлен отзыв)
Размещать объявления и оставлять комментарии имеет право только авторизованный пользователь.


**Инструкция по запуску docker-compose.yml**

*Описание сервисов*

web:
- Создает контейнер веб-приложения, используя Dockerfile в текущем каталоге.
- Предоставляет доступ к HTTP-трафику через порт 8000.
- Подключает текущий каталог к контейнеру.
- web сервис запускается после сервиса db.
- Загружает переменные среды из файла .env.

db:
- Использует официальный образ PostgreSQL версии 16.
- Данные сохраняются в именованном томе postgres_data, расположенном по адресу /var/lib/postgresql/data.
- Загружает переменные среды из файла .env для настройки.

redis:
- Запускает официальный образ Redis версии 7.4.
- Открывает доступ к серверу Redis через порт 6379.
- Сохраняет данные Redis в локальном каталоге (например, ./redis/data).
- Загружает переменные среды из файла .env

Volumes:
- postgres_data: Сохраняет данные базы данных PostgreSQL.
- static_volume: Используется для обработки статических файлов из приложения, гарантируя, что они не будут потеряны между перезапусками контейнера.

Запуск:

Создайте env-файл:

Убедитесь, что в корневом каталоге создан env-файл с необходимыми переменными среды как для веб-сервисов, так и для сервисов базы данных.

- POSTGRES_DB=
- POSTGRES_USER=
- POSTGRES_PASSWORD=
- DATABASE_HOST=
- DATABASE_PORT=

- EMAIL_HOST=
- EMAIL_PORT=
- EMAIL_HOST_USER=
- EMAIL_HOST_PASSWORD=
- EMAIL_USE_TLS=True
- EMAIL_SENDER=
- EMAIL_USE_SSL=False

Создайте и запустите сервисы:

Выполните следующую команду для создания и запуска всех служб, как определено в файле docker-compose.yml:
docker-compose up --build


**Пояснение к файлу Dockerfile**

Предоставленный файл Dockerfile определяет среду для приложения Python:

- Базовый образ: приложение использует python:3.11.9 в качестве базового образа.
- Установка Poetry: он устанавливает Poetry, менеджер зависимостей для Python.
- Переменные среды: для установки зависимостей непосредственно в контейнер задается значение POETRY_VIRTUALENVS_CREATE=false.
- Рабочий каталог: в качестве рабочего каталога задается значение /code.
- Копирование файлов проекта: копируются pyproject.toml и poetry.lock файлы в контейнере и устанавливает зависимости, не включая корневой пакет.
- Заключительная копия: копирует остальной код приложения в контейнер.
- Команда: указывает команду для запуска сервера Django на порту 8000, что делает его доступным из-за пределов контейнера.


**Конвейер Django CI/CD**

Этот репозиторий содержит конфигурацию непрерывной интеграции (CI) для приложения Django, использующего GitHub Actions. Конвейер CI включает в себя три основные задачи: тестирование, создание образа Docker и развертывание на сервере.

Конвейер запускается при событии: push.

Jobs

1. lint

- Check out code: Код извлечен из репозитория.
- Set up Python: Установлена версия Python 3.11.9.
- Install Poetry: Poetry устанавливается с помощью pip.
- Install dependencies: Необходимые зависимости устанавливаются без корневого пакета.
- Run flake8: Программа запускает Flake8 для проверки кода на наличие нарушений стиля и других потенциальных проблем.

2. test

Переменные среды: SECRET_KEY извлекается из GitHub secrets для безопасного хранения.

- Checkout Code: Код извлечен из репозитория.
- Set Up Python: Установлена версия Python 3.11.9.
- Install Poetry: Poetry устанавливается с помощью pip.
- Install dependencies: Необходимые зависимости устанавливаются без корневого пакета.
- Run Tests: Тесты Django выполняются с использованием Poetry.

3. copy_files_in_server

Dependencies: это задание зависит от успешного завершения тестового задания.

- Checkout Code: Код извлечен из репозитория.
- Create .env file: В корневом каталоге проекта создается env-файл. Этот файл заполняется переменными среды, определенными в GitHub Secrets, что позволяет приложению запускаться с необходимой конфигурацией.
- Set up SSH: Настраивает доступ по SSH для безопасной связи с удаленным сервером. В нем используется закрытый SSH-ключ, хранящийся в GitHub Secrets.
- Adding Known Hosts: Добавляет IP-адрес сервера к известным хостам, предотвращая запрос SSH на подтверждение при первом подключении.
- Copy project files to server: Процесс использует rsync для копирования файлов на удаленный сервер. На этом шаге исключаются указанные каталоги и файлы (например, .git, .github и __pycache__), чтобы гарантировать передачу только необходимых файлов.

4. run_server

Это задание запускается только после успешного завершения задания сборки.

Set up SSH: Используйте SSH для безопасного подключения к серверу развертывания с помощью закрытого ключа, хранящегося в GitHub secrets.
Run Server: выполняются следующие команды:
- Измените каталог на каталог развертывания, указанный в секрете DEPLOY_DIR.
- Остановливаются и удаляюся все существующие контейнеры Docker.
- Запускаются контейнеры Docker, определенные в файле docker-compose.yml, с помощью команды docker compose up --build, чтобы убедиться, что используются самые последние образы.

Настройка секретов

Для обеспечения безопасной работы в репозитории GitHub должны быть настроены следующие секреты:

SECRET_KEY: секретный ключ Django.
DOCKER_HUB_USERNAME: имя пользователя в Docker Hub.
DOCKER_HUB_ACCESS_TOKEN: токен доступа Docker Hub для аутентификации.
SSH_KEY: закрытый SSH-ключ для доступа к серверу развертывания.
SSH_USER: имя пользователя сервера по SSH.
SERVER_IP: IP-адрес сервера, на котором будет развернуто приложение.
DEPLOY_DIR: папка на удаленном сервере в которую будет скопирован проект.