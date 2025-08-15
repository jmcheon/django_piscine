
## ex00
```
python manage.py dumpdata auth.User ex.Article --indent 4 > ex/fixtures/data.json
```

## ex01
```
python3 manage.py dumpdata auth.User ex.Article ex.UserFavouriteArticle --indent 4 > ex/fixtures/data.json
```

## Charge toutes les données du kit dans la base de données
python3 manage.py loaddata data.json

