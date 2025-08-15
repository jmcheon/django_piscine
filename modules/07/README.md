
## ex00
```
python manage.py dumpdata auth.User ex.Article --indent 4 > ex/fixtures/data.json
```

## ex01
```
python3 manage.py dumpdata auth.User ex.Article ex.UserFavouriteArticle --indent 4 > ex/fixtures/data.json
```

## Charge toutes les données du kit dans la base de données
```
python3 manage.py loaddata data.json
```


## ex05
```
python3 manage.py makemessages -l fr
python3 manage.py compilemessages
```

```
python3 manage.py makemessages -d django -l fr
python3 manage.py compilemessages -l fr
```


## ex06
python3 manage.py test