# pitter

[https://yatter-python.herokuapp.com/](https://yatter-python.herokuapp.com/)

__Yet Another Twitter clone (now with python!)__

Simple microblogging platform:
 * Register and sign in
 * Post messages
 * Edit and Delete messages
 * ... thats it for now!

# RUS {🇷🇺}

Простенький твиттер:
 * Работает регистрация и вход
 * Можно отправлять сообщения
 * Сообщения можно редактировать и удалять
 * ... и всё!

### Информация для проверяющих

Основная работа была вложена в построение архитектуры приложения.
На мой взгляд стандартный подход с декораторами, не очень хорошо ложится на те принципы ООП, которым мы учим.
В папке x_app - модуль с базовыми классами для всей этой системы.

Я посторался перевести приложене на архитектуру MVC:
 - Model: Файлы с описанием классов для ORM(SQLAlchemy). Папка models.
 - View: Шаблоны + Классы для заполнения этих шаблонов. Папки templates и view_models.
 - Controller: Блюпринты для связи View c основным приложением. Папка controllers.

В одно приложение это все собирается прямо в main.py: здесь объявлен класс PitterApp, в нем подключены все контроллеры.

Источники данных реализованы отдельными классами: 
  - XDataProvider хранит необходимые ссылки для SQLAlchemy.
  - XIdentityProvider - абстрактный менеджер авторизации. Конкретный класс UserProvider - реализация авторизации через Flask-Login, находится в main.py.

Настройки приложения вынесены в файл application.cfg

__Как собрать проект:__
По идее все собирается само из-под PyCharm. Если нет, то нужно просто сделать 
```
pip install -r requirements.txt
python main.py
```
Для удобства проверки всем настройкам заданы значения по умолчанию.
В поставке идет база данных с несколькими пользователями и сообщениями.

__TODO:__
 - возможность редактировать настройки профиля;
 - загрузка картинок на сервер;
 - возможность отслеживать сообщения пользователей;
 - ... лайки, репосты и т.д.

