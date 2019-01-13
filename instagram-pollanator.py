#! /bin/python

##########################################################
#                                                        #
# $$$$$$$$\$$\      $$$$$$\ $$$$$$$$\$$\      $$\        #
# $$  _____$$ |    $$  __$$\$$  _____$$ |     $$ |       #
# $$ |     $$ |    $$ /  \__$$ |     $$ |     $$ |       #
# $$$$$\   $$ |    \$$$$$$\ $$$$$\   $$ |     $$ |       #
# $$  __|  $$ |     \____$$\$$  __|  $$ |     $$ |       #
# $$ |     $$ |    $$\   $$ $$ |     $$ |     $$ |       #
# $$$$$$$$\$$$$$$$$\$$$$$$  $$$$$$$$\$$$$$$$$\$$$$$$$$\  #
# \________\________\______/\________\________\________| #
#                                                        #
##########################################################

# Instagram Pollinator
######################
# Created January 2019
# By elsell (http://github.com/elsell/)


import sys
import json
import os

# Quick & Dirty cross-platform screen clear function
def clearScreen():
    os.system('cls||clear')

# Name Printer!
def printName():
    print(""" ___ _   _ ____ _____  _    ____ ____     _    __  __          
 |_ _| \ | / ___|_   _|/ \  / ___|  _ \   / \  |  \/  |        
  | ||  \| \___ \ | | / _ \| |  _| |_) | / _ \ | |\/| |       
  | || |\  |___) || |/ ___ | |_| |  _ < / ___ \| |  | |        
 |___|_| \_|____/ |_/_/   \_\____|_| \_/_/   \_|_|  |_|        
  ____   ___  _     _        _    _   _    _  _____ ___  ____  
 |  _ \ / _ \| |   | |      / \  | \ | |  / \|_   _/ _ \|  _ \ 
 | |_) | | | | |   | |     / _ \ |  \| | / _ \ | || | | | |_) |
 |  __/| |_| | |___| |___ / ___ \| |\  |/ ___ \| || |_| |  _ < 
 |_|    \___/|_____|_____/_/   \_|_| \_/_/   \_|_| \___/|_| \_ 
                 - github.com/elsell -\n""")

# Input Getter
def getInput():
    followers = None
    percent = None
    
    while not followers or not percent or not followers.isdigit() or not percent.isdigit():
        clearScreen()
        printName()

        followers = raw_input("Number of Followers: ")
        percent = raw_input("Percentage on Poll (ex: 25): ")
   
    returnInput = { "followers":followers, "percent": percent }

    return returnInput

########################
# Ensure correct usage #
########################

if len(sys.argv) != 3 and len(sys.argv) > 1:
    printName()
    print("______________________________")
    print("Usage:")
    print(sys.argv[0] + " <number_of_followers> <percentage>")
    print("\nWhere <number_of_followers> is the follower count of the "\
            +"author of the poll,")
    print("and <percentage> is ONE of the percentages shown"\
            +" on an Instagram Poll\n\n")
    sys.exit()

#########################
#     Get User Data     #  
#########################

followers = ""
percent = ""

if len(sys.argv) != 3:
    userInput = getInput() 
    followers = int(userInput['followers'])
    percent = int(userInput['percent'])
else:
    followers = int(sys.argv[1])
    percent = int(sys.argv[2])

VOTERS = followers

# Assume the more popular, the less loyal :)

if followers > 75:
    VOTERS = int(round(float(followers) * .2))

#########################
#   Initiation Output   #
#########################

clearScreen()
printName()
print("_________________________________________________________________________")
print("Followers: " + str(followers) \
      + " | Effective Voters: " + str(VOTERS) \
      + " | Given Percentage: " + str(percent))
print("_________________________________________________________________________")

print("Calculating Possibilities...")


########################
#   Calculate Results  #
########################

########################
#      Recursive       #
#  Possibility finder  #
########################

def findPossibilities(precision, minimum = 20000000, possible = []):
    if precision < -1:
        return possible

    totalPossibilities = []
    
    for total in range(1,VOTERS + 1):
        for voters in range(1, VOTERS + 1):
            
            result1 = int(round((float(voters) / float(total)) * 100,precision))
            result2 = int(round((float(total - voters) / float(total)) * 100,precision))

            if (result1 + result2) != 100 or result1 < 0 or result2 < 0:
                continue

            if result1 == percent:
                totalPossibilities.append({ 'total': total, 'low': voters, 'high': (total - voters)})
   
    length = len(totalPossibilities)

    if length > minimum or length == 0:
        return findPossibilities(precision - 1, minimum, possible)
    else:
        return findPossibilities(precision - 1, length, totalPossibilities)


result = json.loads(json.dumps(findPossibilities(5)))


########################
#    Output Results    #
########################

print("______________________________")
print("\nRESULTS:")

if len(result) > 0:
    print("Possible Number of Voters:\n")
    for entry in result:
        print("* "\
        + str(entry['total'])\
        + " Total Voters (" + str(entry['low'])\
        + "," + str(entry['high'])\
        + ")")
else:
    print("I can't seem to find any results with those numbers.")

print("______________________________\n")
