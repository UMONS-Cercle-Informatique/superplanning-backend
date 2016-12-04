# superplanning-backend
Superplanning backend.

## iCalRetriever

Ce dossier comprend le script python qui permet de récupérer les liens des fichiers iCal et les enregistrer dans un fichier CSV.

### Dépendances
* Python 3.x et pip
* Selenium (python3 -m pip install selenium)
* Les drivers:
  * Général : Téléchargez l'exécutable, extrayer le fichier dans un dossier et ajouter le chemin jusqu'au dossier dans la variable d'environnement PATH.
  * [Chrome - chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
  * [Firefox - geckodriver](https://github.com/mozilla/geckodriver/releases)
  * Dans le script, mettez le nom approprié à la création du driver (webdriver.Chrome() ou webdriver.Firefox()) 
* [Plus d'informations](http://selenium-python.readthedocs.io/installation.html)

## importSchedule

Ce dossier comprend le script de parsing des fichiers iCal et d'importation dans la base de données.

Chaque fichier iCal est parsé et les horaires sont importés dans une base de données. PostgreSQL 9.5+ est utilisée comme SGDB.

### PostgreSQL

Si vous êtes sous Debian/Ubuntu, vous pouvez installer la dernière version de PostgreSQL avec `apt-get`:
```
sudo apt-get install postgresql
```

Pour faciliter la création, le démarrage, l'arrêt ainsi que la connexion à la
base de données, un Makefile et une configuration par défaut sont fournis. Les
règles définies sont décrites dans le Makefile même.
Une utilisation basique est:
```
make db-init
make db-create
make db-schema
```

Pour accéder à l'interface de PostgreSQL en vous connectant à la base de données, vous pouvez utiliser:
```
make db-psql
```

### Schéma et fichier SQL.

Un diagramme de la base de données peut être trouvé [ici](https://github.com/UMONS-Cercle-Informatique/superplanning) dans le dossier documents.
Un fichier SQL correspondant est fourni (voir `superplanning.sql`).
