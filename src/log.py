import logging
import platform
import os
from datetime import datetime

def initialize_logger(output_dir):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        system = platform.system()
        if system == 'Linux':
            system = ""
        else:
            system = "Mac"
        
        
        # create console handler and set level to info
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(u"%(levelname)s - %(asctime)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # create error file handler and set level to info
        handler = logging.FileHandler(os.path.join(output_dir, "info-{}.log".format(system)),"w", encoding='utf-8', delay="true")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(u"%(levelname)s - %(asctime)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # create error file handler and set level to error
        handler = logging.FileHandler(os.path.join(output_dir, "error-{}.log".format(system)),"w", encoding='utf-8', delay="true")
        handler.setLevel(logging.ERROR)
        formatter = logging.Formatter(u"%(levelname)s - %(asctime)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
        # create debug file handler and set level to debug
        handler = logging.FileHandler(os.path.join(output_dir, "debug-{}.log".format(system)),"w", encoding='utf-8', delay="true")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(u"%(levelname)s - %(asctime)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        