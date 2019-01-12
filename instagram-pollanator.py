#! /bin/python

##################################################

# ███████╗██╗     ███████╗███████╗██╗     ██╗     
# ██╔════╝██║     ██╔════╝██╔════╝██║     ██║     
# █████╗  ██║     ███████╗█████╗  ██║     ██║     
# ██╔══╝  ██║     ╚════██║██╔══╝  ██║     ██║     
# ███████╗███████╗███████║███████╗███████╗███████╗
# ╚══════╝╚══════╝╚══════╝╚══════╝╚══════╝╚══════╝

###################################################

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


########################
# Ensure correct usage #
########################

if len(sys.argv) < 3:
    print("\nInstagram Pollanator")
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

# Calculate the approximate number of votes
# given the number of followers 

followers = int(sys.argv[1])
VOTERS = followers

# Assume the more popular, the less loyal :)

if followers > 75:
    VOTERS = int(round(float(followers) * .2))

# Get one of the percentages shown by Instagram

percent = int(sys.argv[2])


#########################
#   Initiation Output   #
#########################

clearScreen()
print("INSTAGRAM POLL VOTE CALCULATOR")
print("______________________________")
print("Followers:         " + str(followers))
print("Calculated Voters: " + str(VOTERS))
print("Given Percentage:  " + str(percent))
print("______________________________")

print("\nCalculating Possibilities...")


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

            if (result1 + result2) != 100:
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
print("Possible Number of Voters:\n")

for entry in result:
    print("* "\
    + str(entry['total'])\
    + " Total Voters (" + str(entry['low'])\
    + "," + str(entry['high'])\
    + ")")
print("______________________________\n")
