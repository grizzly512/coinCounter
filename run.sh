#!/bin/bash
source ./venv/bin/activate
pip install -r requirements.txt
if python manage.py test; then
    python ./manage.py makemigrations
    python ./manage.py migrate
    python ./manage.py runserver
else
    echo Тесты провалены, проверьте код
fi

deactivate