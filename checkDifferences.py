# -*- coding: utf-8 -*-

# - 9.23.20 - WEBB - Added get_fg_list(); returns a list of all feature gates in a project
# - 9.23.20 - WEBB - Added error_check0(); looks through every feature gate referenced in an option
#                    and checks against the master fg list.

#used to check settings in deliverable
import sys
import codecs
import collections
import csv
import re
import datetime

#____________________RESOURCES______________________________
now = datetime.datetime.now()
log = []
if len(sys.argv)> 1 : 
	language_argument = re.match("^Chinese_Traditional$|^Chinese_Simplified$|^English$|^Danish$|^Finnish$|^German$|^Hebrew$|^Hungarian$|^Italian$|^Korean$|^Portuguese$|^Portuguese_Brazilian$|^Russian$",str(sys.argv[1]))
else : 
	language_argument = False
if language_argument :
		input_file = str(sys.argv[1])
else:
		while (language_argument == False):
			input_file = input('What language do you want to process? ')
			if input_file != '':
				break

input_lang = input_file
input_file = input_file + '_MAIN.txt'
WritingStyle1 = 'Grammar & more' # These are the default names, but are overwritten in a later where loop if necessary.
WritingStyle2 = 'Grammar' ######## These are the default names, but are overwritten in a later where loop if necessary.

def get_fgate_audience(input_grammar: str, fgate_name: str)-> str:
    with open(input_grammar, 'r', encoding='utf-16') as grammar:
        for line in grammar:
            if line.strip() == "== FEATURE GATES ==":
                while True:
                    line = grammar.readline().strip()
                    if re.match(fgate_name + r'\(Audience::(Microsoft|Dogfood|Production|None)\)', line):
                        pattern = re.compile(r'\(Audience::(?P<Audience>Microsoft|Dogfood|Production|None)\)')
                        match = pattern.search(line)
                        return str(match.group('Audience'))
                        break
                    elif line == '== WRITING STYLES REORDERING SCRIPT ==' or line.startswith('== TESTCASE'):
                        break
            elif line == '== WRITING STYLES REORDERING SCRIPT ==' or line.startswith('== TESTCASE'):
                break

def get_fg_list(input_grammar: str)-> list:
	#get a list of all feature gates in the project
	fgs = []
	with open(input_grammar, 'r', encoding='utf-16') as grammar: 
		for line in grammar:
			if line.strip() == '== FEATURE GATES ==':
				complete = False
				while not complete:
					line = grammar.readline().strip()
					#the feature gates are smushed with their audience, so strip the audience away and append this to a master list
					if line.endswith('Production)'):
                                            snip = len(line) - 22 #(audience::production) == 22 characters
                                            line = line[:snip]
                                            fgs.append(line)
					if line.endswith('Microsoft)'):
                                            snip = len(line) - 21 #(audience::microsoft) == 21 characters
                                            line = line[:snip]
                                            fgs.append(line)
					if line.endswith('None)'):
                                            snip = len(line) - 16 # (audience::none) == 16 characters
                                            line = line[:snip]
                                            fgs.append(line)
					if line.startswith('=='):
                                            complete = True
	return fgs

def get_default_value(input_grammar: str, option_name: str, input_dict: dict)-> dict:
    content = input_dict
    with open(input_grammar , 'r', encoding='utf-16') as grammar:
        while True:
            line = grammar.readline().strip()
            if line == '== WRITING STYLES ==':
                WritingStyle1 = next(grammar).strip()
                WritingStyle2 = next(grammar).strip()
                break
    with open(input_grammar, 'r', encoding='utf-16') as grammar:
        for line in grammar:
            if line.strip() == "== OPTION DEFAULT VALUES ==":
                while True:
                    line = grammar.readline().strip()
                    re_scan1 = option_name + r'\t' + WritingStyle1 + r'\t'
                    re_scan2 = option_name + r'\t' + WritingStyle2 + r'\t'
                    #Scans for the Option default lines for each writing style.
                    if re.match(re_scan1, line):
                        snip = len(re_scan1) - 2
                        #While scan needs r'\t' to match the line, the tab characters are not counted for len()
                        content['default_value_1'] = line[snip:]
                    elif re.match(re_scan2, line):
                        snip= len(re_scan2) - 2
                        #While scan needs r'\t' to match the line, the tab characters are not counted for len()
                        content['default_value_2'] = line[snip:]
                    if line.startswith("=="):
                        break
                return content
          
#_________________________OPTIONS___________________________
                    
def get_option(input_grammar: str, option_name: str, fieldnames: str, option_id: str)-> dict:
    content = dict.fromkeys(fieldnames)
    content['name'] = option_name
    content['id'] = option_id
    #Default whiteboard settings. These will be overwritten later where applicable.
    content['wb_licence'] = 'None'
    content['wb_fgate'] = 'None'
    content['audience'] = 'Production' 
    content['wb_app_OL'] = 'Ship'
    content['wb_app_PPT'] = 'Ship'
    with open(input_grammar, 'r', encoding='utf-16') as grammar:
        for line in grammar:
            if line.strip() == "[GC Option]":
                line = grammar.readline().strip()
                if line == option_name:
                    line = grammar.readline().strip()
                    while True:
                        line = grammar.readline().strip()
                        if line == '== GUID ==':
                            content['GUID'] = next(grammar).strip()
                        if line == '== LOCALIZED NAME ==':
                            content['localized_name'] = next(grammar) .strip()
                        if line == '== TYPE ==':
                            content['type'] = next(grammar).strip()
                        if line == '== WHITEBOARD TEST ==':
                            wb_test = str(next(grammar).strip())
                            content['whiteboard_test'] = wb_test
                            #Pull subscription licence information
                            if re.search(r'Licensing\.HaveSubscriptionLicense\=True', wb_test):
                                content['wb_licence'] = 'True'
                            elif re.search(r'Licensing\.HaveSubscriptionLicense\=False', wb_test):
                                content['wb_licence'] = 'False'
                            else:
                                content['wb_licence'] = 'None'
                            #Pull Feature Gate Information
                            if re.search(r'GrammarChecker\.OpenFeatureGates\=\*Contains\(\"([\w|]+)\"\)', wb_test):
                                if re.search(r'GrammarChecker\.OpenFeatureGates\=\*Contains\(\"(EnglishOAC[\w|]+)\"\)', wb_test):
                                    content['wb_fgate'] = 'None' 
                                else:
                                    pattern = re.compile('GrammarChecker\.OpenFeatureGates\=\*Contains\(\"(?P<FeatureGates>[\w>|]+)\"\)')
                                    match = pattern.search(wb_test)
                                    content['wb_fgate'] = str(match.group('FeatureGates'))
                                    if not re.search(r'\|', content['wb_fgate']):
                                        content['audience'] = get_fgate_audience(input_grammar, content['wb_fgate'])
                                    else:
                                        content['audience'] = 'Multi-value'
                            elif re.search(r'GrammarChecker\.OpenFeatureGates\=\*Contains\(\*StartsWith\(([\w>|]+)\)\)', wb_test):
                                pattern = re.compile('GrammarChecker\.OpenFeatureGates\=\*Contains\(\*StartsWith\((?P<FeatureGates>[\w>|]+)\)\)')
                                match = pattern.search(wb_test)
                                content['wb_fgate'] = str('StartsWith(' + match.group('FeatureGates') + ')')
                                content['audience'] = 'Multi-value'
                            else:
                                content['wb_fgate'] = 'None' 
                            #Pull App-specific behaviour for PowerPoint
                            if re.search(r'GrammarChecker\.ApplicationName\?\=NOT.*PowerPoint', wb_test):
                                content['wb_app_PPT'] = "Don't Ship"
                            else:
                                content['wb_app_PPT'] = 'Ship'
                            #Pull App-specific behaviour for Outlook
                            if re.search(r'GrammarChecker\.ApplicationName\?\=NOT.*Outlook', wb_test):
                                content['wb_app_OL'] = "Don't Ship"
                            else:
                                content['wb_app_OL'] = 'Ship'
                        if line == '== IS LIST BASED FOR TELEMETRY PURPOSES ==':
                            content['telemetry'] = "True"
                        if line == '[GC Option]' or line == '[GC Critique Type]':
                            break
                    return content

def pull_option_info(input_file: str):
    options = []
    log.append('Reading Options')
    print('Reading Options')
    with open(
        input_file , 'r', encoding='utf-16') as input_grammar, open(
        input_lang + '_Options.csv', 'w', encoding='utf-8') as whiteboard_file:
        id_counter = 0
        fieldnames = ['id', 'GUID', 'type', 'name', 'localized_name', 'under_title', 'whiteboard_test', 
        'wb_licence', 'wb_fgate', 'audience', 'wb_app_OL', 'wb_app_PPT', 'default_value_1', 'default_value_2']
        whiteboard_file.write('\ufeff')
        file_writer = csv.DictWriter(whiteboard_file, fieldnames, lineterminator='\n')
        file_writer.writeheader()
        last_title = "-"
        for line in input_grammar:
            if line.strip() == "== OPTIONS ==":
                line = input_grammar.readline().strip()
                while True:
                    id_counter += 1
                    row_values = get_option(input_file, line, fieldnames, id_counter)
                    row_values = get_default_value(input_file, line, row_values)
                    if row_values != None:
                        if row_values['type'] == 'Title':
                            last_title = line
                            row_values['under_title'] = '-'
                        elif row_values['type'] != 'Title':
                            row_values['under_title'] = last_title
                        #print('Option ' + '{:<3}: {}'.format(id_counter, line))
                        log.append(str('Option ' + '{:<3}: {}'.format(id_counter, line)))
                        file_writer.writerow(row_values)
                        options += row_values
                        line = input_grammar.readline().strip()
                    else:
                        #print('No more options found.')
                        log.append('Options read successful.')
                        print('Options read successful.')
                        break
#__________________CRITIQUE_TYPES___________________________

def get_crit(input_grammar: str, crit_name: str, fieldnames: str, crit_id: str)-> dict:
    content = dict.fromkeys(fieldnames)
    content['name'] = crit_name
    content['id'] = crit_id
    #Telemetry is only part of Main.txt when set to True. Setting default value false here.
    content['telemetry'] = "False"
    #Default whiteboard settings. These will be overwritten later where applicable.
    content['wb_licence'] = 'None'
    content['wb_fgate'] = 'None'
    content['audience'] = 'Production' 
    content['wb_app_OL'] = 'Ship'
    content['wb_app_PPT'] = 'Ship'
    with open(input_grammar, 'r', encoding='utf-16') as grammar:
        for line in grammar:
            if line.strip() == "[GC Critique Type]":
                line = grammar.readline().strip()
                if line == crit_name:
                    line = grammar.readline().strip()
                    while True:
                        line = grammar.readline().strip()
                        if line == '== GUID ==':
                            content['GUID'] = next(grammar).strip()
                        if line == '== USER-FACING NAME ==':
                            content['localized_name'] = next(grammar) .strip()
                        if line == '== PRIORITY ==':
                            content['priority'] = next(grammar).strip()
                        if line == '== CONTROLLING OPTION ==':
                            content['controlling_option'] = next(grammar).strip()
                        if line == '== WHITEBOARD TEST ==':
                            wb_test = str(next(grammar).strip())
                            content['whiteboard_test'] = wb_test
                            #Pull subscription licence information
                            if re.search(r'Licensing\.HaveSubscriptionLicense\=True', wb_test):
                                content['wb_licence'] = 'True'
                            elif re.search(r'Licensing\.HaveSubscriptionLicense\=False', wb_test):
                                content['wb_licence'] = 'False'
                            else:
                                content['wb_licence'] = 'None'
                            #Pull Feature Gate Information
                            if re.search(r'GrammarChecker\.OpenFeatureGates\=\*Contains\(\"(\w+)\"\)', wb_test):
                                if re.search(r'GrammarChecker\.OpenFeatureGates\=\*Contains\(\"(EnglishOAC[A-Za-z]+)\"\)', wb_test):
                                    print('EnglishOAC critique recognized')
                                    #EnglishOAC FGs are not the FGs associated with critiques. These critiques will maintain their 'None' wb_fgate values
                                else:
                                    pattern = re.compile('GrammarChecker\.OpenFeatureGates\=\*Contains\(\"(?P<FeatureGate>\w+)\"\)')
                                    match = pattern.search(wb_test)
                                    content['wb_fgate'] = str(match.group('FeatureGate'))
                                    content['audience'] = get_fgate_audience(input_grammar, content['wb_fgate'])
                            else:
                                content['wb_fgate'] = 'None'  
                            #Pull App-specific behaviour for PowerPoint
                            if re.search(r'GrammarChecker\.ApplicationName\?\=NOT.*PowerPoint', wb_test):
                                content['wb_app_PPT'] = "Don't Ship"
                            else:
                                content['wb_app_PPT'] = 'Ship'
                            #Pull App-specific behaviour for Outlook
                            if re.search(r'GrammarChecker\.ApplicationName\?\=NOT.*Outlook', wb_test):
                                content['wb_app_OL'] = "Don't Ship"
                            else:
                                content['wb_app_OL'] = 'Ship'
                        if line == '== IS LIST BASED FOR TELEMETRY PURPOSES ==':
                            content['telemetry'] = "True"
                        if line == '[GC Critique Type]' or line == '[Chunk Grammar]':
                            break
                    return content

def pull_crit_info(input_file: str):
    critiques = []
    log.append('Reading Critique Types:')
    print('Reading Critique Types:')
    with open(
        input_file , 'r', encoding='utf-16') as input_grammar, open(
        input_lang + '_Critiques.csv', 'w', encoding='utf-8') as whiteboard_file:
        id_counter = 0
        fieldnames = ['id', 'GUID', 'name', 'localized_name', 'controlling_option', 'priority', 'telemetry',
        'whiteboard_test', 'wb_licence', 'wb_fgate', 'audience', 'wb_app_OL', 'wb_app_PPT', 'default_value_1', 'default_value_2']
        whiteboard_file.write('\ufeff')
        file_writer = csv.DictWriter(whiteboard_file, fieldnames, lineterminator='\n')
        file_writer.writeheader()
        for line in input_grammar:
            if line.strip() == "== CRITIQUE TYPES ==":
                line = input_grammar.readline().strip()
                while True:
                    id_counter += 1
                    row_values = get_crit(input_file, line, fieldnames, id_counter)
                    if row_values != None:
                        row_values = get_default_value(input_file, row_values['controlling_option'], row_values)
                        #print('Critique ' + '{:<3}: {}'.format(id_counter, line))
                        log.append('Critique ' + '{:<3}: {}'.format(id_counter, line))
                        file_writer.writerow(row_values)
                        critiques += row_values
                        line = input_grammar.readline().strip()
                    else:
                        #print('No more critiques found.')
                        log.append('Critique Types read successful.')
                        print('Critique Types read successful.')
                        break
                    
#____________________COMPILE_FILES_________________________________
                
def pull_info(input_grammar: str):
    pull_option_info(input_grammar)
    log.append('____________________________________')
    print('____________________________________')
    pull_crit_info(input_grammar)

#_____________________ERROR_CHECKS_________________________________
    
def error_check0(input_options):
    #for each option, if that option references a feature gate, check that that fg exists
    log.append('')
    log.append('ROUND 0')
    log.append('Scanning for non-existent FGs...')
    print('')
    print('ROUND 0')
    print('Scanning for non-existent FG references...')
    with open(input_options, 'r', encoding='utf-8') as options:
        options = csv.DictReader(options)
        for option in options:
            if option['wb_fgate'] not in feature_gate_list:
                if option['wb_fgate'] != 'None':
                    log.append('  MISMATCH OR POSSIBLE ERROR @ NON-EXISTENT FG REFERENCE IN "' + option['name'] + '".')
                    log.append(option['wb_fgate'] + ' referenced in ' + option['name'] + ' is not a listed feature gate')

def error_check1(input_options):
    log.append('')
    log.append('ROUND 1')
    log.append('Checking for incongruities in Title and Binary Options.')
    print('')
    print('ROUND 1')
    print('Checking for incongruities in Title and Binary Options.')
    with open(input_options, 'r', encoding='utf-8') as options:
        options = csv.DictReader(options)
        for option in options:
            if option['type'] == "Title":
                log.append('')
                print('')
                log.append('Now processing Title Option "' + option['name'] + '".')
                print('Now processing Title Option "' + option['name'] + '".')
                if option['whiteboard_test'] == '':
                    count_w_o_whiteboard = 0
                    with open(input_options, 'r', encoding='utf-8') as options2:
                        options2 = csv.DictReader(options2)
                        for binary in options2:
                            if binary['under_title'] == option['name']:
                                if binary['whiteboard_test'] == '':
                                    count_w_o_whiteboard += 1
                        if count_w_o_whiteboard == 0:
                            log.append('  MISMATCH DETECTED for Option "' + option['name'] + '".')
                            log.append('   Title option "' + option['name'] + '" has no whiteboard test, yet no listed binary option is unrestricted.')
                            print('  MISMATCH DETECTED for Option "' + option['name'] + '".')
                            print('   Title option "' + option['name'] + '" has no whiteboard test, yet no listed binary option is unrestricted.')
                elif option['whiteboard_test'] != '':
                    fgates = []
                    fgates_output = []
                    needs_fgate = True #Default
                    needs_licence = True #Default
                    with open(input_options, 'r', encoding='utf-8') as options3:
                        options3 = csv.DictReader(options3)
                        for binary in options3:
                            if binary['under_title'] == option['name']:
                                if binary['wb_licence'] != 'True': 
                                    needs_licence = False # If one binary option does not contain a licence check, neither should the Title Option.
                                if binary['wb_fgate'] != 'None':
                                    fgates.append(binary['wb_fgate'])
                                else:
                                    needs_fgate = False # If one binary option does not contain a feature gate check, neither should the Title Option.
                    if needs_licence == True and option['wb_licence'] != 'True':
                        log.append(' MISMATCH DETECTED! Title Option has no licence check, yet all binary options are restricted.')
                        print(' MISMATCH DETECTED! Title Option has no licence check, yet all binary options are restricted.')
                    elif needs_licence == False and option['wb_licence'] == 'True':
                        log.append(' MISMATCH DETECTED! Title Option has licence check, yet at least one binary options is unrestricted.')
                        print(' MISMATCH DETECTED! Title Option has licence check, yet at least one binary options is unrestricted.')
                    if needs_fgate == True:
                        mismatches = 0
                        if option['wb_fgate'].startswith('StartsWith' or 'Contains' or 'EndsWith'):
                            log.append(' Feature Gate restriction for "' + option['name'] + '" ("' + option['wb_fgate'] + '")is not a literal match. Please review manually.')
                            print(' Feature Gate restriction for "' + option['name'] + '" ("' + option['wb_fgate'] + '")is not a literal match. Please review manually.')
                        else:
                            for fgate in fgates:
                                if re.search(fgate, option['wb_fgate']):
                                    fgates_output.append('Present: ' + fgate)
                                else:
                                    fgates_output.append('Missing: ' + fgate)
                                    mismatches += 1 # If all binary options have Feature Gate checks, the Title Option should be restricted for all these Feature Gates as well.
                            if mismatches > 0:
                                log.append(' MISMATCH DETECTED! More Feature Gate restrictions required. Feature Gates check should contain:')
                                print(' MISMATCH DETECTED! More Feature Gate restrictions required. Feature Gates check should contain:')
                                for fgate in fgates_output:
                                    log.append(fgate)          

def error_check2(input_options, input_critiques):
    log.append('')
    log.append('ROUND 2')
    log.append("Checking for incongruities in Critique Types' and Options' Settings.")
    print('')
    print('ROUND 2')
    print("Checking for incongruities in Critique Types' and Options' Settings.")
    with open(input_options, 'r', encoding='utf-8') as options:
        options = csv.DictReader(options)
        title_count = 0 #If Title_count is == 1, Option is "Grammar", if > 1, Option is Style/ENT
        for option in options:
            if option['type'] == 'Title':
                title_count += 1
            if option['type'] == "Binary":
                log.append('')
                print('')
                log.append('Now processing Binary Option "' + option['name'] + '".')
                print('Now processing Binary Option "' + option['name'] + '".')
                crit_count = 0
                with open(input_critiques, 'r', encoding='utf-8') as critiques:
                    critiques = csv.DictReader(critiques)
                    for critique in critiques:
                        #print('Now processing: ' + critique['name'] + ' for ' + option['name'])
                        if critique['controlling_option'] == option['name']:
                            #print('___________Match found!____________')
                            crit_count += 1
                if crit_count == 0:
                    log.append('   ATTENTION: "' + option['name'] + '" is not governing any Critique Types.')
                    print('   ATTENTION: "' + option['name'] + '" is not governing any Critique Types.')
                elif crit_count == 1:
                    log.append(' "' + option['name'] + '" is governing ' + str(crit_count) + ' Critique.')
                    print(' "' + option['name'] + '" is governing ' + str(crit_count) + ' Critique.')
                    #If only one critique is governed by an option, its whiteboard tests should restrict the same elements.
                    with open(input_critiques, 'r', encoding='utf-8') as critiques:
                        critiques = csv.DictReader(critiques)
                        for critique in critiques:
                            if critique['controlling_option'] == option['name']:
                                if critique['wb_licence'] != option['wb_licence']:
                                    log.append('  MISMATCH DETECTED for licence check in Option "' + option['name'] + '" and its critique "' + critique['name'] + '".')
                                    print('  MISMATCH DETECTED for licence check in Option "' + option['name'] + '" and its critique "' + critique['name'] + '".')
                                if critique['wb_fgate'] != option['wb_fgate']:

                                    #EN OAC feature gates cause a non-fatal discrepancy between option and default value.
                                    gateCheck = option['wb_fgate']
                                    if gateCheck.startswith('EnglishOAC'):
                                        print('  NONFATAL OAC MISMATCH DETECTED in Feature Gate restriction in Option "' + option['name'] + '" and its Critique "' + critique['name'] + '".')
                                    else:
                                        log.append('  MISMATCH DETECTED in Feature Gate restriction in Option "' + option['name'] + '" and its Critique "' + critique['name'] + '".')
                                        print('  MISMATCH DETECTED in Feature Gate restriction in Option "' + option['name'] + '" and its Critique "' + critique['name'] + '".')
                                if critique['wb_app_OL'] != option['wb_app_OL']:
                                    log.append('  MISMATCH DETECTED for App-specific behaviour for Outlook in Option "' + option['name'] + '" and its Critique "' + critique['name'] + '".')
                                    print('  MISMATCH DETECTED for App-specific behaviour for Outlook in Option "' + option['name'] + '" and its Critique "' + critique['name'] + '".')
                                if critique['wb_app_PPT'] != option['wb_app_PPT']:
                                    log.append('  MISMATCH DETECTED for App-specific behaviour for PowerPoint in Option "' + option['name'] + '" and its Critique "' + critique['name'] + '".')
                                    print('  MISMATCH DETECTED for App-specific behaviour for PowerPoint in Option "' + option['name'] + '" and its Critique "' + critique['name'] + '".')
                                if int(critique['priority']) > 3:
                                    
                                    #EN has priority values higher than 3. This allows team to review aberrant cases.
                                    priorityResolution = True
                                    while priorityResolution:
                                        if (language_argument == False):
                                            x = input('Potential priority error detected for ' + critique['name'] + '. If you expected a value of ' + critique['priority'] + ', enter Y. Press any other key to log this error.')
                                            if x == "Y":
                                                priorityResolution=False
                                            else:
                                                log.append('  ERROR DETECTED for Priority value ("' + critique['priority'] + '") in Critique "' + critique['name'] +'" for Option "' + option['name'] + '".')
                                                log.append('   Priority Settings larger than "3" are invalid.')
                                                print('  ERROR DETECTED for Priority value ("' + critique['priority'] + '") in Critique "' + critique['name'] +'" for Option "' + option['name'] + '".')
                                                print('   Priority Settings larger than "3" are invalid.')
                                                priorityResolution=False
                                        else:
                                            if input_lang == "English":
                                                priorityResolution=False
                                            else:
                                                log.append('  ERROR DETECTED for Priority value ("' + critique['priority'] + '") in Critique "' + critique['name'] +'" for Option "' + option['name'] + '".')
                                                log.append('   Priority Settings larger than "3" are invalid.')
                                                print('  ERROR DETECTED for Priority value ("' + critique['priority'] + '") in Critique "' + critique['name'] +'" for Option "' + option['name'] + '".')
                                                print('   Priority Settings larger than "3" are invalid.')
                                                priorityResolution=False

                                elif critique['priority'] == '1' and not critique['name'].startswith("NRC"):
                                    log.append('  ERROR DETECTED for Priority value ("' + critique['priority'] + '") in Critique "' + critique['name'] +'" for Option "' + option['name'] + '".')
                                    log.append('   Only NRC Critiques are allowed to be set to Priority 1.')
                                    print('  ERROR DETECTED for Priority value ("' + critique['priority'] + '") in Critique "' + critique['name'] +'" for Option "' + option['name'] + '".')
                                    print('   Only NRC Critiques are allowed to be set to Priority 1.')
                                elif critique['name'].startswith("NRC") and critique['priority'] != '1':
                                    log.append('  ERROR DETECTED for Priority value ("' + critique['priority'] + '") in Critique "' + critique['name'] +'" for Option "' + option['name'] + '".')
                                    log.append('    NRC Critiques are required to be set to Priority 1.')
                                    print('  ERROR DETECTED for Priority value ("' + critique['priority'] + '") in Critique "' + critique['name'] +'" for Option "' + option['name'] + '".')
                                    print('    NRC Critiques are required to be set to Priority 1.')
                                elif critique['priority'] == '3' and title_count == 1:
                                    log.append('  MISMATCH DETECTED for Priority Setting in Critique "' + critique['name'] + '" in Option "' + option['name'] + '".')
                                    log.append('   Critique has Priority "' + critique['priority'] + '" (Style) but is governed by a Grammar option.')
                                    print('  MISMATCH DETECTED for Priority Setting in Critique "' + critique['name'] + '" in Option "' + option['name'] + '".')
                                    print('   Critique has Priority "' + critique['priority'] + '" (Style) but is governed by a Grammar option.')
                                elif (critique['priority'] == '1' or  critique['priority'] == '2') and title_count > 1:
                                    log.append('  MISMATCH DETECTED for Priority Setting in Critique "' + critique['name'] + '" in Option "' + option['name'] + '".')
                                    log.append('   Critique has Priority "' + critique['priority'] + '" (Grammar) but is governed by a Style option.')
                                    print('  MISMATCH DETECTED for Priority Setting in Critique "' + critique['name'] + '" in Option "' + option['name'] + '".')
                                    print('   Critique has Priority "' + critique['priority'] + '" (Grammar) but is governed by a Style option.')
                else:
                    log.append(' "' + option['name'] + '" is governing ' + str(crit_count) + ' Critiques.')
                    print(' "' + option['name'] + '" is governing ' + str(crit_count) + ' Critiques.')
                    if option['wb_licence'] == 'True':
                        with open(input_critiques, 'r', encoding='utf-8') as critiques:
                            critiques = csv.DictReader(critiques)
                            for critique in critiques:
                                if critique['controlling_option'] == option['name'] and critique['wb_licence'] != 'True':
                                    log.append('  MISMATCH DETECTED for licence check in Option "' + option['name'] + '" and its Critique "' + critique['name'] + '".')
                                    log.append('   Option is subscription only, yet Critique is not!')
                                    print('  MISMATCH DETECTED for licence check in Option "' + option['name'] + '" and its Critique "' + critique['name'] + '".')
                                    print('   Option is subscription only, yet Critique is not!')
                    if option['wb_app_OL'] == 'Off':
                        with open(input_critiques, 'r', encoding='utf-8') as critiques:
                            critiques = csv.DictReader(critiques)
                            for critique in critiques:
                                if critique['controlling_option'] == option['name'] and critique['wb_app_OL'] == 'On':
                                    log.append('  MISMATCH DETECTED for App-specific behaviour for Outlook in Option "' + option['name'] + '" and its Critique "' + critique['name'] + '".')
                                    log.append('   Option is restricted in Outlook, yet Critique is not!')
                                    print('  MISMATCH DETECTED for App-specific behaviour for Outlook in Option "' + option['name'] + '" and its Critique "' + critique['name'] + '".')
                                    print('   Option is restricted in Outlook, yet Critique is not!')
                    if option['wb_app_PPT'] == 'Off':
                        with open(input_critiques, 'r', encoding='utf-8') as critiques:
                            critiques = csv.DictReader(critiques)
                            for critique in critiques:
                                if critique['controlling_option'] == option['name'] and critique['wb_app_PPT'] == 'On':
                                    log.append('  MISMATCH DETECTED for App-specific behaviour for Outlook in Option "' + option['name'] + '" and its Critique "' + critique['name'] + '".')
                                    log.append('   Option is restricted in PowerPoint, yet Critique is not!')
                                    print('  MISMATCH DETECTED for App-specific behaviour for Outlook in Option "' + option['name'] + '" and its Critique "' + critique['name'] + '".')
                                    print('   Option is restricted in PowerPoint, yet Critique is not!')
                    if option['wb_fgate'] == 'None':
                        with open(input_critiques, 'r', encoding='utf-8') as critiques:
                            critiques = csv.DictReader(critiques)
                            errors = []
                            warning = True
                            for critique in critiques:
                                if critique['controlling_option'] == option['name']:
                                    if critique['wb_fgate'] == 'None':
                                        warning = False #No warning is issued if at least one critique has no Feature Gate.
                                    else:
                                        errors.append(str(critique['name']))
                            if warning == True:
                                log.append('  MISMATCH DETECTED for Feature Gates in Option "' + option['name'] + '" and its critique(s):')
                                print('  MISMATCH DETECTED for Feature Gates in Option "' + option['name'] + '" and its critique(s):')
                                for error in errors:
                                    log.append('   ' + str(error))
                    with open(input_critiques, 'r', encoding='utf-8') as critiques:
                        critiques = csv.DictReader(critiques)
                        for critique in critiques:
                            if critique['controlling_option'] == option['name']:
                                if int(critique['priority']) > 3:
                                    log.append('  ERROR DETECTED for Priority value ("' + critique['priority'] + '") in Critique "' + critique['name'] +'" for Option "' + option['name'] + '".')
                                    log.append('   Priority Settings larger than "3" are invalid.')
                                    print('  ERROR DETECTED for Priority value ("' + critique['priority'] + '") in Critique "' + critique['name'] +'" for Option "' + option['name'] + '".')
                                    print('   Priority Settings larger than "3" are invalid.')
                                elif critique['priority'] == '1' and not critique['name'].startswith("NRC"):
                                    log.append('  ERROR DETECTED for Priority value ("' + critique['priority'] + '") in Critique "' + critique['name'] +'" for Option "' + option['name'] + '".')
                                    log.append('   Only NRC Critiques are allowed to be set to Priority 1.')
                                    print('  ERROR DETECTED for Priority value ("' + critique['priority'] + '") in Critique "' + critique['name'] +'" for Option "' + option['name'] + '".')
                                    print('   Only NRC Critiques are allowed to be set to Priority 1.')
                                elif critique['name'].startswith("NRC") and critique['priority'] != '1':
                                    log.append('  ERROR DETECTED for Priority value ("' + critique['priority'] + '") in Critique "' + critique['name'] +'" for Option "' + option['name'] + '".')
                                    log.append('    NRC Critiques are required to be set to Priority 1.')
                                    print('  ERROR DETECTED for Priority value ("' + critique['priority'] + '") in Critique "' + critique['name'] +'" for Option "' + option['name'] + '".')
                                    print('    NRC Critiques are required to be set to Priority 1.')
                                elif critique['priority'] == '3' and title_count == 1:
                                    log.append('  MISMATCH DETECTED for Priority Setting in Critique "' + critique['name'] + '" in Option "' + option['name'] + '".')
                                    log.append('   Critique has Priority "' + critique['priority'] + '" (Style) but is governed by a Grammar option.')
                                    print('  MISMATCH DETECTED for Priority Setting in Critique "' + critique['name'] + '" in Option "' + option['name'] + '".')
                                    print('   Critique has Priority "' + critique['priority'] + '" (Style) but is governed by a Grammar option.')
                                elif (critique['priority'] == '1' or  critique['priority'] == '2') and title_count > 1:
                                    log.append('  MISMATCH DETECTED for Priority Setting in Critique "' + critique['name'] + '" in Option "' + option['name'] + '".')
                                    log.append('   Critique has Priority "' + critique['priority'] + '" (Grammar) but is governed by a Style option.')
                                    print('  MISMATCH DETECTED for Priority Setting in Critique "' + critique['name'] + '" in Option "' + option['name'] + '".')
                                    print('   Critique has Priority "' + critique['priority'] + '" (Grammar) but is governed by a Style option.') 

def error_check3(input_options):
    log.append('')
    log.append('ROUND 3')
    log.append('Checking for incongruities in Option Default Values.')
    log.append('')
    print('')
    print('ROUND 3')
    print('Checking for incongruities in Option Default Values.')
    print('')
    resume_title_index = -1
    with open(input_options, 'r', encoding='utf-8') as options:
        options = csv.DictReader(options)
        title_count = 0
        for option in options:
            if option['type'] == 'Title':
                title_count += 1
                if option['name'] == 'TitleResume':
                    resume_title_index = title_count
            if option['type'] == 'Binary':
                if option['default_value_2'] != "":
                    if option['default_value_1'] != option['default_value_2'] and title_count == 1:
                        log.append('  MISMATCH DETECTED for Default Values in Grammar Option "' + option['name'])
                        log.append('')
                        print('  MISMATCH DETECTED for Default Values in Grammar Option "' + option['name'])
                        print('')
                    if title_count == resume_title_index:
                        if option['default_value_1'] != "$IsResume_1_Else_0" or option['default_value_2'] != "$IsResume_1_Else_0":
                            log.append('  MISMATCH DETECTED for Default Values in (presumed) Resume Option "' + option['name'])
                            log.append('   Default value should be a function "$IsResume_1_Else_0" for both Writing Styles')
                            log.append('')
                            print('  MISMATCH DETECTED for Default Values in (presumed) Resume Option "' + option['name'])
                            print('   Default value should be a function "$IsResume_1_Else_0" for both Writing Styles')
                            print('')
                    else:
                        if option['default_value_2'] != "False" and title_count >1:
                            #Some style critiques in EN have a $IsResume_1_Else_0 value per NLX.
                            if option['default_value_2'] == "$IsResume_1_Else_0":
                                print('(STYLE)' + option['name'] + ' has an $IsResume... value for "Grammar".')
                            else:
                                log.append('  ERROR DETECTED for Default Value in "Grammar" Writing Style for Option "' + option['name'] + '".')
                                log.append('   Default value in "Grammar" must be "FALSE" for all Style options.')
                                log.append('')
                                print('  ERROR DETECTED for Default Value in "Grammar" Writing Style for Option "' + option['name'] + '".')
                                print('   Default value in "Grammar" must be "FALSE" for all Style options.')
                                print('')
                else:
                    continue

    ###############_RUNTIME_########################
total_error_count = 0
log.append(str(now))
log.append('')
feature_gate_list = get_fg_list(input_file)
pull_info(input_file)
error_check0(input_lang + "_Options.csv")
error_check1(input_lang + "_Options.csv")
error_check2(input_lang + "_Options.csv",input_lang + "_Critiques.csv")
error_check3(input_lang + "_Options.csv")
print('')
print('TESTING COMPLETED.')
print('')
with open(input_lang + '_log.txt', 'w', encoding='utf-8') as log_file:
    log_file.write('\ufeff')
    for line in log:
        log_file.write(line + "\n")
        if re.search(r"(MISMATCH|ERROR|ATTENTION)", line):
            total_error_count += 1
    if total_error_count == 0:
        log_file.write("No errors detected.\n")
        print("No errors detected.")
    else:
        log_file.write(str(total_error_count) + " errors found. Please review.\n")  
        print(str(total_error_count) + " errors found. Please review.")
while (language_argument == False):
    print('Log file created.')
    print('')
    x = input('Press any key to close.')
    if x != None:
        break


        
    
