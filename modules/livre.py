class Livre:
    _id_counter = 1
    _livres = []
    _bibliothque = []

    def __init__(self,titre, auteur, categorie, statut):
        # ID unique auto-incrémenté (attribut de classe)
        self.id_livre = Livre._id_counter
        Livre._id_counter += 1

        # Attributs d'instance : on garde les valeurs reçues
        self.titre = titre
        self.auteur = auteur
        self.categorie = categorie
        self.statut = statut

        # Enregistrer automatiquement dans le "catalogue"
        Livre._livres.append(self)


    @classmethod
    def add(cls, titre, auteur, categorie, statut):
        """Crée un livre et l’ajoute à la bibliothèque."""
        return cls(titre, auteur, categorie, statut)

    @classmethod
    def historique(cls):
        """ Histoirque d'ajout des livres """
        for livre in cls._livres:
            print(f"ID : {livre.id_livre}")
            print(f"Titre       : {livre.titre}")
            print(f"Auteur      : {livre.auteur}")
            print(f"Catégorie   : {livre.categorie}")
            print(f"Statut      : {livre.statut}")
            print("-" * 50)



    @classmethod
    def resume_global(cls):
        """Affiche un résumé complet pour tous les titres présents."""
        resume = {}

        for livre in cls._livres:
            titre = livre.titre.strip().lower()
            if titre not in resume:
                resume[titre] = {
                    "titre": livre.titre,
                    "auteurs": set(),
                    "nb_total": 0,
                    "nb_disponible": 0,
                    "nb_emprunte": 0
                }

            resume[titre]["nb_total"] += 1
            resume[titre]["auteurs"].add(livre.auteur)

            if livre.statut.strip().lower() == "disponible":
                resume[titre]["nb_disponible"] += 1
            elif livre.statut.strip().lower() == "emprunté":
                resume[titre]["nb_emprunte"] += 1

        # Affichage propre du résumé
        print("\nRésumé global de la bibliothèque :")
        for titre, infos in resume.items():
            print(f"\n{infos['titre']}")
            print(f"   Auteurs       : {', '.join(infos['auteurs'])}")
            print(f"   Total         : {infos['nb_total']}")
            print(f"   Disponibles   : {infos['nb_disponible']}")
            print(f"   Empruntés     : {infos['nb_emprunte']}")

    @classmethod
    def supp(cls,id_livre):
        for i, livre in enumerate(cls._livres):
            if livre.id_livre == id_livre:
                del cls._livres[i]
                print(f"Livre id {id_livre} supprimé.")
                return True
        print(f"Aucun livre trouvé avec l'id {id_livre}.")
        return False

    @classmethod
    def modifier(cls, id_livre, titre=None, auteur=None, categorie=None,
                statut=None):
        """
        Met à jour les informations d'un livre existant à partir de son ID.
        Seuls les champs fournis sont modifiés.
        """
        for livre in cls._livres:
            if livre.id_livre == id_livre:
                # Mise à jour uniquement si une nouvelle valeur est fournie
                if titre is not None:
                    livre.titre = titre
                if auteur is not None:
                    livre.auteur = auteur
                if categorie is not None:
                    livre.categorie = categorie
                if statut is not None:
                    livre.statut = statut

                print(f"Livre {id_livre} mis à jour avec succès.")
                return livre

        print(f"Aucun livre trouvé avec l'ID {id_livre}.")
        return None

        
    
        
   
            
            

                

# Démo

livre1 = Livre.add("1984", "George Orwell", "Roman", "Disponible")
livre2 = Livre.add("Dune", "Frank Herbert", "Science-Fiction", "Emprunté")
livre3 = Livre.add("Le Petit Prince", "Antoine de Saint-Exupéry", "Conte", "Disponible")
livre4 = Livre.add("Le Petit Prince", "Antoine de Saint-Exupéry", "Conte", "Emprunté")


# Livre.supp(1)
Livre.resume_global()
Livre.modifier(2, statut="Disponible")
Livre.historique()




      
        

    


