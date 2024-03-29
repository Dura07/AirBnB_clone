#!/usr/bin/python3
"""
Console module.
"""

import cmd
import shlex
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    Command interpreter for HBNB console.
    """

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """
        Quit command to exit the program.
        """
        return True

    def do_EOF(self, arg):
        """
        EOF command to exit the program.
        """
        print()
        return True

    def emptyline(self):
        """
        Do nothing on an empty input line.
        """
        pass

    def help_quit(self):
        """
        Help documentation for quit command.
        """
        print("Quit command to exit the program")

    def help_EOF(self):
        """
        Help documentation for EOF command.
        """
        print("EOF command to exit the program")

    def do_create(self, arg):
        """
        Create a new instance of BaseModel, save it, and print the id.
        """
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        new_instance = globals()[class_name]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """
        Print the string representation of an instance.
        """
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        objects = storage.all()
        if key not in objects:
            print("** no instance found **")
            return
        print(objects[key])

    def do_destroy(self, arg):
        """
        Delete an instance based on the class name and id.
        """
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        objects = storage.all()
        if key not in objects:
            print("** no instance found **")
            return
        del objects[key]
        storage.save()

    def do_all(self, arg):
        """
        Print all string representation of all instances.
        """
        args = shlex.split(arg)
        objects = storage.all()
        if args and args[0] not in globals():
            print("** class doesn't exist **")
            return
        class_name = args[0] if args else None
        print([str(obj) for key, obj in objects.items() if
               not class_name or key.startswith(class_name)])

    def do_update(self, arg):
        """
        Update an instance based on the class name and id.
        """
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        objects = storage.all()
        if key not in objects:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        attribute_name = args[2]
        if len(args) < 4:
            print("** value missing **")
            return
        attribute_value_str = args[3]
        attribute_value = attribute_value_str
        try:
            # Attempt to cast the value to int or float
            attribute_value = int(attribute_value_str)
        except ValueError:
            try:
                attribute_value = float(attribute_value_str)
            except ValueError:
                pass
        setattr(objects[key], attribute_name, attribute_value)
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
