import os
from jacktokenizer import JackTokenizer
from compilationengine import CompilationEngine
import sys


if __name__ == '__main__':
    if len(sys.argv) == 1:  # if did not supply filename or directory
        print("Usage:\n\tpython jackanalyzer.py file")
        exit(0)
    filename = sys.argv[1]
    if not os.path.exists(filename):
        print("File/Directory does not exist")
    if os.path.isdir(filename):
        files = os.listdir(filename)
        for file in files:
            path = os.path.join(filename, file)
            tokenizer = JackTokenizer(path)
            name, extension = file.split('.')
            # after compiling one file, there will be a .xml file, and it will be included in files
            if extension == "xml":
                continue
            output_file = open(os.path.join(filename, name + ".xml"), 'w+')
            engine = CompilationEngine(tokenizer, output_file)
    else:
        tokenizer = JackTokenizer(filename)
        name = filename.split('.')[0] if '.' in filename else filename
        output_file = open(name + '.xml', "w+")
        engine = CompilationEngine(tokenizer, output_file)
