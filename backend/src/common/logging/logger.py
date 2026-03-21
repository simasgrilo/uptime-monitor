"""Logger module for the application, based on Python's standard logging library"""

import os
import logging


class Logger:
    """General logging class for the services contained in this project"""

    def __init__(self, object_name: str, log_handler: logging.Handler):
        """Constructor for the logging wrapper

        Args:
            log_handler (logging.Handler): this parameter is a reference to a kind of handler that allows
            the caller of the logging to set the output of the logging facility to the desired
            handler, be it a file, stdio or else.
        """
        default_path = '../static/logs/'
        self.logger = logging.getLogger(f'uptime-monitor {object_name}')
        # by default, we always log debug calls to a specific file based on the day and hour the call happened
        file_handler_path = os.environ['LOG_FILE_PATH'] or default_path
        file_handler = logging.FileHandler(file_handler_path)
        file_handler.setLevel(logging.DEBUG)
        # add any other handler if passed by the callee
        self.logger.addHandler(file_handler)
        if file_handler:
            self.logger.addHandler(log_handler)
        self.logger.setLevel(logging.INFO)

    def get_logger(self):
        """Returns the logger instance
        """
        return self.logger
    
    def set_level(self, level: int):
        """Allows dynamically setting of
           the level of the logger. useful
           when the default level might be changed in
           runtime for a specific use case (e.g., debugging)

        Args:
            level (int): levels of logging. it can be the following:
            CRITICAL = 50
            FATAL = CRITICAL
            ERROR = 40
            WARNING = 30
            WARN = WARNING
            INFO = 20
            DEBUG = 10
            NOTSET = 0

        Raises:
            ValueError: if level does not meet any of the values above
        """
        if level not in {50, 40, 30, 20, 10, 0}:
            raise ValueError(f'invalid level {level}. Please follow the conventions found in logging.__init__.py')
        self.logger.setLevel(level)

