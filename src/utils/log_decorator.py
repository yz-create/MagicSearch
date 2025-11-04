import logging.config
import numbers
from functools import wraps


class LogIndentation:
    """To indent logs when entering a new method"""

    current_indentation = 0

    @classmethod
    def increase_indentation(cls):
        """Increase the indentation level"""
        cls.current_indentation += 1

    @classmethod
    def decrease_indentation(cls):
        """Decrease the indentation level"""
        cls.current_indentation -= 1

    @classmethod
    def get_indentation(cls):
        """Get the current indentation as spaces"""
        return "    " * cls.current_indentation


def log(func):
    """Decorator to log method calls

    When applied to a method, this decorator logs:
    - the call to the method with parameter values
    - the output returned by the method
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(__name__)

        LogIndentation.increase_indentation()
        indentation = LogIndentation.get_indentation()

        # Retrieve method parameters
        class_name = args[0].__class__.__name__ if args else ""
        method_name = func.__name__
        args_list = list(
            [str(arg) if not isinstance(arg, numbers.Number) else arg for arg in args[1:]]
            + list(kwargs.values())
        )

        # Hide passwords
        param_names = func.__code__.co_varnames[1: func.__code__.co_argcount]
        for i, v in enumerate(param_names):
            if v in ["password", "passwd", "pwd", "pass", "mot_de_passe", "mdp"]:
                args_list[i] = "*****"

        # Convert to tuple for display
        args_list = tuple(args_list)

        # Log method entry
        logger.info(f"{indentation}{class_name}.{method_name}{args_list} - START")
        result = func(*args, **kwargs)
        logger.info(f"{indentation}{class_name}.{method_name}{args_list} - END")

        # Shorten output display if too long
        if isinstance(result, list):
            result_str = str([str(item) for item in result[:3]])
            result_str += f" ... ({len(result)} elements)"
        elif isinstance(result, dict):
            result_str = [(str(k), str(v)) for k, v in result.items()][:3]
            result_str += f" ... ({len(result)} elements)"
        elif isinstance(result, str) and len(result) > 50:
            result_str = result[:50] + f" ... ({len(result)} characters)"
        else:
            result
