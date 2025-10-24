from abstract_filter.py import AbstractFilter

class FilterNumeric(AbstractFilter):
    
    _TYPE_NAME = "filter_num"

    def filter(self, variable_filtered: str, type_of_filtering: str, filtering_value) -> list:
        """ Filters the magic TG database along a numerical variable 
        The filter is applied along a numerical variable defined using the "variable_filtered" and
        a certain criterion depending on the "type_of_filtering" and the "filtering_value"
        
        Parameters
        ----------
        variable_filtered :
            (this parameter is not defined with an int type because the variables toughness and power have some str values 
            despite being numerical variables)
            is a numerical variable chosen among the following : "power", "toughness"

        type_of_filtering: str
            defines the way we want to filter the variable. It can only take "higher_than", "lower_than" or "equal_to" as input
            higher_than meaning that the filter will select all cards with a value in the variable_filtered higher than the filtering_value
            lower_than meaning that the filter will select all cards with a value in the variable_filtered lower than the filtering_value
            equal_to meaning that the filter will select all cards with a value in the variable_filtered equal to the filtering_value

        filtering_value: str
            is the value (corresponding to the variable_filtered) we want to filter our database along

        returns
        -------
            list : the list of all the cards that fit the chosen criteria
        """
        return 








# est ce que pour mettre en place les filtres ou non je mettrais pas un attribut 0. enabled qui est un booléen qui dit si on met ce filtre ou pas

# je veux faire chaque filtre avec deux attrivbut 1. filtre qui garde que des valeurs au dessus, que des valeurs en dessous ou des valeurs égales à
#2. le chiffre

# il  y aura deux filtres un sur la variable power et un sur la variable toughness QUI DOIVENT ËTRE CONVERTIES EN STR


# manaValue 
class FilterNum(AbstractFilter):
    _TYPE_NAME = "filter_num"
    def add_value_num(self, treshhold_value :int )-> filter_num: # ici  j'ai mis int au lieu de float et je ne crois pas 
        #que ca rende un booléen, je pense que ça rend un filter num 

    def add_filter(self, raw_name : str, value: int) -> filter_num: # je pense que ça rend un filter num 
        
