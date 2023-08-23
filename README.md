Сервис для интеграции с elma

Назначение: проверка наличия переданного в запросе почтового адреса в БД с наличием значения True поля верификации 
этого email 

Интерфейс: API из одного endpoint

    Спецификация endpoint:
       url: /check_email/<email>, где вместо <email> указывается почтовый адрес
       HTTP method: GET
       response:
         type: JSON
         content: {user_find: <boolean>}, где означает: 
            true - email верифицирован, false - отсутствуетв БД, либо не верифицирован

Стек проекта:
  - docker-compose на два контейнера - для приложения на flask и СУБД Postgres
  - контейнеры приложения и Postgres на базе Debian 12 bookworm
  - приложение получает запросы по порту 80 через веб-сервер nginx
  - flask использует ORM SQLAlchemy для обращения к СУБД Postgres 
    