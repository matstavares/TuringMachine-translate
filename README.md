# TuringMachine-translator
From infinity tape to a semi-infinity tape (as used in, eg, Sipser) and also on the other way...and removing stationary movement, because why not?

Using http://morphett.info/turing/turing.html to simulate

Reserved symbols are #, &, %, £, ¢, §

## How to use

python infinity2semi-infinity.py
or 
python3 infinity2semi-infinity.py 

args:

-i <name with extension of the input file> 
-o <name with extension of the output file> 

-isOne [the input file works on a tape with only one infinite side, so It will be translated to a tape with two infinities sides]

-isDouble [the input file works on a tape with inifinite on both sides, so It will be translated to a tape with only one infinite side]

If no input is set, It will look for "sameamount10.in" and assume that it works with two sides (-isDouble) and It will translate it to a semi-infinity tape
