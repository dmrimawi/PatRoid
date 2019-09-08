# PatRoid

__Authors__ : Diaeddin M. Rimawi, Dr. Samer Zein

__Email__ : dmrimawi@gmail.com, szain@birzeit.edu

__Title__ : A Model Based Approach for Android Design Patterns Detection (PatRoid)

__Status__ : Prove of Concept

## Abstract

PatRoid, an automated framework for detecting design patterns. PatRoid is a model-based approach that is able to detect design patterns laying inside Android apps source code. The model is based on a graph isomorphism approach, where design patterns are divided into sub-patterns that can be aggregated to formulate design patterns. We have conducted a preliminary evaluation and the results show that PatRoid can detect all of the 23 GoF design patterns.

## PatRoid Workflow

![PatRoid Workflow Diagram](https://github.com/dmrimawi/PatRoid/blob/master/Android%20Design%20Patterns%20Detection%20Model.png)

## PatRoid Structure

![PatRoid Strucure Diagram](https://github.com/dmrimawi/PatRoid/blob/master/ADPD%20Structure.png)

## Usage
```
python .\PatRoid.py -h
usage: PatRoid.py [-h] [-p PROJECT_PATH] [-m MODULE_FILE_NAME] [-d]

Copyright 2019, A Model-Based Approach for Design Patterns Detection in
Android Apps

optional arguments:
  -h, --help            show this help message and exit

Running Mode:
  -d, --debug-mode      Print traceback

Android project source code:
  -p PROJECT_PATH, --path PROJECT_PATH
                        A path to the input project to extract design patterns
                        from

Name and location of the relationships module:
  -m MODULE_FILE_NAME, --module-file-name MODULE_FILE_NAME
                        XML file to save the relationships in and/or read them
                        from
```

## Example

```
python .\PatRoid.py -p "AndroidProjectRootDir" -m RelationalModel.xml
```
