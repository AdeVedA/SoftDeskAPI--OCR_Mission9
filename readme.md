### <p align="center"><bold>SoftDeskAPI - OCR_Mission[9]</bold></p>
<p align="center">=====================================</p>
<p align="center">
  <picture> 
    <img alt="logo de SoftDeskAPI" src="https://user.oc-static.com/upload/2023/06/28/16879473703315_P10-02.png" width="800">
  </picture>
  <br/>
</p>

# <p align="center"><bold>- SoftDeskAPI -</bold></p>
### <p align="center">- API RESTful sécurisée pour la gestion collaborative de projets et le suivi des problèmes techniques -</p>
# <p align="center"> I. Description du Projet</p>

SoftDesk API est une API RESTful sécurisée permettant de remonter et suivre des problèmes/enjeux techniques pour des projets collaboratifs. Cette solution B2B permet aux entreprises de :

Créer et gérer des projets (titre, description, type...)
Attribuer des contributeurs aux projets
Créer et suivre des "problèmes/enjeux" sur un projet (issues : titre, description, priorité, tag, status, attribution)
Créer et suivre des commentaires sur les "problèmes/enjeux"
Gérer les permissions et l'authentification des utilisateurs (par JSON Web Token)

Fonctionnalités principales

Authentification JWT (JSON Web Token)
Gestion des permissions CRUD basée sur les rôles (auteur, contributeur) et sur les choix de consentement des utilisateurs
Conformité RGPD (consentement, condition d'âge, modification/suppression du compte)
Pagination des ressources
Optimisation des requêtes (Green Code)

Points de terminaison de l'API :

------------------------------------------

## <p align="center">I - Setup windows</p>

#### ( si [Git](https://github.com/git-for-windows/git/releases/download/v2.46.2.windows.1/Git-2.46.2-64-bit.exe) et [python 3.12+](https://www.python.org/ftp/python/3.12.6/python-3.12.6-amd64.exe) ne sont pas installés, commencez par l'annexe 1 !)
------------------------------------------
  #### A - Créez un répertoire pour le programme
Lancez votre explorateur windows (WIN+E) 
Créez un répertoire (CTRL+MAJ+N) pour le programme où vous le souhaitez et **nommez-le**
ex. : vous pouvez l'appeler **SoftDesk** dans d:\chemin\vers\mon\dossier\SoftDesk
**double-cliquez** sur le répertoire créé pour aller dedans.

  #### B - lancez l'interpréteur de commande windows
Clic gauche dans la barre d'adresse de l'explorateur, écrivez **"cmd"** (à la place de l'adresse)
et appuyez sur **"entrée"** (comme à chaque instruction en ligne future):

	cmd
	
  #### C - clonez le repo Github du projet dans ce répertoire
dans le terminal (l'invite de commande) qui indique bien que vous êtes à l'adresse du dossier créé, écrivez tour à tour:

	git init

puis : 

	git pull https://github.com/AdeVedA/SoftDeskAPI--OCR_Mission9 -t main

  #### D - installez un environnement virtuel dans un dossier 'env' du projet, toujours par l'invite de commande :
	
	python -m venv env
 
  #### E - activez l'environnement virtuel créé précédemment :
	
	env\Scripts\activate.bat
 
  #### F - installez les librairies requises :
	
	pip install -r requirements.txt

  #### G - mettez-vous dans le répertoire du projet et lancez le serveur (l'environnement virtuel doit avoir été activé avant):

    cd softdeskapi

puis

	py manage.py runserver

  #### H - démarrez l'application Web SoftDeskAPI dans votre navigateur web en inscrivant l'adresse :

	http://127.0.0.1:8000/

  #### I - fermez le serveur et désactivez l'environnement virtuel quand vous avez fini dans le terminal :

	ctrl +c

puis

	deactivate
-------------------------
-------------------------

## <p align="center">II - Setup Linux/Mac</p>

#### ( si **[Git](https://sourceforge.net/projects/git-osx-installer/files/git-2.23.0-intel-universal-mavericks.dmg/download?use_mirror=autoselect)** et **[python](https://www.python.org/ftp/python/3.12.6/python-3.12.6-macos11.pkg)** ne sont pas installés, commencez par l'annexe 1 !)

-------------------------
	
  #### A- lancez un terminal

clic sur loupe/recherche lancez

	terminal
	
  #### B - Créez un répertoire pour le programme et placez-vous dedans
  par exemple si vous souhaitez appeler ce dossier "SoftDeskAPI" :

	mkdir SoftDesk

puis :

	cd SoftDesk

  #### C - clonez le repo Github du projet dans ce répertoire
dans le terminal (l'invite de commande) qui indique bien que vous êtes à l'adresse du dossier créé, écrivez tour à tour:

	git init

puis : 

	git pull https://github.com/AdeVedA/SoftDeskAPI--OCR_Mission9 -t main

  #### D - installez un environnement virtuel dans un dossier 'env' du projet, toujours par le terminal :
	
	python3 -m venv env

  #### E - activez l'environnement virtuel créé précédemment :
	
	source env/bin/activate
 
  #### F - installez les librairies requises :
	
	pip install -r requirements.txt

  #### G - mettez-vous dans le répertoire du projet et lancez le serveur (l'environnement virtuel doit avoir été activé avant):

    cd softdeskapi

puis

	python3 manage.py runserver

  #### H - démarrez l'application Web SoftDeskAPI dans votre navigateur web en inscrivant l'adresse :

	http://127.0.0.1:8000/

  #### I - fermez le serveur et désactivez l'environnement virtuel quand vous avez fini dans le terminal :

	ctrl +c

puis

	deactivate


-------------------------
# <p align="center">Annexe 1 - installation de Python & Git</p>
<p align="center">====================================================</p>

pour Windows 64bits :
--------------------

installez **[Git](https://github.com/git-for-windows/git/releases/download/v2.46.2.windows.1/Git-2.46.2-64-bit.exe)** 
verifiez en tapant "cmd" dans le menu démarrer puis "git version" dans le terminal

installez **[python](https://www.python.org/ftp/python/3.12.6/python-3.12.6-amd64.exe)** en vous assurant que ***"Add to PATH"*** est coché (laissez les autres choix par défaut)
verifiez en tapant "cmd" dans le menu démarrer puis "python --version" dans le terminal

pour Mac/Linux :
--------------------
**Git**
cliquez sur l'icone de recherche (loupe), écrivez "terminal" (on vérifie si git est déjà présent)

	git version

si ok, passez à python. 
sinon, installez ce qu'il vous propose d'installer ("command line developer tools") puis recommencez "git version" en terminal,
sinon : installez **[Git](https://sourceforge.net/projects/git-osx-installer/files/git-2.33.0-intel-universal-mavericks.dmg/download?use_mirror=autoselect)**
puis revérifiez git version dans le terminal

**Python**
installez **[python](https://www.python.org/ftp/python/3.12.6/python-3.12.6-macos11.pkg)**

-------------------------
-------------------------
