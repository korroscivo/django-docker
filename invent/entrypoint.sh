python manage.py makemigrations customers
python manage.py migrate_schemas --shared
# python manage.py collectstatic --noinput --clear
python manage.py shell
import schemas2.view
schemas2.view.migration_sql()