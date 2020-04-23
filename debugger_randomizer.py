import sys, re
import numpy as np

def WordIndices(line, word):
    indexArr = []
    counter = 0
    for i in line:
        if i == word:
            indexArr.append(line.index(i))
            counter += 1
    return indexArr




def randomize_Word(filepath, word, replace):

    new_filepath = "randWordReplace_"+word+"_to_"+replace+".als" # name this something based on the number x
    # create a new file with only one fact
    new = open(new_filepath, 'w')
    # open the file and read through it line by line
    numWord = 0
    with open(filepath, 'r') as file_object:

        line = file_object.readline()
        while line:
            tempLine = line.split()
            if word in tempLine:
                numWord += 1
            line = file_object.readline()
        if numWord == 0:
            print("Given file does not contain: "+word)
            return

        randLine = np.random.randint(1, numWord+1)
        counter = 0
        replacedLine = ""

        file_object.seek(0)
        line = file_object.readline()
        while line:
            tempLine = line.split()
            if word in tempLine:
                counter += 1
                if counter != randLine:
                    new.write(line)
                    line = file_object.readline()
                    continue

                # There may be multiple instances of word in a given line

                indices = WordIndices(tempLine, word)
                randIndex = indices[np.random.randint(len(indices))]
                tempLine[randIndex] = replace
                replacedLine = ' '.join(tempLine)
                replacedLine += '\n'
                print(line+"\twas replaced with\t" + replacedLine)
                new.write(replacedLine)
                line = file_object.readline()
                continue

            # copy every line to new file
            new.write(line)
            line = file_object.readline()
    return

    #  and->or, all -> some, in -> =,

if __name__ == '__main__':
    if sys.argv[1] is None:
        print("Usage: /path/to/als/file")
        exit()
    if sys.argv[2] is None:
        print("Usage: TO_REPLACE")
        exit()
    if sys.argv[3] is None:
        print("Usage: REPLACEMENT")
        exit()



    # get filepath to open original uspec .als file
    filepath = sys.argv[1]
    randomize_Word(filepath, sys.argv[2], sys.argv[3])
