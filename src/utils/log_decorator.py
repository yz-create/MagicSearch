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
    """Decorator to log method calls safely for instance methods."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(__name__)

        # Determine class name if first arg is 'self'
        class_name = args[0].__class__.__name__ if args else ""
        method_name = func.__name__

        # Build argument list, hide passwords
        args_list = []
        for i, arg in enumerate(args[1:] if args else args):
            args_list.append("*****" if i == 1 else str(arg))
        for k, v in kwargs.items():
            args_list.append("*****" if k in ["password", "passwd", "pwd", "pass", "mdp"] else str(v))
        args_list = tuple(args_list)

        logger.info(f"{class_name}.{method_name}{args_list} - START")
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"{class_name}.{method_name} raised an exception")
            raise

        # Shorten output for logging
        if isinstance(result, list):
            result_str = str([str(item) for item in result[:3]])
            if len(result) > 3:
                result_str += f" ... ({len(result)} elements)"
        elif isinstance(result, dict):
            result_str = str(list(result.items())[:3])
            if len(result) > 3:
                result_str += f" ... ({len(result)} elements)"
        elif isinstance(result, str) and len(result) > 50:
            result_str = result[:50] + f" ... ({len(result)} characters)"
        else:
            result_str = str(result)

        logger.info(f"{class_name}.{method_name}{args_list} - END └─> Output: {result_str}")

        return result

    return wrapper