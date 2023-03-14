import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
import glob
## MIGRATE BVTS automates the process of selecting the correct BVTs
##for each BVT
##1. Choose the BVT you need specs for
##2. Choose the destination to copy specs to
##3. *UNSUPPORTED - Run the BVT script once migration is complete, toggle

DOGFOOD_ALL_SPECS = ['LS English FS23 A or An.xml', 
                     'LS English FS23 Academic Degrees.xml', 
                     'LS English FS23 Adjective Adverb Use.xml', 
                     'LS English FS23 Adjective Order.xml', 
                     'LS English FS23 Adverb instead of Adjective.xml', 
                     'LS English FS23 Adverb Placement.xml', 
                     'LS English FS23 An And Confusion.xml', 
                     'LS English FS23 Avoid First Person References.xml', 
                     'LS English FS23 Capitalization of March and May.xml', 
                     'LS English FS23 Capitalization of Personal Titles.xml', 
                     'LS English FS23 Capitalization.xml', 
                     'LS English FS23 Collective Nouns.xml', 
                     'LS English FS23 Collocations.xml', 
                     'LS English FS23 Colloquial Verb Phrase.xml', 
                     'LS English FS23 Colloquialisms.xml', 
                     'LS English FS23 Comma after Conjunction.xml', 
                     'LS English FS23 Comma After Greetings.xml', 
                     'LS English FS23 Comma Before Quotations.xml', 
                     'LS English FS23 Comma Splice.xml', 
                     'LS English FS23 Comma Use.xml', 
                     'LS English FS23 Comma with Adverbials.xml', 
                     'LS English FS23 Comma with Conjunction.xml', 
                    'LS English FS23 Comma with Conjunctive Adverbs.xml',
                    'LS English FS23 Commas around Descriptive Clause.xml', 
                    'LS English FS23 Commonly Confused Words.xml', 
                    'LS English FS23 Comparative Use.xml', 
                    'LS English FS23 Complex and Abstract Words.xml', 
                    'LS English FS23 Conjunction Overuse.xml', 
                    'LS English FS23 Controversial Place Names.xml', 
                    'LS English FS23 Correlative Conjunction Mismatch.xml', 
                    'LS English FS23 Date Formatting.xml', 
                    'LS English FS23 Double Gerund.xml', 
                    'LS English FS23 Double Negation.xml', 
                    'LS English FS23 Eggcorns.xml', 
                    'LS English FS23 ELL Commonly Confused Words.xml', 
                    'LS English FS23 Embarrassing Words.xml', 
                    'LS English FS23 Extra Word.xml', 
                    'LS English FS23 Extraneous Use of Will and Would.xml', 
                    'LS English FS23 Former Geopolitical Entity.xml', 
                    'LS English FS23 Gender Neutral Pronouns.xml', 
                    'LS English FS23 Geopolitical Bias.xml', 
                    'LS English FS23 Geopolitical Term Referent Confusion.xml', 
                    'LS English FS23 Hedges.xml', 
                    'LS English FS23 Hyphen Use.xml', 
                    'LS English FS23 Incomplete Correlative Conjunction Pair.xml', 
                    'LS English FS23 Incorrect Auxiliary.xml', 
                    'LS English FS23 Incorrect Comma.xml', 
                    'LS English FS23 Incorrect Determiner.xml', 
                    'LS English FS23 Incorrect Dispreferred Geopolitical Term.xml', 
                    'LS English FS23 Incorrect Inflection.xml', 
                    'LS English FS23 Incorrect Negation.xml', 
                    'LS English FS23 Incorrect Number Ending.xml', 
                    'LS English FS23 Incorrect Offensive Geopolitical Entity Name.xml', 
                    'LS English FS23 Incorrect Preposition.xml', 
                    'LS English FS23 Incorrect Pronoun Case.xml', 
                    'LS English FS23 Incorrect Reflexive Pronoun Use.xml', 
                    'LS English FS23 Incorrect Use of Bare Infinitive.xml', 
                    'LS English FS23 Incorrect Use of That.xml', 
                    'LS English FS23 Indirect Questions.xml', 
                    'LS English FS23 Introductory Phrase.xml', 
                    'LS English FS23 Jargon.xml', 
                    'LS English FS23 Language Dialect Confusion.xml', 
                    'LS English FS23 Language Name Confusion.xml', 
                    'LS English FS23 Missing Auxiliary in Question.xml', 
                    'LS English FS23 Missing Auxiliary.xml', 
                    'LS English FS23 Missing Comma between Adjectives.xml', 
                    'LS English FS23 Missing Comma.xml', 
                    'LS English FS23 Missing End Punctuation.xml', 
                    'LS English FS23 Missing Preposition.xml', 
                    'LS English FS23 Modal Confusion.xml', 
                    'LS English FS23 Multiple Modals.xml', 
                    'LS English FS23 Nominalizations.xml', 
                    'LS English FS23 Noun Number.xml', 
                    'LS English FS23 Number Agreement.xml', 
                    'LS English FS23 Number Formatting.xml', 
                    'LS English FS23 Number Words.xml', 
                    'LS English FS23 Obsolete Geopolitical Terms.xml', 
                    'LS English FS23 Opinion Markers.xml', 
                    'LS English FS23 Outdated Geopolitical Entity Names.xml', 
                    'LS English FS23 Oxford Comma.xml', 
                    'LS English FS23 Participle or Adjective Form.xml', 
                    'LS English FS23 Passive Voice Generic Expansion.xml', 
                    'LS English FS23 Passive Voice.xml', 
                    'LS English FS23 Possessive Use.xml', 
                    'LS English FS23 Preposition at End of Clause.xml', 
                    'LS English FS23 Profanity.xml', 
                    'LS English FS23 Progressive Use.xml', 
                    'LS English FS23 Racial Bias Colonization of America.xml', 
                    'LS English FS23 Redundant Colon.xml', 
                    'LS English FS23 Redundant Comma Before Complement Clause.xml', 
                    'LS English FS23 Redundant Comma Before Object.xml', 
                    'LS English FS23 Redundant Comma Following Subject.xml', 
                    'LS English FS23 Redundant Question Mark.xml', 
                    'LS English FS23 Repeated Auxiliary.xml', 
                    'LS English FS23 Restricted Geopolitical Entity Names.xml', 
                    'LS English FS23 Semicolon Use.xml', 
                    'LS English FS23 Sentence Structure.xml', 
                    'LS English FS23 Slang.xml', 
                    'LS English FS23 Split Infinitives.xml', 
                    'LS English FS23 Subject Verb Agreement.xml', 
                    'LS English FS23 Subjunctive Mood.xml', 
                    'LS English FS23 Superfluous Expressions.xml', 
                    'LS English FS23 Too Many Verbs.xml', 
                    'LS English FS23 Unnecessary Comma.xml', 
                    'LS English FS23 Unnecessary Determiner.xml', 
                    'LS English FS23 Unnecessary Hyphen.xml', 
                    'LS English FS23 Unsuitable Expressions.xml', 
                    'LS English FS23 Use of Cliches.xml', 
                    'LS English FS23 Use of Contractions.xml', 
                    'LS English FS23 Use of Euphemisms.xml', 
                    'LS English FS23 Use of Lack.xml', 
                    'LS English FS23 Vague Adjectives.xml', 
                    'LS English FS23 Vague or Superfluous Adverbs.xml', 
                    'LS English FS23 Vague Quantifiers.xml', 
                    'LS English FS23 Vague Verbs.xml', 
                    'LS English FS23 Verb Form.xml', 
                    'LS English FS23 Verb Use.xml', 
                    'LS English FS23 Weak Verb Adverb Combinations.xml', 
                    'LS English FS23 Weak Verbs.xml', 
                    'LS English FS23 Whether vs If.xml', 
                    'LS English FS23 Who Whom Confusion.xml', 
                    'LS English FS23 Word Order.xml', 
                    'LS English FS23 Word Split.xml', 
                    'LS English FS23 Wordiness and Redundancy.xml', 
                    'LS English FS23 Wrong Verb Tense.xml']

# Create the GUI window
window = tk.Tk()

# Set the window title
window.title("File Migration")

# Set the window size
window.geometry("600x300")

# Create a list of options for the dropdown
options = ["DOGFOOD_ALL", "DOGFOOD_DEFAULT", "PROD_DEFAULT", "PROD_ALL"]

# Create a label widget for the selected directory
dir_label = ttk.Label(window, text="No directory selected")
dir_label.pack(pady=10)

# Create the dropdown widget
dropdown = ttk.Combobox(window, values=options, width = "80")
dropdown.set("Choose a BVT to migrate those specs from the dir you're in to a destination you choose")
dropdown.pack(pady=10)

# Create a label widget for the destination directory
dest_label = ttk.Label(window, text="No destination selected")
dest_label.pack(pady=10)

# Create a button to select the destination directory
def select_dest_dir():
    dest_dir_path = filedialog.askdirectory()
    if dest_dir_path:
        dest_label.config(text=dest_dir_path)
        button.config(text="BEGIN MIGRATION", bg="green")
    else:
        button.config(text="Please select a destination directory", bg="red")

# Create a button widget to select the destination directory
dest_button = tk.Button(window, text="Select Destination Directory", command=select_dest_dir)
dest_button.pack(pady=2)

# Create a checkbox widget for running BVT after migration
run_bvt_var = tk.BooleanVar()
run_bvt_checkbox = tk.Checkbutton(window, text="Run BVT after migration", variable=run_bvt_var)
run_bvt_checkbox.pack(pady=10)

def get_spec_array(_s):
    if _s == 'DOGFOOD_ALL':
        return DOGFOOD_ALL_SPECS
    elif _s == 'DOGFOOD_DEFAULT':
        return DOGFOOD_DEFAULT_SPECS
    elif _s == "PROD DEFAULT":
        return PROD_DEFAULT_SPECS
    elif _s == "PROD ALL":
        return PROD_ALL_SPECS
    
# Create a button widget to begin the migration
def begin_migration():
    selection = dropdown.get()
    dest_dir_path = dest_label.cget("text")
    if not selection or not dest_dir_path:
        messagebox.showerror("Error", "Please select a BVT and a destination directory")
        return
    current_dir = os.getcwd()
    for file_name in get_spec_array(selection):
        for file_path in glob.glob(os.path.join(current_dir, file_name)):
            src_path = file_path
            dest_path = os.path.join(dest_dir_path, os.path.basename(file_path))
            shutil.copy(src_path, dest_path)
            print(f"Copied {file_path} to {dest_path}")
    messagebox.showinfo("Success", "Migration completed successfully")
    if run_bvt_var.get():
        # Run the additional script here
        print("Running BVT after migration")

# Create a button widget to begin the migration
button = tk.Button(window, text="Please select an option and a destination directory", command=begin_migration, bg="red")
button.pack(pady=10)

# Start the GUI event loop
window.mainloop()
