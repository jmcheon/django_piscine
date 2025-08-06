

## C'est quoi `models.Model` ?

c'est une **classe de base** fournie par Django. c'est comme `modèle` ou `gabarit` pour créer des tables de base de données.

```python
from django.db import models

class Movies(models.Model):
    title = models.CharField(max_length=64)
    # ... autres champs
```

Je veux créer une table dans ma base de données. Cette table sera représentée en Python par la classe `Movies`. chaque instance de la classe sera une ligne dans la table.

En héritant la classe `models.Model`, la classe `Movies` acquiert automatiquement toutes les fonctionnalités nécessaires pour interagir avec la base de données: sauvegarder, supprimer, chercher des données etc.

Chaque attribut défini devient une **colonne** dans la table de la base de données.


Convention de nommage automatique pour éviter les conflits entre les applications.
```
nom_de_l_application + _ + nom_du_modèle_en_minuscules
```