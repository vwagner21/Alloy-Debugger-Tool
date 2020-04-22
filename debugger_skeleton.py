import sys, re
import time
import shlex, subprocess
import argparse

def create_graph(alloyOut, filename):
    # Create graph for current file
    filename = "graph_"+filename
    filename_GraphOut = filename+"_GRAPH"
    fgraph = open(filename, 'w')
    fgraph.write(alloyOut)
    p = subprocess.Popen(["python", "checkmate/util/release-generate-graphs.py",
                          "-i", filename, "-c",
                          "checkmate_simple","-o", filename_GraphOut], stdout=subprocess.PIPE)


def create_image():

    p = subprocess.Popen(["python", "checkmate/util/release-generate-images.py",
                          "-i", "graphs/", "-o",
                          "imgs/"], stdout=subprocess.PIPE)


def create_file_flip(filepath, x):
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
            if "fact" in line:
                counter += 1
                currentLine = line.split()
                unnamedFact = True
                factInd = currentLine.index('fact')

                if currentLine[factInd+1] != '{':
                    unnamedFact = False

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


def create_file_pair(filepath, x, y):

    new_filepath = "factPairs_"+str(x)+str(y)+".als" # name this something based on the number x

    # create a new file with a pair of facts
    new = open(new_filepath, 'w')

    # open the file and read through it line by line
    with open(filepath, 'r') as file_object:
        counter = 0
        line = file_object.readline()
        while line:
            if "fact" in line:
                counter += 1
                print(x)
                print(y)
                print(counter)
                currentLine = line.split()
                unnamedFact = True
                factInd = currentLine.index('fact')

                if currentLine[factInd+1] != '{':
                    unnamedFact = False

                if counter != x or counter != y:
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
    parser = argparse.ArgumentParser(description='Alloy Debugging Program')

    parser.add_argument('-i',
                        metavar='InFile',
                        type=str,
                        help='The input alloy file',
                        required=True)

    parser.add_argument('-t',
                        metavar='testAlloy',
                        type=str,
                        help='The alloy test instance name',
                        required=True)

    parser.add_argument('-o',
                        metavar='OutFile',
                        type=str,
                        help='Where to output the file',
                        required=True)

    parser.add_argument('-g', action='store_true', help='Enable graph output')
    parser.add_argument('-p', action='store_true', help='Enable fact pairing')


    args = parser.parse_args()

    banner = "################################\n"
    banner+= "#           BEGINNING          #\n"
    banner+= "#        DEBUGGER Program      #\n"
    banner+= "################################\n"
    print(banner)

    if args.t == None or args.o == None or args.i == None:
        print("Missing args")

    # get filepath to open original uspec .als file
    filepath = args.i
    test = args.t
    fout = open(args.o, 'w') # this should be a path to an output file -- can be anything

    # open the file
    with open(filepath, 'r') as file_object:
        # count number of instances of "fact"
        allFacts = re.findall('fact', file_object.read())
        n = len(allFacts)

        if args.p:
            for x in range(n+1):
                y = x+1
                for y in range(n+1):
                    new_filepath = create_file_pair(filepath, x, y)
                    test_time_start = time.time()
                    p = subprocess.Popen(["java", "-cp", "org.alloytools.alloy-5.1.0/org.alloytools.alloy.dist/target/org.alloytools.alloy.dist.jar", # TODO: this should be a path to Alloy
                                          "edu.mit.csail.sdg.alloy4whole.MainClass", "-n", "1",
                                          "-f", new_filepath, test], stdout=subprocess.PIPE) # TODO: probably will need to run this script from same folder as original .als so that it can locate checkmate.als
                    out, _  = p.communicate()

                    if args.g:
                        filename = str(x)+str(y)
                        create_graph(out, filename)

                    test_time_elapsed = time.time() - test_time_start

                    # record results in output file
                    fout.write(test + ": ")
                    if "---INSTANCE---" in out:
                      fout.write(test + ", Observable, ")

                    else:
                      fout.write(test + ", Unobservable, ")

                    fout.write(str(test_time_elapsed) + " sec\n")
        else:
            # create a file for each instance
            for x in range(n+1):
                new_filepath = create_file_flip(filepath, x)
                 # run each file as it is created
                test_time_start = time.time()
                p = subprocess.Popen(["java", "-cp", "org.alloytools.alloy-5.1.0/org.alloytools.alloy.dist/target/org.alloytools.alloy.dist.jar", # TODO: this should be a path to Alloy
                                      "edu.mit.csail.sdg.alloy4whole.MainClass", "-n", "1",
                                      "-f", new_filepath, test], stdout=subprocess.PIPE) # TODO: probably will need to run this script from same folder as original .als so that it can locate checkmate.als
                out, _  = p.communicate()

                if args.g:
                    # Create graph for current file
                    filename = "graph_"+str(x)
                    fgraph = open(filename, 'w')
                    fgraph.write(out)
                    counter = 0


                test_time_elapsed = time.time() - test_time_start

                # record results in output file
                fout.write(test + ": ")
                if "---INSTANCE---" in out:
                  fout.write(test + ", Observable, ")

                else:
                  fout.write(test + ", Unobservable, ")

                fout.write(str(test_time_elapsed) + " sec\n")

        if args.g:
            create_image()

    fout.close()
