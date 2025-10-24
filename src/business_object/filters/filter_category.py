from abstract_filter.py import AbstractFilter


class FilterCategory(AbstractFilter):
    
    _TYPE_NAME = "filter_cat"

    # pas de __init__ parce que ya la classe abstraite
    def filter(self, variable_filtered: str, type_of_filtering="positive": str, filtering_value: str) -> list:
        """ Filters the magic TG database along a categorical variable 
        The filter is applied along a categorical variable defined using the "variable_filtered" and
        a certain criterion depending on the "type_of_filtering" and the "filtering_value"
        
        Parameters
        ----------
        variable_filtered: str
            is a categorical variable chosen among the following :

        type_of_filtering: str
            defines the way we want to filter the variable.
            It can only take "positive" or "negative" as an input
            positive meaning that the filter will select all cards
            with a value in the variable_filtered equal to the filtering_value
            negative meaning that the filter will select all cards
            with a value in the variable_filtered different from the filtering_value
            
        filtering_value: str
            is the value (corresponding to the variable_filtered)
            we want to filter our database along

        returns
        -------
            list : the list of all the cards that fit the chosen criteria
        """
        return 





# est ce que pour mettre en place les filtres ou non je mettrais pas un attribut 0. enabled qui est un booléen qui dit si on met ce filtre ou pas
# je voudrais que ce filtre permettre 1. toutes les cartes d'une catégorie ou 2. toutes les cartes SAUF celles de cette catégorie sur ça je pense que 
# je vais faire une seule méthode avec deux attributs 1. negative or positive filter avec comme setting de base positive filter
#2. un attribut catégorie. Le filtre catégorie concerne les espèces  donc la variable types  je crois
# peut être qu'il faut faire en sorte que sur l'API les utilisateurs aient accès a une liste des catégories
# est ce qu'on peut agréger des filtres  = mettre un filtre puis un deuxième ?



class FilterCategory(AbstractFilter):
    
    _TYPE_NAME = "filter_cat"
    #def __init__(self, value :str): #pourquoi
    #    self._value : 
    #def add_value_num(self, )-> filter_cat: 

    #def add_filter(self, raw_name : str) ->filter_cat: