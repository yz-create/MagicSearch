class Card:
    def __init__(
        self,
        id_card: int,
        layout: str,
        name: str,
        type_line: str,
        embedded: list = None,
        short_embedded: list = None,
        ascii_name: str = None,
        color_identity: list = None,
        color_indicator: list = None,
        colors: list = None,
        converted_mana_cost: float = None,
        defense: int = None,
        edhrec_rank: int = None,
        edhrec_saltiness: float = None,
        face_mana_value: float = None,
        face_name: str = None,
        first_printing: str = None,
        foreign_data: list = None,
        hand: int = None,
        has_alternative_deck_limit: bool = None,
        is_funny: bool = None,
        is_reserved: bool = None,
        keywords: list = None,
        leadership_skills: dict = None,
        legalities: dict = None,
        life: int = None,
        loyalty: str = None,
        mana_cost: str = None,
        mana_value: float = None,
        power: str = None,
        printings: list = None,
        purchase_urls: dict = None,
        rulings: list = None,
        side: str = None,
        subtypes: list = None,
        supertypes: list = None,
        text: str = None,
        toughness: str = None,
        types: list = None
    ):
        self.ascii_name = ascii_name
        self.color_identity = color_identity
        self.color_indicator = color_indicator
        self.colors = colors
        self.converted_mana_cost = converted_mana_cost
        self.edhrec_rank = edhrec_rank
        self.edhrec_saltiness = edhrec_saltiness
        self.face_mana_value = face_mana_value
        self.face_name = face_name
        self.hand = hand
        self.has_alternative_deck_limit = has_alternative_deck_limit
        self.id_card = id_card
        self.is_funny = is_funny
        self.is_reserved = is_reserved
        self.keywords = keywords or []
        self.layout = layout
        self.leadership_skills = leadership_skills or {}
        self.legalities = legalities or {}
        self.life = life
        self.loyalty = loyalty
        self.mana_cost = mana_cost
        self.mana_value = mana_value
        self.name = name
        self.power = power
        self.printings = printings or []
        self.purchase_urls = purchase_urls or {}
        self.rulings = rulings or []
        self.side = side
        self.subtypes = subtypes or []
        self.supertypes = supertypes or []
        self.text = text
        self.toughness = toughness
        self.type_line = type_line
        self.types = types or []
        self.defense = defense
        self.first_printing = first_printing
        self.foreign_data = foreign_data or []
        self._embedded = embedded
        self._short_embedded = short_embedded

    def show_card(self):
        card_dict = {"id_card": self.id_card,
                     "layout": self.layout,
                     "name": self.name,
                     "type_line": self.type_line}
        list_columns = [
            "color_identity", "color_indicator", "colors", "keywords", "printings",
            "rulings", "subtypes", "supertypes", "types"
            ]
        dict_columns = ["leadership_skills", "legalities", "purchase_urls"]
        other_columns = [
            "ascii_name", "converted_mana_cost", "defense", "edhrec_rank", "edhrec_saltiness",
            "face_mana_value", "face_name", "first_printing", "hand", "has_alternative_deck_limit",
            "is_funny", "is_reserved", "life", "loyalty", "mana_cost", "mana_value", "power",
            "side", "text", "toughness"
        ]
        for column in other_columns:
            if getattr(self, column) is not None:
                card_dict[column] = getattr(self, column)
        for column in list_columns:
            if len(getattr(self, column)) != 0:
                card_dict[column] = getattr(self, column)
        if len(self.foreign_data) != 0:
            foreign_data = []
            for language in self.foreign_data:
                language_data = {}
                for key in language:
                    if language[key] is not None:
                        language_data[key] = language[key]
                foreign_data.append(language_data)
            card_dict["foreignData"] = foreign_data
        for column in dict_columns:
            column_dict = {}
            for key in getattr(self, column):
                if getattr(self, column)[key]:
                    column_dict[key] = getattr(self, column)[key]
            if column_dict != {}:
                card_dict[column] = column_dict
        return card_dict

    def __str__(self):
        return f"Card(name={self.name}, id={self.id_card})"

    def __repr__(self):
        return f"Card(name={self.name}, id={self.id_card})"
