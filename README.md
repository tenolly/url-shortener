![Flask](https://img.shields.io/badge/flask-v1.1.2-blue?style=flat-square)
![MongoDB](https://img.shields.io/badge/pymongo-v3.11.3-blue?style=flat-square)
![Waitress](https://img.shields.io/badge/waitress-v1.4.4-blue?style=flat-square)

### What is it?
This is a simple url shortener. Written with using flask, mongodb and waitress.<br>
Heroku: https://u-sh.herokuapp.com/<br>
Note: heroku uses a different collection ;)

### Installation
1) Download repository:
```bash
git clone https://github.com/Good5263/url-shortener.git
```
2) Install dependencies:
```bash
pip install -r requirements.txt
```

### Using
Run development server:
```bash
cd src
python app.py
```
Run wsgi server:
```bash
cd src
waitress-serve app:app
```
Exit:
```bash
Ctrl+C  
```
