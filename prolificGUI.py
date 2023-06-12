import PySimpleGUI as sg
#import os.path

## Messages ##
msgLoadingWindow = "Loading input file"
msgLoadingFolder = "Choose the folder where the file from the CAM-App is stored"
msgSavingFolder = "Choose a folder for saving the output"

msgSavingWindow = "Defining output file"
msgLoadingFilename = "Specify the name of the file (without the ending .txt)"
msgSavingFilename = "Choose a filename (files of the same name will be overwritten). The ending .txt will be created automatically"

msgLoadingModel = "Choose the folder where your language model file is stored"


def MissingPath():
    layout = [[sg.Text("Path (and/or filename) not propperly chosen")], [sg.Button("OK")]]

    # Create the window
    window = sg.Window("Error", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "OK" or event == sg.WIN_CLOSED:
            break

    window.close()

def MissingInput():
    layout = [[sg.Text("You entered no input!")], [sg.Button("OK")]]

    # Create the window
    window = sg.Window("Error", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "OK" or event == sg.WIN_CLOSED:
            break

    window.close()


def End(savepathTables):
    layout = [[sg.Text(("Operation completed."))], [sg.Button("OK")]] #Tables saved to %s"%(str(savepathTables))))], [sg.Button("OK")]]

    # Create the window
    window = sg.Window("Finished", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "OK" or event == sg.WIN_CLOSED:
            break

    window.close()


def folderMode():
    ch = sg.popup_ok_cancel("Do you want to apply ID substitution on a whole folder (including subfolders and all files contained)? ", 
    "Press OK to continue editing whole folders", 
    "Press Cancel to edit specific files but not whole folders",  title="Apply on whole folder?")
    if ch=="OK":
        print ("You pressed OK")
        return True
    if ch=="Cancel":
        print ("You pressed Cancel")
        return False

def overWriteConfirmation(filename):
    ch = sg.popup_ok_cancel(str("Press Ok to proceed OVERWRITING " + filename), "Press cancel to skip",  title="OverwriteSkip")
    if ch=="Overwrite":
        print ("You pressed OK")
        return True
    if ch=="Skip":
        print ("You pressed Cancel")
        return False


def ChooseFiles():
    files = sg.popup_get_file('Select files from which IDs should be removed', multiple_files=True, title="Select files")
    print(files.split(';'))
    if files == "" or None:
        MissingPath()
        ChooseFiles()
    else:
        return files.split(';')


def ChooseLoadingFolder():
    folder = sg.popup_get_folder('''Select Folders from which IDs should be removed.
    -> in a first step all json (txt), csv (txt) and xlsx files will be considered. Images follow in a second step''', title="Loading all from folder")
    if folder == "" or None:
        MissingPath()
        ChooseLoadingFolder()
    else:
        print(folder)
        return folder


def saveInPlace():
    ch = sg.popup_ok_cancel("Do you want to save edited files in the same folder as the original (they will have another filename)? ", "Press OK to continue editing filenames", "Press Cancel to skip",  title="Edit filenames?")
    if ch=="OK":
        print ("You pressed OK")
        return True
    if ch=="Cancel":
        print ("You pressed Cancel")
        return False


def safeTables():
    ch = sg.popup_ok_cancel("Do you want to safe the cleaned tables? ", "Press OK to continue saving files", "Press Cancel to skip",  title="Edit filenames?")
    if ch=="OK":
        print ("You pressed OK")
        return True
    if ch=="Cancel":
        print ("You pressed Cancel")
        return False


def ChooseSavingFolder():
    folder = sg.popup_get_folder('''Select Folder where results should be saved.
    -> Please mind that only folders (not the files they may contain) are shown on this screen, so make sure you do not overwrite existing files''', title="Saving to folder")
    if folder == "" or None:
        MissingPath()
        ChooseSavingFolder()
    else:
        print(folder)
        return folder

def ChooseIdentifierColumn():
    identInp = sg.popup_get_text('''Please, enter the EXACT names of the columns from which IDs can be identified, separated by a KOMMA.  
    -> Do NOT use blank spaces after the komma (unless they are part of the column name). 
    -> Mind CAPITALIZATION. 
    -> ONLY IDs that are also contained in the specified columns can be substituted, even though they will be substituted if they appear at another part of the table/json files''', title="Enter column-names")
    if identInp == "" or None:
        MissingInput()
        ChooseIdentifierColumn()
    else:
        identList = identInp.split(',')
        print(identList)
        return identList
    

def ChooseFilePrefix():
    prefix = sg.popup_get_text('''Please, choose a prefix for the filenames of the output files
    -> This is to your own safety, so that you do not confuse or overwrite the original files and the files where IDs have been substituted.''', title="Enter column-names")
    if prefix == "" or None:
        MissingInput()
        ChooseFilePrefix()
    else:
        print(prefix)
        return prefix
    

def editingFilenames():
    ch = sg.popup_ok_cancel("Do you want to edit filenames too? ", "Press OK to continue editing filenames", "Press Cancel to skip",  title="Edit filenames?")
    if ch=="OK":
        print ("You pressed OK")
        return True
    if ch=="Cancel":
        print ("You pressed Cancel")
        return False
  

def chooseEditFiles():
    files = sg.popup_get_file('Select Files of which the name changed acording to the changes performed to the tables', multiple_files=True, title="Select files for name edit")
    print(files.split(';'))
    if files == "" or None:
        MissingPath()
        chooseEditFiles()
    else:
        return files.split(';')

#editingFilenames()
#ChooseFiles()
#ChooseSavingFolder()
#ChooseIdentifierColumn()
#ChooseFilePrefix()
#overWriteConfirmation("filename_XYZ")
