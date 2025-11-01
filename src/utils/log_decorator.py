import logging.config
import numbers

from functools import wraps


class LogIndetation:
    """Pour indenter les logs lorsque l'on rentre dans une nouvelle méthode"""

    current_indentation = 0

    @classmethod
    def increase_indentation(cls):
        """Ajouter une indentation"""
        cls.current_indentation += 1

    @classmethod
    def decrease_indentation(cls):
        """Retirer une indentation"""
        cls.current_indentation -= 1

    @classmethod
    def get_indentation(cls):
        """Obtenir l'indentation"""
        return "    " * cls.current_indentation


def log(func):
    """Création d'un décorateur nommé log
    Lorsque ce décorateur est appliqué à une méthode, cela affichera dans les logs :
    - l'appel de cette méthode avec les valeurs de paramètres
    - la sortie retournée par cette méthode
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(__name__)

        LogIndetation.increase_indentation()
        indentation = LogIndetation.get_indentation()

        # Recuperation des parametres de la methode
        class_name = args[0].__class__.__name__ if args else ""
        method_name = func.__name__
        args_list = list(
            [str(arg) if not isinstance(arg, numbers.Number) else arg for arg in args[1:]]
            + list(kwargs.values())
        )

        # pour cacher les mots de passe
        param_names = func.__code__.co_varnames[1: func.__code__.co_argcount]
        for i, v in enumerate(param_names):
            if v in ["password", "passwd", "pwd", "pass", "mot_de_passe", "mdp"]:
                args_list[i] = "*****"

        # Transforme en tuple pour avoir un affichage avec des parentheses
        args_list = tuple(args_list)

        # Affichage dans le fichier de log
        logger.info(f"{indentation}{class_name}.{method_name}{args_list} - DEBUT")
        result = func(*args, **kwargs)
        logger.info(f"{indentation}{class_name}.{method_name}{args_list} - FIN")

        # Reduction de l affichage de la sortie si trop longue
        if isinstance(result, list):
            result_str = str([str(item) for item in result[:3]])
            result_str += " ... (" + str(len(result)) + " elements)"
        elif isinstance(result, dict):
            result_str = [(str(k), str(v)) for k, v in result.items()][:3]
            result_str += " ... (" + str(len(result)) + " elements)"
        elif isinstance(result, str) and len(result) > 50:
            result_str = result[:50]
            result_str += " ... (" + str(len(result)) + " caracteres)"
        else:
            result_str = str(result)

        logger.info(f"{indentation}   └─> Sortie : {result_str}")

        LogIndetation.decrease_indentation()

        return result

    return wrapper
