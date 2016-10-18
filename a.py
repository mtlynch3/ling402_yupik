#!/usr/bin/python3


# Yupik syllables must be of the form:
#
# * CV
# * CVC
# * CVV
# * CVVC
#
# Additionally, the first syllable of a word may be of the form:
#
# * V
# * VC
# * VV
# * VVC
#
# Where C represents a Yupik consonant and V represents a Yupik vowel.
# 
#
# In all cases, the only instances of VV that are allowed are:
#
# * ii
# * aa
# * uu
#
#
# Yupik words may contain apostrophe (to separate otherwise ambiguous grapheme sequences).
#
#
# Write a Python program that accepts a text, tokenizes it into words, 
#    and outputs a list of all words that violate any of the above rules.
#
# In other words, this program will function as a basic Yupik spell checker.
#
#
# No sample expected output will be provided for this program.
