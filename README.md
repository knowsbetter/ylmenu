# Menu application

 Homework for Ylab course.

# Запуск на локальном компьютере:

<ul>
 <li>В корневом каталоге проекта создаём файл с именем .env и помещаем в него следующие переменные окружения (см. example_env):<br>
  <b>SQLALCHEMY_DATABASE_URL=postgresql://user:password@postgresserverhost:port/dbname</b>,<br>
  где <b>user:password</b> - данные для подключения к базе данных, <b>postgresserverhost:port</b> - имя и порт сервера базы данных, <b>dbname</b> - название базы данных.
 <li>В командной строке переходим в папку проекта, выполняем установку необходимых пакетов командой:<br>
  <b>$ pip install -r requirements.txt</b></li>
 <li>Запускаем проект из командной строки:<br>
  <b>$ uvicorn mainapp.main:app</b><br>Проект по умолчанию доступен на localhost:8000/docs.
 </li>
</ul>

# Запуск в контейнере:

<ul>
 <li>Запускаем проект в контейнере командой:<br>
  <b>$ docker-compose -f docker-compose.yml up -d</b><br>
  После запуска API будет доступен на localhost:8000/docs,
  база данных - по схеме posrgres:postgres@localhost:9000/postgres.
 </li>
 <li>Запускаем тесты проекта в контейнере командой:<br>
  <b>$ docker-compose -f docker-compose-test.yml up</b>
 </li>
</ul>
