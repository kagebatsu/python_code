import os
import re
import xlsxwriter

"""
We use spec (XML) files to maintain documentation of the various pieces of the grammar project. 
However, they are too numerous to keep track of. 

This script goes through every spec (200) and finds comments that have been left open,
prints them to excel, and then allows the rest of the team to look through the excel doc
to determine which specs have comments that need their attention.
"""

def find_comments():
    # Create the Excel workbook and sheets
    workbook = xlsxwriter.Workbook('open comments.xlsx')
    qa_sheet = workbook.add_worksheet('DEV')
    dev_sheet = workbook.add_worksheet('QA')
    other_sheet = workbook.add_worksheet('Other')

    # Set up column headings
    qa_sheet.set_column('A:A', 50)
    qa_sheet.set_column('B:B', 100)
    dev_sheet.set_column('A:A', 50)
    dev_sheet.set_column('B:B', 100)
    other_sheet.set_column('A:A', 50)
    other_sheet.set_column('B:B', 100)

    # Set sheet tab colors
    qa_sheet.set_tab_color('red')
    dev_sheet.set_tab_color('blue')

    # Set up column headings
    qa_sheet.write('A1', 'Document')
    qa_sheet.write('B1', 'Comment')
    dev_sheet.write('A1', 'Document')
    dev_sheet.write('B1', 'Comment')
    other_sheet.write('A1', 'Document')
    other_sheet.write('B1', 'Comment')

    # Keep track of row numbers for each sheet
    qa_row = 2
    dev_row = 2
    other_row = 2

    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".xml"):
            with open(filename, "r", encoding="latin1") as f:
                xml_string = f.read()
                title_regex = r"<my:DocumentTitle>.*FS23\s(.*)<\/my:DocumentTitle>"
                title_match = re.search(title_regex, xml_string)
                if title_match:
                    title = title_match.group(1)
                comment_regex = r"<my:CommentTable_(\d+)>(.*?)<\/my:CommentTable_\d+>"
                comment_role_regex = r"<my:CommentRole_\d+>(.*?)<\/my:CommentRole_\d+>"
                comment_regex_numbered = r"<my:Comment_(\d+)>(.*?)<\/my:Comment_\d+>"
                action_regex_numbered = r"<my:Action_(\d+)>(Dev|QA)<\/my:Action_\d+>"
                for match in re.findall(comment_regex, xml_string, re.DOTALL):
                    comment_table_num = match[0]
                    comment_table_text = match[1]
                    comment_role_match = re.search(comment_role_regex, comment_table_text)
                    if comment_role_match:
                        comment_role = comment_role_match.group(1)
                        action_match = re.search(action_regex_numbered, comment_table_text)
                        if action_match and action_match.group(2) != "CLOSED":
                            comment_num = action_match.group(1)
                            comment_text_match = re.search(comment_regex_numbered, comment_table_text)
                            if comment_text_match:
                                comment_text = comment_text_match.group(2)
                                # Check if comment starts with "QA-" or "DEV-"
                                if comment_text.startswith('QA-'):
                                    qa_sheet.write(f'A{qa_row}', title)
                                    qa_sheet.write(f'B{qa_row}', comment_text)
                                    qa_row += 1
                                elif comment_text.startswith('DEV-'):
                                    dev_sheet.write(f'A{dev_row}', title)
                                    dev_sheet.write(f'B{dev_row}', comment_text)
                                    dev_row += 1
                                else:
                                    other_sheet.write(f'A{other_row}', title)
                                    other_sheet.write(f'B{other_row}', comment_text)
                                    other_row += 1

    workbook.close()

find_comments()
