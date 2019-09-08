#!/usr/bin/env python

##################
# Python Imports #
##################

import xml.etree.ElementTree as ET

#################
# Local Imports #
#################

from ADPDException import ADPDException


class CreateRelationsModule(object):
    """
    This class aims to convert the relationships lists to a common module (XML)
    """
    def __init__(self, module_file_name):
        """
        Constructor
        :param module_file_name: The module_file_name
        """
        self.module_file_name = module_file_name

    def define_root_node(self):
        """
        This method intiates the tree by creating the root node
        :return: Return a root object from the tree
        """
        root = ET.Element("ADPD")
        return root

    def add_relations_to_subnode(self, node, relations):
        """
        Add the given relations to the given node
        :param node: dep, ass, agg or inh node
        :param relations: list of dictionaries
        :return: nothing
        """
        for relation in relations:
            cj = relation.keys()[0]
            ci = relation.values()[0]
            relation_node =  ET.SubElement(node, "relation")
            relation_node.set("ci", ci)
            relation_node.set("cj", cj)

    def add_depends_relations(self, root, depends_relations):
        """
        This method add the depends relationships to the module root
        :param root: Tree root
        :param depends_relations: list of dictionary
        :return: nothing
        """
        depends = ET.SubElement(root, "depends")
        self.add_relations_to_subnode(depends, depends_relations)

    def add_association_relations(self, root, association_relations):
        """
        This method add the association relationships to the module root
        :param root: Tree root
        :param association_relations: list of dictionary
        :return: nothing
        """
        association = ET.SubElement(root, "association")
        self.add_relations_to_subnode(association, association_relations)

    def add_inheritance_relations(self, root, inheritance_relations):
        """
        This method add the inheritance relationships to the module root
        :param root: Tree root
        :param inheritance_relations: list of dictionary
        :return: nothing
        """
        inheritance = ET.SubElement(root, "inheritance")
        self.add_relations_to_subnode(inheritance, inheritance_relations)

    def add_aggregation_relations(self, root, aggregation_relations):
        """
        This method add the aggregation relationships to the module root
        :param root: Tree root
        :param aggregation_relations: list of dictionary
        :return: nothing
        """
        aggregation = ET.SubElement(root, "aggregation")
        self.add_relations_to_subnode(aggregation, aggregation_relations)

    def add_manifest_info(self, root, manifest_info):
        """
        This method add the manifest file info to the module root
        :param root: Tree root
        :param manifest_info: dictionary
        :return: nothing
        """
        manifest = ET.SubElement(root, "manifest")
        for activity in manifest_info:
            activity_node = ET.SubElement(manifest, "activity")
            activity_node.set('name', activity.get("name"))
            category = ('None', activity.get("category"))[activity.get("category") is not None]
            activity_node.set('category', category)
            related_classes = ET.SubElement(activity_node, "related_classes")
            if len(activity.get("classes")) == 0:
                continue
            for class_name in activity.get("classes"):
                class_node = ET.SubElement(related_classes, "activity")
                class_node.set('name', class_name)

    def build_relations_module(self, depends_relations, association_relations, inheritance_relations,
                               aggregation_relations, manifest_info):
        """
        Build the whole module and write to XML file
        :param depends_relations: list of dictionary
        :param association_relations: list of dictionary
        :param inheritance_relations: list of dictionary
        :param aggregation_relations: list of dictionary
        :param manifest_info: dictionary
        :return: nothing
        """
        root = self.define_root_node()
        self.add_depends_relations(root, depends_relations)
        self.add_aggregation_relations(root, aggregation_relations)
        self.add_association_relations(root, association_relations)
        self.add_inheritance_relations(root, inheritance_relations)
        self.add_manifest_info(root, manifest_info)
        tree = ET.ElementTree(root)
        tree.write(self.module_file_name)
