import pandas as pd
import os

def is_leaderboard_exist():
    return os.path.exists('Leaderboard.xlsx')

def createLeaderBoardFile():
    data = {"username": [], "score": []}
    df = pd.DataFrame(data)
    df.to_excel('Leaderboard.xlsx', sheet_name='sheet0', index=False)

def update_leaderboard(username,score):
    if not is_leaderboard_exist():
        createLeaderBoardFile()
    df = pd.read_excel('Leaderboard.xlsx', sheet_name='sheet0')
    username_list = list(df['username'].values)
    if username in username_list:
        i = username_list.index(username)
        df.loc[i, 'score'] = df.loc[i, 'score'] + score
    else:
        i = len(username_list)
        df.loc[i] = [username, score]
    df.to_excel('Leaderboard.xlsx', sheet_name='sheet0', index=False)

def show_leaderboard():
    if not is_leaderboard_exist():
        return ""
    df = pd.read_excel('Leaderboard.xlsx', sheet_name='sheet0')
    score_record = []
    for i in range(df.shape[0]):
        score_record.append(tuple(df.loc[i].values))
    leaderboard = sorted(score_record, key=lambda x: x[1], reverse=True)
    # print(leaderboard)       [('GA', 1000), ('TEST', 999), ('ga', 88), ('a', 9), ('a', 9), ('a', 8), ('a', 7)]
    res = "{:^10s}".format('RANK')  + "{:^15s}".format('USER') + "{:^15s}".format('SCORE') + "\n"
    print(res, end="") 
    rank=0
    for i in leaderboard:  
        rank = rank + 1
        print("{:^10d}".format(rank),"{:^15s}".format(i[0]),"{:^15f}".format(i[1]))
        res = res + "{:^10d}".format(rank) + " " + "{:^15s}".format(i[0]) + " " + "{:^15f}".format(i[1]) + "\n"
    return res
