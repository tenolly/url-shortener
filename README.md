![Flask](https://img.shields.io/badge/flask-v1.1.2-blue?style=flat-square)
![MongoDB](https://img.shields.io/badge/pymongo-v3.11.3-blue?style=flat-square)
![Waitress](https://img.shields.io/badge/waitress-v1.4.4-blue?style=flat-square)

### URL Shortener
Это простой скоращатель url, написанный с использованием flask, mongodb и js.<br>
(Мне очень лень заливать все это дело на Heroku, поэтому пока так).

### Установка
1) Скачиваем репозиторий zip-файлом или с помощью команды:
```bash
git clone https://github.com/Good5263/url-shortener.git
```
2) Устанавливаем зависимости:
```bash
pip install -r requirements.txt
```

### Использование
Запуск (wsgi server):
```bash
cd src
waitress-serve app:app
```
Запуск (development server):
```bash
cd src
python app.py
```
Отключение:
```bash
Ctrl+C  
```
