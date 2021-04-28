#!/bin/bash

python main.py buat_db
python main.py migrasi init
python main.py migrasi migrate
python main.py runserver --port=80 --host=0.0.0.0

exit 0