from modules.livre import Livre
import hashlib

class Utilisateur:
    _id_counter = 1
    def __init__(self, nom, email, password):
        self.uuid : int = self._id_counter
        self._id_counter += 1

class Lecteur(Utilisateur):
    def __init__(self, nom, email, password):
        self.nom : str = nom
        self.email : str = email
        self.password : str = hashlib.sha256(password)
        self.role = 1

    def emprunter(self):
        id_livre = int(input("\nID du livre à emprunter \n -> "))
        # Vérifier que le livre est disponible
        Livre.modifier(id_livre, statut="emprunte")

    def rendre(self):
        id_livre = int(input("\nID du livre à rendre \n -> "))
        # Vérifier que le livre est emprunté par la personne
        Livre.modifier(id_livre, statut="disponible")

class Bibliothecaire(Utilisateur):
    def __init__(self, nom, email, password):
        self.nom : str = nom
        self.email : str = email
        self.password : str = hashlib.sha256(password)
        self.role = 2

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