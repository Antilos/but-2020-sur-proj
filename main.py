import os, re

## return format:
# JMENO SKORE ROZHODNUTI
class Result:
    def __init__(self, result, score, decision):
        self.res = result
        self.score = score
        self.decision = decision

    def GetContent(self):
        return self.res, self.score, self.decision
    
    def __repr__(self):
        return "{} {} {}\n".format(self.res, self.score, self.decision)

### main

targetdir = "."

results = []

## iterate through a directory

for filename in os.listdir(targetdir):
    match = re.search(r"(.+)\.png$", filename):
        if match:
            pic_name = filename
            audio_name = "{}.wav".format(match.groups(1))
            
