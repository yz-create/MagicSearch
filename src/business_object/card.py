class Card:
    def __init__(self, id_card: int, name: str, embedded: float):
        self._id_card = id_card
        self._name = name
        self._embedded = embedded

    def show_card(self) -> str:
        """
        Return the official (or informal) representation.


        Commentaire : 
        - peut être appeler la méthode __repr__ (ou __str__) ?
        - choisir les attribut à présenter
        """
        return f"MagicTG Card : {self._name}" 

    def get_embedded(self) -> list[float]:
        """
        Return the embedded vector of the card.
        """
        return [float(x.strip()) for x in self._embedded.split(",")]

