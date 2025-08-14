

## ex00
Si la table `django_session`, utilisée par Django pour stocker les information de session, n'a pas été créée dans la base de données.

```
python3 manage.py migrate
```


```
python3 manage.py runserver
```


## ex02

```
python3 manage.py makemigrations
python3 manage.py migrate
```

## ex04
pour créer un superutilisateur

```
python3 manage.py createsuperuser
```