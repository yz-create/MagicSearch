from abc import ABC, abstractmethod


#checker la bdd pour comprendre à quoi sert row name donc add_row_name
#comprendre à quoi

class AbstractFilter(ABC):
    def __init__(self, row_name :str): 
        self.row_name = row_name

    def add_row_name(self, row_name:str):
        """
        Parameter: 
        ---------
        row_name : str
            
        Returns: 
        --------
        bool
        """

    def get_filter(self):
        """
        """

    #@abstractmethod
    #   def add_value_num(self): # ici problème car les méthodes diffèrent notamment dans leurs attributs
        #pass

    
    #@abstractmethod
    
    #def add_filter(self, row_name : str, value):# value peut être str pour filter cat ou int pour
         # même problème : est ce que c'est des méthodes abstraites ?