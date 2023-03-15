import os

#######################################################################
### WEBB - 2023 - LRC EN GRAMMAR PROJECT                            ###
### A helper function which returns the name of all files in a      ###
### folder as strings.                                              ###	
#######################################################################

def get_files_with_spaces():
    # Get the current working directory
    current_dir = os.getcwd()

    # Get a list of all the files in the current directory
    files = os.listdir(current_dir)

    # Create an empty list to store the filenames with spaces
    filenames_with_spaces = []

    # Loop through the files and add any filenames with spaces to the list
    for file in files:
        if " " in file:
            filenames_with_spaces.append(file)

    # Return the list of filenames with spaces
    return filenames_with_spaces

files = get_files_with_spaces()
print(files)
