# ------------------------------------------------------------------------------
# ***** ------------------------ START OF PROGRAM ------------------------ *****
# ------------------------------------------------------------------------------

# ------------------------ LIBRARIES ------------------------
from datetime import datetime
import os
import keyboard

# ------------------------ CONSTANTS ------------------------

rootDir = 'testFiles'
recBin = 'Recycling Bin'
notToDelete = [rootDir]

manageData = True
filesCounted = False

maxCTime = 10000
maxMTime = 1000
maxATime = 100
# ------------------------ VARIABLES ------------------------

totalFiles = 0
totalDir = 0
totalBytes = 0

# ------------------------ FUNCTIONS ------------------------
#         ----------- Data Management Functions -----------

def resetTotals():
    global totalDir
    global totalFiles
    global totalBytes

    totalFiles = 0
    totalDir = 0
    totalBytes = 0

def calculateSize(bytes):

    bSize = float(bytes)
    c = 0
    fileSizes = ["B", "KB", "MB", "GB", "TB"]

    while float(bSize / 1000.00) > 1 and c < len(fileSizes):
        c += 1
        bSize /= 1000.00

    finalSize = [bSize, fileSizes[c]]
    return finalSize

def moveFiles(dir, file, log):
    global notToDelete

    askToDel = True
    c = -1

    if os.path.getsize(os.path.join(dir, file)) == 0:
        for f in notToDelete:
            c += 1
            if os.path.join(dir, file) == f:
                askToDel = False
                break
    else:
        askToDel = False

    if askToDel:
        print(file + " in " + dir + " is unused. ")
        chr = 'w'
        while (chr[0].lower() != "y" and chr[0].lower() != "n"):
            chr = input("Would you like to delete this file (yes/no)? ")

        if chr[0].lower() == "y":
            log.write("{" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") +
                      "} \nFile " + file + " moved to recycling bin\n")
            print("File " + file + " moved to " + recBin + "\n")
            os.rename(os.path.join(dir, file), os.path.join(os.path.join(rootDir, recBin), file))
        elif chr[0].lower() == "n":
            askToDel = False
            notToDelete.append(str(os.path.join(dir, file)))
            log.write("{" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") +
                      "} \nFile " + file + " added to notToDelete\n")
            print("Added to notToDelete: " + os.path.join(dir, file))

    global totalBytes
    global totalDir

    if not askToDel:
        splitFName = os.path.splitext(file)
        splitDir = os.path.split(dir)
        dirFound = False

        if splitDir[0] == '':
            splitDir = splitDir[1:]

        while not dirFound and len(splitDir) > 1:
            for fN in os.listdir(dir):
                if os.path.isdir(os.path.join(dir, fN)) and ((fN in splitFName[0]) or ((splitFName[1])[1:] == fN)):
                    splitDir[len(splitDir) - 1] += os.path.join(splitDir[len(splitDir) - 1], fN)
                    dirFound = True
                    break

            if dirFound:
                dest = "\\".join(splitDir)

                if dest != dir:
                    log.write("{" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") +
                              "} \nFile " + file + " moved from " + dir + " to "
                              + dest + "\n")
                    print("Moved " + os.path.join(dir, file) + " to " + os.path.join(dest, file))
                    os.rename(os.path.join(dir, file), os.path.join(dest, file))
                    totalBytes += os.path.getsize(os.path.join(dest, file))
            elif not dirFound:
                if (splitDir[len(splitDir) - 1] not in splitFName[0]) or (
                        (splitFName[1])[1:] != splitDir[len(splitDir) - 1]):
                    splitDir = splitDir[:len(splitDir) - 2]
                else:
                    dirFound = True

        if not dirFound and (len(splitDir) == 1 and splitDir[0] == rootDir):
            if not os.path.isdir(os.path.join(rootDir, (splitFName[1])[1:])):
                os.mkdir(os.path.join(rootDir, (splitFName[1])[1:]))
                totalDir += 1

            if os.path.join(rootDir, (splitFName[1])[1:]) != dir:
                log.write("{" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") +
                          "} \nFile " + file + " moved from " + dir + " to "
                          + os.path.join(rootDir, (splitFName[1])[1:]) + "\n")
                print("Moved " + os.path.join(dir, file) + " to " + os.path.join(rootDir, (splitFName[1])[1:]))
                os.rename(os.path.join(dir, file), os.path.join(os.path.join(rootDir, (splitFName[1])[1:]), file))
                totalBytes += os.path.getsize(os.path.join(os.path.join(rootDir, (splitFName[1])[1:]), file))

        if c >= 0:
            notToDelete[c] = os.path.join(os.path.join(rootDir, (splitFName[1])[1:]), file)

def manageFiles(dir, log):
    global totalDir
    global totalFiles
    global totalBytes

    for files in os.listdir(dir):
        if (os.path.isdir(os.path.join(dir, files))):

            if not (dir == rootDir and files == recBin):
                if len(os.listdir(os.path.join(dir, files))) == 0:
                    log.write("{" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") +
                              "} \nDeleting directory " + os.path.join(dir, files) + "; empty directory\n")
                    os.rmdir(os.path.join(dir, files))
                    print(os.path.join(dir, files) + " directory deleted")
                else:
                    totalDir += 1
                    manageFiles(os.path.join(dir, files), log)
            else:
                totalDir += 1

        elif (os.path.isfile(os.path.join(dir, files))):
            if files != "log.txt":
                moveFiles(dir, files, log)
            totalFiles += 1


#         ----------------- Main Function -----------------
def main():
    global manageData
    global filesCounted

    print("* ------------------------------------------------------------------------------------- *")
    print("\t * Data Management Automation: Started")
    print("\t * Start time: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print("\n\t   Press Esc to stop program")

    logFile = open(os.path.join(rootDir, "log.txt"), "a")
    logFile.write("\n\n-----------------------------------------------------------------------------------------------")
    logFile.write("\nTask Automation Started at [[ " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "]]\n")

    if not os.path.isdir(os.path.join(rootDir, recBin)):
        os.mkdir(os.path.join(rootDir, recBin))

    while manageData:
        resetTotals()
        manageFiles(rootDir, logFile)

        if not filesCounted:
            logFile.write("[ " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " ] File Recount\n")
            print("Total files: " + str(totalFiles))
            logFile.write("Total files: " + str(totalFiles) + "\n")
            print("Total directories: " + str(totalDir))
            logFile.write("Total directories: " + str(totalDir) + "\n")
            totalSize = calculateSize(totalBytes)
            print("Total size of " + rootDir + ": " + str(totalSize[0]) + totalSize[1]+ "\n\n\n")
            logFile.write("Total size of " + rootDir + ": " + str(round(totalBytes, 3)) + " bytes; ("
                          + str(round(totalSize[0], 5)) + " " + totalSize[1] + ")\n")


            filesCounted = True

        if keyboard.is_pressed('Escape'):
            manageData = False

    logFile.write("Task Automation Ended at [[ " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "]]")
    logFile.write("-----------------------------------------------------------------------------------------------")

    print("\t * Data Management Automation: Ended")
    print("\t * End time: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print("* ------------------------------------------------------------------------------------- *")
    logFile.close()

main()

# ------------------------------------------------------------------------------
# ***** ------------------------- END OF PROGRAM ------------------------- *****
# ------------------------------------------------------------------------------