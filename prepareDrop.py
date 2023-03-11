#! /usr/bin/env python
#
# prepare_drop.py path/to/drop/folder

# TODO: add possibility to choose location from which to get the files; at the moment the working directory is used

import shutil
import argparse
import sys
import os
import re
import datetime

now = str(datetime.datetime.now())
lcids = {"Brazilian_Portuguese": "1046", "Chinese_Simplified": "2052", "Chinese_Traditional": "1028", "Danish": "1030", "English": "1033", "Finnish": "1035", "German": "1031",
         "Hebrew": "1037", "Hungarian": "1038", "Italian": "1040", "Korean": "1042", "Portuguese": "2070", "Russian": "1049"}

#PARAMTER PARSER FOR CMD USE
parser = argparse.ArgumentParser(description='Create a drop directory for EDC Sprint drops.')
parser.add_argument("-i", "--input", action="store", help="Specify the input project folder path.")
parser.add_argument("-o", "--output", action="store", help="Specify the Drop folder path.")
parse_arguments = parser.parse_args()
_input = parse_arguments.input
_output = parse_arguments.output

#DETERMINE INPUT FOLDER PATH
INPUT_FOLDER = _input
if INPUT_FOLDER == None:
      INPUT_FOLDER = str(os.path.dirname(os.path.realpath(__file__)))
print("Input taken from:")
print(INPUT_FOLDER)
print("__________________________________")
#DETERMINE PROJECT LANGUAGE
try:
      for dr in os.listdir(INPUT_FOLDER + "\GrammarCheckers"):
            LANGUAGE = str(dr)
except:
      raise NameError("Unrecognized project folder structure. Please place the script in the right location or pass an --input parameter.")
try:
      LCID = lcids[LANGUAGE]
except:
      raise NameError("LCID not on file for " + LANGUAGE + ". Please add the appropriate LCID to the dictionary.")
print("Detected Language:")
print(LANGUAGE + "//" + LCID)
print("__________________________________") 
#DETERMINE DROP FOLDER PATH
DROP_FOLDER = _output
if DROP_FOLDER == None:
      DROP_FOLDER = str("EDC#LRC#" + LANGUAGE + "#Drop#Sprint#" + now[0:10].replace("-", ""))
print("Generating output to:")
print(DROP_FOLDER)
print("__________________________________")

#LIST OF RELEVANT FILES FOR DROP
FILES = [
    (f"GrammarCheckers\{LANGUAGE}\Schemas\{LANGUAGE}Syntax.ans", True),
    (f"GrammarCheckers\{LANGUAGE}\Dictionaries", True),
    (f"GrammarCheckers\{LANGUAGE}\{LANGUAGE}.wscape", True),
    (f"GrammarCheckers\{LANGUAGE}\{LANGUAGE}_MAIN.txt", True),
    (f"GrammarCheckers\{LANGUAGE}\{LANGUAGE}_UI_MAIN.txt", False),
    (f"GrammarCheckers\{LANGUAGE}\LS_{LANGUAGE}_DD25_Grammar_Design_Document_for_LRC.docm", True),
    (f"ModuleProjects\POSAnnotation\{LANGUAGE}\Submodules\CRFModel.bin", True),
    (f"ModuleProjects\POSAnnotation\{LANGUAGE}\Submodules\CRFModel.bin.FeatureLexicon.bin", True),
    (f"ModuleProjects\POSAnnotation\{LANGUAGE}\Submodules\CRFNGramFilter.txt", True),
    (f"MorphModels\{LANGUAGE}\{LANGUAGE}.bin", False),
    (f"MorphModels\{LANGUAGE}\{LANGUAGE}.morph", True),
    (f"MorphModels\{LANGUAGE}\{LANGUAGE}.mproj", True),
    (f"MorphModels\{LANGUAGE}\{LANGUAGE}.mwes.cs.txt", True),
    (f"MorphModels\{LANGUAGE}\{LANGUAGE}.mwes.csGrammarMWE.txt", True),
    (f"MorphModels\{LANGUAGE}\{LANGUAGE}.mwes.csMorphMWE_NoLBC.txt", True),
    (f"MorphModels\{LANGUAGE}\{LANGUAGE}.mwes.csStyleMWE.txt", True),
    (f"MorphModels\{LANGUAGE}\{LANGUAGE}.mwes.GrammarMWE.txt", True),
    (f"MorphModels\{LANGUAGE}\{LANGUAGE}.mwes.MorphMWE_NoLBC.txt", True),
    (f"MorphModels\{LANGUAGE}\{LANGUAGE}.mwes.StyleMWE.txt", True),
    (f"MorphModels\{LANGUAGE}\{LANGUAGE}.mwes.txt", True),
    (f"TemplateLexicons\{LANGUAGE}\{LANGUAGE}ThesaurusData.xml", True),
    (f"TemplateLexicons\{LANGUAGE}\{LANGUAGE}TemplateLexicon.tlx", False),
    (f"TemplateLexicons\{LANGUAGE}\lexdata.txt", True),
    (f"TemplateLexicons\{LANGUAGE}\LS_{LANGUAGE}_DE02_Generic_Linguistic_Design_Document.docm", True),
    (f"TemplateLexicons\{LANGUAGE}\SE28_{LCID}_Bugs_RegressionData.xlsx", True),
    (f"ModuleProjects\POSAnnotation\{LANGUAGE}\Data\{LANGUAGE}_POSTrainingData.atxt", False),
    (f"ModuleProjects\POSAnnotation\{LANGUAGE}\Data\Training.zdataset", True),
    (f"TemplateLexicons\{LANGUAGE}\{LANGUAGE}WordList.wdl", False),
    (f"TemplateLexicons\{LANGUAGE}\SpellerBuildConfig.ini", True),
    (f"TemplateLexicons\{LANGUAGE}\strings.rc", False),
    (f"TemplateLexicons\{LANGUAGE}\stringsimm.lab", False),
    (f"TemplateLexicons\{LANGUAGE}\RestrictedNamedEntities.txt", True)
]

#ENGLISH SPECIFIC PROJECT FILES
LS_FILES_EN = [
	(f"TemplateLexicons\{LANGUAGE}\SE28_4105_Bugs_RegressionData.xlsx", True),
	(f"TemplateLexicons\{LANGUAGE}\SE28_3081_Bugs_RegressionData.xlsx", True),
	(f"TemplateLexicons\{LANGUAGE}\SE28_2057_Bugs_RegressionData.xlsx", True),
	(f"TemplateLexicons\{LANGUAGE}\SE28_1033_NIIAC_Bugs_RegressionData.xlsx", True),
    (f"MorphModels\{LANGUAGE}\{LANGUAGE}.mwes.csResumeMWE.txt", True),
    (f"MorphModels\{LANGUAGE}\{LANGUAGE}.mwes.ResumeMWE.txt", True),
    (f"MorphModels\{LANGUAGE}\{LANGUAGE}.mwes.csSpecialMWE.txt", True),
    (f"MorphModels\{LANGUAGE}\{LANGUAGE}.mwes.SpecialMWE.txt", True),
    (f"MorphModels\{LANGUAGE}\{LANGUAGE}.mwes.csSuggestionlessResumeMWE.txt", True),
    (f"MorphModels\{LANGUAGE}\{LANGUAGE}.mwes.SuggestionlessResumeMWE.txt", True),
    (f"MorphModels\{LANGUAGE}\{LANGUAGE}.mwes.SuggestionlessStyleMWE.txt", True),
    (f"MorphModels\{LANGUAGE}\{LANGUAGE}.mwes.csSuggestionlessStyleMWE.txt", True),
    (f"GrammarCheckers\{LANGUAGE}\RuleActions.ResourceScript.cs", True),
    (f"GrammarCheckers\{LANGUAGE}\Schemas\{LANGUAGE}Consistency.ans", True),
    (f"TemplateLexicons\{LANGUAGE}\DD24_Lexical_Needs_Analysis_for_LRC.xlsx", True)
]

if LANGUAGE == "English":
      for item in LS_FILES_EN:
            FILES.append(item)

if not os.path.exists(DROP_FOLDER):
      os.mkdir(DROP_FOLDER)
      
Missing_file_error = "Error! Could not locate file: "
Missing_opt_file_error = "Warning! Optional file not found: "

for (file, val) in FILES:
      if file.endswith("Grammar_Design_Document_for_LRC.docm"):
            try:
                  shutil.copy2(os.path.join(INPUT_FOLDER, file), DROP_FOLDER)
            except:
                  try:
                        shutil.copy2(os.path.join(INPUT_FOLDER, file.replace("GrammarCheckers","TemplateLexicons")), DROP_FOLDER)
                  except:
                        if val == True:
                              print(Missing_file_error)
                        else:
                              print(Missing_opt_file_error)
                        print(file)
      else:
            if file.endswith("Dictionaries"):
                  try:
                        shutil.copytree(os.path.join(INPUT_FOLDER, file), DROP_FOLDER + "\Dictionaries")
                  except:
                        print("Dictionaries folder not found.")
            else:
                  try:
                        shutil.copy2(os.path.join(INPUT_FOLDER, file), DROP_FOLDER)
                  except:
                        if val == True:
                              print(Missing_file_error)
                        else:
                              print(Missing_opt_file_error)
                        print(file)

