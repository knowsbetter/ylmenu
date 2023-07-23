# Menu application

 Домашняя работа для интенсива Ylab.

# Запуск на локальном компьютере:

<ul>
 <li>В корневом каталоге проекта создаём файл с именем .env и помещаем в него следующие переменные окружения (см. example_env):<br>
  <b>SQLALCHEMY_DATABASE_URL=postgresql://user:password@postgresserverhost:port/dbname</b>,<br>
  где <b>user:password</b> - данные для подключения к базе данных, <b>postgresserverhost:port</b> - имя и порт сервера базы данных, <b>dbname</b> - название базы данных.
 </li>
 <li>В командной строке переходим в папку проекта, выполняем установку необходимых пакетов командой:<br>
  <b>$ pip install -r requirements.txt</b></li>
 <li>Запускаем проект из командной строки:<br>
  <b>$ uvicorn menuapp.main:app</b><br>Проект по умолчанию доступен на localhost:8000/docs.
 </li>
</ul>
