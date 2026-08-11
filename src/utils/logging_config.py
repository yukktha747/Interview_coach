import logging
import sys

_configured = False


def get_logger(name: str) -> logging.Logger:
    """
    Central logger factory. Logs to both console and interview_coach.log,
    so you have a persistent trail of what happened during a session —
    useful for debugging failures that happen mid-run, and for eventually
    feeding into observability tooling (e.g. MLflow) later.
    """
    global _configured

    if not _configured:
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%H:%M:%S",
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        root.addHandler(console_handler)

        file_handler = logging.FileHandler("interview_coach.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)

        _configured = True

    return logging.getLogger(name)