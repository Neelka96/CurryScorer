# Import dependencies
import logging as log
import sys

# Import configuration
import config as C

def init_log(
        name: str = None
        ,file_out: bool = False
        ) -> log.Logger:
    '''Creates centralized logger.

    Args:
        name (str, optional): Defaults to None.
        file_out (bool, optional): Defaults to False.

    Returns:
        log.Logger: Master logger for project. 
    '''
    # Logging level
    _level = log.INFO

    # Create or get the logger
    logger = log.getLogger(name)
    
    # Avoid adding handlers multiple times if already configured
    if logger.hasHandlers():
        return logger

    # Set the log level to INFO
    logger.setLevel(_level)
    
    # Create a stream handler (logs to console)
    ch = log.StreamHandler()
    ch.setLevel(_level)
    
    # Create a formatter with date/time, logger name, level, and message
    formatter = log.Formatter(
        '%(asctime)s %(name)s: %(levelname)s - %(message)s',
        datefmt='%m-%d-%y %H:%M:%S'
    )
    ch.setFormatter(formatter)
    
    # Add the handler to the logger
    logger.addHandler(ch)

    if file_out:
        # Add a file handler to log messages to a file
        fh = log.FileHandler('app.log')
        fh.setLevel(_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    return logger


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')