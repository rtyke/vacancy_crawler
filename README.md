1. Склонируйте репозитарий

2 Получить API KEY у superjob
https://api.superjob.ru/info/

3. В файле webapp/config.py:
удалить строку ```from webapp.api_key import SJ_KEY```
SJ_KEY заменить Secret key полученным в предыдущем пункте

4. Установить зависимости из requirements.txt
```
pip install -r requirements.txt
```

5. Установить:
 - postgresql
 - rabbitMQ

Запуск:
```
rabbitmq-server
```

```
postgres -D /usr/local/var/postgres
```

6. Создать базу данных
python create_db.py

7. Получить обновления за последние 30 дней.
Запуск очереди
```
celery -A get_vacancies_all worker --loglevel=info
```
В новом окне:
```
python get_vacancies_all.py
```
Это займет около часа. Можно сократить срок, за который получашеь обновления изменив срок обновления в файле webapp/config.py:
INIT_DOWNLOAD_VACANCIES_FOR_X_DAYS

8. Получать регулярные обновления:
```
celery -A get_vacancies_updates worker --loglevel=info
```
В новом окне:
```
celery -A get_vacancies_updates beat
```
9. Запуск сервера
export FLASK_APP=webapp && export FLASK_ENV=development && export RDS_PORT=5432 && flask run

10. Посмотреть результат работы
http://127.0.0.1:5000/


---

celery -A get_vacancies_all worker --loglevel=info

celery -A get_vacancies_updates worker --loglevel=info
celery -A get_vacancies_updates beat

