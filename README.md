# Система для обнаружения, оценки и мониторинга нефтеразливов
Реализованная функциональность

    Получение и обработка данных со спутника;
    Распознавание нефтеразливов с использованием нейронной сети;
    Scheduler - сервис для своевременного обновления данных;

Особенность проекта в следующем:

    Модульная архитектура с возможностью замены компонентов системы;
    Использование внешних спутниковых данных для оперативности получения информации;
    Распознавание некорректных входных данных - высокая облачность или отсутствие данных;
    Автоматическое обновление информации и рассылка уведомлений;

Основной стек технологий:

    Python
    ASP.NET
    HTML, CSS, JavaScript
    PostgreSQL
    PyTorch
    eolearn

### Демо

Демо сервиса доступно по адресу: https://myp3a.noip.me/rosatom/  

## Среда запуска
1. Требуется установленная СУБД PostgreSQL.
2. Требуется установленный интерпретатор Python 3.6+
3. Требуются установленные библиотеки Python: pytorch, eolearn

## Установка
### Установка PostgreSQL
Перейдите по ссылке https://www.postgresql.org/download/. Требуемый пакет будет определен автоматически.
Установите привычным способом для вашей операционной системы.
### Установка Python
Перейдите по ссылке https://www.python.org/downloads/.
Выберите пакет для вашей операционной системы, установите привычным образом.
### Установка зависимостей Python
Выполните
```
pip install pytorch eolearn
```

## Запуск 
Скомпилировать `Prod/Core` и `Prod/Scheduler`, запустить  
Запустить сервис распознавания, перейдя в `Prod/app` и выполнив `python launch.py`
Запустить UI, перейдя в папку `WebApplication` и выполнив `dotnet watch` 
Сервис будет доступен по указанному адресу  

## Использование
Страница данных о разливах доступна по адресу http://127.0.0.1:8080/. На ней отображена информация о участках и результат анализа информации.  
Scheduler в фоне будет получать данные со спутников и добавлять их в БД.  
Нейронная сеть получает запрос на распознавание от Scheduler и возвращает обработанное изображение.  

## Разработчики
Жарков Валерий (капитан, бэкенд) - https://t.me/MCZhar  
Городничин Константин (бэкенд) - https://t.me/Myp3a  
Хабитов Салим (бэкенд) - https://t.me/BZADZHINADZHA  
Мария Чумикова (дизайнер, презентация) - https://t.me/Maria12788 
