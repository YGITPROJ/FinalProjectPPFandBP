#
#
#
try:
    from colorama import Fore, Style, init

    init(autoreset=True)

    SUCCESS = Fore.GREEN + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    INFO = Fore.CYAN + Style.BRIGHT
    HIGHLIGHT = Fore.MAGENTA + Style.BRIGHT
    PROMPT = Fore.WHITE + Style.BRIGHT

    _COLORS_ENABLED = True

except ImportError:

    class DummyStyle:
        def __getattr__(self, name):
            return ""

    Fore = DummyStyle()
    Style = DummyStyle()

    SUCCESS = ""
    ERROR = ""
    WARNING = ""
    INFO = ""
    HIGHLIGHT = ""
    PROMPT = ""

    _COLORS_ENABLED = False


def are_colors_enabled():
    """Повертає True, якщо colorama завантажено успішно."""
    if not _COLORS_ENABLED:
        print("(Warning: 'colorama' package not found. Colors will be disabled.)")
        print("(Run 'pip install colorama' to enable colors.)")
    return _COLORS_ENABLED
