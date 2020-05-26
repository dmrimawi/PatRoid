#!/usr/bin/env python

##################
# Python Imports #
##################

import re

#################
# Local Imports #
#################

from PatRoidException import PatRoidException
from Common import CommonMethods

#############
# CONSTANTS #
#############

METHODS_REGEX = r"((?:(?:public|private|protected|static|final|abstract|synchronized|volatile)\s+)*)\s*(\w+)\s+(\w+)" \
                    "\(([\w|\s|,|@]*)\)\s*({(?:{[^{}]*(?:{[^{}]*}|.)*?[^{}]*}|.)*?})[^;]"
OBJECTS_DEFINITION_REGEX = r"(\w*)\s*(\w+)\[{0,1}\]{0,1}\s+(\w+)\s*=.*?;"
CLASS_NAME_AND_PARENT_REGEX = r"class\s+(\w+)(?:\s+extends\s+(\w+))*"
STATIC_METHOD_CALL_REGEX = r"(\w+)\.\w+\(.*\);"
CLASS_NAME_FROM_PATH = r"(\w+)\.java"


class RegexHandler(object):
    """
    This class contains all the regex used in this project,
    Each regex should have its own method that takes file_path or a string
    and returns a group of matches for that regex
    The methods need to use the common methods (get_search_in_text, apply_regex)
    """
    def __init__(self):
        """
        Constructor
        """
        pass

    def get_search_in_text(self, file_path=None, string=None):
        """
        This method is a common method to be called by all apply regex methods
        It prepare the search in string.
        :param file_path: File path to search in
        :param string: String to search in
        :return: Text
        """
        search_in = string
        if not search_in and file_path:
            search_in = CommonMethods.read_file(file_path=file_path)
        if not search_in:
            raise PatRoidException("To apply a regex you have to provide either a file or a string")
        return search_in

    def apply_regex(self, search_in_text, regex_ptrn, flags=re.DOTALL):
        """
        This method is a common method to be called in all apply regex methods
        :param search_in_text: The string to search in
        :param regex_ptrn: The regex pattern to search for
        :param flags: re flags (if no flags -> pass zero as flags value)
        :return: re.findall object
        """
        try:
            result = re.findall(regex_ptrn, search_in_text, flags)
        except Exception as exp:
            raise PatRoidException(exp)
        return result

    def apply_methods_regex(self, file_path=None, string=None):
        """
        This method take the given (file or string) and apply the regex METHODS_REGEX
        :param file_path: File to search for regex in
        :param string: String to search for regex in
        :return: re.findall object [(access_modifier, return_type, name, arguments, body),...]
        """
        search_in_text = self.get_search_in_text(file_path=file_path, string=string)
        result = self.apply_regex(search_in_text=search_in_text, regex_ptrn=METHODS_REGEX)
        if result is None:
            raise PatRoidException("Couldn't apply the method pattern, nothing was found")
        return result

    def apply_object_definition_regex(self, file_path=None, string=None):
        """
        This method take the given (file or string) and apply the regex OBJECTS_DEFINITION_REGEX
        :param file_path: File to search for regex in
        :param string: String to search for regex in
        :return: re.findall object
        """
        search_in_text = self.get_search_in_text(file_path=file_path, string=string)
        result = self.apply_regex(search_in_text=search_in_text, regex_ptrn=OBJECTS_DEFINITION_REGEX)
        if result is None:
            raise PatRoidException("Couldn't apply the object definition pattern, nothing was found")
        return result

    def apply_class_name_and_parent_regex(self, file_path=None, string=None):
        """
        This method take the given (file or string) and apply the regex CLASS_NAME_AND_PARENT_REGEX
        :param file_path: File to search for regex in
        :param string: String to search for regex in
        :return: re.findall object
        """
        search_in_text = self.get_search_in_text(file_path=file_path, string=string)
        result = self.apply_regex(search_in_text=search_in_text, regex_ptrn=CLASS_NAME_AND_PARENT_REGEX)
        if result is None:
            raise PatRoidException("Couldn't apply the class name and parent pattern, nothing was found")
        return result

    def apply_static_method_call_regex(self, file_path=None, string=None):
        """
        This method take the given (file or string) and apply the regex STATIC_METHOD_CALL_REGEX
        :param file_path: File to search for regex in
        :param string: String to search for regex in
        :return: re.findall object
        """
        search_in_text = self.get_search_in_text(file_path=file_path, string=string)
        result = self.apply_regex(search_in_text=search_in_text, regex_ptrn=STATIC_METHOD_CALL_REGEX)
        if result is None:
            raise PatRoidException("Couldn't apply the class name and parent pattern, nothing was found")
        return result

    def apply_class_name_from_path_regex(self, file_path=None, string=None):
        """
        This method take the given (file or string) and apply the regex CLASS_NAME_FROM_PATH
        :param file_path: File to search for regex in
        :param string: String to search for regex in
        :return: re.findall object
        """
        search_in_text = self.get_search_in_text(file_path=file_path, string=string)
        result = self.apply_regex(search_in_text=search_in_text, regex_ptrn=CLASS_NAME_FROM_PATH)
        if result is None:
            raise PatRoidException("Couldn't apply the class name and parent pattern, nothing was found")
        return result