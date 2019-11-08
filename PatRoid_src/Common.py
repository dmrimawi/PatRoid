#!/usr/bin/env python

##################
# Python Imports #
##################


#################
# Local Imports #
#################

from PatRoidException import PatRoidException

#############
# CONSTANTS #
#############


class CommonMethods(object):
    """
        This class contains common methods used in the project
    """
    def __init__(self):
        """
        Constructor of class
        """
        pass

    @staticmethod
    def read_file(file_path):
        """
        This method reads the file and return its content
        :param file_path: the file to read
        :return: content
        """
        try:
            file = open(file_path, "r")
            data = file.read()
        except Exception as exp:
            raise PatRoidException(exp)
        finally:
            file.close()
        return data