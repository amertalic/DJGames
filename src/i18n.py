from typing import Callable, Dict
import importlib


def get_translation(language_code: str) -> Callable:
    """
    Returns a translation function for the specified language.
    Falls back to Bosnian if the language is not supported.
    """
    try:
        # Try to import the requested language module
        lang_module = importlib.import_module(f"locales.{language_code}")
        translations = lang_module.translations
    except (ImportError, AttributeError):
        # Fall back to Bosnian if the language is not supported
        lang_module = importlib.import_module("locales.bs")
        translations = lang_module.translations

    def translate(key: str, **kwargs) -> str:
        """
        Translates a key into the selected language.
        Falls back to the key itself if the translation is not available.
        Allows for parameter substitution with {param_name} syntax.
        """
        if key in translations:
            text = translations[key]
            # Replace any parameters
            for param_name, param_value in kwargs.items():
                text = text.replace(f"{{{param_name}}}", str(param_value))
            return text
        return key

    return translate
