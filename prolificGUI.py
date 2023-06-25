import PySimpleGUI as sg


## Messages ##
msgWelcome = """Welcome to the ID-replacer, version {}!

Please mind that - although we have tested this program to some degree - this program is still in development and you should always check that the results obtained are valid. 

By clicking on continue you agree that any use of or reliance on this program, the contents created by this program or the information provided through this program will be at your sole risk. 
We make no representations or warranties whatsoever as to the accuracy of the information or results provided by this program."""

msgLoadingFolderTables = """Select Folders from which IDs should be removed.
-> in a first step all json (txt), csv (txt) and xlsx files will be considered. Changing filenames of e.g., images follows in a second step"""

msgLoadingFolderFilenames = """Select Folders that contains files with filenames from which IDs should be removed."""

msgLoadingWindow = "Loading input file"
#msgLoadingFolder = "Choose the folder where the file from the CAM-App is stored"
msgSavingFolder = "Choose a folder for saving the output"

msgSavingWindow = "Defining output file"
msgLoadingFilename = "Specify the name of the file (without the ending .txt)"
msgSavingFilename = "Choose a filename (files of the same name will be overwritten). The ending .txt will be created automatically"

msgLoadingModel = "Choose the folder where your language model file is stored"


def welcome(progVer):
    layout = [[sg.Text(msgWelcome.format(str(progVer)))], [sg.Button("Continue"), sg.Button("Abort")]] #Tables saved to %s"%(str(savepathTables))))], [sg.Button("OK")]]

    # Create the window
    window = sg.Window("Welcome", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "Continue" or event == sg.WIN_CLOSED or event == "Abort":
            break

    window.close()
    return event


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


def InvalidFolder():
    layout = [[sg.Text("The folder you specified does not exist/is not valid!")], [sg.Button("OK")]]

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


def safeInPlace():
    layout = [[sg.Text(("Do you want to save the new files in the same folders als the original ones or in another place?"))], [sg.Button("In the same folders"), sg.Button("In another place")],] #Tables saved to %s"%(str(savepathTables))))], [sg.Button("OK")]]
    # Create the window
    window = sg.Window("Where to save the results?", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if (event == "In the same folders") or (event == "In another place") or (event == sg.WIN_CLOSED):
            break
    window.close()
    if event == "In the same folders":
        return True
    else:
        return False


def folderMode():
    layout = [[sg.Text(("Do you want to apply ID substitution on an entire folder (including subfolders and all files contained) or do you want so select specific files?"))], [sg.Button("Apply on an entire folder"), sg.Button("Select specific files")],] 
    # Create the window
    window = sg.Window("Apply on whole folder?", layout)
    

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if (event == "Apply on an entire folder") or (event == "Select specific files") or (event == sg.WIN_CLOSED):
            break
    window.close()
    if event == "Apply on an entire folder":
        print("you chose to apply on an entire folder")
        return True
    else:
        print("you chose to select specific files")
        return False


def overWriteConfirmation(filename):
    ch = sg.popup_ok_cancel(str("Press Ok to proceed OVERWRITING " + filename), "Press cancel to skip",  title="OverwriteSkip")
    if ch=="Overwrite":
        print ("You pressed OK")
        return True
    if ch=="Skip":
        print ("You pressed Cancel")
        return False


def ChooseFiles(fileTypes=None):
    fileTypes = ("Any type", "*") if fileTypes == None else tuple([("Any type", "*"), *fileTypes])
    files = sg.popup_get_file('Select files from which IDs should be removed', multiple_files=True, file_types=(fileTypes), title="Select files")
    print(files.split(';'))
    if files == "" or None:
        MissingPath()
        ChooseFiles()
    else:
        return files.split(';')
    

def ChooseMappingFile():
    file = sg.popup_get_file('Select already existing mapping file (csv)', multiple_files=False, title="Select mapping files")
    print(file.split(';'))
    if file == "" or None:
        MissingPath()
        ChooseMappingFile()
    else:
        return file


def ChooseLoadingFolder(tablesOnly: bool = True):
    msg = msgLoadingFolderTables if tablesOnly else msgLoadingFolderFilenames
    folder = sg.popup_get_folder(msg, title="Loading all from folder")
    if folder == "" or None:
        MissingPath()
        ChooseLoadingFolder()
    else:
        print(folder)
        return folder


def loadMappingFile():
    layout = [[sg.Text(("""Do you want to load an existing mapping of new IDs to original IDs from a csv file previously created by this program?
        -> column names must be originalId and newId"""))], 
        [sg.Button("Yes, load existing mapping"), sg.Button("No, create new mapping")],] #Tables saved to %s"%(str(savepathTables))))], [sg.Button("OK")]]
    
    window = sg.Window("Load existing mapping?", layout) # Create the window

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if (event == "Yes, load existing mapping") or (event == "No, create new mapping") or (event == sg.WIN_CLOSED):
            break
    window.close()
    if event == "Yes, load existing mapping":
        return True
    else:
        return False


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
    -> The IDs identified in this step can in the following steps be substituted in other places too
       but ONLY IDs that can be identified in the specified columns now can be substituted later.''', title="Enter column-names")
    if identInp == "" or None:
        MissingInput()
        ChooseIdentifierColumn()
    else:
        identList = identInp.split(',')
        print(identList)
        return identList
    

def ChooseFilePrefix():
    prefix = sg.popup_get_text('''Please, choose a prefix for the filenames of the output files
    -> This is to your own safety, so that you do not confuse or overwrite the original files and the files where IDs have been substituted.''', title="Enter file-prefix")
    if prefix == "" or None:
        MissingInput()
        ChooseFilePrefix()
    else:
        print(prefix)
        return prefix


def saveMapping():
    layout = [[sg.Text(("""Do you want to save the mapping of new IDs to original IDs in a (csv) file?
        -> Keep in mind that this is sensitive data as it allows to trace back the new IDs to the original ones!"""))], 
        [sg.Button("Yes"), sg.Button("No")],] #Tables saved to %s"%(str(savepathTables))))], [sg.Button("OK")]]
    
    window = sg.Window("Save mapping of IDs into a file?", layout) # Create the window

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if (event == "Yes") or (event == "No") or (event == sg.WIN_CLOSED):
            break
    window.close()
    if event == "Yes":
        return True
    else:
        return False


def ChooseFileName():
    fileName = sg.popup_get_text('''Please, choose a name of the output file (without any ending like e.g., .csv)''', title="Enter filename")
    if fileName == "" or None:
        MissingInput()
        ChooseFileName()
    else:
        print(fileName)
        return fileName


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
#print(safeInPlace())
#print(saveMapping())