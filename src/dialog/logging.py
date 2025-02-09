import logging
import re
import sys
from contextlib import contextmanager
from logging import LogRecord
from typing import Dict, Literal, Union

from rich.logging import RichHandler
from rich.text import Text

from . import strings, console


__all__ = ["LOG_LEVEL", "silence_loggers"]


SILENCED_LOGGERS = [
    "asyncio",
    "blib2to3",
    "pip._internal",
    "rich",
    "urllib3",
]


# --- Logging configuration ----------------------------------------------------
# Infer log level from command line arguments or default to INFO

LOG_LEVEL = "INFO"

__log_level = re.search(
    r"\s(?:-v\s?|--log-level(?:\s|=){1})([a-zA-Z-_]+)",
    " ".join(sys.argv),
)

if __log_level:
    LOG_LEVEL = str(__log_level.group(1)).upper()
    remove = __log_level.group(0).strip().split()
    remove_index = sys.argv.index(remove[0])
    del sys.argv[remove_index : remove_index + len(remove)]

    if LOG_LEVEL not in ("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"):
        raise ValueError(f"Invalid log level {LOG_LEVEL!r}")


# --- Logging handler customization --------------------------------------------
# Display the log level as a single character in a colored box

class DialogRichHandler(RichHandler):
    """Custom `RichHandler` to show the log level as a single character in a colored box."""

    symbols: Dict[Union[int, Literal["default"]], str] = {
        logging.CRITICAL: "~",
        logging.ERROR: "-",
        logging.WARNING: "!",
        logging.INFO: "i",
        logging.DEBUG: "#",
        "default": "?",
    }

    def get_level_text(self, record: LogRecord) -> Text:
        """Get the level name from the record.

        :param LogRecord record: LogRecord instance from the logging handler.
        :return: A tuple of the style and level name.
        :rtype: rich.Text
        """
        level_text = super().get_level_text(record)
        level_text.plain = self.get_level_symbol_text(record.levelno)
        return level_text

    def get_level_symbol_text(self, level: int) -> str:
        """Get the representation of the symbol associated with the level.

        :param level: Log level.
        :return: The formatted symbol.
        :rtype: str
        """
        symbol = self.symbols.get(level, self.symbols["default"])
        return f"[{symbol}]".ljust(3)

    def format(self, record: LogRecord) -> str:
        return strings.normalize_indent(super().format(record))


# --- Logging module initialization --------------------------------------------
# Initialize the logging module with a rich handler, formatter and set its level

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(message)s"
    if LOG_LEVEL != "DEBUG"
    else "[color.black](%(name)s)[/color.black] %(message)s",
    handlers=[
        DialogRichHandler(
            rich_tracebacks=True,
            tracebacks_show_locals=True,
            show_time=False,
            console=console,
            markup=True,
        )
    ],
)

for logger in SILENCED_LOGGERS:
    logging.getLogger(logger).setLevel(logging.CRITICAL)


# --- Context manager to silence loggers ---------------------------------------
# Context manager to silence loggers temporarily while executing a block of code

@contextmanager
def silence_loggers(*names: str):
    """Context manager to silence loggers.

    :param names: Names of the loggers to silence.
    :type names: Sequence[str]
    """
    loggers = [logging.getLogger(name) for name in names]
    levels = [logger.level for logger in loggers]

    for logger in loggers:
        logger.setLevel(logging.CRITICAL)

    yield

    for logger, level in zip(loggers, levels):
        logger.setLevel(level)
