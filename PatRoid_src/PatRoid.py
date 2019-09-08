#!/usr/bin/env python

"""
    This project contains a prove of concept for detecting design patterns used
    inside an Android application.
    It is part of Diaeddin M. Rimawi seminar under the supervision of Dr. Samer Al_Zain
    Seminar title: A Model-Based Approach for Design Patterns Recognition in Android Apps
    Joint Master of Software Engineering | Birzeit University
"""

##################
# Python Imports #
##################

import sys
import argparse
import traceback

#################
# Local Imports #
#################

from ADPDException import ADPDException
from GetManiAndJava import GetManiAndJava
from ManifestParser import ManifestParser
from JavaFilesInfo import JavaFilesInfo
from CreateRelationsModule import CreateRelationsModule
from SubPatterns import SubPatterns
from DetectDP import DetectDP
from Logger import Logger
logger = Logger()

#############
# CONSTANTS #
#############

__author__ = "Diaeddin M. Rimawi"
__copyright__ = "Copyright 2019, A Model-Based Approach for Design Patterns Detection in Android Apps"
__credits__ = ["Dr. Samer Al-Zain"]
__license__ = "GPL"
__version__ = "1.0.0-1"
__maintainer__ = "Diaeddin M. Rimawi"
__email__ = "dmrimawi@gmail.com"
__status__ = "Prototype"

DEFAULT_MODULE_NAME = "output_module.xml"

##################
# Global methods #
##################


def add_args():
    """
    This method adds the needed arguments for this project
    :return: argparse object
    """
    parser = argparse.ArgumentParser(description=__copyright__)
    debug = parser.add_argument_group("Running Mode")
    project_location = parser.add_argument_group("Android project source code")
    module_name = parser.add_argument_group("Name and location of the relationships module")
    project_location.add_argument("-p", "--path", dest="project_path", help="A path to the input project to extract "
                                                                            "design patterns from", default=None)
    module_name.add_argument("-m", "--module-file-name", dest="module_file_name", help="XML file to save the "
                                                                                       "relationships in and/or read "
                                                                                       "them from", default=None)
    debug.add_argument("-d", "--debug-mode", dest="debug_mode", help="Print traceback", default=False,
                       action='store_true')
    return parser


def parse_ags():
    """
    This method call the add_args method and parse the arguments to start work
    :return: raise an exception if there is a missing argument, and parseargs object otherwise
    """
    args = add_args().parse_args()
    if args.project_path is None and args.module_file_name is None:
        raise ADPDException("Both project path and module file are missing, please provide one or both to continue.")
    elif args.module_file_name is None:
        logger.warning("Module file name is missing, will use default name instead: %s"% DEFAULT_MODULE_NAME)
        args.module_file_name = DEFAULT_MODULE_NAME
    return args

################
# Driver Class #
################


class Driver(object):
    """
    This class is a navigator to run the project
    """
    def __init__(self):
        """
        Set global attributes
        """
        self.sagg_relations = None
        self.iagg_relations = None
        self.ci_relations = None
        self.ica_relations = None
        self.agpi_relations = None
        self.dci_relations = None
        self.dpi_relations = None
        self.iass_relations = None
        self.icd_relations = None
        self.iiagg_relations = None
        self.ipag_relations = None
        self.ipas_relations = None
        self.ipd_relations = None
        self.mli_relations = None
        self.sass_relations = None


    @staticmethod
    def build_module_file_flow(args):
        rc = 0
        get_mani_and_java = GetManiAndJava(args.project_path)
        java_files = get_mani_and_java.get_all_java_files()
        if len(java_files) == 0:
            raise ADPDException("Project doesn't contain any java files")
        manifest_file = get_mani_and_java.get_project_manifest()
        if manifest_file is None:
            raise ADPDException("Project doesn't contain a Manifest file")
        logger.info("Manifest file is: \n%s" % manifest_file)
        parse_manifest = ManifestParser(manifest_file)
        manifest_info = parse_manifest.get_activities_classes_dict(java_files)
        logger.info("Activities are: %s" % manifest_info)
        logger.info("Java files are (#%s): \n%s" % (len(java_files), "\n".join(java_files)))
        java_classes = JavaFilesInfo.get_list_of_classes_names(java_files)
        logger.info("Java classes are: %s" % java_classes)
        inheritance_relation = JavaFilesInfo.get_inherentance_relations(java_files)
        logger.info("Inheritance: %s" % inheritance_relation)
        association_relation = JavaFilesInfo.get_association_relations(java_files)
        logger.info("Association relationships are between: %s" % association_relation)
        aggregation_relation = JavaFilesInfo.get_aggregation_relations(java_files)
        logger.info("Aggregation relationships are between: %s" % aggregation_relation)
        depends_relation = JavaFilesInfo.get_depends_relations(java_files)
        logger.info("Depends relationships are between: %s" % depends_relation)
        build_module_file = CreateRelationsModule(args.module_file_name)
        logger.info("Writing relations to the module file...")
        build_module_file.build_relations_module(depends_relation, association_relation, inheritance_relation,
                                                 aggregation_relation, manifest_info)
        logger.info("Done")
        return rc

    def set_definitions(self):
        """
        This method set all 15 definitions
        :return: it sets values as class parameters
        """
        sub_patterns = SubPatterns(args.module_file_name)
        self.ica_relations = sub_patterns.ICA()
        logger.info("1. ICA relations: %s" % self.ica_relations)
        self.ci_relations = sub_patterns.CI()
        logger.info("2. CI relations: %s" % self.ci_relations)
        self.iagg_relations = sub_patterns.IAGG()
        logger.info("3. IAGG relations: %s" % self.iagg_relations)
        self.ipag_relations = sub_patterns.IPAG()
        logger.info("4. IPAG relations: %s" % self.ipag_relations)
        self.mli_relations = sub_patterns.MLI()
        logger.info("5. MLI relations: %s" % self.mli_relations)
        self.iass_relations = sub_patterns.IASS()
        logger.info("6. IASS relations: %s" % self.iass_relations)
        self.sagg_relations = sub_patterns.SAGG()
        logger.info("7. SAGG relations: %s" % self.sagg_relations)
        self.iiagg_relations = sub_patterns.IIAGG()
        logger.info("8. IIAGG relations: %s" % self.iiagg_relations)
        self.sass_relations = sub_patterns.SASS()
        logger.info("9. SASS relations: %s" % self.sass_relations)
        self.icd_relations = sub_patterns.ICD()
        logger.info("10. ICD relations: %s" % self.icd_relations)
        self.dci_relations = sub_patterns.DCI()
        logger.info("11. DCI relations: %s" % self.dci_relations)
        self.ipas_relations = sub_patterns.IPAS()
        logger.info("12. IPAS relations: %s" % self.ipas_relations)
        self.agpi_relations = sub_patterns.AGPI()
        logger.info("13. AGPI relations: %s" % self.agpi_relations)
        self.ipd_relations = sub_patterns.IPD()
        logger.info("14. IPD relations: %s" % self.ipd_relations)
        self.dpi_relations = sub_patterns.DPI()
        logger.info("15. DPI relations: %s" % self.dpi_relations)

    def detect_design_patterns(self):
        """
        This method calls the design patterns detection class methods, to filter and print detected design patterns
        :return: dict of design patterns and where they found
        """
        detected_design_patterns = dict()
        detect_dp = DetectDP()
        detected_design_patterns["singleton"] = detect_dp.detect_singleton(self.sass_relations)
        detected_design_patterns["composite"] = detect_dp.detect_composite(self.sagg_relations, self.ci_relations,
                                                                  self.iiagg_relations, self.iagg_relations)
        detected_design_patterns["template"] = detect_dp.detect_template(self.ci_relations)
        detected_design_patterns["abstract_factory"] = detect_dp.detect_abstract_factory(self.dci_relations, self.icd_relations,
                                                                         self.ci_relations)
        detected_design_patterns["adapter"] = detect_dp.detect_adapter(self.ci_relations, self.ica_relations)
        detected_design_patterns["bridge"] = detect_dp.detect_bridge(self.ipag_relations, self.ci_relations)
        detected_design_patterns["builder"] = detect_dp.detect_builder(self.ica_relations, self.agpi_relations)
        detected_design_patterns["chain_of_responsibility"] = detect_dp.detect_chain_of_responsibility(self.sass_relations, self.ci_relations)
        detected_design_patterns["command"] = detect_dp.detect_command(self.agpi_relations, self.ica_relations)
        detected_design_patterns["decorator"] = detect_dp.detect_decorator(self.ci_relations, self.iagg_relations,
                                                                  self.mli_relations)
        detected_design_patterns["facad"] = detect_dp.detect_facad(self.icd_relations)
        detected_design_patterns["factory"] = detect_dp.detect_factory(self.icd_relations, self.dci_relations)
        detected_design_patterns["flyweight"] = detect_dp.detect_flyweight(self.ci_relations, self.agpi_relations)
        detected_design_patterns["interpreter"] = detect_dp.detect_interpreter(self.iagg_relations, self.ipd_relations,
                                                                    self.ci_relations)
        detected_design_patterns["iterator"] = detect_dp.detect_iterator(self.dci_relations, self.ica_relations,
                                                                 self.icd_relations)
        detected_design_patterns["mediator"] = detect_dp.detect_mediator(self.ica_relations, self.ci_relations,
                                                                 self.ipas_relations)
        detected_design_patterns["memento"] = detect_dp.detect_memento(self.agpi_relations, self.dpi_relations)
        detected_design_patterns["observer"] = detect_dp.detect_observer(self.agpi_relations, self.icd_relations)
        detected_design_patterns["prototype"] = detect_dp.detect_prototype(self.ci_relations, self.agpi_relations)
        detected_design_patterns["proxy"] = detect_dp.detect_proxy(self.ci_relations, self.ica_relations,
                                                              self.iass_relations)
        detected_design_patterns["state"] = detect_dp.detect_state(self.agpi_relations, self.ci_relations)
        detected_design_patterns["strategy"] = detect_dp.detect_strategy(self.agpi_relations, self.ci_relations)
        detected_design_patterns["visitor"] = detect_dp.detect_visitor(self.agpi_relations, self.icd_relations,
                                                                self.dpi_relations)
        return detected_design_patterns

    def print_dp_final_dict(self, detected_design_patterns):
        """
        This method prints the founded design patterns and where they were found
        :param detected_design_patterns: dict if founded design patterns
        :return: Nothins just pring output
        """
        for dp_name, dp_info in detected_design_patterns.iteritems():
            if len(dp_info):
                logger.info("Design Pattern [%s] is found in: %s" % (dp_name, dp_info))

    def main(self, args):
        """
        Main method to manage the project
        :param: args: Project cmd line args
        :return: rc
        """
        rc = 0
        if args.project_path:
            rc = Driver.build_module_file_flow(args) or rc
        self.set_definitions()
        detected_design_patterns = self.detect_design_patterns()
        self.print_dp_final_dict(detected_design_patterns)
        return rc


if __name__ == "__main__":
    try:
        args = parse_ags()
        driver = Driver()
        rc = driver.main(args)
        sys.exit(rc)
    except Exception as exp:
        logger.error("%s" % exp)
        if args.debug_mode:
            traceback.print_exc()
        sys.exit(1)
