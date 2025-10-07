from abstract_filter.py import AbstractFilter

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
