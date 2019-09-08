#!/usr/bin/env python

##################
# Python Imports #
##################

import re

#################
# Local Imports #
#################

from ADPDException import ADPDException
from regex_handler import RegexHandler

#############
# CONSTANTS #
#############

DATA_TYPES_KEYWORDS = ['String', 'char', 'int', 'double', 'float', 'boolean', 'bool']


class JavaFilesInfo(object):
    """
    This class create a dictionaries for the java files info
    """
    def __init__(self):
        """
        Constructor
        """
        pass

    @staticmethod
    def get_method_arguments(arguments):
        """
        This method prepare a dictionary for all arguments in the method
        :param arguments: method args
        :return: list of dictionaries [{"int", "x"}, ...]
        """
        results = None
        if arguments:
            args = arguments.split(",")
            results = list()
            argument_dict = dict()
            for arg in args:
                arg = arg.strip().split()
                if len(arg) > 2:
                    arg_name = " ".join(arg[:-1])
                    argument_dict[str(arg_name)] = arg[-1]
                elif len(arg) == 2:
                    argument_dict[arg[0]] = arg[1]
                if argument_dict:
                    results.append(argument_dict)
        return results

    @staticmethod
    def create_methods_dictionary(file_path):
        """
        This method takes a java file name and return a dicionary of the methods it contains
        :param file_path: Java File path
        :return: List of dictionaries of the file methods
        """
        methods_list = list()
        method_handler = RegexHandler()
        methods = method_handler.apply_methods_regex(file_path=file_path)
        for (access_modifier, return_type, name, arguments, body) in methods:
            method_dict = dict()
            method_dict["access_modifier"] = access_modifier
            method_dict["return_type"] = return_type
            method_dict["name"] = name
            method_dict["arguments"] = JavaFilesInfo.get_method_arguments(arguments)
            method_dict["body"] = body
            methods_list.append(method_dict)
        return methods_list

    @staticmethod
    def get_list_of_classes_names_and_parents(java_files):
        """
        It return a dictionary of java classes names  and their parents in the given java files
        :param java_files: List of .java files
        :return: List of [{class_name: parent}, {...}, ...]
        """
        class_list = list()
        regex_handler = RegexHandler()
        for java_file in java_files:
            class_and_parent = regex_handler.apply_class_name_and_parent_regex(file_path=java_file)
            classes_dict = dict()
            for (class_name, class_parent)in class_and_parent:
                classes_dict[class_name] = class_parent
            class_list.append(classes_dict)
        return class_list

    @staticmethod
    def get_list_of_classes_names(java_files):
        """
        It return a list of java classes names
        :param java_files: List of .java files
        :return: List of classes_names
        """
        classes = list()
        regex_handler = RegexHandler()
        for java_file in java_files:
            class_name = regex_handler.apply_class_name_from_path_regex(string=java_file)
            classes.append(class_name[0])
        return classes

    @staticmethod
    def get_inherentance_relations(java_files):
        """
        It return a dictionary with class and its parent from this project
        :param java_files: List of .java files
        :return: List of [{class_name: parent}, {...}, ...]
        """
        class_list = list()
        classes = JavaFilesInfo.get_list_of_classes_names(java_files)
        classes_and_parents = JavaFilesInfo.get_list_of_classes_names_and_parents(java_files)
        for class_and_parent in classes_and_parents:
            for key, val in class_and_parent.iteritems():
                if val in classes:
                    inheritance_relation = dict()
                    inheritance_relation[key] = val
                    class_list.append(inheritance_relation)
        return class_list

    @staticmethod
    def get_methods_specific_info(java_file, info):
        """
        This method prepare a list of specific info from all methods in class
        :param java_file: Class
        :param info: name, arguments, data_type, etc. (check create_methods_dictionary)
        :return: List
        """
        list_of_info = list()
        java_methods = JavaFilesInfo.create_methods_dictionary(java_file)
        for method in java_methods:
            list_of_info.append(method.get(info))
        return list_of_info

    @staticmethod
    def get_attributes_types(java_file, only_final=False):
        """
        This method prepare a list of specific info from all attributes defined in the given class
        :param java_file: Class
        :param only_final: Include only final attributes
        :return: List
        """
        list_of_data_types = list()
        regex_handler = RegexHandler()
        attributes = regex_handler.apply_object_definition_regex(file_path=java_file)
        for (final_field, data_type, _) in attributes:
            if only_final and final_field == "final":
                list_of_data_types.append(data_type)
            elif not only_final and final_field != "final":
                list_of_data_types.append(data_type)
        return list_of_data_types

    @staticmethod
    def __create_relation(java_file, data_type):
        """
        This private method prepare dictionary of classi and classj which have a relation
        :param java_file: class
        :param data_type: object data type or a return data type
        :return: dictionary
        """
        relation = dict()
        regex_handler = RegexHandler()
        class_name = regex_handler.apply_class_name_from_path_regex(string=java_file)[0]
        relation[data_type] = class_name
        return relation

    @staticmethod
    def get_association_relations(java_files):
        """
        It return a dictionary with classes that have association relation
        :param java_files: List of .java files
        :return: List of [{ci: cj}, {...}, ...], where class ci has an attribute that is a type of class cj,
        or class ci has a method which returns a cj object.
        """
        class_list = list()
        classes = JavaFilesInfo.get_list_of_classes_names(java_files)
        for java_file in java_files:
            methods_return_types = JavaFilesInfo.get_methods_specific_info(java_file, "return_type")
            attributes_types = JavaFilesInfo.get_attributes_types(java_file)
            for data_type in methods_return_types + attributes_types:
                if data_type in classes:
                    relation = JavaFilesInfo.__create_relation(java_file, data_type)
                    if relation not in class_list:
                        class_list.append(relation)
        return class_list

    @staticmethod
    def get_aggregation_relations(java_files):
        """
        It return a dictionary with classes that have aggregation relation
        :param java_files: List of .java files
        :return: List of [{ci: cj}, {...}, ...], where class ci has an attribute that is a type of class cj.
        The aggregation is considered as a special kind of association relationship,
        in which class ci is the whole class and class cj is the partial class.
        """
        class_list = list()
        classes = JavaFilesInfo.get_list_of_classes_names(java_files)
        for java_file in java_files:
            attributes_types = JavaFilesInfo.get_attributes_types(java_file, only_final=True)
            for data_type in attributes_types:
                if data_type in classes:
                    relation = JavaFilesInfo.__create_relation(java_file, data_type)
                    if relation not in class_list:
                        class_list.append(relation)
        return class_list

    @staticmethod
    def get_depends_relations_from_methods_args(java_file, methods_args, classes):
        """
        This method search in method args for objects to add a depends relation
        :param java_file: Java class
        :param methods_args: All methods arguments in class
        :return: list of dictionaries[{ci:cj}, ..]
        """
        class_list = list()
        if methods_args:
            for method_args in methods_args:
                if method_args:
                    for arg in method_args:
                        data_type = arg.keys()[0]
                        if data_type in classes:
                            relation = JavaFilesInfo.__create_relation(java_file, data_type)
                            if relation not in class_list:
                                class_list.append(relation)
        return class_list

    @staticmethod
    def get_static_method_calls(java_file, classes=None):
        """
        Apply static method call pattern and return a list of all classes called a static method
        :param java_file: Java class
        :return: list of classes and object called a method
        """
        list_of_classes_or_objects = list()
        regex_handler = RegexHandler()
        objects_or_classes = regex_handler.apply_static_method_call_regex(file_path=java_file)
        if classes:
            for class_name in objects_or_classes:
                if class_name in classes:
                    list_of_classes_or_objects.append(class_name)
        else:
            list_of_classes_or_objects = objects_or_classes
        return list_of_classes_or_objects

    @staticmethod
    def get_depends_relations(java_files):
        """
        It return a dictionary with classes that have depends relation
        :param java_files: List of .java files
        :return: List of [{ci: cj}, {...}, ...], where:
        (i) The instance of class ci calls a static method in class cj
        (ii) An instance of class cj is used as the parameter passed to a method in class ci
        """
        class_list = list()
        classes = JavaFilesInfo.get_list_of_classes_names(java_files)
        for java_file in java_files:
            static_method_call = JavaFilesInfo.get_static_method_calls(java_file, classes=classes)
            for class_name in static_method_call:
                relation = JavaFilesInfo.__create_relation(java_file, class_name)
                if relation not in class_list:
                    class_list.append(relation)
            methods_args = JavaFilesInfo.get_methods_specific_info(java_file, "arguments")
            class_list.extend(JavaFilesInfo.get_depends_relations_from_methods_args(java_file, methods_args, classes))
        return class_list
