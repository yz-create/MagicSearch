from abstract_filter.py import AbstractFilter
# je veux faire un filtre avec deux attrivbut 1. str catégorique qu
class FilterNum(AbstractFilter):
    _TYPE_NAME = "filter_num"
    def add_value_num(self, treshhold_value :int )-> filter_num: # ici  j'ai mis int au lieu de float et je ne crois pas 
        #que ca rende un booléen, je pense que ça rend un filter num 

    def add_filter(self, raw_name : str, value: int) -> filter_num: # je pense que ça rend un filter num 
