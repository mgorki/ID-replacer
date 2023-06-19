import os
from pathlib import Path
#import fnmatch
import shutil
#import glob
import pandas as pd
import openpyxl
import prolificGUI as GUI 


class TableFile:
  def __init__(self, path, fileFormat, df):
    self.path = path  # For storing the files path
    self.fileFormat = fileFormat  # For storing a string indicating the files format (currently supported: xlsx, json, csv (, txt))
    self.df = df  # For storing pandas dataframes
    #self.filenameOut = filenameOut


def listFilesInFolder(folderPath: str, patterns: list) -> list:  # Returns a list of all json, txt, csv, xlsx files in a folder and (recursively) all its subfolders
    #patterns = [".json", ".csv", ".xlsx", ".txt"]
    filepaths = []
    for pattern in patterns:
        folder = Path(folderPath) 
        for filename in map(str, list(folder.rglob("*"))): 
            if filename.endswith(pattern):
                filepaths.append(filename)

    return filepaths                


### Goes over all table files provided (currently supported formats: xlsx, csv, json (, txt)) and:
# 1. Collects all unique IDs that are contained in all files in columns of the names contained in idColNames
# 2. Creates a unique new substitute ID for each original ID
# 3. Returns: 
#   (3a) a list of TableFile objects (see above; one for each table file)
#   (3b) a tuple of the original IDs
#   (3c) a tuble of the new IDs
def cleanTables(filesIn, idColNames, filenamePrefix, saveFolder, inPlace=False):
    tables = []
    mappingDF = pd.DataFrame(columns=["originalId"])
    originalIds = []

    for fIn in filesIn:
        if inPlace == True:  # If the user has chosen to save the results in the files original directory
            saveFolder = os.path.dirname(fIn)
        else:
            pass

        if os.path.isfile(os.path.join(saveFolder, str(filenamePrefix + os.path.basename(fIn)))) == True:
            overwrite = GUI.overWriteConfirmation(str(filenamePrefix + os.path.basename(fIn)))
            if overwrite == True:
                fOut = os.path.join(saveFolder, str(filenamePrefix + os.path.basename(fIn)))
        else:
            fOut = os.path.join(saveFolder, str(filenamePrefix + os.path.basename(fIn)))

        if Path(fIn).is_file() and Path(fIn).suffix == ('.txt' or '.csv' or '.json'):
            try:
                table = TableFile(fIn, "json", pd.read_json(fIn))
                print(str(table.path), " was read as a ", table.fileFormat, " file")
            except ValueError:
                try:
                    table = TableFile(fIn, "json", pd.read_json(fIn, lines=True))
                    print(str(table.path), " was read as a ", table.fileFormat, " file")
                except ValueError:
                    try:
                        table = TableFile(fIn, "csv", pd.read_csv(fIn))
                        print(str(table.path), " was read as a ", table.fileFormat, " file")
                    except:
                        print("There was an error loading " + str(fIn) + ". Crashing now :-(")
            except:
                print("There was an error loading " + str(fIn)+ ". Crashing now :-(")
        elif Path(fIn).is_file() and Path(fIn).suffix == '.xlsx':
            try:
                df0 = pd.read_excel(fIn)
                table = TableFile(fIn, "xlsx", df0)
                print(str(table.path), " was read as a ", table.fileFormat, " file")
            except:
                print("There was an error loading ", str(fIn), ". Crashing now :-(")
        else:
            print(str(fIn), " has an unknown file format. Crashing now :-(")

        for idColName in idColNames:
            try:
                originalIds.extend(table.df[idColName].values)  # column with the original ID 
                #print(originalIds)
            except:
                pass               
        try:
            table.filenameOut = fOut
            #print(table.filenameOut)
            tables.append(table)
        except:
            print("There was some error reading " , str(fIn))

    try:
        originalIds = [i for i in originalIds if i != ""]
    except:
        print("No empty IDs found")
    mappingDF["originalId"] = originalIds
    #print("mapping before dropping duplicates", mappingDF)
    mappingDF = mappingDF.drop(mappingDF[mappingDF.originalId.isnull()].index)  # Dropping rows where the original ID is an empty cell
    mappingDF = mappingDF.drop(mappingDF[mappingDF.originalId == ""].index)  # Dropping rows where the original ID is just an empty string 
    mappingDF = mappingDF.drop_duplicates(subset=['originalId']).reset_index(drop=True)#.dropna(inplace = True)  # Getting rid of duplicates and resetting index
    #print(mappingDF)
    #print(mappingDF["originalId"].index.values)
    mappingDF["newId"] = mappingDF["originalId"].index.values.astype(int) + 1  # "new" IDs created from the index of the old IDs //  mappingDF["originalId"].index.values + 1
    #print(mappingDF["newId"])
    #print(mappingDF["originalId"])
    originalIdsUnique = tuple(mappingDF["originalId"])
    newIds = tuple(mappingDF["newId"])

    return tables, originalIdsUnique, newIds, mappingDF


### Writes files (in the same format as the original files) for the tables where the original ID is replaced by the new id. ###
def writeTables(tables, originalIds, newIds):  
    for element in tables: 
        print(element) 
        if element.fileFormat == ("json" or "csv"):
            fin = open(element.path, "rt")
            fout = open(element.filenameOut, "wt")
            for line in fin:
                for check, rep in zip(originalIds, newIds):
                    line = line.replace(str(check), str(rep))
                fout.write(line)    
            fin.close()
            fout.close()

        elif element.fileFormat == "xlsx":
            # load excel with its path
            wb = openpyxl.load_workbook(element.path)  
            sh = wb.active
            # iterate through excel and display data
            for row in sh.iter_rows():
                for cell in row:
                    if not cell.value == None:
                        for check, rep in zip(originalIds, newIds):
                            cell.value = str(cell.value).replace(str(check), str(rep))
            wb.save(element.filenameOut)


### Save copies of files with a new filename, where IDs in the filename are substituted. 
# The IDs and their substitutes must be provided by the arguments originalIds, newIDs
# Files of the same name in the location defined by the saveFolder argument will NOT be overwritten (a message is shown in the console)
def cleanFilenames(filesIn, saveFolder, originalIds, newIDs, inPlace=False):
    counter = 0
    for file in filesIn:
        if Path(file).is_file():
            name = str(os.path.basename(file))
            print(name)
            for check, rep in zip(originalIds, newIds):
                name = name.replace(str(check), str(rep))

            if inPlace:  # If user has chosen to save new files in the same directory as the original files
                saveFolder = os.path.dirname(file)  # Set the saveFolder to the folder of the original file
            else:
                pass
            newfile = os.path.join(saveFolder, name)
            print(newfile)
            if not os.path.isfile(newfile):
                shutil.copyfile(file, newfile)
                counter += 1
            else:
                print(newfile, " ALREADY EXISTS! Skipping.")
        else:
            print(file, " is not a valid file")
    print(str(counter), " files have been saved with the new ID in their filename")


### User chooses (GUI) whether he/she wants to go over a whole folder (including subfolders) and all its redable content or select specific files
if GUI.folderMode() == True:  
    files = listFilesInFolder(folderPath=GUI.ChooseLoadingFolder(), patterns=[".json", ".csv", ".xlsx", ".txt"])
else:
    files = GUI.ChooseFiles()


### User chooses (GUI) whether he/she wants so save table files (don't safe them if you just want to edit e.g., the file-names of images)
# If he/she wants to safe them: chooses (GUI) a folder for saving new files and a prefix for the new files' names
safeTables = GUI.safeTables()
if safeTables == True:
    inPlace = GUI.safeInPlace()
    if inPlace == False:
        saveDirTables = GUI.ChooseSavingFolder()
    else: 
        saveDirTables = "placeholder"
else:
    saveDirTables = "placeholder"
identifierColNames = GUI.ChooseIdentifierColumn()
prefix=GUI.ChooseFilePrefix()

tables, uniqueOriginalIds, newIds, mappingDF = cleanTables(filesIn=files, idColNames=identifierColNames, filenamePrefix=prefix, saveFolder=saveDirTables, inPlace=inPlace)
if safeTables:
    writeTables(tables=tables, originalIds=uniqueOriginalIds, newIds=newIds) # TableFiles are written
else:
    pass

### User chooses whether the mapping of original and new IDs be saved in a file (csv), and if so, he/she cooses a folder and a filename 
if GUI.saveMapping() == True:
    while True:
        while True:  # Checking if chosen folder is valid (if not user has to choose again)
            saveMappingDir = GUI.ChooseSavingFolder()
            if os.path.isdir(saveMappingDir):
                break
            else:
                GUI.InvalidFolder()
                pass
        saveMappingFilename = GUI.ChooseFileName()
        saveMappingPath = os.path.join(saveMappingDir, (saveMappingFilename + ".csv"))

        if os.path.isfile(saveMappingPath):  # If file already exists
            overwrite = GUI.overWriteConfirmation(str(saveMappingPath))  # Dialog if ixisting file should be overwritten
            if overwrite == True:
                mappingDF.to_csv(saveMappingPath, index=False)
                break
            else:
                pass
        else:
            mappingDF.to_csv(saveMappingPath, index=False)
            break
else:
    del mappingDF


### User chooses (GUI) whether he/she wants to substitute IDs in filenames (the IDs must have been identified in the tables read in before) ###
# If this is the case, the respective files and a folder for saving the copies with new filenames must be chosen (GUI)
fileNameEdit = False
fileNameEdit = GUI.editingFilenames()
if fileNameEdit == True:
    try:
        inPlace = GUI.safeInPlace()
        if inPlace == False:
            saveDirFiles = GUI.ChooseSavingFolder()
        else: 
            saveDirFiles = "placeholder"
        cleanFilenames(filesIn=GUI.ChooseFiles(), saveFolder=saveDirFiles, originalIds=uniqueOriginalIds, newIDs=newIds, inPlace=inPlace)
    except:
        print("An error occured while trying to change filenames :-(")
else:
    pass


### Present message, that programm has finished ###
GUI.End(saveDirTables)
