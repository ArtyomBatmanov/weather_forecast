## Прогноз погоды

### Для запуска приложения:

1) Пройдите регистрацию в https://www.weatherapi.com/
2) Создайте API ключ
3) В корне проекта создайте файл .env по шаблону .env.template
4) Создайте вируальное окружение командой python3 -m venv venv и активируйте его sourve/venv/bin/activate (для Linux)
5) Установите все зависимости pip isntall -r requirements.txt

### Приложение может вернуть:

1) GET /api/weather/{city}/now - прогноз погоды сейчас
2) GET /api/weather/{city}/today - прогноз погоды сегодня
3) GET /api/weather/{city}/tomorrow - прогноз погоды завтра
4) GET /api/weather/{city}/3-days/ - прогноз погоды на 3 дня
