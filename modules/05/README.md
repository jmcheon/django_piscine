

what is ORM
SQL vs ORM
what is text field and what's the diff b/w char field
what is migration

to create migration file
```
python3 manage.py makemigrations ex01
```

apply the migration
```
python3 manage.py migrate ex01
```

la methode copy_from de psycopg2


```
python3 manage.py loaddata ex09_initial_data.json
```

```
python3 manage.py makemigrations ex10
python3 manage.py migrate ex10
python3 manage.py loaddata ex10_initial_data.json
```