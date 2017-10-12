from difflib import SequenceMatcher
import difflib

source_msg="Ayam poland nya kakak";
title="";
temp = source_msg.split(" ")[:4];
for i in range(0, len(temp)):
    title = title + " "+temp[i]

print title;