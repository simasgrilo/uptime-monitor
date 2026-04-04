"""Unit test module for Logger class"""
from logging import StreamHandler
from unittest import TestCase
from tempfile import TemporaryFile
from backend.src.common.custom_logging.logger import Logger

class TestLogger(TestCase):
    """Test class to test the logger wrapper will always logs to the
       desired output as defined in class Logger from this project

    Args:
        TestCase (_type_): _description_
    """
    def setUp(self) -> None:
        self.temp_file = TemporaryFile('w+')
        self.logger = Logger(__name__, StreamHandler(stream=self.temp_file))
        return super().setUp()
    
    def test_logging_uses_set_handlers(self):
        """ Basic unit test for the logger wrapping utility
        """
        logger = self.logger.get_logger()
        with self.assertLogs(logger) as cm:
            logger.info("info level message")
            logger.debug("this has been flushed to a file")
        print(cm.output)
        # self.assertEqual(cm.output, [f'INFO:{__name__}:info level message',
        #                              f'DEBUG:{__name__}:I want this flushed to a file'])
        #reads from the beginning of the file
        self.temp_file.seek(0)
        print(self.temp_file)
        file_content = self.temp_file.read()
        print(file_content)
        print("end")
        
        
    def tearDown(self) -> None:
        self.temp_file.close()
        return super().tearDown()