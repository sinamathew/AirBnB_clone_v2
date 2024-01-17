#!/usr/bin/python3
"""Console module
this module defines console program entry point
"""
import cmd
import re
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.place import Place
from models.city import City
from models import storage


class HBNBCommand(cmd.Cmd):
    """ this class is a subclass for cmd.Cmd class """

    @staticmethod
    def missing_name():
        """ print class name is missing message """
        print("** class name missing **")

    @staticmethod
    def wrong_class():
        """ print class doesn't exist message """
        print("** class doesn't exist **")

    @staticmethod
    def missing_id():
        """ print instance id is missing message """
        print("** instance id missing **")

    @staticmethod
    def invalid_instance():
        """ print no instance found """
        print("** no instance found **")

    def value_conversion(self, value):
        """ perform value conversion """

        # Strip off the double quote [""] around values
        value = value.strip('"')
        if value.isdecimal():
            val = int(value)
            return val
        try:
            val = float(value)
            return val
        except ValueError:
            return value

    # Handle interactive mode and non interactive mode
    if os.isatty(0):
        prompt = "(hbnb) "
    else:
        prompt = ""

    def do_quit(self, args):
        """usage: quit
        Quit the program
        """
        return True

    def do_EOF(self, args):
        """usage: (hbnb) ^D or (hbnb) EOF
        Mark End of the file => Quit the program
        """
        return True

    def update_dict(self, line):
        """ update an instance Given update value in form of dictionary """
        model, id_param, dict_val = line
        my_storage = storage.all()
        if my_storage == {}:
            self.handle_empty_dict([model, id_param])
            return
        models = [
                "BaseModel",
                "User",
                "Place",
                "Review",
                "City",
                "State",
                "Amenity"
                ]
        if model not in models:
            self.missing_name()
            return
        elif id_param == "":
            self.missing_id()
            return
        else:
            obj_updated = False
            id_model = f"{model}.{id_param}"
            try:
                obj = my_storage[id_model]
                for attr_name, attr_value in dict_val.items():
                    setattr(obj, attr_name, attr_value)
                    obj_updated = True
                if obj_updated:
                    obj.save()
            except Exception:
                self.invalid_instance()

    def precmd(self, line):
        """ preprocess the input command before main process occur """
        user_all = re.compile(r'^(\D+)\.all\(\)')
        user_count = re.compile(r'^(\D+)\.count\(\)')
        user_show = re.compile(r'^(\D+)\.(\D+)\([\'"](.*)[\'"]\)')
        update = re.compile(r'^(\D+)\.update\("(.*)", "(.*)", "(.*)"\)')
        update_dict = re.compile(r'^(\D+)\.update\("(.*)", (\{.*})\)')

        if update_dict_match := update_dict.match(line):
            my_storage = storage.all()
            model = update_dict_match.group(1)
            id_param = update_dict_match.group(2)
            dict_str = update_dict_match.group(3)
            json_str = dict_str.replace("'", '"')
            actual_dict = json.loads(json_str)
            self.update_dict((model, id_param, actual_dict))
            return ""
        if update_match := update.match(line):
            model = update_match.group(1)
            id_param = update_match.group(2)
            attr = update_match.group(3)
            value = update_match.group(4)
            return f'update {model} {id_param} {attr} "{value}"'
        elif user_match := user_all.match(line):
            return f"all {user_match.group(1)}"
        elif user_show_match := user_show.match(line):
            model = user_show_match.group(1)
            command = user_show_match.group(2)
            id_param = user_show_match.group(3)
            return f"{command} {model} {id_param}"
        elif user_count_match := user_count.match(line):
            model = user_count_match.group(1)
            return f"count {model}"
        else:
            return line

    def handle_empty_dict(self, args_list):
        """ handle case when dictionary is empty """
        m = ['BaseModel',
             'Place',
             'User',
             'City',
             'State',
             'Amenity',
             'Review'
             ]
        if args_list[0] not in m:
            self.wrong_class()
            return
        if args_list[0] in m and len(args_list) == 1:
            self.missing_id()
            return
        self.invalid_instance()
        return

    def emptyline(self):
        """emptyline + Enter
        make sure nothing is executed when the line is empty
        """
        pass

    def convert_value(self, value):
        converted = False
        try:
            value = int(value)
            converted = True
        except Exception:
            pass
        try:
            if not converted:
                value = float(value)
                converted = True
        except Exception:
            pass
        if not converted and value != "":
            value = value[1:-1]
        return value

    def do_create(self, model):
        """Create an instance of BaseModel """
        obj_dict = {
                "BaseModel": BaseModel,
                "User": User,
                "Place": Place,
                "City": City,
                "Amenity": Amenity,
                "State": State,
                "Review": Review
                }
        if model == "":
            self.missing_name()
            return
        args = model.split()
        model = args[0]
        if model not in obj_dict:
            self.wrong_class()
            return
        tokens = args[1:]
        obj = obj_dict[model]()
        for token in tokens:
            token_arr = token.split("=")
            if len(token_arr) == 2:
                key, value = token_arr
                value = self.convert_value(value)
                if value != "":
                    setattr(obj, key, value)
        print(obj.id)
        obj.save()

    def do_count(self, model):
        """ count number of instance a model appear in the json file """
        my_storage = storage.all()
        user_count = 0
        if my_storage == {}:
            print(user_count)
        else:
            for key, user in my_storage.items():
                class_name = user.__class__.__name__
                if model == class_name:
                    user_count += 1
            print(user_count)

    def do_show(self, args):
        """ show an instance of BaseModel """
        args_list = args.split()
        my_storage = storage.all()
        if len(args_list) == 0:
            self.missing_name()
            return
        class_exist = False
        id_exist = False

        # handle case when storage is empty
        if my_storage == {}:
            self.handle_empty_dict(args_list)
            return

        for key, obj in my_storage.items():
            class_name = obj.__class__.__name__
            if class_name == args_list[0]:
                class_exist = True
                if len(args_list) == 1:
                    self.missing_id()
                    return
                if obj.id == args_list[1]:
                    print(obj)
                    return

        # Check if class and id exist
        if not class_exist:
            self.wrong_class()
            return
        if not id_exist:
            self.invalid_instance()
            return

    def do_all(self, args):
        """ print all instances """
        my_storage = ""
        m = ['BaseModel',
             'Place',
             'User',
             'City',
             'State',
             'Amenity',
             'Review'
             ]
        obj_list = []
        if args == "":
            my_storage = storage.all()
        elif args in m:
            my_storage = storage.all(args)
        if args == "" or (args in m and my_storage == {}):
            for user_id in my_storage.keys():
                obj_list.append(str(my_storage[user_id]))
            print(obj_list)
            return
        class_exist = False
        for key, obj in my_storage.items():
            class_name = obj.__class__.__name__
            if class_name == args:
                obj_list.append(str(obj))
                class_exist = True

        if class_exist:
            print(obj_list)
            return

        if not class_exist:
            self.wrong_class()

    def do_destroy(self, args):
        """ delete a given instance from the json file """
        args_list = args.split()
        my_storage = storage.all()
        if len(args_list) == 0:
            self.missing_name()
            return
        class_exist = False
        id_exist = False

        # handle case when storage is empty
        if my_storage == {}:
            self.handle_empty_dict(args_list)
            return

        for key, obj in my_storage.items():
            class_name = obj.__class__.__name__
            if class_name == args_list[0]:
                class_exist = True
                if len(args_list) == 1:
                    self.missing_id()
                    return
                if obj.id == args_list[1]:
                    id_exist = True
                    storage.delete(key)
                    storage.save()
                    return

        # check if class and id doesnt exist
        if not class_exist:
            self.wrong_class()
            return
        if not id_exist:
            self.invalid_instance()

    def do_update(self, args):
        """ update an instance """
        my_storage = storage.all()
        args_list = args.split()
        if len(args_list) == 0:
            self.missing_name()
            return

        # handle case when storage is empty
        if my_storage == {}:
            self.handle_empty_dict(args_list)
        else:
            class_exist = False
            id_exist = False
            for key, obj in my_storage.items():
                class_name = obj.__class__.__name__
                if class_name == args_list[0]:
                    class_exist = True
                    if len(args_list) == 1:
                        self.missing_id()
                        return
                    if obj.id == args_list[1]:
                        id_exist = True
                        if len(args_list) == 2:
                            print("** attribute name missing **")
                            return
                        if len(args_list) == 3:
                            print("** value missing **")
                            return
                        attr = args_list[2]
                        value = args_list[3]
                        c_a = "created_at"
                        u_a = "updated_at"
                        if attr != "id" and attr != c_a and attr != u_a:
                            val = self.value_conversion(value)
                            setattr(obj, attr, val)
                            obj.save()
                            return

            # Check if class name or id does not match
            if not class_exist:
                self.wrong_class()
            if not id_exist:
                self.invalid_instance()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
