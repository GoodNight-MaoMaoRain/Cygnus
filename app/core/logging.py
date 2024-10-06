import logging
import os.path
from datetime import timedelta
from types import FrameType
from typing import cast

from loguru import logger

from app.common.common import ROOT


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:

        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )
