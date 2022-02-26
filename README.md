# scrabbing

Сервис собирает данные репозиториев с github.com по ссылке на конктретного пользователя либо списку ссылок введенных пользователем. 
Сохраняет данные в БД MongoDB и можно получить JSON файл. 
Сервис принимает на вход ссылки разделенные пробелами(пример ввода):
    
    site.com/home site.com/page site.com/catalog 

# Установка

    git clone https://github.com/Omoegod/scrabbing.git
    python -m venv env
    cd ./env/scripts/activate
    pip install -r requirements.txt
    
# Запуск программы

Переходим в директорию:

    cd .\scrabbing\proj\app\spiders

запуск

    scrapy crawl gitscrab     

запуск + запись JSON файл

    scrapy crawl gitscrab -o items.json -t json
    
    
    
    
