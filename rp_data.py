"""Practical data store: loads `RP info.txt` and looks practicals up by name.

Kept free of tkinter so it can be imported (and tested) without a display.
The file is a 97-slot hash table, one Python dict literal per line, placed at
index sum(ord(c) for c in name) % 97 with linear probing on collisions.
"""

import ast
import os

TABLE_SIZE = 97
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RP info.txt")


def hashKey(key):
    """Return the home slot for a practical name."""
    hash_val = 0
    for letter in key:
        hash_val += ord(letter)
    return hash_val % TABLE_SIZE


def loadTable(path=DATA_FILE):
    """Read the hash table file and return its lines (newlines stripped)."""
    with open(path, "r", encoding="utf-8") as database:
        return [line.rstrip("\n") for line in database]


RP_dicts = loadTable()


def hashGet(key, table=None):
    """Return the practical dict whose "name" is `key`, probing linearly from its home slot."""
    if table is None:
        table = RP_dicts
    hash_val = hashKey(key)
    for _ in range(len(table)):
        line = table[hash_val % len(table)]
        if not line:
            break  # an empty slot ends the probe: the key isn't stored
        entry = ast.literal_eval(line)
        if entry["name"] == key:
            return entry
        hash_val += 1
    raise KeyError(key)
