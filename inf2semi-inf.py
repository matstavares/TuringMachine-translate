#!/usr/bin/python
# Mateus Seenem Tavares


import argparse


# Construct an argument parser
all_args = argparse.ArgumentParser()

# Add arguments to the parser
all_args.add_argument("-i", "--InputFile", required=False, 
                        help="Name of input file")
all_args.add_argument("-o", "--OutputFile", required=False, 
                        help="Name of output file")
all_args.add_argument("-isone", "--isOne", required=False, 
                        help="From 1 infinity side to 2 infinity tape sides", action='store_true')
all_args.add_argument("-isdouble", "--isDouble", required=False, 
                        help="From 2 infinity sides to 1 infinity tape side", action='store_true')
all_args.add_argument("-removeStationary", "--removeStationary", required=False, 
                        help="Remove Stationary movement", action='store_true')                      
args = vars(all_args.parse_args())


nameFile = "sameamount10.in"
# nameFile = "palindrome.in"

if args['InputFile']: 
  nameFile = args['InputFile']
  print("Input file is '{}'".format(nameFile))
else:
  print("No input file was given (-i InputFile), using '{}'".format(nameFile))

nameFileOut = nameFile[:-3]+".out"

if args['OutputFile']: 
  nameFileOut = args['OutputFile']
  print("Output file will be '{}'".format(nameFileOut))
else:
  print("No name for an output file was given (-o OutputFile), using '{}'".format(nameFileOut))

if args['isOne']:
  if args['isDouble']:
    print("Only one type of translation each time!")
    exit()
  print("Translating to Double...")
elif args['isDouble']:
  print("Translating to One...")
else:
  print("No type of translation was given (-isDouble or -isOne), assuming -isDouble...")
  args['isDouble'] = True

if args['removeStationary']: removeStationary = True
else: removeStationary = False

##########################
def can_typecast(state):
  try:
    exec("int('{}')".format(state))
  except ValueError:
    return False
  return True

file = open(nameFile, 'r+')
Lines = file.readlines()
Lines2 = []
rawStates = []
states = []
rawAlphabet = ["_"]
alphabet = []


# increasing states numbers to insert my 0 state
# http://morphett.info/turing/turing.html starts at 0
for line in Lines:
  currentState, currentSymbol, newSymbol, direction, nextState = line.split()
  
  # checking type to avoid "increase" words
  if can_typecast(currentState): currentStateInc = int(currentState) + 1
  else: currentStateInc = currentState
  
  if can_typecast(nextState): nextStateInc = int(nextState) + 1
  else: nextStateInc = nextState

  # removing stationary movement
  if direction == "*" and removeStationary:
    Lines2.append("{} {} {} {} £££{}".format(currentStateInc, currentSymbol, newSymbol, "r", nextStateInc))
    Lines2.append("£££{} {} {} {} {}".format(nextStateInc, "*", "*", "l", nextStateInc))

    rawStates.append("£££{}".format(nextStateInc))

  else:
    # gathering all states and the alphabet used
    rawStates.append("{}".format(currentStateInc))
    rawStates.append("{}".format(nextStateInc))
    
    rawAlphabet.append("{}".format(currentSymbol))
    rawAlphabet.append("{}".format(newSymbol))

    Lines2.append("{} {} {} {} {}".format(currentStateInc, currentSymbol, newSymbol, direction, nextStateInc))


Lines1 = Lines2
# making unique entries
states = set(rawStates)
alphabet = set(rawAlphabet)


# From Double to One side infinity

if args['isDouble']:

  for s in states:

    # When space is needed on the left

    # all states can read initial symbol
    Lines2.append("{} {} {} {} &{}".format(s, "&", "&", "r", s))
    Lines2.append("&{} {} {} {} &{}".format(s, "*", "*", "r", s))

    # if a '%' is found, create space on the right
    Lines2.append("&{} {} {} {} ¢{}".format(s, "%", "#", "r", s))
    Lines2.append("¢{} {} {} {} §{}".format(s, "_", "%", "l", s))

    # skipping '#' symbol, my 'blank symbol'
    Lines2.append("§{} {} {} {} §{}".format(s, "#", "#", "l", s))
    
    # shiffting symbols to right
    for a in alphabet:
      Lines2.append("§{} {} {} {} §{}§{}".format(s, a, "#", "r", s, a))
      Lines2.append("§{}§{} {} {} {} §{}".format(s, a, "#", a, "l", s))  

    # The Arrival, on the beginning..going back to normal
    Lines2.append("§{} {} {} {} &&&{}".format(s, "&", "&", "r", s))
    Lines2.append("&&&{} {} {} {} &&&{}".format(s, "#", "_", "l", s))
    Lines2.append("&&&{} {} {} {} {}".format(s, "&", "&", "r", s))


    # When space is needed on the right

    # all states can read final symbol
    Lines2.append("{} {} {} {} %{}".format(s, "%", "_", "r", s))
    Lines2.append("%{} {} {} {} {}".format(s, "_", "%", "l", s))


  # adding initial and final symbol for each symbol

  # initial word doesn't have spaces between
  alphabet.remove("_")
  for a in alphabet:
    # saving first element, using intermediary state based on that information
    Lines2.append("0 {} {} {} ¢¢{}".format(a, "&", "r", a))
    
    #going right and setting final
    Lines2.append("¢¢{} {} {} {} ¢¢{}".format(a, "*", "*", "r", a))
    Lines2.append("¢¢{} {} {} {} ££{}".format(a, "_", "#", "r", a))
    Lines2.append("££{} {} {} {} §§{}".format(a, "_", "%", "l", a))

    # skipping '#', my 'blank symbol'
    Lines2.append("§§{} {} {} {} §§{}".format(a, "#", "#", "l", a))
    
    # shiffting symbols to right
    for symbol in alphabet:
      Lines2.append("§§{} {} {} {} §§§{}§§§{}".format(a, symbol, "#", "r", a, symbol))
      Lines2.append("§§§{}§§§{} {} {} {} §§{}".format(a, symbol, "#", symbol, "l", a))  

    # found initial, go back one, insert element and go to "natural 0" + 1
    Lines2.append("§§{} {} {} {} &&{}".format(a, "&", "&", "r", a))
    Lines2.append("&&{} {} {} {} &&{}".format(a, "#", a, "l", a))
    Lines2.append("&&{} {} {} {} 1".format(a, "&", "&", "r"))


  # encoding with utf-8
  f = open(nameFileOut, "w+", encoding='utf-8')
  for line in Lines2:
      f.write(line)
      f.write('\n')
  f.close()


# From One to Double side infinity

if args['isOne']:
  # go left, create the limiter and go back to beginning
  Lines1.append("0 {} {} {} &&&&0".format("*", "*", "l"))
  Lines1.append("&&&&0 {} {} {} 1".format("_", "&", "r"))

  for s in states:
    # all states should go right if a '&' is read
    Lines1.append("{} {} {} {} {}".format(s, "&", "&", "r", s))
  
  # encoding with utf-8  
  f = open(nameFileOut, "w+", encoding='utf-8')
  for line in Lines2:
      f.write(line)
      f.write('\n')
  f.close()
