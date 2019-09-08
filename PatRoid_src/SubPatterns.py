#!/usr/bin/env python

##################
# Python Imports #
##################

import xml.etree.ElementTree as ET

#################
# Local Imports #
#################

from ADPDException import ADPDException
from Logger import Logger
logger = Logger()

#############
# CONSTANTS #
#############


class SubPatterns(object):
    """
    This class takes the XML module as an input,
    then it uses the method to create the sub_patterns
    15 sub_patterns are implemented in this class
    """
    def __init__(self, module_file):
        """
        Constructor
        """
        self.module_file = module_file

    def get_xml_root(self):
        """
        parse xml
        :return: return the root node
        """
        tree = ET.parse(self.module_file)
        root = tree.getroot()
        return root

    def get_node_by_name(self, name):
        """
        Search for the node with the specified name
        :param name: node name
        :return: node
        """
        root = self.get_xml_root()
        return root.find(name)

    def __ICA_helper(self, inh, ass):
        """
        This is a helper method for the ICA method
        :param inh: inheritance node
        :param ass: association node
        :return:
        """
        ica_relations = list()
        if inh is None or ass is None:
            logger.warning("There are no ICA relations")
        else:
            for parent_and_child in inh:
                parent = parent_and_child.attrib.get("ci")
                child = parent_and_child.attrib.get("cj")
                for relation in ass:
                    if child == relation.attrib.get("cj"):
                        ica_tuple = (parent, child, relation.attrib.get("ci"))
                        ica_relations.append(ica_tuple)
                        logger.debug("Found ICA: (%s, %s, %s)" % (ica_tuple[0], ica_tuple[1], ica_tuple[2]))
        ica_relations = list(dict.fromkeys(ica_relations))
        return ica_relations

    def ICA(self):
        """
        ICA(Inheritance Child Association)
        :return: return list of tuples for classes that have ICA relation
        """
        logger.info("ICA(Inheritance Child Association)")
        logger.info("Step1: Get all parent and child classes")
        inh = self.get_node_by_name("inheritance")
        logger.debug("inheritance: %s" % inh)
        logger.info("Step2: Get all Association relation classes")
        ass = self.get_node_by_name("association")
        logger.debug("association: %s" % ass)
        logger.info("Step3: Find child classes with association relation")
        return self.__ICA_helper(inh, ass)

    def __CI_helper(self, inh):
        """
        Helper for CI method
        :param inh: inheritance
        :return: list of tuples
        """
        list_of_ci_relation = list()
        if inh is None:
            logger.info("There are no CI relations")
        else:
            for parent_and_child in inh:
                parent = parent_and_child.attrib.get("ci")
                child = parent_and_child.attrib.get("cj")
                for inner_parent_and_child in inh:
                    inner_parent = inner_parent_and_child.attrib.get("ci")
                    inner_child = inner_parent_and_child.attrib.get("cj")
                    if inner_parent == parent and inner_child != child:
                        ci_tuple = (parent, child, inner_child)
                        list_of_ci_relation.append(ci_tuple)
                        logger.debug("Found CI: (%s, %s, %s)" % (ci_tuple[0], ci_tuple[1], ci_tuple[2]))
        list_of_ci_relation = list(dict.fromkeys(list_of_ci_relation))
        index = 0
        while True:
            if index == len(list_of_ci_relation):
                break
            for ci in list_of_ci_relation:
                if index == len(list_of_ci_relation):
                    break
                if list_of_ci_relation[index] == ci:
                    continue
                # check if both parents are the same (index zero in tuple is for parent)
                if ci[0] == list_of_ci_relation[index][0]:
                    if sorted(ci) == sorted(list_of_ci_relation[index]):
                        del list_of_ci_relation[index]
                        index = 0
                index = index + 1
        return list_of_ci_relation

    def CI(self):
        """
        CI (Common Inheritance)
        :return: return list of tuples for classes that have CI relation
        """
        logger.info("CI (Common Inheritance)")
        logger.info("Step1: Get all parent and child classes")
        inh = self.get_node_by_name("inheritance")
        logger.debug("inheritance: %s" % inh)
        logger.info("Step2: Find all children shares the same parent")
        return self.__CI_helper(inh)

    def __IAGG_helper(self, inh, agg):
        """
        Helper for IAGG method
        :param inh: inheritance
        :param agg: aggregation
        :return: list of tuples
        """
        list_of_iagg_relation = list()
        if inh is None or agg is None:
            logger.info("There are no IAGG relations")
        else:
            for parent_and_child in inh:
                parent = parent_and_child.attrib.get("ci")
                child = parent_and_child.attrib.get("cj")
                for relation in agg:
                    agg_relation_class_1 = relation.attrib.get("cj")
                    agg_relation_class_2 = relation.attrib.get("ci")
                    if agg_relation_class_1 == parent and agg_relation_class_2 == child:
                        iagg_tuple = (parent, child)
                        list_of_iagg_relation.append(iagg_tuple)
                        logger.debug("Found IAGG: (%s, %s)" % (iagg_tuple[0], iagg_tuple[1]))
        list_of_iagg_relation = list(dict.fromkeys(list_of_iagg_relation))
        return list_of_iagg_relation

    def IAGG(self):
        """
        IAGG (Inheritance AGGregation)
        :return: return list of tuples for classes that have IAGG relation
        """
        logger.info("IAGG (Inheritance AGGregation)")
        logger.info("Step1: Get all parent and child classes")
        inh = self.get_node_by_name("inheritance")
        logger.debug("inheritance: %s" % inh)
        logger.info("Step2: Get all classes with aggregation relation")
        agg = self.get_node_by_name("aggregation")
        logger.debug("aggregation: %s" % agg)
        logger.info("Step3: Find classes that have both inheritance and aggregation")
        return self.__IAGG_helper(inh, agg)

    def __IPAG_helper(self, inh, agg):
        """
        Helper for IPAG method
        :param inh: inheritance
        :param agg: aggregation
        :return: list of tuples
        """
        list_of_ipag_relation = list()
        if inh is None or agg is None:
            logger.info("There are no IPAG relations")
        else:
            for parent_and_child in inh:
                parent = parent_and_child.attrib.get("ci")
                child = parent_and_child.attrib.get("cj")
                for relation in agg:
                    agg_relation_class_1 = relation.attrib.get("ci")
                    agg_relation_class_2 = relation.attrib.get("cj")
                    if agg_relation_class_1 == parent and agg_relation_class_2 != child:
                        ipag_tuple = (parent, child, agg_relation_class_2)
                        list_of_ipag_relation.append(ipag_tuple)
                        logger.debug("Found IPAG: (%s, %s, %s)" % (ipag_tuple[0], ipag_tuple[1], ipag_tuple[2]))
        list_of_ipag_relation = list(dict.fromkeys(list_of_ipag_relation))
        return list_of_ipag_relation

    def IPAG(self):
        """
        IPAG (Inheritance Parent AGgregation)
        :return: return list of tuples for classes that have IPAG relation
        """
        logger.info("IPAG (Inheritance Parent AGgregation)")
        logger.info("Step1: Get all parent and child classes")
        inh = self.get_node_by_name("inheritance")
        logger.debug("inheritance: %s" % inh)
        logger.info("Step2: Get all classes with aggregation relation")
        agg = self.get_node_by_name("aggregation")
        logger.debug("aggregation: %s" % agg)
        logger.info("Step3: Find classes that have inheritance and the parent have aggregation with other")
        return self.__IPAG_helper(inh, agg)

    def __MLI_helper(self, inh):
        """
        Helper for MLI method
        :param inh: inheritance
        :return: list of tuples
        """
        list_of_mli_relation = list()
        if inh is None:
            logger.info("There are no MLI relations")
        else:
            for parent_and_child in inh:
                parent = parent_and_child.attrib.get("ci")
                child = parent_and_child.attrib.get("cj")
                for inner_parent_and_child in inh:
                    inner_parent = inner_parent_and_child.attrib.get("ci")
                    inner_child = inner_parent_and_child.attrib.get("cj")
                    if inner_parent == child:
                        mli_tuple = (parent, child, inner_child)
                        list_of_mli_relation.append(mli_tuple)
                        logger.debug("Found MLI: (%s, %s, %s)" % (mli_tuple[0], mli_tuple[1], mli_tuple[2]))
        list_of_mli_relation = list(dict.fromkeys(list_of_mli_relation))
        return list_of_mli_relation

    def MLI(self):
        """
        MLI (Multi-Level Inheritance)
        :return: return list of tuples for classes that have MLI relation
        """
        logger.info("MLI (Multi-Level Inheritance)")
        logger.info("Step1: Get all parent and child classes")
        inh = self.get_node_by_name("inheritance")
        logger.debug("inheritance: %s" % inh)
        logger.info("Step2: Find all classes that their parent is a child for other parent")
        return self.__MLI_helper(inh)

    def __IASS_helper(self, inh, ass):
        """
        Helper for IASS method
        :param inh: inheritance
        :param ass: association
        :return: list of tuples
        """
        list_of_iass_relation = list()
        if inh is None or ass is None:
            logger.info("There are no IASS relations")
        else:
            for parent_and_child in inh:
                parent = parent_and_child.attrib.get("ci")
                child = parent_and_child.attrib.get("cj")
                for relation in ass:
                    if child == relation.attrib.get("ci") and parent == relation.attrib.get("cj"):
                        iass_tuple = (parent, child)
                        list_of_iass_relation.append(iass_tuple)
                        logger.debug("Found IASS: (%s, %s)" % (iass_tuple[0], iass_tuple[1]))
        list_of_iass_relation = list(dict.fromkeys(list_of_iass_relation))
        return list_of_iass_relation

    def IASS(self):
        """
        IASS (Inheritance ASSociation)
        :return: return list of tuples for classes that have IASS relation
        """
        logger.info("IASS (Inheritance ASSociation)")
        logger.info("Step1: Get all parent and child classes")
        inh = self.get_node_by_name("inheritance")
        logger.debug("inheritance: %s" % inh)
        logger.info("Step2: Get all Association relation classes")
        ass = self.get_node_by_name("association")
        logger.debug("association: %s" % ass)
        return self.__IASS_helper(inh, ass)

    def __SAGG_helper(self, agg):
        """
        Helper for SAGG method
        :param agg: aggregation
        :return: list of tuples
        """
        list_of_sagg_relation = list()
        if agg is None:
            logger.info("There are no SAGG relations")
        else:
            for relation in agg:
                if relation.attrib.get("ci") == relation.attrib.get("cj"):
                    sagg_tuple = tuple()+ (relation.attrib.get("ci"), )
                    list_of_sagg_relation.append(sagg_tuple)
                    logger.debug("Found SAGG: (%s)" % (sagg_tuple[0]))
            list_of_sagg_relation = list(dict.fromkeys(list_of_sagg_relation))
        return list_of_sagg_relation

    def SAGG(self):
        """
        SAGG (Self-Aggregation)
        :return: return list of tuples for classes that have IASS relation
        """
        logger.info("SAGG (Self-Aggregation)")
        logger.info("Step1: Get all Aggregation relation classes")
        agg = self.get_node_by_name("aggregation")
        logger.debug("aggregation: %s" % agg)
        return self.__SAGG_helper(agg)

    def __IIAGG_helper(self, inh, agg):
        """
        Helper for IIAGG method
        :param inh: inheritance
        :param agg: aggregation
        :return: list of tuples
        """
        list_of_iiagg_relation = list()
        if inh is None or agg is None:
            logger.info("There are no IIAGG relations")
        else:
            for parent_and_child in inh:
                parent = parent_and_child.attrib.get("ci")
                child = parent_and_child.attrib.get("cj")
                for inner_parent_and_child in inh:
                    inner_parent = inner_parent_and_child.attrib.get("ci")
                    inner_child = inner_parent_and_child.attrib.get("cj")
                    if inner_parent == child:
                        for relation in agg:
                            if inner_child == relation.attrib.get("ci") and parent == relation.attrib.get("cj"):
                                iiagg_tuple = (parent, child, inner_child)
                                list_of_iiagg_relation.append(iiagg_tuple)
                                logger.debug("Found IIAGG: (%s, %s, %s)" % (iiagg_tuple[0], iiagg_tuple[1],
                                                                            iiagg_tuple[2]))
            list_of_iiagg_relation = list(dict.fromkeys(list_of_iiagg_relation))
        return list_of_iiagg_relation

    def IIAGG(self):
        """
        IIAGG (Indirect Inheritance AGGregation)
        :return: return list of tuples for classes that have IIAGG relation
        """
        logger.info("IIAGG (Indirect Inheritance AGGregation)")
        logger.info("Step1: Get all parent and child classes")
        inh = self.get_node_by_name("inheritance")
        logger.debug("inheritance: %s" % inh)
        logger.info("Step2: Get all Aggregation relation classes")
        agg = self.get_node_by_name("aggregation")
        logger.debug("aggregation: %s" % agg)
        return self.__IIAGG_helper(inh, agg)

    def __SASS_helper(self, ass):
        """
        Helper for SASS method
        :param ass: association
        :return: list of tuples
        """
        list_of_sass_relation = list()
        if ass is None:
            logger.info("There are no SASS relations")
        else:
            for relation in ass:
                if relation.attrib.get("ci") == relation.attrib.get("cj"):
                    sass_tuple = tuple() + (relation.attrib.get("ci"), )
                    list_of_sass_relation.append(sass_tuple)
                    logger.debug("Found SASS: (%s)" % (sass_tuple[0]))
        list_of_sass_relation = list(dict.fromkeys(list_of_sass_relation))
        index = 0
        while True:
            if list_of_sass_relation[index] in self.SAGG():
                del list_of_sass_relation[index]
                index = 0
            else:
                index = index + 1
            if index == len(list_of_sass_relation):
                break
        return list_of_sass_relation

    def SASS(self):
        """
        SASS (Self-ASSociation)
        :return: return list of tuples for classes that have SASS relation
        """
        logger.info("SASS (Self-ASSociation)")
        logger.info("Step1: Get all Association relation classes")
        ass = self.get_node_by_name("association")
        logger.debug("association: %s" % ass)
        return self.__SASS_helper(ass)

    def __ICD_helper(self, inh, dep):
        """
        Helper for ICD method
        :param ass: association
        :return: list of tuples
        """
        list_of_ica_relation = list()
        if inh is None or dep is None:
            logger.info("There are no ICD relations")
        else:
            for parent_and_child in inh:
                parent = parent_and_child.attrib.get("ci")
                child = parent_and_child.attrib.get("cj")
                for relation in dep:
                    if relation.attrib.get("cj") == child:
                        dci_tuple = (parent, child, relation.attrib.get("ci"))
                        list_of_ica_relation.append(dci_tuple)
                        logger.debug("Found ICD: (%s, %s, %s)" % (dci_tuple[0], dci_tuple[1], dci_tuple[2]))
        list_of_ica_relation = list(dict.fromkeys(list_of_ica_relation))
        return list_of_ica_relation

    def ICD(self):
        """
        ICD (Inheritance Child Dependency)
        :return: return list of tuples for classes that have ICD relation
        """
        logger.info("ICD (Inheritance Child Dependency)")
        logger.info("Step1: Get all parent and child classes")
        inh = self.get_node_by_name("inheritance")
        logger.debug("inheritance: %s" % inh)
        logger.info("Step2: Get all Depends relation classes")
        dep = self.get_node_by_name("depends")
        logger.debug("depends: %s" % dep)
        return self.__ICD_helper(inh, dep)

    def __DCI_helper(self, inh, dep):
        """
        Helper for DCI method
        :param ass: association
        :return: list of tuples
        """
        list_of_dci_relation = list()
        if inh is None or dep is None:
            logger.info("There are no DCI relations")
        else:
            for parent_and_child in inh:
                parent = parent_and_child.attrib.get("ci")
                child = parent_and_child.attrib.get("cj")
                for relation in dep:
                    if relation.attrib.get("ci") == child:
                        icd_tuple = (parent, child,relation.attrib.get("cj"))
                        list_of_dci_relation.append(icd_tuple)
                        logger.debug("Found DCI: (%s, %s, %s)" % (icd_tuple[0], icd_tuple[1], icd_tuple[2]))
        list_of_dci_relation = list(dict.fromkeys(list_of_dci_relation))
        return list_of_dci_relation

    def DCI(self):
        """
        DCI (Dependency Child Inheritance)
        :return: return list of tuples for classes that have DCI relation
        """
        logger.info("DCI (Dependency Child Inheritance)")
        logger.info("Step1: Get all parent and child classes")
        inh = self.get_node_by_name("inheritance")
        logger.debug("inheritance: %s" % inh)
        logger.info("Step2: Get all Depends relation classes")
        dep = self.get_node_by_name("depends")
        logger.debug("depends: %s" % dep)
        return self.__DCI_helper(inh, dep)

    def __IPAS_helper(self, inh, ass):
        """
        Helper for IPAS method
        :param inh: inheritance
        :param ass: association
        :return: list of tuples
        """
        list_of_ipas_relation = list()
        if inh is None or ass is None:
            logger.info("There are no IPAS relations")
        else:
            for parent_and_child in inh:
                parent = parent_and_child.attrib.get("ci")
                child = parent_and_child.attrib.get("cj")
                for relation in ass:
                    if parent == relation.attrib.get("cj"):
                        ipas_tuple = (parent, child, relation.attrib.get("ci"))
                        list_of_ipas_relation.append(ipas_tuple)
                        logger.debug("Found IPAS: (%s, %s, %s)" % (ipas_tuple[0], ipas_tuple[1], ipas_tuple[2]))
        list_of_ipas_relation = list(dict.fromkeys(list_of_ipas_relation))
        return list_of_ipas_relation

    def IPAS(self):
        """
        IPAS (Inheritance Parent ASsociation)
        :return: return list of tuples for classes that have IPAS relation
        """
        logger.info("IPAS (Inheritance Parent ASsociation)")
        logger.info("Step1: Get all parent and child classes")
        inh = self.get_node_by_name("inheritance")
        logger.debug("inheritance: %s" % inh)
        logger.info("Step2: Get all Association relation classes")
        ass = self.get_node_by_name("association")
        logger.debug("association: %s" % ass)
        return self.__IPAS_helper(inh, ass)

    def __AGPI_helper(self, inh, agg):
        """
        Helper for AGPI method
        :param inh: inheritance
        :param agg: aggregation
        :return: list of tuples
        """
        list_of_agpi_relation = list()
        if inh is None or agg is None:
            logger.info("There are no AGPI relations")
        else:
            for parent_and_child in inh:
                parent = parent_and_child.attrib.get("ci")
                child = parent_and_child.attrib.get("cj")
                for relation in agg:
                    if parent == relation.attrib.get("cj"):
                        agpi_tuple = (parent, child, relation.attrib.get("ci"))
                        list_of_agpi_relation.append(agpi_tuple)
                        logger.debug("Found AGPI: (%s, %s, %s)" % (agpi_tuple[0], agpi_tuple[1], agpi_tuple[2]))
        list_of_agpi_relation = list(dict.fromkeys(list_of_agpi_relation))
        return list_of_agpi_relation

    def AGPI(self):
        """
        AGPI (AGgregation Parent Inherited)
        :return: return list of tuples for classes that have AGPI relation
        """
        logger.info("AGPI (AGgregation Parent Inherited)")
        logger.info("Step1: Get all parent and child classes")
        inh = self.get_node_by_name("inheritance")
        logger.debug("inheritance: %s" % inh)
        logger.info("Step2: Get all Aggregation relation classes")
        agg = self.get_node_by_name("aggregation")
        logger.debug("aggregation: %s" % agg)
        return self.__AGPI_helper(inh, agg)

    def __IPD_helper(self, inh, dep):
        """
        Helper for IPD method
        :param ass: association
        :return: list of tuples
        """
        list_of_ipd_relation = list()
        if inh is None or dep is None:
            logger.info("There are no IPD relations")
        else:
            for parent_and_child in inh:
                parent = parent_and_child.attrib.get("ci")
                child = parent_and_child.attrib.get("cj")
                for relation in dep:
                    if relation.attrib.get("cj") == parent:
                        ipd_tuple = (parent, child, relation.attrib.get("ci"))
                        list_of_ipd_relation.append(ipd_tuple)
                        logger.debug("Found IPD: (%s, %s, %s)" % (ipd_tuple[0], ipd_tuple[1], ipd_tuple[2]))
        list_of_ipd_relation = list(dict.fromkeys(list_of_ipd_relation))
        return list_of_ipd_relation

    def IPD(self):
        """
        IPD (Inheritance Parent Dependency)
        :return: return list of tuples for classes that have IPD relation
        """
        logger.info("IPD (Inheritance Parent Dependency)")
        logger.info("Step1: Get all parent and child classes")
        inh = self.get_node_by_name("inheritance")
        logger.debug("inheritance: %s" % inh)
        logger.info("Step2: Get all Depends relation classes")
        dep = self.get_node_by_name("depends")
        logger.debug("depends: %s" % dep)
        return self.__IPD_helper(inh, dep)

    def __DPI_helper(self, inh, dep):
        """
        Helper for DPI method
        :param dep: association
        :return: list of tuples
        """
        list_of_dpi_relation = list()
        if inh is None or dep is None:
            logger.info("There are no DPI relations")
        else:
            for parent_and_child in inh:
                parent = parent_and_child.attrib.get("ci")
                child = parent_and_child.attrib.get("cj")
                for relation in dep:
                    if relation.attrib.get("ci") == parent:
                        dpi_tuple = (parent, child, relation.attrib.get("cj"))
                        list_of_dpi_relation.append(dpi_tuple)
                        logger.debug("Found DPI: (%s, %s, %s)" % (dpi_tuple[0], dpi_tuple[1], dpi_tuple[2]))
        list_of_dpi_relation = list(dict.fromkeys(list_of_dpi_relation))
        return list_of_dpi_relation

    def DPI(self):
        """
        DPI (Dependency Parent Inherited)
        :return: return list of tuples for classes that have DPI relation
        """
        logger.info("DPI (Dependency Parent Inherited)")
        logger.info("Step1: Get all parent and child classes")
        inh = self.get_node_by_name("inheritance")
        logger.debug("inheritance: %s" % inh)
        logger.info("Step2: Get all Depends relation classes")
        dep = self.get_node_by_name("depends")
        logger.debug("depends: %s" % dep)
        return self.__DPI_helper(inh, dep)
