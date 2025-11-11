from modules.livre import Livre
import hashlib
from modules.bibliotheque import Bibliotheque

class Utilisateur:
    _id_counter = 1

    def generer_uuid(self):
        uuid = Utilisateur._id_counter
        Utilisateur._id_counter += 1
        return uuid

class Lecteur(Utilisateur):
    def __init__(self, nom, email, password):
        self.role = 1
        self.nom : str = nom
        self.email : str = email
        self.password : str = hashlib.sha256(password.encode())
        self.uuid : int = self.generer_uuid()

    def emprunter(self):
        id_livre = int(input("\nID du livre à emprunter \n -> "))
        livre = Bibliotheque.trouver_par_id(id_livre)
        if livre.statut == "disponible":
            livre.modifier(statut="emprunté")
            return
        else:
            print("Livre indisponible")

    def rendre(self):
        id_livre = int(input("\nID du livre à rendre \n -> "))
        livre = Bibliotheque.trouver_par_id(id_livre)
        if livre.statut == "disponible":
            print("Livre déjà rendu")
            return
        else:
            livre.modifier(statut="disponible")

class Bibliothecaire(Utilisateur):
    def __init__(self, nom, email, password):
        self.role = 2
        self.nom : str = nom
        self.email : str = email
        self.password : str = hashlib.sha256(password.encode())
        self.uuid : int = self.generer_uuid()

    def ajouter(self):
        titre = input(f"\nTitre du livre \n -> ")
        auteur = input(f"\nAuteur \n ->")
        categorie = input(f"\nCatégorie \n ->")
        statut = input(f"\nStatut \n ->")
        livre = Livre.add(titre, auteur, categorie, statut)
        print(f"Livre ({livre.titre}, {livre.auteur}, {livre.categorie}, {livre.statut}) ajouté avec succès.")
    
    def modifier(self):
        id_livre = int(input("\nID du livre à modifier \n -> "))
        titre = input(f"\nTitre du livre ({Livre.Livre.titre}) (Entrée pour passer) \n -> ") or None
        auteur = input(f"\nAuteur ({Livre.Livre.auteur}) (Entrée pour passer) \n ->") or None
        categorie = input(f"\nCatégorie ({Livre.categorie}) (Entrée pour passer) \n ->") or None
        statut = input(f"\nStatut ({Livre.statut}) (Entrée pour passer) \n ->") or None
        Livre.modifier(id_livre, titre, auteur, categorie, statut)
    
    def supprimer(self):
        id_livre = int(input("\nID du livre à supprimer \n -> "))
        Livre.supp(id_livre)

class Admin(Utilisateur):
    def __init__(self, nom, email, password):
        self.role = 99
        self.nom : str = nom
        self.email : str = email
        self.password : str = hashlib.sha256(password.encode())
        self.uuid : int = self.generer_uuid()
