# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility
import re

regex = r"[:|/]"

test_str = ("STEEM:BTS\n"
            "BTC/USD\n"
            "open.BTC/bitUSD\n"
            "ZEPH:BTS\n"
            "bridge.BTC/rudex.BTC")

matches = re.finditer(regex, test_str)

print(test_str)

for matchNum, match in enumerate(matches):
    matchNum = matchNum + 1

    print ("Match {matchNum}: was found at {start}-{end}: {match}".format(matchNum = matchNum,
                                                                          start = match.start(), 
                                                                          end = match.end(), 
                                                                          match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, 
                                                                         start = match.start(groupNum), 
                                                                         end = match.end(groupNum), 
                                                                         group = match.group(groupNum)))



