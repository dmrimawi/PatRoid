#!/usr/bin/env python

##################
# Python Imports #
##################

import time
import datetime

#################
# Local Imports #
#################

from PatRoidException import PatRoidException

#############
# CONSTANTS #
#############


class Logger(object):
    """
    This class prints on screen and append on log file
    What is going on
    """
    def __init__(self, log_file=None):
        """
        Constructor
        """
        if not log_file:
            log_file = "PatRoid.log"
        self.log_file = log_file

    def append_to_file(self, msg):
        """
        The message to be write to the log file
        :param msg: Text msg
        :return:nothing
        """
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        msg = "%s: %s" % (st, msg)
        try:
            file = open(self.log_file, "a")
            file.write(msg)
            file.write("\n")
            file.close()
        except Exception as exp:
            raise PatRoidException(exp)

    def info(self, text):
        """
        This method prints the message on screen as -I-
        and print it on the file
        :param text:
        :return: nothing
        """
        text = "-I- %s" % text
        print(text)
        self.append_to_file(text)

    def warning(self, text):
        """
        This method prints the message on screen as -W-
        and print it on the file
        :param text:
        :return: nothing
        """
        text = "-W- %s" % text
        print(text)
        self.append_to_file(text)

    def debug(self, text):
        """
        This method only prints the msg on the file
        :param text:
        :return: nothing
        """
        text = "-D- %s" % text
        self.append_to_file(text)

    def error(self, text):
        """
        This method prints the message on screen as -E-
        and print it on the file
        :param text:
        :return: nothing
        """
        text = "-E- %s" % text
        print(text)
        self.append_to_file(text)
