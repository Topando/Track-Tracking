*python backend/manage.py runserver* - запуск сервера

*pip freeze > requirements.txt* - обновление requirements

for client:

1.cd client

2.npm install

3.npm run dev


api/v1/user/ - это стандарт
register/ - username email password POST

confirm-email/<str:uidb64>/<str:token>/ - GET 

login/ - email or username, password  
