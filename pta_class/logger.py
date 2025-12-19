from __future__ import annotations

import os
import sys
from typing import Optional

from loguru import logger
from tqdm import tqdm

# Use tqdm.write to keep progress bars intact when logging
_tqdm_stream = sys.stderr

def _tqdm_sink(msg: str) -> None:
    # Loguru sends a final "\n", tqdm.write handles its own newline behavior
    tqdm.write(msg.rstrip(), file=_tqdm_stream)
    try:
        _tqdm_stream.flush()
    except Exception:
        pass

def setup_logging(
    *,
    console_level: str = "INFO",
    file_level: str = "TRACE",
    log_file: str = os.path.join("logs", "pta.log"),
    rotation: str = "10 MB",
    retention: Optional[str] = None,
    enqueue: bool = True,
    colorize: bool = True,
    backtrace: bool = True,
    diagnose: bool = False,
) -> None:
    """Configure Loguru sinks.

    - Console: writes via tqdm to avoid breaking progress bars
    - File: rotating file with high verbosity
    """
    # Ensure log directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger.remove()

    # Console sink through tqdm
    logger.add(
        _tqdm_sink,
        colorize=colorize,
        enqueue=False,  # keep console synchronous to avoid mixing with input/print
        level=console_level,
        backtrace=backtrace,
        diagnose=diagnose,
    )

    # Rotating file sink
    logger.add(
        log_file,
        rotation=rotation,
        retention=retention,
        level=file_level,
        enqueue=enqueue,
        backtrace=backtrace,
        diagnose=diagnose,
        encoding="utf-8",
    )
