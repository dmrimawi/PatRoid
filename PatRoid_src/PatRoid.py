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
import os

#################
# Local Imports #
#################

from PatRoidException import PatRoidException
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
__credits__ = ["Dr. Samer Zein"]
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
    project_location.add_argument("-d", "--dir", dest="projects_dir", help="A directory the contains one or more "
                                                                           "Android App", default=None)
    module_name.add_argument("-m", "--module-file-name", dest="module_file_name", help="XML file to save the "
                                                                                       "relationships in and/or read "
                                                                                       "them from. "
                                                                                       "Run with --path, "
                                                                                       "or as input.", default=None)
    debug.add_argument("--debug-mode", dest="debug_mode", help="Print traceback", default=False,
                       action='store_true')
    return parser


def parse_ags():
    """
    This method call the add_args method and parse the arguments to start work
    :return: raise an exception if there is a missing argument, and parseargs object otherwise
    """
    args = add_args().parse_args()
    if args.projects_dir is None and args.project_path is None and args.module_file_name is None:
        raise PatRoidException("Input is missing, please use [--path | --dir | --module-file-name]")
    elif args.module_file_name is None and args.project_path is not None:
        logger.warning("Module file name is missing, will save module in: %s" % DEFAULT_MODULE_NAME)
        args.module_file_name = DEFAULT_MODULE_NAME
    else:
        logger.warning("You will find the module file inside the src dir, each holding the Android App name")
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
        self.sub_patterns_dict = None

    @staticmethod
    def build_module_file_flow(args):
        rc = 0
        get_mani_and_java = GetManiAndJava(args.project_path)
        java_files = get_mani_and_java.get_all_java_files()
        if len(java_files) == 0:
            raise PatRoidException("Project doesn't contain any java files")
        manifest_file = get_mani_and_java.get_project_manifest()
        if manifest_file is None:
            raise PatRoidException("Project doesn't contain a Manifest file")
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

    def set_definitions(self, args):
        """
        This method set all 15 definitions
        :return: it sets values as class parameters
        """
        sub_patterns = SubPatterns(args.module_file_name)
        self.sub_patterns_dict = dict()
        self.sub_patterns_dict["ICA"] = sub_patterns.ICA()
        self.sub_patterns_dict["CI"] = sub_patterns.CI()
        self.sub_patterns_dict["IAGG"] = sub_patterns.IAGG()
        self.sub_patterns_dict["IPAG"] = sub_patterns.IPAG()
        self.sub_patterns_dict["MLI"] = sub_patterns.MLI()
        self.sub_patterns_dict["IASS"] = sub_patterns.IASS()
        self.sub_patterns_dict["SAGG"] = sub_patterns.SAGG()
        self.sub_patterns_dict["IIAGG"] = sub_patterns.IIAGG()
        self.sub_patterns_dict["SASS"] = sub_patterns.SASS()
        self.sub_patterns_dict["ICD"] = sub_patterns.ICD()
        self.sub_patterns_dict["DCI"] = sub_patterns.DCI()
        self.sub_patterns_dict["IPAS"] = sub_patterns.IPAS()
        self.sub_patterns_dict["AGPI"] = sub_patterns.AGPI()
        self.sub_patterns_dict["IPD"] = sub_patterns.IPD()
        self.sub_patterns_dict["DPI"] = sub_patterns.DPI()
        logger.debug("For module [%s], sub-patterns are: %s" % (args.module_file_name, self.sub_patterns_dict))

    def detect_design_patterns(self):
        """
        This method calls the design patterns detection class methods, to filter and print detected design patterns
        :return: dict of design patterns and where they found
        """
        detected_design_patterns = dict()
        detect_dp = DetectDP()
        detected_design_patterns["singleton"] = detect_dp.detect_singleton(self.sub_patterns_dict["SASS"])
        detected_design_patterns["composite"] = detect_dp.detect_composite(self.sub_patterns_dict["SAGG"],
                                                                           self.sub_patterns_dict["CI"],
                                                                           self.sub_patterns_dict["IIAGG"],
                                                                           self.sub_patterns_dict["IAGG"])
        detected_design_patterns["template"] = detect_dp.detect_template(self.sub_patterns_dict["CI"])
        detected_design_patterns["abstract_factory"] = detect_dp.detect_abstract_factory(self.sub_patterns_dict["DCI"],
                                                                                         self.sub_patterns_dict["ICD"],
                                                                                         self.sub_patterns_dict["CI"])
        detected_design_patterns["adapter"] = detect_dp.detect_adapter(self.sub_patterns_dict["CI"],
                                                                       self.sub_patterns_dict["ICA"])
        detected_design_patterns["bridge"] = detect_dp.detect_bridge(self.sub_patterns_dict["IPAG"],
                                                                     self.sub_patterns_dict["CI"])
        detected_design_patterns["builder"] = detect_dp.detect_builder(self.sub_patterns_dict["ICA"],
                                                                       self.sub_patterns_dict["AGPI"])
        detected_design_patterns["chain_of_responsibility"] = detect_dp.detect_chain_of_responsibility(
            self.sub_patterns_dict["SASS"], self.sub_patterns_dict["CI"])
        detected_design_patterns["command"] = detect_dp.detect_command(self.sub_patterns_dict["AGPI"],
                                                                       self.sub_patterns_dict["ICA"])
        detected_design_patterns["decorator"] = detect_dp.detect_decorator(self.sub_patterns_dict["CI"],
                                                                           self.sub_patterns_dict["IAGG"],
                                                                           self.sub_patterns_dict["MLI"])
        detected_design_patterns["facad"] = detect_dp.detect_facad(self.sub_patterns_dict["ICD"])
        detected_design_patterns["factory"] = detect_dp.detect_factory(self.sub_patterns_dict["ICD"],
                                                                       self.sub_patterns_dict["DCI"])
        detected_design_patterns["flyweight"] = detect_dp.detect_flyweight(self.sub_patterns_dict["CI"],
                                                                           self.sub_patterns_dict["AGPI"])
        detected_design_patterns["interpreter"] = detect_dp.detect_interpreter(self.sub_patterns_dict["IAGG"],
                                                                               self.sub_patterns_dict["IPD"],
                                                                               self.sub_patterns_dict["CI"])
        detected_design_patterns["iterator"] = detect_dp.detect_iterator(self.sub_patterns_dict["DCI"],
                                                                         self.sub_patterns_dict["ICA"],
                                                                         self.sub_patterns_dict["ICD"])
        detected_design_patterns["mediator"] = detect_dp.detect_mediator(self.sub_patterns_dict["ICA"],
                                                                         self.sub_patterns_dict["CI"],
                                                                         self.sub_patterns_dict["IPAS"])
        detected_design_patterns["memento"] = detect_dp.detect_memento(self.sub_patterns_dict["AGPI"],
                                                                       self.sub_patterns_dict["DPI"])
        detected_design_patterns["observer"] = detect_dp.detect_observer(self.sub_patterns_dict["AGPI"],
                                                                         self.sub_patterns_dict["ICD"])
        detected_design_patterns["prototype"] = detect_dp.detect_prototype(self.sub_patterns_dict["CI"],
                                                                           self.sub_patterns_dict["AGPI"])
        detected_design_patterns["proxy"] = detect_dp.detect_proxy(self.sub_patterns_dict["CI"],
                                                                   self.sub_patterns_dict["ICA"],
                                                                   self.sub_patterns_dict["IASS"])
        detected_design_patterns["state"] = detect_dp.detect_state(self.sub_patterns_dict["AGPI"],
                                                                   self.sub_patterns_dict["CI"])
        detected_design_patterns["strategy"] = detect_dp.detect_strategy(self.sub_patterns_dict["AGPI"],
                                                                         self.sub_patterns_dict["CI"])
        detected_design_patterns["visitor"] = detect_dp.detect_visitor(self.sub_patterns_dict["AGPI"],
                                                                       self.sub_patterns_dict["ICD"],
                                                                       self.sub_patterns_dict["DPI"])
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

    def __call_def_db_detect(self, args):
        """
        This is a helper method just to call repeatedly called code
        :param args: Script args
        :return: detected_design_patterns
        """
        self.set_definitions(args)
        detected_design_patterns = self.detect_design_patterns()
        self.print_dp_final_dict(detected_design_patterns)
        detected_design_patterns["SUBPATTERNS"] = self.sub_patterns_dict
        return detected_design_patterns

    def build_module_dir_flow(self, args):
        """
        This method go over all the Android Apps and
        :param args: Scrip args
        :return: dictionary with all apps and their db dict
        """
        rc = 0
        general_dict = dict()
        directory = args.projects_dir
        all_android_repos = os.listdir(directory)
        for android_app in all_android_repos:
            logger.info("Searching for DPs in: %s" % android_app)
            args.module_file_name = os.path.join(directory, "%s.xml" % android_app)
            args.project_path = os.path.join(directory, android_app)
            if not os.path.isdir(args.project_path):
                continue
            try:
                rc = self.build_module_file_flow(args) or rc
                general_dict[android_app] = self.__call_def_db_detect(args)
            except PatRoidException as exp:
                logger.warning("Android App [%s] has an issue that indicate that no DPs were used: %s" %
                               (android_app, exp))
                general_dict[android_app] = dict()
        logger.info("Found the following DPs: \n%s" % general_dict)
        return rc

    def main(self, args):
        """
        Main method to manage the project
        :param: args: Project cmd line args
        :return: rc
        """
        rc = 0
        if args.project_path:
            rc = self.build_module_file_flow(args) or rc
            _ = self.__call_def_db_detect(args)
        elif args.projects_dir:
            rc = self.build_module_dir_flow(args) or rc
        else:
            _ = self.__call_def_db_detect(args)
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
