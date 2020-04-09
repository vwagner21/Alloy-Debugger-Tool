import sys, re
import time
import shlex, subprocess

def create_file(filepath, x):
    """
    Parse text at given filepath

    Parameters
    ----------
    filepath : str
        Filepath for file_object to be parsed
    x : int
        Number of axioms in file

    Returns
    -------
    new_filepath : str
        Name of created file

    """

    new_filepath = "factToPred_"+str(x)+".als" # name this something based on the number x

    # create a new file with only one fact
    new = open(new_filepath, 'w')

    # open the file and read through it line by line
    with open(filepath, 'r') as file_object:
        counter = 0
        line = file_object.readline()
        while line:
            # print("Current line: "+line)
            if "fact" in line:
                counter += 1
                currentLine = line.split()
                unnamedFact = True
                factInd = currentLine.index('fact')

                if currentLine[factInd+1] != '{':
                    unnamedFact = False
                # 
                # print(currentLine[factInd+1])
                # print(unnamedFact)

                # print(f"FOUND FACT NUMBER {counter}")
                if counter != x:
                    # Replace module
                    if unnamedFact:
                        replaceStr = "pred PRED" + str(counter)
                        new.write(line.replace("fact",replaceStr))
                    else:
                        new.write(line.replace("fact","pred"))
                    line = file_object.readline()
                    continue

            # copy every line to new file
            new.write(line)
            line = file_object.readline()
    return new_filepath

if __name__ == '__main__':
    if sys.argv[1] is None:
        print("Usage: /path/to/als/file")
        exit()
    # get filepath to open original uspec .als file
    filepath = sys.argv[1]
    test = "test_sb" # FiveStages test instance, just using as placeholder.
    # tests = {}
    # create output file to record results
    fout = open("out.txt", 'w') # TODO: this should be a path to an output file -- can be anything

    # open the file
    with open(filepath, 'r') as file_object:
        # count number of instances of "fact"
        allFacts = re.findall('fact', file_object.read())
        n = len(allFacts)

        # create a file for each instance
        for x in range(n+1):
            new_filepath = create_file(filepath, x)
             # run each file as it is created
            test_time_start = time.time()
            p = subprocess.Popen(["java", "-cp", "org.alloytools.alloy-5.1.0/org.alloytools.alloy.dist/target/org.alloytools.alloy.dist.jar", # TODO: this should be a path to Alloy
                                  "edu.mit.csail.sdg.alloy4whole.MainClass", "-n", "1",
                                  "-f", new_filepath, test], stdout=subprocess.PIPE) # TODO: probably will need to run this script from same folder as original .als so that it can locate checkmate.als
            out, _  = p.communicate()
            test_time_elapsed = time.time() - test_time_start

            # record results in output file
            fout.write(test + ": ")
            if "---INSTANCE---" in out:
              fout.write(test + ", Observable, ")

            else:
              fout.write(test + ", Unobservable, ")

            fout.write(str(test_time_elapsed) + " sec\n")

    fout.close()
