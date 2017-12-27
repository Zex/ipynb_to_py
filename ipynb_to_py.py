# extract source code from ipynb
# Author: Zex Li  <top_zlynch@yahoo.com>
import ujson
import os
import glob


OUTPUT_BASE = 'ipynb_py'

def foreach_cell(cell):
    if cell.get('cell_type') == 'code':
        return ''.join(cell.get('source')) + '\n'
    return ''


def foreach_ipynb(path):
    if not path or not os.path.isfile(path):
        return None
    with open(path) as fd:
        source = ujson.load(fd)
    if not source:
        return None

    content = '\n'.join(list(map(foreach_cell, source.get('cells'))))
    to_py(content, path)


def to_py(content, path):
    relpath = os.path.basename(path).replace('ipynb', 'py')
    output = os.path.join(OUTPUT_BASE, \
            os.path.dirname(path).replace(os.getcwd()+'/', ''), relpath)
    output_base = os.path.dirname(output)

    if not os.path.isdir(output_base):
        os.makedirs(output_base)

    print("++ [create] {} from {}".format(output, path))
    with open(output, 'w') as fd:
        fd.write(content)


def load_ipynb(base):
    list(map(foreach_ipynb, glob.iglob(base+'/*.ipynb')))


def start_scan(base=None):
    if not base:
        base = os.getcwd()
    list(map(load_ipynb, glob.iglob(os.path.join(base, '*'))))

if __name__ == '__main__':
    start_scan()
