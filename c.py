#!/usr/bin/python3

# Yupik has voiced and voiceless nasals and fricatives.
#
# Certain Yupik fricatives and nasals are "doubleable";
#    that is, they exist in voiced/voiceless pairs
#    where the voiced/voiceless distinction is denoted graphemically through "doubling":
#
# l   -> ll
# r   -> rr
# g   -> gg
# gh  -> ghh
# ghw -> ghhw
# n   -> nn
# m   -> mm
# ng  -> ngng
# ngw -> ngngw
#
#
# The remaining Yupik consonants do not show this doubling pattern.
#
#
#
# Write a Python program that accepts text from standard input,
# lowercases it, and tokenizes it into Yupik graphemes, applies the following devoicing rules, 
# and then prints the corresponding output (formatted as words, not lists of graphemes).
#
#
# For each tokenized word, apply the following automatic devoicing rules:
#
# 1a) If an undoubled (but doubleable) fricative occurs immediately before OR after an unvoiced consonant
#     (where that other consonant is not doubleable),
#     the grapheme for the doubleable voiced fricative is replaced with its voiceless counterpart.
#
# 2) If an undoubled (but doubleable) nasal occurs immediately after an unvoiced consonant
#     (where that other consonant is not doubleable), 
#     the grapheme for the doubleable voiced nasal is replaced with its voiceless counterpart.
#
# 3a) If an undoubled (but doubleable) nasal or fricative occurs immediately after an unvoiced fricative
#     (where that other consonant is doubled),
#     the grapheme for the doubleable voiced consonant is replaced with its voiceless counterpart.
#
# 3b) If an undoubled (but doubleable) nasal or fricative occurs immediately before the unvoiced fricative ll
#     the grapheme for the doubleable voiced consonant is replaced with its voiceless counterpart.
import sys
import string
import nltk

#create dict
d = {}
with open("ipa.tsv") as ipa:
    for line in ipa:
        line_split = line.split('\t')
        grapheme = line_split[0]
        ipa_char = line_split[1].rstrip()
        if not grapheme.startswith('#') and grapheme != '':
            d[grapheme] = ipa_char

#get graphemes            
graphemes = []
for key in d:
    graphemes.append(key)

#sort graphemes by length
graphemes.sort(key=len, reverse=True)

#input text file
f = sys.stdin.read()
f_words = []
for line in f.splitlines():
    f_words.append(nltk.word_tokenize(line))

#remove punctuation
new_words = []
for line in f_words:
    temp  = []
    for word in line:
        new_str = ""
        for ltr in word:
            if ltr == "’" or ltr.isalpha() == True or ltr == '\'':
                new_str = new_str + ltr
        if len(new_str) > 0:
            temp.append(new_str)
    new_words.append(temp)
f_words = new_words

#do the things
ret = []
for line in f_words:
    temp  = []
    for word in line:
        ret_word = []
        word = word.lower()
        curr_idx = 0
        while curr_idx < len(word):
            if word[curr_idx] == "'" or word[curr_idx] == "’":
                curr_idx = curr_idx + 1
                continue
            didFind = False
            for g in graphemes:
                if word.find(g, curr_idx) == curr_idx:
                    ret_word.append(g)
                    curr_idx = curr_idx + len(g)
                    didFind = True
                    break
            if didFind == False:
                ret_word.append(word[curr_idx])
                curr_idx = curr_idx + 1
        temp.append(ret_word)
    ret.append(temp)


#PART C

double_dict = {'l': 'll', 'r': 'rr', 'g': 'gg', 'gh': 'ghh', 'ghw': 'ghhw', 'n': 'nn', 'm': 'mm', 'ng': 'ngng', 'ngw': 'ngngw'}
double_fricatives = ['l', 'r', 'g', 'gh', 'ghw']
double_nasals = ['n', 'm', 'ng', 'ngw']
unvoiced_consonants = ['p', 't', 'k', 'kw', 'q', 'qw', 'f', 'll', 's', 'rr', 'gg', 'wh', 'ghh', 'ghhw', 'h', 'mm', 'nn', 'ngng', 'ngngw']
unvoiced_fricatives = ['f', 'll', 's', 'rr', 'gg', 'wh', 'ghh', 'ghhw', 'h']

#undoubled, but doubleable
doubleable = []
for key in double_dict:
    doubleable.append(key)
#doubled
doubled = double_dict.values()

for line in ret:
    for word in line:
        ret_str = ""
        didDouble = False
        for i,grapheme in enumerate(word):
            end_idx = len(word)
            vowels = []
            #1a
            #word initial grapheme
            if i == 0:
                if word[i] in double_fricatives and (word[i+1] in unvoiced_consonants and word[i+1] not in doubleable):
                    ret_str += double_dict[word[i]]
                    didDouble = True
            #word final grapheme
            elif i == end_idx-1:
                if word[i] in double_fricatives and (word[i-1] in unvoiced_consonants and word[i-1] not in doubleable):
                    ret_str += double_dict[word[i]]
                    didDouble = True
            else:
                if word[i] in double_fricatives and ((word[i+1] in unvoiced_consonants or word[i-1] in unvoiced_consonants) \
                   and (word[i+1] not in doubleable or word[i-1] not in doubleable)):
                        ret_str += double_dict[word[i]]
                        didDouble = True
            if didDouble:
                continue
            didDouble = False
            #2
            if i > 0:
                if word[i] in double_nasals and (word[i-1] in unvoiced_consonants and word[i-1] not in doubleable):
                    ret_str += double_dict[word[i]]
                    didDouble = True
            if didDouble:
                continue
            didDouble = False
            #3a
            if i > 0:
                if (word[i] in double_nasals or word[i] in double_fricatives) and (word[i-1] in unvoiced_fricatives and word[i-1] in doubled):
                    ret_str += double_dict[word[i]]
                    didDouble = True
            if didDouble:
                continue
            didDouble = False
            #3b
            if i < end_idx-1:
                if (word[i] in double_nasals or word[i] in double_fricatives) and word[i+1] == 'll':
                    ret_str += double_dict[word[i]]
                    didDouble = True
            if didDouble == False:
                ret_str += grapheme
        print(ret_str, end=" ")
    print()
                
            
