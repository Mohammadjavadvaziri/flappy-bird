import sqlite3

con = sqlite3.connect("Database/Database.db")
cur = con.cursor()
get_score = cur.execute("SELECT * FROM score")


def get_best_score():
    scoreList = []

    for score_tuple in cur.execute("SELECT * FROM score"):
        for score in score_tuple:
            scoreList.append(int(score))
    return max(scoreList)


def insert_score(score):
    cur.execute(f"INSERT INTO score(score) values ('{score}') ")



