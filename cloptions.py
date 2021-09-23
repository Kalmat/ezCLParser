# THis is a sample command-line definition file (play with it to understand how it works)
# WARNING: The content is just a sample. It doesn't make any sense at all!!!
# WARNING: When calling the script, place arguments first, then options
#          Options must always start by an 'indicator' (otherwise, will be considered as "Free" arguments or values)
# SUGGESTION: Try to cover different cases by program, instead of defining highly complex command-line rules
#             'Defaulting' to specific actions/values is also a good practice
# SUGGESTION: Check default values if you intend to leave any ot these variables empty

# ARGUMENTS: Define script functionality (with no values), or are always required (e.g. an object to work with)
#            Arguments may start by "-" or not
#            Arguments not starting by "-" are considered "Free" Arguments (e.g. a filename) and are treated separately
#            NOTE: MutExc define mutually exclusive arguments. They are not compatible when put together
#            NOTE: You may leave "Values" empty {} if you do not use any argument, but you better fill the other entries
arguments = {
    "Usage": "python3 clparser.py ARGUMENT [OPTIONS]",
    "Values": {
        "-e": {"Name": "encrypt", "Help": "Encrypt data"},
        "+d": {"Name": "decrypt", "Help": "Decrypt data"},
        "-g": {"Name": "generate key", "Help": "Generate key"},
    },
    "MinArg": 1,
    "MaxArg": 2,
    "MutExc": [("-e", "+d")],
    "FreeArgs": True,
    "FreeArgsDesc": "file name",
    "MinFreeArgs": 0,
    "MaxFreeArgs": 3
}

# OPTIONS: Define different behaviors for the selected functionality
#          Options must always start by "-", and may require a value, several or none (flag)
#          They are mainly optional!!!
#          NOTE: isFlag: False means it requires a value (True means no value is required. In fact, will be ignored)
#          NOTE: FreeValues: True means you can put as many values as you want, returned as a list (eventhough empty)
#          NOTE: NoContent: Ignore means the option will be ignored if it requires a value, but does not have any.
#                Otherwise, will return an ERROR and will exit the script.
#          NOTE: You may leave "Values" empty {} if you do not use any option, but you better fill the other entries
options = {
    "Values": {
        "-i": {"Name": "input file", "isFlag": False, "FreeValues": False, "NoContent": "Ignore", "Help": "Input file to Encrypt/Decrypt"},
        "-iq": {"Name": "QR input file", "isFlag": False, "FreeValues": False, "NoContent": "Ignore", "Help": "Input file in QR format (.png)"},
        "-m": {"Name": "QR input file", "isFlag": False, "FreeValues": True, "NoContent": "Ignore", "Help": "Message to Encrypt/Decrypt"},
        "-o": {"Name": "output file", "isFlag": False, "FreeValues": False, "NoContent": "Ignore", "Help": "Output file to write encrypted/decrypted data or key"},
        "-oq": {"Name": "QR output file", "isFlag": False, "FreeValues": False, "NoContent": "Ignore", "Help": "Output file in QR format (.png)"},
        "-p": {"Name": "password", "isFlag": True, "FreeValues": False, "NoContent": "Ignore", "Help": "Password to Encrypt/Decrypt data (use quotation marks to delimit)"},
        "-k": {"Name": "key", "isFlag": False, "FreeValues": False, "NoContent": "Ignore", "Help": "Key to Encrypt/Decrypt data (use quotation marks to delimit)"}
    },
    "MutExc": [("-i", "-iq"), ("-o", "-oq")],
    "RequiredIf": [["-iq", "-oq"]]
}

# Rules when combining arguments and options (others than "general" rules defined above, depending on the arguments set)
# You may leave all this variable empty {} if no specific rules apply
arg_opt = {
    "-g": {"Required": ["-p", "-m"], "RequiredIf": [("-i", ["-o"])], "MutExc": [("-i", "-iq"), ("-o", "-oq")], "Ignored": ["-i", "-iq", "-m", "-k"]}
}
