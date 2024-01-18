#!/usr/bin/python3
""" Test
"""
import os

if os.path.exists("file.json"):
    os.remove("file.json")

from models.engine.file_storage import FileStorage
from models.state import State

if os.path.exists(FileStorage._FileStorage__file_path):
    os.remove(FileStorage._FileStorage__file_path)


fs = FileStorage()

# All with nothing
all_objs = fs.all()
if len(all_objs.keys()) > 0:
    print("all() is returning result when it should not")
    exit(1)

# Create a new State
new_state = State()
new_state.name = "California"
fs.new(new_state)
fs.save()
key_search = "{}.{}".format("State", new_state.id)

all_objs = fs.all()
if len(all_objs.keys()) != 1:
    print("all() is not returning the new State created")
    exit(1)

if all_objs.get(key_search) is None:
    print("State created should be in the list of objects")
    exit(1)

print("OK", end="")
