#!/usr/bin/sh

python main.py buat_db
python main.py migrasi init
python main.py migrasi migrate

exit 0