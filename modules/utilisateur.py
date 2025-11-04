class Utilisateur:
    _id_counter = 1
    def __init__(self, nom, email):
        self.uuid : int = self._id_counter
        self._id_counter += 1
        self.nom : str = nom
        self.email : str = email

class Lecteur(Utilisateur):
    def emprunter(self, Livre):
        Livre.add()
    def rendre(self, Livre):
        Livre.add()

class Bibliothecaire(Utilisateur):
    def ajouter(self, Livre):
        
    def modifier(self, Livre):
        pass
    def supprimer(self, Livre):
        pass

utilisateur = Utilisateur(14, "bob")