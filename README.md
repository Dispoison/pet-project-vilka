# Pet project Vilka
Pet project: online store, created by me to demonstrate, first of all, to myself, my knowledge and abilities in the Django framework.
The site template was taken from [here](https://www.insales.ru/collection/themes/product/shablon-internet-magazina-fine).

## Install

Run the following commands to install your environment:
  
    python3 -m venv venv   
    source venv/bin/activate
    pip3 install -r requirements.txt

    cp .env.template .env
    while read file; do
       export "$file"
       done < .env

Run the app:

    python3 manage.py runserver

