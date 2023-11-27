<h1> ticket_system </h1>

<h2> Инструкция по запуску </h2>

<h3>1. Клонируем репозиторий </h3>
&nbsp &nbsp &nbsp git clone https://github.com/Gektor918/ticket_system

<h3>2. Создаем виртуальное окружение </h3>
&nbsp &nbsp &nbsp python3 -m venv name_venv

<h3>3. Запускаем виртуальное окружение </h3>
&nbsp &nbsp &nbsp source name_venv/bin/activate

<h3>4. Устанавливаем зависимости </h3>
&nbsp &nbsp &nbsp pip install -r requirements.txt

<h3>5. Настройка </h3>
&nbsp &nbsp &nbsp  в model.py вставте свои настройки для бд
&nbsp &nbsp &nbsp  в bot.py вставте токен бота

<h3>6. Запускаем сервер </h3>
&nbsp &nbsp &nbsp  uvicorn main:app --reload

<h3>7. Запускаем бота </h3>
&nbsp &nbsp &nbsp  python3 bot.py

<h3>8. Создание таблиц </h3>
&nbsp &nbsp &nbsp  перейдите на http://127.0.0.1:8000/docs#/
&nbsp &nbsp &nbsp  создание таблиц POST/create_tables/
&nbsp &nbsp &nbsp  создание сотрудника POST/create_employee/
