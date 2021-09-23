# COMMAND LINE PARSER by alef 
This is a very simple tool to parse command-line options for your python scripts

You just need to create a command-line definition file into your script directory (see cloptions.py file as a sample)

When calling the script, you have to place arguments first, then options. It would be easy to allow arguments 
and options in any order, but it could be messy to use.

I chose python dict instead of json because it's easier to import, it allows other variable types (not just 'str'),  
can nest tuple (json can only use array), and won't be sent/used to/by another application/system/non-python program. 

Why I didn't use argparse or click? Mainly, for fun. Besides, they are powerful, but complex and hard to fine-tune.
This one is simple and perfectly covers my needs... and I/You can evolve it at will!

## Command-Line Definition File SAMPLE:
   CHECK: cloptions.py
