import time
import functools

from src.utils.logging_config import get_logger

logger = get_logger(__name__)


def retry_with_backoff(max_attempts: int = 3, base_delay: float = 1.0, exceptions=(Exception,)):
    """
    Retries a function on failure with exponential backoff (1s, 2s, 4s, ...).
    Use on anything calling an external API that can fail transiently —
    rate limits (429), timeouts, brief network blips. Does NOT catch and
    hide bugs in your own code — it only wraps calls you explicitly mark,
    and it re-raises after the final attempt so the caller still knows
    the operation ultimately failed.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts:
                        logger.error(
                            f"{func.__name__} failed after {max_attempts} attempts: {e}"
                        )
                        raise
                    delay = base_delay * (2 ** (attempt - 1))
                    logger.warning(
                        f"{func.__name__} failed (attempt {attempt}/{max_attempts}): {e}. "
                        f"Retrying in {delay:.1f}s..."
                    )
                    time.sleep(delay)
            raise last_exception  # unreachable in practice, keeps type checkers happy
        return wrapper
    return decorator