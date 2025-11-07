from modules.bibliotheque import Bibliotheque as B

B.ajouter_livre("1984", "George Orwell", "Roman", "Disponible")
B.ajouter_livre("Dune", "Frank Herbert", "Science-Fiction", "Emprunté")
B.ajouter_livre("Le Petit Prince", "Antoine de Saint-Exupéry", "Conte", "Disponible")
B.modifier_livre(
    2,                   # id du livre à modifier
    statut="Disponible", # nouveau statut
    categorie="Roman SF" # tu peux modifier plusieurs champs à la fois
)
B.historique()
B.resume_global(as_print=True)

B.save_resume_json()
B.save_catalog_json()
