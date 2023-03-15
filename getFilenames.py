import os
import tkinter as tk
from tkinter import filedialog
import nltk
import codecs

#######################################################################
### WEBB - 2023 - LRC EN GRAMMAR PROJECT                            ###
### This cript allows a user to select a folder containing text     ###
### files. It then goes through each file in the folder, and for    ###
### each file it tokenizes the text into sentences and then into    ###
### words. The script then uses the Natural Language Toolkit (nltk) ###
### to tag each word with its corresponding part-of-speech (POS).   ###
### The output is printed to the console as well as saved to a file ###
### in the selected folder like (('Token', ('tag'))                 ###
### 1. Select a folder where your sentences are                     ###
### 2. Check output						    ###	
#######################################################################



##webb: This is a Python script that allows a user to select a folder containing text files. It then goes through each file in the folder, and for each file it
##tokenizes the text into sentences and then into words. The script then uses the Natural Language Toolkit (nltk) to tag each word with its corresponding part-of-speech (POS) tag. The output is printed to the console as well as saved to a file in the selected folder.
#<!----------------!>

#WARNING: Double clicking seems to not work,
# so open the file in IDLE and run the module that way.

#the script wasn't working at first without everything below; i dont know if it needs to be ran for each individual person or just once per vm
# set up the nltk tagger
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
tagger = nltk.pos_tag

def get_encoding(file_path):
    """Returns the encoding of a text file"""
    with open(file_path, 'rb') as f:
        raw = f.read(4)
        if raw.startswith(codecs.BOM_UTF8):
            return 'utf-8-sig'
        elif raw.startswith(codecs.BOM_UTF16_LE):
            return 'utf-16-le'
        elif raw.startswith(codecs.BOM_UTF16_BE):
            return 'utf-16-be'
        else:
            return 'utf-8'

def process_files():
    """Processes all text files in a selected folder and outputs POS tags"""
    # get the folder to process
    folder_path = filedialog.askdirectory(title="Select Folder")
    if not folder_path:
        return
    
    # iterate over all files in the folder
    for filename in os.listdir(folder_path):
        # only process text files
        if not filename.endswith('.txt'):
            continue
        
        # get the full file path
        file_path = os.path.join(folder_path, filename)
        
        # get the file encoding
        encoding = get_encoding(file_path)
        
        # read the file contents
        with open(file_path, encoding=encoding) as f:
            text = f.read()
        
        # tokenize the text and get POS tags
        sentences = nltk.sent_tokenize(text)
        pos_tags_sentences = []
        for sentence in sentences:
            tokens = nltk.word_tokenize(sentence)
            pos_tags = tagger(tokens)
            pos_tags_sentences.append(pos_tags)
        
        # output the results
        print(f"Results for {filename}:")
        for sentence, pos_tags in zip(sentences, pos_tags_sentences):
            print(f"Sentence: {sentence}")
            print(f"POS tags: {pos_tags}\n")
            
            # write to file
            output_file_path = os.path.join(folder_path, f"{filename}_output.txt")
            with open(output_file_path, 'a', encoding='utf-8') as f:
                f.write(sentence + '\n')
                f.write(str(pos_tags) + '\n')
                
# create the GUI window
window = tk.Tk()
window.title("POS Tagger")
window.geometry("400x150")

# create the select folder button
select_button = tk.Button(window, text="Select Folder", command=process_files)
select_button.pack(pady=20)

# start the GUI event loop
window.mainloop()
