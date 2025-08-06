

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


## PostgreSQL Configuration
```
psql postgres
```

```
-- Create the database for the project.
CREATE DATABASE formationdjango;

-- Create the user with a specific password, as required by the project.
CREATE USER djangouser WITH PASSWORD 'secret';

-- Grant all necessary permissions on the new database to the new user.
GRANT ALL PRIVILEGES ON DATABASE formationdjango TO djangouser;
```

```
\q
```

Connection check
```
psql -d formationdjango -U djangouser
```

## migration
C'est l'étape où Django va générer le SQL pour vous et créer la table.

1. Créez le fichier de migration(plan) : Cette commande lit models.py et crée un "plan" pour construire la table.
```sh
python3 manage.py makemigrations `nom de l'application``
```

Django regarde les fichiers `models.py` (uniquement dans cette application). Il les compare à l'état actuel de mes `plans` (les fichiers de migration existants). S'il détecte un changement, il génère **un nouveau fichier** dans la dossier `nom de l'application/migrations`.

le nouveau fichier, par exemple `0001_initial.py`, c'est une sorte de plan de construction. Il contient les instructions en Python.

les plans sont indépendants de la base de données

2. Appliquez la migration : Cette commande exécute le "plan" et crée la table dans la base de données PostgreSQL.

Django regarde tous les `plan de construction` (les fichiers de migration) qui n'ont pas encore été appliqués à la base de données.

Il exécute ces plans. Il lit les instructions dans le fichier et les traduit en commandes SQL et les envoie à la base de données PostgreSQL.


3. Vérification

- Mac
```sh
psql -d formationdjango
```

- linux
```sh
sudo -u postgres psql -d formationdjango
```