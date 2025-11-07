# modules/livre.py
class Livre:
    """
    Représente un livre unique.
    Ne gère pas la collection complète (c'est le rôle de Bibliotheque).
    """

    def __init__(self, id_livre, titre, auteur, categorie, statut):
        self.id_livre = id_livre
        self.titre = titre
        self.auteur = auteur
        self.categorie = categorie
        self.statut = statut  # "Disponible" / "Emprunté"

    # --------- Méthodes d'instance (concernent UN livre) ---------
    def modifier(self, titre=None, auteur=None, categorie=None, statut=None):
        """Met à jour les champs fournis pour CE livre."""
        if titre is not None:
            self.titre = titre
        if auteur is not None:
            self.auteur = auteur
        if categorie is not None:
            self.categorie = categorie
        if statut is not None:
            self.statut = statut
        return self

    def to_dict(self):
        """Sérialisation simple (catalogue complet)."""
        return {
            "id_livre": self.id_livre,
            "titre": self.titre,
            "auteur": self.auteur,
            "categorie": self.categorie,
            "statut": self.statut,
        }

    @classmethod
    def from_dict(cls, d):
        """Recrée un objet Livre depuis un dict (pour import catalogue)."""
        return cls(
            id_livre=d["id_livre"],
            titre=d["titre"],
            auteur=d["auteur"],
            categorie=d["categorie"],
            statut=d["statut"],
        )

    def __repr__(self):
        return f"<Livre {self.id_livre} - {self.titre} ({self.auteur}) [{self.statut}]>"




      
        

    


