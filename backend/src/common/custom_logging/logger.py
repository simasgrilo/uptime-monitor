"""Logger module for the application, based on Python's standard logging library"""

import os
import logging
from typing import Optional

class Logger:
    """General logging class for the services contained in this project"""

    def __init__(self, object_name: str, file_handler: Optional[logging.Handler]):
        """Constructor for the logging wrapper. In this application. I want to standardize
           all handler calls:
           - every debug and above call should be logged to a file
           - every info and above call should be logged to stdio.
           
           Maybe we should rephrase this approach later on to only log critical issues to an email group or
           something like that.
        Args:
            object_name: the name of the logger object. to follow best practices with 
            Python's standard logging library, it's expected to be the the module/class name 
        
            file_handler (logging.Handler): this parameter is a reference to a fileHandler
            the caller of the logging to set the output of the logging facility to the desired
            handler, be it a file, stdio or else.
        """
        self.logger = logging.getLogger(object_name)
        format = '%(asctime)s - %(name)s - %(funcname)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(format)
        # prevents attaching two loggers to the same logger that was already instantiated.
        # this is also true to the root logger. if I don't do this, then the logging
        # will duplicate any entry whenever I call logging.getLogger(object_name)
        if not self.logger.handlers:
            default_path = '../static/logs/'
            if not file_handler:
                file_handler_path = os.getenv('LOG_FILE_PATH') or default_path
                file_handler = logging.FileHandler(file_handler_path)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            # root logger pass the error messages to stdio:
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.ERROR)
        stream_handl = logging.StreamHandler()
        stream_handl.setFormatter(formatter)
        self.logger.addHandler(stream_handl)
            

    def get_logger(self):
        """Gets the current logger name

        Args:
            name (str): Logger name

        Returns:
            logging.Logger: Standard Python logger tool
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

