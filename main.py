import sys
import os

import similarity
from config import Config
from ast import ast
from ui import get_opts, read_docs_from_list


def _main():
    """ Main function. Prints the AST of a file. """
    config = Config()
    filesname = get_opts(sys.argv[1:], config)
    files = []
    if len(filesname) == 1 and os.path.isfile(filesname[0]):
        for line in ast(config, '\n'.join(open(filesname[0]).readlines())):
            print line
        return
    for filename in filesname:
        if os.path.isdir(filename):
            for root, dirs, d_files in os.walk(filename):
                for d_file in d_files:
                    files.append(root + os.sep + d_file)
        else:
            files.append(filename)
    files = filter(lambda item: item.endswith('.py'), files)
    docs = read_docs_from_list(config, files)
    conn = similarity.main(config['sim'], [x for x in docs.values() if x])
    for d1, d2, value in conn:
        print d1.name, d2.name, value

if __name__ == '__main__':
    _main()
