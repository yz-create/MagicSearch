from dao.card_dao import CardDao
from business_object.card import Card

# Créer une carte simple
my_card = Card(
    id_card=None,  # Sera généré automatiquement
    embedded=[0.1, 0.2, 0.3],
    layout="normal",
    name="Lightning Bolt",
    type_line="Instant",
    ascii_name="Lightning Bolt",
    colors=["R"],
    color_identity=["R"],
    mana_cost="{R}",
    mana_value=1.0,
    text="Lightning Bolt deals 3 damage to any target.",
    types=["Instant"],
    subtypes=[],
    supertypes=[]
)

# L'ajouter à la base
dao = CardDao()
if dao.create_card(my_card):
    print("✅ Carte ajoutée avec succès !")
else:
    print("❌ Erreur lors de l'ajout")