#!/usr/bin/env python

##################
# Python Imports #
##################

import xml.etree.ElementTree as ET

#################
# Local Imports #
#################

from JavaFilesInfo import JavaFilesInfo
from Common import CommonMethods


class ManifestParser(object):
    """
    This class aims to parse the AndroidManifest.xml file and initialize an activity dictionary
    """
    def __init__(self, manifest_file):
        """
        Constructor
        :param manifest_file: The full path to the manifest file
        """
        self.manifest_file = manifest_file

    def get_xml_root(self):
        """
        parse xml
        :return: return the root node
        """
        tree = ET.parse(self.manifest_file)
        root = tree.getroot()
        return root

    def get_specific_node_list(self, node_name, root_node=None):
        """
        Takes a node name and return all of this node instances
        :param node_name: the node name to search for
        :param root_node: the node to search in
        :return: list of instances of the given node_name
        """
        nodes = list()
        if root_node is None:
            root = self.get_xml_root()
            root_node = root.find('application')
        if root_node is not None:
            nodes = root_node.findall(node_name)
        return nodes

    def get_category_value(self, categories_nodes):
        """
        This method search for the category type in the given nodes
        :param categories_nodes: categories to search in
        :return: "LAUNCHER" OR "DEFAULT" OR None
        """
        category = None
        for cat in categories_nodes:
            for category_value in cat.attrib.values():
                if "DEFAULT" in category_value:
                    category = "DEFAULT"
                    break
                if "LAUNCHER" in category_value:
                    category = "LAUNCHER"
                    break
        return category

    def get_activities_dictionary(self):
        """
        This method parse the manifest file and return a dictionary of activities names
        :return: dictionary of activities {activity-name: activity-category}
        """
        activities_dict_list = list()
        activities = self.get_specific_node_list('activity')
        for activity in activities:
            activities_dict = dict()
            activity_name = None
            category = None
            for key, val in activity.attrib.iteritems():
                if "}name" in key:
                    activity_name = val.split(".")[-1]
                    break
            if activity_name:
                intent_filter_node = self.get_specific_node_list('intent-filter', root_node=activity)
                if len(intent_filter_node) == 1:
                    categories_nodes = self.get_specific_node_list('category', root_node=intent_filter_node[0])
                    category = self.get_category_value(categories_nodes)
                else:
                    category = None
                activities_dict["name"] = activity_name
                activities_dict["category"] = category
                activities_dict_list.append(activities_dict)
        return activities_dict_list

    def get_classes_related_to_activity(self, activity_name, java_files, classes, related_classes=list()):
        """
        Generated a list of all the classes that mentioned in the give activity name recursively
        :param activity_name: Search for
        :param java_files:Search in
        :param classes: Name of classes
        :param related_classes: list of already known relations
        :return: Final list
        """
        activity_file = None
        for file in java_files:
            if file.endswith("%s.java" % activity_name):
                activity_file = file
                break
        if activity_file:
            class_content = CommonMethods.read_file(activity_file)
            classes_in_activity = [class_name for class_name in classes if class_name in class_content]
            for class_name in classes_in_activity:
                if class_name not in related_classes:
                    related_classes.extend(self.get_classes_related_to_activity(activity_name=class_name,
                                                                                java_files=java_files, classes=classes,
                                                                                related_classes=classes_in_activity))
            related_classes.extend(classes_in_activity)
            related_classes = list(dict.fromkeys(related_classes))
        return related_classes

    def get_activities_classes_dict(self, java_files):
        """
        This method prepare a dictionary of the activities and all the related classes to it.
        :param java_files: List of all java files in the project
        :return: Dict{"activity_name": ["class1", "class2",...], ...}
        """
        activities_dict = self.get_activities_dictionary()
        all_classes = JavaFilesInfo.get_list_of_classes_names(java_files)
        for activity in activities_dict:
            activity_name = activity.get("name")
            activity["classes"] = self.get_classes_related_to_activity(activity_name, java_files, all_classes)
        return activities_dict

