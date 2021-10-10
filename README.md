<p align="center">
    <a href="#" target="_blank" rel="noopener noreferrer">
        <img width="100" src="docs/_static/195513_1280_800.jpg" title="Laut Academy">
    </a>
</p>

<h2 align="center">SOCIAL NETWORK</h2>

[![Join the chat at https://gitter.im/djangochannel/community](https://badges.gitter.im/djangochannel/community.svg)](https://gitter.im/djangochannel/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


### Описание проекта:
Проект создан для связи людей друг с другом да и просто, как развлечение.

- Связь 
- Сообщества
- Полноценный профиль
- Лента

### Инструменты разработки

**Стек:**
- Python >= 3.7
- Django >= 2
- PostgreSQL
- JavaScript
- Django REST


**Ссылки**:
- [ВК](https://vk.com/lautariano)
- [GitHub](https://github.com/lautarianoo)




*Создать Issues можно и тем, кто не хочет работать с нами над проектом, а просто хочет задать вопросы и дать нам совет*

## Разработка

##### 1) Сделать форк репозитория и поставить звездочку)

##### 2) Клонировать репозиторий

    git clone ссылка_сгенерированная_в_вашем_репозитории

##### 3) Создать виртуальное окружение

    python -m venv venv
    
##### 4) Активировать виртуальное окружение

##### 5) В local_settings.py и прописать конект к базе

##### 6) Устанавливить зависимости:

    pip install -r req.txt

##### 7) Выполнить команду для выполнения миграций

    python manage.py deploy
    
##### 8) Создать суперпользователя

    python manage.py createsuperuser
    
##### 9) Запустить сервер

    python manage.py runserver


### Синхронизировать с основной веткой репозитория проекта, когда она изменилась:


##### 1. Добавить удалённый репозиторий

    git remote add название_ветки_на_локальной_машине https://github.com/DJWOMS/djangochannel

##### 2. Проверить добавилась ли ссылка

    git remote -v

##### 3. Синхронизируем с основной веткой на своей машине

    git pull название_ветки_на_локальной_машине develop

##### 4. Внесенные изменения добавляем в ветку в своем репозитории и пушим в свой удаленный репозиторий

    git add .

    git commit -m "четкое_и_понятное_описание_проделанной_работы""

    git push

##### 5. Сделать пулл реквест в основной ветке Django Channel в develop branch

##### Разработка осуществляется через ветку develop


## License

[BSD 3-Clause License](https://opensource.org/licenses/BSD-3-Clause)

Copyright (c) 2021-present, lautarianoo - Volf Alexander



