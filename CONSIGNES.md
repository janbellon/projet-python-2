# Projet Python – Système de gestion d’une bibliothèque numérique
## Objectif général :
Concevoir et développer une application Python permettant de gérer une bibliothèque
numérique complète, incluant :
- la gestion des livres, des utilisateurs et des emprunts ;
- la recherche et le filtrage avancés ;
Le projet doit exploiter toutes les notions fondamentales du langage (structures de données,
conditions, boucles, fonctions) et appliquer rigoureusement la POO (classes, héritage,
encapsulation, polymorphisme).
# 1. Spécifications fonctionnelles
## 1.1 Gestion des livres
L’application doit permettre :
- d’ajouter, modifier et supprimer un livre ;
- d’afficher la liste complète des livres ;
- de rechercher un livre par :
    - titre,
    - auteur,
    - catégorie,
    - disponibilité (emprunté ou non).
Chaque livre doit comporter :
- un ID unique (auto-incrémenté),
- un titre,
- un auteur,
- une catégorie (ex. Roman, Science, Informatique…),
- un nombre d’exemplaires disponibles,
- un statut (disponible / emprunté).
## 1.2 Gestion des utilisateurs
L’application doit gérer différents types d’utilisateurs :
- Lecteurs : peuvent emprunter et rendre des livres ;
- Bibliothécaires : peuvent ajouter/modifier/supprimer des livres.
Chaque utilisateur doit comporter :
- un identifiant unique,
- un nom complet,
- un email,
- un type d’utilisateur (Lecteur ou Bibliothécaire).
Implémentez ces rôles à l’aide de l’héritage de classes (Utilisateur → Lecteur,
Bibliothécaire).
## 1.3 Emprunts et retours
- Un lecteur peut emprunter un livre s’il est disponible.
- Lorsqu’un livre est emprunté :
    - le nombre d’exemplaires disponibles diminue ;
    - l’application enregistre la date d’emprunt.
- Lorsqu’un livre est rendu :
    - le nombre d’exemplaires disponibles augmente ;
    - l’application met à jour le statut du livre.
Utilisez un set ou un dictionnaire pour stocker les emprunts (clé = ID du lecteur, valeur =
liste de livres empruntés).
# 2. Exigences techniques
## 2.1 Structures de données
- Utilisez listes, tuples, sets et dictionnaires selon le besoin :
    - liste des livres,
    - dictionnaire des utilisateurs,
    - set pour les livres empruntés par un lecteur, etc.
## 2.2 Contrôle du flux
- Conditions pour vérifier les rôles et les statuts ;
- Boucles pour afficher les listes, naviguer dans le menu, etc.
## 2.3 Fonctions
- Créez des fonctions modulaires pour :
    - ajouter un livre,
    - rechercher un livre,
    - afficher les emprunts, etc.
## 2.4 POO
Créez au minimum les classes suivantes :
```python
class Livre:
pass
class Utilisateur:
pass
class Lecteur(Utilisateur):
pass
class Bibliothecaire(Utilisateur):
pass
class Bibliotheque:
pass
```
La classe Bibliotheque sera le cœur du système, centralisant les listes et gérant toutes les
opérations.
## 2.5 Gestion des erreurs
- Empêcher l’emprunt de livres non disponibles.
- Vérifier les doublons d’ID ou de titre.
# 3. Fonctionnalités avancées
1. Tri et filtrage avancé (par titre, auteur, disponibilité…).
2. Statistiques : nombre total de livres, de lecteurs, de livres empruntés.
3. Interface en ligne de commande dynamique avec un menu principal :
4. 1. Gérer les livres
5. 2. Gérer les utilisateurs
6. 3. Gérer les emprunts
7. 4. Quitter
8. Date d’emprunt / retour automatique avec le module datetime.
9. Système de pénalité : afficher un message si un livre est gardé plus de 14 jours.
# Livrables attendus
- Un dossier contenant :
    - Le code source complet (.py)
    - Un court fichier README.txt expliquant comment exécuter le programme.