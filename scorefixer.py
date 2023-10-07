# If you were using this bot before October 2023 run this py to keep your scores (changed to saving them as lower case)

import os
import pickle
import time

scoreboard = {}

def load_scores():
    global scoreboard
    global DUCKLINES_TARGET
    if os.path.getsize('duckhunt.pkl') > 0:
        with open('duckhunt.pkl', 'rb') as fp:
            scoreboard = pickle.load(fp)
    if "ducklines" in scoreboard:
        DUCKLINES_TARGET = scoreboard["ducklines"]
    if "MISS_CHANCE" in scoreboard:
        MISS_CHANCE = scoreboard["MISS_CHANCE"]
    if "stats" not in scoreboard:
        scoreboard["stats"] = {}
        scoreboard["stats"]["totalmissed"] = 0
        scoreboard["stats"]["!bangmissed"] = 0
        scoreboard["stats"]["!befmissed"] = 0
        scoreboard["stats"]["total!bang"] = 0
        scoreboard["stats"]["total!bef"] = 0
        save_scores()
        time.sleep(1)
    print("Scores loaded!")
    print(scoreboard)


load_scores()

scoreboard["real_nicks"] = {}
x = scoreboard["!bang"]
y = scoreboard["!bef"]
scoreboard["stats"] = {}
print(x)
print("-")
print(y)
print("-")
for i in x.copy():
    score = x[i]
    x.pop(i)
    x[i.lower()] = score
    print(i, ":", score)
    print(i.lower(), ":", x[i.lower()])
    scoreboard["real_nicks"][i.lower()] = i
    print(i.lower(), "real_nicks ->", scoreboard["real_nicks"][i.lower()])
print("-")

for i in y.copy():
    score = y[i]
    y.pop(i)
    y[i.lower()] = score
    print(i, ":", score)
    print(i.lower(), ":", y[i.lower()])
    scoreboard["real_nicks"][i.lower()] = i
    print(i.lower(), "real_nicks ->", scoreboard["real_nicks"][i.lower()])

print(scoreboard["!bang"])
print("-")
print(scoreboard["!bef"])
print("-")
print(scoreboard["real_nicks"])

def save_scores():
    global scoreboard
    with open('duckhunt.pkl', 'wb') as fp:
        pickle.dump(scoreboard, fp)

save_scores()
time.sleep(2)
scoreboard = {}
load_scores()
