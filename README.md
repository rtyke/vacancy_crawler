1. Склонируйте репозитарий

2 Получить API KEY у superjob
https://api.superjob.ru/info/

3. В файле webapp/config.py:
удалить строчку ```from webapp.api_key import SJ_KEY```
SJ_KEY заменить Secret key полученным в предыдущем пункте

4. Установить зависимости из requiremtns.txt

5. Создать базу данных
python create_db.py

6. Получить обновления за послдение 20 дней
python get_vacancies_all.py
Это займет около 30 минут! Можно сократить срок, за который получашеь обновления изменив срок обновления в файле webapp/config.py:
INIT_DOWNLOAD_VACANCIES_FOR_X_DAYS

7. Получать обновления:
python get_vacancies_updates.py

8. Запуск сервера
export FLASK_APP=webapp && export FLASK_ENV=development && flask run

9. Посмотреть результат работы
http://127.0.0.1:5000/