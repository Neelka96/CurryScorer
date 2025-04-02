# Import dependencies
import logging as log

def init_log(
        name: str = None
        ,log_level: int | str = log.INFO
        ,file: str = 'app.log'
        ) -> log.Logger:
    '''Creates centralized logger.

    Args:
        name (str, optional): Defaults to None.
        log_level (int, optional): Defaults to `log.INFO`. Levels are 0, 10, 20, 30, 40, 50.
        file (str, optional): Defaults to `app.log`

    Returns:
        log.Logger: Master logger for project. 
    '''
    # Create or get the logger
    logger = log.getLogger(name)
    
    # Avoid adding handlers multiple times if already configured
    if logger.hasHandlers():
        return logger

    # Set the log level to INFO
    logger.setLevel(log_level)
    
    # Create a stream handler (logs to console)
    ch = log.StreamHandler()
    ch.setLevel(log_level)
    
    # Create a formatter with date/time, logger name, level, and message
    formatter = log.Formatter(
        '%(asctime)s %(name)s: %(levelname)s - %(message)s',
        datefmt='%m-%d-%y %H:%M:%S'
    )
    ch.setFormatter(formatter)
    
    # Add the handler to the logger
    logger.addHandler(ch)

    if file:
        # Add a file handler to log messages to a file
        fh = log.FileHandler(file)
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    return logger


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')