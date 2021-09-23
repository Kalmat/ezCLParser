#!/usr/bin/python3
# -*- coding: utf-8 -*-

__version__ = "1.0.0"

"""
********* VERY SIMPLE YET EFFECTIVE COMMAND LINE PARSER by alef ********* 
This is a very simple tool to parse command-line options for your python scripts

You just need to create a command-line definition file into your script directory (see cloptions.py file as a sample)
When calling the script, you have to place arguments first, then options. It would be easy to allow arguments 
and options in any order, but it could be messy to use.

I chose python dict instead of json because it's easier to import, it allows other variable types (not just 'str'),  
can nest tuple (json can only use array), and won't be sent/used to/by another application/system/non-python program. 
Why I didn't use argparse or click? Mainly, for fun. Besides, they are powerful, but complex and hard to fine-tune.
This one is simple and perfectly covers my needs... and I/You can evolve it at will!
"""

import sys


def format_type(value):
    return str(type(value)).replace("<class ", "").replace(">", "")


def raise_error(section, error_type, level, values):
    if error_type == "missing":
        if level == 1:
            print("WARNING; %s: Missing '%s' entry in cl-definition file. Assuming '%s'"
                  % (section, values[0], values[1]))
        else:
            print("WARNING: %s: Missing entry '%s' for key '%s' in '%s' section in cl-definition file. Assuming '%s'"
                  % (section, values[0], values[1], values[2], values[3]))
    else:
        if level == 1:
            print("ERROR: %s: the value for key '%s' in cl-definition file has a wrong type. It should be %s, not %s"
                  % (section, values[0], format_type(values[1]), format_type(values[2])))
        else:
            print("ERROR: %s: the value in cl-definition file for entry '%s' in key '%s' and subkey '%s' "
                  "has a wrong type. It should be %s, not %s"
                  % (section, values[0], values[1], values[2], format_type(values[3]), format_type(values[4])))
        exit()


def check_cl_definition_file(arguments, options, arg_opt, script_name, chk_warn=False):

    # Keys, structure and default values of the expected content of the command-line definition file
    check_arguments = [
        ("Usage", "'" + script_name + " ARGUMENTS" + " [OPTIONS]" + "'"),
        ("Values", {}, [("Name", ""), ("Help", "")]),
        ("MinArg", 0), ("MaxArg", 0), ("MutExc", []),
        ("FreeArgs", True), ("MinFreeArgs", 1), ("MaxFreeArgs", 1), ("FreeArgsDesc", "")
    ]
    
    check_options = [
        ("Values", {}, [("Name", ""), ("isFlag", True), ("FreeValues", False), ("NoContent", "Ignore"), ("Help", "")]),
        ("MutExc", []),
        ("RequiredIf", [])
    ]

    check_arg_opt = [
        ("Required", []), ("RequiredIf", []), ("MutExc", []), ("Ignored", [])
    ]

    # Check file according to rules defined above
    # PENDING: Check values types of 2nd and further levels (e.g. "MutExc")
    arguments_result = arguments.copy()
    for key in check_arguments:
        if key[0] not in arguments.keys():
            arguments_result[key[0]] = key[1]
            if chk_warn:
                raise_error("Arguments", "missing", 1, (key[0], key[1]))
        elif type(key[1]) != type(arguments[key[0]]):
            if chk_warn:
                raise_error("Arguments", "type", 1, (key[0], key[1], arguments[key[0]]))
        else:
            if len(key) > 2:
                for subkey in arguments[key[0]].keys():
                    for i, entry in enumerate(key[2]):
                        if entry[0] not in arguments[key[0]][subkey].keys():
                            arguments_result[key[0]][subkey][entry[0]] = key[2][i][1]
                            if chk_warn:
                                raise_error("Arguments", "missing", 2, (entry[0], subkey, key[0], entry[1]))
                        elif type(entry[1]) != type(arguments[key[0]][subkey][entry[0]]):
                            if chk_warn:
                                raise_error("Arguments", "type", 2, (entry[0], key[0], subkey, entry[1],
                                                                     arguments[key[0]][subkey][entry[0]]))

    options_result = options.copy()
    for key in check_options:
        if key[0] not in options.keys():
            options_result[key[0]] = key[1]
            if chk_warn:
                raise_error("Options", "missing", 1, (key[0], key[1]))
        elif type(key[1]) != type(options[key[0]]):
            if chk_warn:
                raise_error("Options", "type", 1, (key[0], key[1], options[key[0]]))
        else:
            if len(key) > 2:
                for subkey in options[key[0]].keys():
                    for i, entry in enumerate(key[2]):
                        if entry[0] not in options[key[0]][subkey].keys():
                            options_result[key[0]][subkey][entry[0]] = key[2][i][1]
                            if chk_warn:
                                raise_error("Options", "missing", 2, (entry[0], subkey, key[0], entry[1]))
                        elif type(entry[1]) != type(options[key[0]][subkey][entry[0]]):
                            if chk_warn:
                                raise_error("Options", "type", 2, (entry[0], key[0], subkey,
                                                                   entry[1], options[key[0]][subkey][entry[0]]))

    arg_opt_result = arg_opt.copy()
    for key in arg_opt.keys():
        for entry in check_arg_opt:
            if entry[0] not in arg_opt[key].keys():
                arg_opt_result[key][entry[0]] = entry[1]
                if chk_warn:
                    raise_error("Arguments/Options", "missing", 1, (entry[0], key, entry[1]))
            elif type(entry[1]) != type(arg_opt[key][entry[0]]):
                if chk_warn:
                    raise_error("Arguments/Options", "type", 1, (entry[0], entry[1], arg_opt[key][entry[0]]))

    return arguments_result, options_result, arg_opt_result


def print_help(arguments, options, script_name=""):

    print_arguments = False
    if "Values" in arguments.keys() and len(arguments["Values"]) > 0:
        print_arguments = True
    print_options = False
    if "Values" in options.keys() and len(options["Values"]) > 0:
        print_options = True

    if "Usage" in arguments.keys():
        usage = arguments["Usage"]
    else:
        usage = "'python3 " + script_name
        if print_arguments:
            usage += " ARGUMENTS"
        if print_options:
            usage += " [OPTIONS]"
        usage += "'"

    print("USAGE:", usage)
    if print_arguments:
        print("ARGUMENTS:")
        for key in arguments["Values"].keys():
            print(" "*3, key, " "*(4-len(key)), arguments["Values"][key]["Help"])
    if print_options:
        print("OPTIONS:")
        for key in options["Values"].keys():
            print(" "*3, key, " "*(4-len(key)), options["Values"][key]["Help"])

    exit()


def get_arguments(cl_values, arguments, options):

    # Gather arguments
    args = []
    arg_names = []
    free_arg_values = []
    for i in range(1, len(cl_values)):
        if cl_values[i] in arguments["Values"].keys():
            if not cl_values[i] in args:
                args.append(cl_values[i])
                arg_names.append(arguments["Values"][cl_values[i]]["Name"])
            else:
                print("WARNING: Argument %s duplicated. Second and further occurrences will be ignored" % cl_values[i])
        elif arguments["FreeArgs"] and \
                cl_values[i] not in arguments["Values"].keys() and cl_values[i] not in options["Values"].keys():
            free_arg_values.append(cl_values[i])
        else:
            break

    # Check if arguments number (min and max) is correct
    if len(args) < arguments["MinArg"]:
        print("ERROR: Need to choose at least %i and a maximum of %i valid arguments"
              % (arguments["MinArg"], arguments["MaxArg"]))
        print_help(arguments, options)
    if len(args) > arguments["MaxArg"]:
        print("ERROR: Too many arguments. Choose a minimum of %i and a maximum of %i from %s"
              % (arguments["MinArg"], arguments["MaxArg"], list(arguments["Values"].keys())))
        print_help(arguments, options)
    if arguments["FreeArgs"]:
        if len(free_arg_values) < arguments["MinFreeArgs"]:
            print("ERROR: Need to enter at least %i and a maximum of %i %s arguments"
                  % (arguments["MinFreeArgs"], arguments["MaxFreeArgs"], arguments["FreeArgsDesc"]))
            print_help(arguments, options)
        if len(free_arg_values) > arguments["MaxFreeArgs"]:
            print("ERROR: Too many %s arguments. enter a minimum of %i and a maximum of %i"
                  % (arguments["FreeArgsDesc"], arguments["MinFreeArgs"], arguments["MaxFreeArgs"]))
            print_help(arguments, options)

    # Check if arguments are not mutually exclusive
    if len(args) > 1:
        for i in range(len(arguments["MutExc"])):
            common = list(set(args).intersection(arguments["MutExc"][i]))
            if len(common) > 1:
                print("ERROR: Arguments are not compatible:", common)
                print_help(arguments, options)

    return args, arg_names, free_arg_values


def get_options(cl_values, arguments, options, pos):

    # Gather options and its values
    opts = []
    opt_values = []
    while pos < len(cl_values):
        if cl_values[pos] in options["Values"].keys():
            if not cl_values[pos] in opts:
                opts.append(cl_values[pos])
                if not options["Values"][cl_values[pos]]["isFlag"]:
                    value_found = False
                    if options["Values"][cl_values[pos]]["FreeValues"]:
                        free_values = []
                        while True:
                            if len(cl_values) > pos + 1 and cl_values[pos+1] not in options["Values"].keys():
                                free_values.append(cl_values[pos + 1])
                                pos += 1
                                value_found = True
                            else:
                                break
                        opt_values.append(free_values)
                    elif len(cl_values) > pos + 1 and cl_values[pos+1] not in options["Values"].keys():
                        opt_values.append(cl_values[pos + 1])
                        pos += 1
                        value_found = True
                    if not value_found:
                        opts = opts[:-1]
                        if options["Values"][cl_values[pos]]["NoContent"] == "Ignore":
                            print("WARNING: option %s needs a value. It will be ignored" % cl_values[pos])
                        else:
                            print("ERROR: option %s requires a value" % cl_values[pos])
                            print_help(arguments, options)
                else:
                    opt_values.append(None)
                    printed = False
                    for i in range(pos + 1, len(cl_values)):
                        if cl_values[i] not in options["Values"].keys():
                            if not printed:
                                print("WARNING: Option %s is a flag. All its values will be ignored" % cl_values[pos])
                                printed = True
                            pos += 1
                        else:
                            break
            else:
                print("WARNING: Option %s duplicated. Second and further occurrences will be ignored" % cl_values[pos])
                for i in range(pos + 1, len(cl_values)):
                    if cl_values[i] not in options["Values"].keys():
                        pos += 1
                    else:
                        break
        else:
            print("WARNING: Option %s not valid. It will be ignored" % cl_values[pos])
        pos += 1

    # Check other options rules: MutExc (Mutually Exclusive) and RequiredIf (other option present)
    for i in range(len(options["MutExc"])):
        common = list(set(opts).intersection(options["MutExc"][i]))
        if len(common) > 1:
            print("ERROR: Options are not compatible:", common)
            print_help(arguments, options)
    for i in range(len(options["RequiredIf"])):
        if options["RequiredIf"][i][0] in opts:
            common = list(set(opts).intersection(options["RequiredIf"][i][1]))
            if len(common) == 0:
                print("ERROR: Option %s requires %s"
                      % (options["RequiredIf"][i][0], options["RequiredIf"][i][1]))
                print_help(arguments, options)

    return opts, opt_values


def check_args_opts(arguments, options, args, opts, arg_opt):

    # Check if options meet the rules for every argument: Required, RequiredIf (other option set), MutExc (incompatible)
    for key in args:
        if key in arg_opt.keys():
            for i in range(len(arg_opt[key]["MutExc"])):
                common = list(set(opts).intersection(arg_opt[key]["MutExc"][i]))
                if len(common) > 1:
                    print("ERROR: Options are not compatible:", common)
                    print_help(arguments, options)
            for i in range(len(arg_opt[key]["Required"])):
                if arg_opt[key]["Required"][i] not in opts:
                    print("ERROR: Argument %s requires %s" % (key, arg_opt[key]["Required"]))
                    print_help(arguments, options)
            for i in range(len(arg_opt[key]["RequiredIf"])):
                if arg_opt[key]["RequiredIf"][i][0] in opts:
                    common = list(set(opts).intersection(arg_opt[key]["RequiredIf"][i][1]))
                    if len(common) == 0:
                        print("ERROR: Option %s requires %s for argument %s"
                              % (arg_opt[key]["RequiredIf"][i][0], arg_opt[key]["RequiredIf"][i][1], key))
                        print_help(arguments, options)
            common = list(set(opts).intersection(arg_opt[key]["Ignored"]))
            if len(common) > 0:
                print("WARNING: Options %s have no effect for argument %s" % (common, key))

    return


def read_command_line(cl_values, arguments, options, arg_opt, chk_warn=False):

    if len(cl_values) == 1 or cl_values[1] in ("-h", "--help", "-?", "--?"):
        print_help(arguments, options, cl_values[0])

    arguments, options, arg_opt = check_cl_definition_file(arguments, options, arg_opt, cl_values[0], chk_warn)

    args, arg_names, free_arg_values = get_arguments(cl_values, arguments, options)
    opts, opt_values = get_options(cl_values, arguments, options, len(args) + len(free_arg_values) + 1)
    check_args_opts(arguments, options, args, opts, arg_opt)

    return args, arg_names, free_arg_values, opts, opt_values


if __name__ == "__main__":

    from cloptions import *

    args, arg_names, free_arg_values, opts, opt_values = read_command_line(sys.argv, arguments, options, arg_opt, True)

    print("ARGUMENTS:", args)
    print("ARGUMENTS NAMES:", arg_names)
    print("OTHER ARGUMENTS:", free_arg_values)
    print("OPTIONS:", opts)
    print("OPTIONS VALUES:", opt_values)
