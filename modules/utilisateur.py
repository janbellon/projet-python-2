from modules.livre import Livre
import hashlib
from modules.bibliotheque import Bibliotheque
import json

class Utilisateur:
    id_counter = 1

    def generer_uuid(self):
        uuid = Utilisateur.id_counter
        Utilisateur.id_counter += 1
        return uuid

class Lecteur(Utilisateur):
    def __init__(self, nom, email, password):
        self.role = 1
        self.nom : str = nom
        self.email : str = email
        self.password : str = password
        self.uuid : int = self.generer_uuid()

    def emprunter(self):
        try:
            id_livre = int(input("\nID du livre à emprunter \n -> "))
            livre = Bibliotheque.trouver_par_id(id_livre)
            if livre.statut.lower() == "disponible":
                livre.modifier(statut="Emprunté")
                print(f"Livre {livre.titre} emprunté !")
                return
            else:
                print("Livre indisponible")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")

    def rendre(self):
        try:
            id_livre = int(input("\nID du livre à rendre \n -> "))
            livre = Bibliotheque.trouver_par_id(id_livre)
            if livre.statut.lower() == "disponible":
                print("Livre déjà rendu")
                return
            else:
                livre.modifier(statut="Disponible")
                print(f"Livre {livre.titre} rendu avec succès !")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")

class Bibliothecaire(Utilisateur):
    def __init__(self, nom, email, password):
        self.role = 2
        self.nom : str = nom
        self.email : str = email
        self.password : str = password
        self.uuid : int = self.generer_uuid()

    def ajouter(self):
        try:
            titre = input(f"\nTitre du livre \n -> ")
            auteur = input(f"\nAuteur \n -> ")
            categorie = input(f"\nCatégorie \n -> ")
            livre = Bibliotheque.ajouter_livre(titre, auteur, categorie)
            print(f"Livre {livre.titre} écrit par {livre.auteur} dans la catégorie {livre.categorie} ajouté avec succès.")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")

    def modifier(self):
        try:
            id_livre = int(input("\nID du livre à modifier \n -> "))
            titre = input(f"\nTitre du livre ({Livre.Livre.titre}) (Entrée pour passer) \n -> ") or None
            auteur = input(f"\nAuteur ({Livre.Livre.auteur}) (Entrée pour passer) \n ->") or None
            categorie = input(f"\nCatégorie ({Livre.categorie}) (Entrée pour passer) \n ->") or None
            statut = input(f"\nStatut ({Livre.statut}) (Entrée pour passer) \n ->") or None
            Livre.modifier(id_livre, titre, auteur, categorie, statut)
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")   

    def supprimer(self):
        try:
            id_livre = int(input("\nID du livre à supprimer \n -> "))
            Bibliotheque.supprimer_livre(id_livre)
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")  

class Admin(Utilisateur):
    def __init__(self, nom, email, password):
        self.role = 99
        self.nom : str = nom
        self.email : str = email
        self.password : str = password
        self.uuid : int = self.generer_uuid()

    def save_users_json(filename, utilisateurs):
        """Sauvegarde les Utilisateurs (rechargeable)."""
        try:
            payload = {
                "id_counter": Utilisateur.id_counter,
                "users": [
                    {
                        "role": utilisateurs[u].role,
                        "nom": utilisateurs[u].nom,
                        "email": utilisateurs[u].email,
                        "password": utilisateurs[u].password
                    } for u in utilisateurs]
            }
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=4)
            print(f"Utilisateurs sauvegardés : {filename}")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")  

    def load_users_json(filename, utilisateurs):
        """Recharge le CATALOGUE COMPLET (garde les IDs cohérents)."""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                payload = json.load(f)
        except Exception as e:
            print(f"Erreur lors de l'ouverture : {e}")
            return

        for u in payload.get("users", []):
            nom = u["nom"]
            email = u["email"]
            pwd = u["password"]
            match u["role"]:
                case 1:
                    u = Lecteur(nom, email, pwd)
                    utilisateurs[u.uuid] = u
                    print(f"Lecteur créé → ID {u.uuid} | {u.nom} <{u.email}> (role=Lecteur)")
                case 2:
                    u = Bibliothecaire(nom, email, pwd)
                    utilisateurs[u.uuid] = u
                    print(f"Bibliothécaire créé → ID {u.uuid} | {u.nom} <{u.email}> (role=Bibliothecaire)")
                case 99:
                    u = Admin(nom, email, pwd)
                    utilisateurs[u.uuid] = u
                    print(f"Administrateur créé → ID {u.uuid} | {u.nom} <{u.email}> (role=Admin)")  

        print(f"Utilisateurs chargés depuis : {filename}")
