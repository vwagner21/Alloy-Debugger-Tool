import sys, re
import numpy as np

def randomize_Word(filepath, word, replace):

    new_filepath = "/Users/viniciuswagner/Desktop/IW Spring 2020/Alloy Debugger Tool/Alloy-Debugger-Tool/output/randWordReplace" # name this something based on the number x
    # create a new file with only one fact
    new = open(new_filepath, 'w')
    # open the file and read through it line by line
    with open(filepath, 'r') as file_object:
        allWords = re.findall(word, file_object.read())
        n = len(allWords)

        randLine =
        counter = 0
        line = file_object.readline()
        while line:
            # print("Current line: "+line)
            if word in line:
                tempLine = line.split()
                indices = [i for i, s in enumerate(tempLine) if word in s]
                randIndex = indices[np.random.randint(len(indices))]
                tempLine[randIndex] = replace
                line = ' '.join(tempLine)
            # copy every line to new file
            new.write(line)
            line = file_object.readline()
    return ( , )

    #  and->or, all -> some, in -> =,
    #   

if __name__ == '__main__':
    if sys.argv[1] is None:
        print("Usage: /path/to/als/file")
        exit()
    # get filepath to open original uspec .als file
    filepath = sys.argv[1]

    randomizeStatus = randomize_Word(filepath, "or", "and")
