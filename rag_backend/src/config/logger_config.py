import logging


class LoggerConfig:
    _loggers = {}  # Store logger instances

    @staticmethod
    def setup_console_logger(name="app", level=logging.INFO):
        # Return existing logger if already created
        if name in LoggerConfig._loggers:
            return LoggerConfig._loggers[name]

        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Only add handler if none exist
        if not logger.handlers:
            # Create console handler and set level
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)

            # Create formatter
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

            # Add formatter to handler
            console_handler.setFormatter(formatter)

            # Add handler to logger
            logger.addHandler(console_handler)

            # Prevent propagation to root logger
            logger.propagate = False

        # Store logger instance
        LoggerConfig._loggers[name] = logger
        return logger
