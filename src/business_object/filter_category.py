from abstract_filter.py import AbstractFilter
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