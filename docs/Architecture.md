# Architecture

## 1. Présentation

Stockflow est un gestionnaire de stock d'une boutique fictive, son but premier est de gérer les stocks, les produits, les mouvements de stocks et les fournisseurs.
L'utilisateur pourra consulter les produits et les stocks, enregistrer des mouvements, définir et consulter les alertes de stock bas.
L'application a pour but premier de servir de projet pour mon portfolio et pour cela j'utilise Python avec pywebview pour l'interface bureau et SQLite pour la base de données (avec des données fictives).
Ce document contient toute l'architecture et la conception de l'application .
## 2. Stack technique

**Python:** Je l'es choisis par préférence et car c'est un des language que je maîtrise le mieux , je l'es aussi choisi pour les librairie (pywebview et sqlite3) qui sont des librairie adapter a mon projet.
**pywebview:** Étant familiariser avec le web j'ai choisi pywebview pour avoir une interface web sur bureau . Ça me permet de mieux gérer l'interfaces et de le rendre plus ergonomique plus facilement .je n'est pas choisi tkinter ou PyQt car je les maîtrise mal et que je trouve leurs coté apparences trop complexe pour ce projet
**SQLite:** J'ai choisi SQLite pour sa légèreté et son architecture serverless (sans serveur). Installer un SGBD traditionnel aurait été inutilement complexe et contre-productif pour ce projet.
**Git:** J’utilise Git et GitHub pour versionner le projet : c’est l’outil de référence dans le métier, et l’historique des commits montre l’avancement du projet étape par étape.
**unittest:**Je les choisi par default car c'est le seul que j'ai deja utiliser mais une evolution vers pytest est possible a l'avenir du project.
**drawDB:** Je les utiliser pour créer une schema pour ma base de donnée et exporter tout ça en un fichier meme si j'ai du modifier ma base de donnée pour y ajouter des contrainte que drawDB ne gère pas

## 3. Vue d'ensemble

<img src="architecture-couches.png" alt="Schéma des couches de l'application" width="350" align="right">

*l'application est organisée en couches, et le schéma montre comment une demande de l'utilisateur les traverse.*

**Rôle de chaque couche**

- **Interface** : Affiche en HTML les données reçues et permet à l'utilisateur d'effectuer des demandes d'action. Elle ne contient aucune logique métier.
- **API** : Fait le lien entre l'interface et les services. Elle reçoit les actions de l'interface par pywebview, les transmet aux services, puis renvoie le résultat à l'interface (données ou erreur). Elle ne contient aucune règle métier.
- **Services** : Contiennent la logique métier de l'application (par exemple, refuser une sortie si le stock est insuffisant). Ils vérifient les données, gèrent les actions et pilotent les transactions. Ils ne connaissent ni pywebview ni le SQL.
- **Repository** : Sert d'intermédiaire entre les services et la base de données. Il s'occupe de créer, lire, modifier et supprimer des données (CRUD) et est le seul à écrire du SQL.
- **Base de données** : Fichier SQLite qui regroupe toutes les données dans différentes tables (voir la section 6).

**Règle de dépendance**

Chaque couche ne communique qu’avec celle située juste en dessous : l’interface appelle l’API, l’API appelle les services, les services appellent le repository, et seul le repository accède à la base de données. Les services ne connaissent ni pywebview ni l’interface : ils peuvent donc être testés sans lancer la fenêtre, et l’interface peut changer sans toucher à la logique métier.

**Chemin d'une erreur**

L'erreur naît dans les services (stock insuffisant par exemple) et remonte a l'api qui convertie l'erreur pour que l'interface puissent l'afficher.

<br clear="right">

## 4. Structure du projet

> Arborescence commentée des dossiers et des fichiers principaux. Une phrase par dossier sur sa responsabilité.

## 5. Les couches en détail

### 5.1 Base de données et repositories
> Rôle, ce qui y est autorisé, ce qui est interdit (aucune règle métier). Comment la connexion est gérée, activation des clés étrangères.

### 5.2 Services (logique métier)
> Rôle, liste des services et de leurs responsabilités. Pourquoi c'est ici que sont les règles et les transactions.

### 5.3 API pywebview
> Rôle de pont entre le JS et les services. Format commun des réponses (succès, données, type d'erreur, message). Pourquoi elle reste fine.

### 5.4 Interface
> Pages, organisation du HTML/CSS/JS, comment le JS appelle l'API, affichage des notifications et de la page d'erreur.

## 6. Modèle de données

> Diagramme drawDB (image ou export) puis, pour chaque table : son rôle, ses colonnes importantes, ses relations.

- `product`
- `stocks`
- `movements`
- `supplier`
- `supplier_product`
- `alert`

### Conventions
> Unités et formats : prix en centimes (entiers), dates en timestamp entier (UTC ou local ? pourquoi), booléens (0/1), noms de colonnes en anglais, valeurs d'enum (catégories, types de mouvement) et où elles sont définies.

### Contraintes d'intégrité
> Les `CHECK`, `UNIQUE` et clés étrangères ajoutés à la main dans le script de création, et ce que chacun protège.

## 7. Règles métier

> Liste numérotée des règles (ex : une sortie est refusée si le stock est insuffisant, un produit archivé ne reçoit plus de mouvement, comment fonctionne un transfert réserve → magasin, comment se calcule le seuil d'alerte).

## 8. Transactions et cohérence

> Où commence et finit une transaction, qui la pilote, ce qui se passe en cas d'erreur (rollback). Explique le principe de l'audit de cohérence entre les compteurs et la somme des mouvements, et comment gérer le stock initial.

## 9. Gestion des erreurs et logs

> Les deux familles d'erreurs (métier / inattendues), les exceptions personnalisées, ce que voit l'utilisateur, ce qui va dans le fichier de log.

## 10. Exemple de flux complet

> Déroule pas à pas une sortie de stock, du clic dans l'interface jusqu'à la base, puis le retour à l'écran. Fais-le aussi pour un cas d'erreur (stock insuffisant).

## 11. Tests

> Ce qui est testé (surtout les services), comment (base en mémoire, jeux de données), comment lancer les tests, ce qui n'est pas testé et pourquoi.

## 12. Décisions de conception

> Un tableau ou une liste : décision, alternatives envisagées, raison du choix. À remplir au fil du projet.

| Décision | Alternatives | Pourquoi |
|---|---|---|
| Architecture en couches | MVC classique | |
| Un compteur par ligne de `stocks` ou deux | | |
| Dates en timestamp entier | Texte ISO 8601 | |
| Enums gérés en Python | Tables de référence | |
| Table `alert` séparée | Colonne dans `product` | |
| Archivage (`is_active`) plutôt que suppression | | |
| Compteur dénormalisé + audit par les mouvements | Calcul à la volée | |

## 13. Limites et pistes d'amélioration

> Ce qui n'est pas fait volontairement (commandes fournisseurs, rôles utilisateurs, import CSV...) et ce que tu ferais avec plus de temps.