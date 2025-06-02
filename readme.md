# Analyse de la Consommation Énergétique Française

---

Copyright © 2025 Cristóvão GUIHO. Tous droits réservés.

**Auteur:** Cristóvão GUIHO
- M2 3EA T3I

**Master:** Électronique, Énergie Électrique, Automatique - Parcours Traitement de l'Information et Instrumentation pour l'Ingénieur
**Projet:** Programmation et Acquisition

---

## 🎯 Objectif du Projet

Ce projet vise à analyser et visualiser la consommation quotidienne brute d'électricité et de gaz en France. Il utilise des données ouvertes officielles fournies par ODRE (OpenData Réseaux Énergies) et mises à jour régulièrement. L'application permet de récupérer ces données, d'afficher des statistiques clés et de visualiser les tendances de consommation.

---

## ✨ Fonctionnalités Principales

* **Récupération de Données en Temps Réel :** Connexion à l'API d'ODRE pour obtenir les données de consommation les plus récentes.
* **Traitement des Données :** Utilisation de la bibliothèque `pandas` pour structurer et nettoyer les données récupérées.
* **Affichage de Statistiques :** Calcul et présentation de statistiques descriptives clés (moyenne, écart-type, variance, min, max) sur la consommation.
* **Interface Graphique Utilisateur (GUI) :** Une interface conviviale développée avec PySide6 et Qt Designer pour interagir avec l'application.
* **Visualisation (Prévue) :** Un espace est prévu pour afficher des graphiques de l'évolution de la consommation (par exemple, avec `pyqtgraph`).
* **Exportation des Données :** Possibilité de sauvegarder les données traitées au format CSV.

---

## 🛠️ Aspects Techniques

* **Langage :** Python 3
* **Interface Graphique :** PySide6 (liaisons Python officielles pour Qt6)
* **Conception UI :** Qt Designer (les fichiers `.ui` sont compilés en fichiers Python)
* **Bibliothèques Principales :**
    * `requests` : Pour les requêtes API.
    * `pandas` : Pour la manipulation et l'analyse des données.
    * `PySide6` : Pour l'interface graphique.
    * (Optionnel/Futur) `pyqtgraph` ou `matplotlib` : Pour les graphiques.

---

##  GIT : Gestion de Versions pour ce Projet Qt

Git est essentiel pour suivre l'évolution de ce projet, collaborer (si applicable) et gérer les différentes versions du code. Voici comment Git est utilisé dans le contexte de ce projet Qt/PySide6 :

### 📝 Commits

Les commits sont des "instantanés" de votre projet à un moment donné. Ils permettent de sauvegarder les modifications de manière atomique avec un message descriptif.

**Bonnes pratiques pour les commits dans ce projet :**

* **Fréquence :** Faites des commits réguliers et petits. Dès qu'une fonctionnalité mineure est ajoutée, qu'un bug est corrigé, ou qu'une partie de l'interface utilisateur est modifiée, c'est un bon moment pour commiter.
* **Messages clairs :** Rédigez des messages de commit explicites en français (ou anglais, selon la convention de votre projet). Par exemple :
    * `git commit -m "Ajout du bouton de récupération des données API"`
    * `git commit -m "Correction : Calcul de la moyenne pour la consommation totale"`
    * `git commit -m "Interface : Mise à jour des labels statistiques dans design_ui.py"`
* **Quoi commiter :**
    * **Code source Python (`.py`) :** Tous vos scripts (`main.py`, `data_handler.py`, le fichier UI compilé `design_ui.py`, etc.).
    * **Fichiers UI de Qt Designer (`.ui`) :** Il est crucial de commiter le fichier `.ui` source. Cela permet à quiconque (y compris vous-même dans le futur) de modifier le design dans Qt Designer et de le recompiler.
    * **Fichiers de ressources (`.qrc`) :** Si vous utilisez des icônes ou d'autres ressources, commitez le fichier `.qrc` et les ressources elles-mêmes.
    * **`README.md` et autres documentations.**
    * **Fichier `.gitignore` :** Pour exclure les fichiers non nécessaires (ex: `__pycache__`, fichiers d'environnement virtuel `.venv/`, fichiers temporaires de l'IDE).
        *Exemple de `.gitignore` pour un projet Python/Qt :*
        ```gitignore
        # Byte-compiled / optimized / DLL files
        __pycache__/
        *.py[cod]
        *$py.class

        # Virtual environment
        .venv/
        venv/
        ENV/

        # IDE / Editor specific files
        .vscode/
        .idea/
        *.swp
        ```
* **Synchronisation avec le fichier `.ui` :** Si vous modifiez le fichier `design.ui` dans Qt Designer, n'oubliez pas de **recompiler ce fichier en `design_ui.py`** (avec `pyside6-uic design.ui -o design_ui.py`) et de commiter **les deux fichiers** (`design.ui` ET `design_ui.py`) pour que le code Python reflète les changements visuels. Certains préfèrent ne pas commiter le fichier `.py` généré et le générer à la volée lors du build, mais pour des projets plus simples, commiter les deux est courant.

### 🏷️ Tags (Étiquettes)

Les tags sont utilisés pour marquer des points spécifiques dans l'historique des commits, typiquement pour indiquer des versions ou des jalons importants.

**Utilisation des tags pour ce projet :**

* **Versions :** Lorsque vous atteignez une version stable de votre application (par exemple, une version fonctionnelle avec un ensemble de fonctionnalités clés), vous pouvez la taguer.
    * `git tag -a v0.1.0 -m "Version 0.1.0 : Récupération et affichage des statistiques de base"`
    * `git tag -a v0.2.0 -m "Version 0.2.0 : Ajout de la fonctionnalité d'export CSV"`
    * `git tag -a v1.0.0 -m "Version 1.0.0 : Première version stable complète"`
* **Publication des tags :** Pour partager vos tags avec un dépôt distant (comme GitHub) :
    * `git push origin v0.1.0` (pour un tag spécifique)
    * `git push origin --tags` (pour tous les tags)
* **Consulter les tags :**
    * `git tag` (liste tous les tags)
    * `git show v0.1.0` (montre les informations du tag et le commit associé)

L'utilisation de commits descriptifs et de tags pour les versions rendra votre projet beaucoup plus facile à maintenir, à comprendre et à potentiellement revenir à des états antérieurs si nécessaire.

---

## 🚀 Lancement de l'Application (Instructions de Base)

1.  **Cloner le dépôt (si applicable) :**
    ```bash
    git clone [URL_DU_DEPOT]
    cd [NOM_DU_DOSSIER_PROJET]
    ```
2.  **Installer les dépendances** (de préférence dans un environnement virtuel) :
    ```bash
    # Créer un environnement virtuel (si pas déjà fait)
    # python -m venv .venv
    # Activer l'environnement
    # source .venv/Scripts/activate  (Git Bash/Linux)
    # .venv\Scripts\activate  (Windows CMD)

    pip install PySide6 requests pandas
    ```
3.  **Compiler le fichier UI (si nécessaire) :**
    Si vous avez modifié `design.ui` et que `design_ui.py` n'est pas à jour :
    ```bash
    pyside6-uic source/design.ui -o source/design_ui.py
    ```
4.  **Exécuter l'application :**
    ```bash
    python source/main.py
    ```

---
