#!/usr/bin/env python3
import psycopg2
import sys
import datetime


def connect(db="news"):
    # Connects to PostgreSQL database
    try:
        global conn, cur
        conn = psycopg2.connect("dbname={}".format(db))
        cur = conn.cursor()
    except:
        # Prints error, plays an error sound
        print("Couldn't connect to PostgreSQL database \"{}\".\a".format(db))
        # Stops program
        sys.exit()

# First question


def top_articles(top=3):
    # Sends SQL query for top articles by views
    cur.execute("""
    select title, count(*) as views
        from articles, log
        where substr(log.path, 10) = articles.slug
        group by articles.title
        order by views desc
        limit {};
    """.format(top))
    results = ["\nWhat are the most popular three articles of all time?"]
    for i in cur.fetchall():
        results.append("\t\"{}\" - {} views".format(i[0], i[1]))
    return "\n".join(results)

# Second question


def top_authors():
    # Sends SQL query for top authors by their article views
    cur.execute("""
    select name, count(*) as views
        from authors, log, articles
        where substr(log.path, 10) = articles.slug
        and articles.author = authors.id
        group by authors.name
        order by views desc;
    """)
    results = ["\nWho are the most popular article authors of all time?"]
    for i in cur.fetchall():
        results.append("\t{} - {} views".format(i[0], i[1]))
    return "\n".join(results)

# Third question


def worst_days(percent=1):
    # Sends SQL query for days when more than x% of requests resulted in errors
    cur.execute("""
    select errors, requests, errors.day,
    round(errors * 100.0 / requests, 1) as percentage
        from
        (select date(time) as day,
            count(*) as errors
            from log
            where log.status != '200 OK'
            group by day)
        errors,
        (select date(time) as day,
            count(*) as requests
            from log
            group by day)
        requests
        where round(errors * 100.0 / requests, 1) > 1
        and errors.day = requests.day;
    """.format(str(percent)))
    results = ["\nOn which days did more than 1% of requests lead to errors?"]
    for i in cur.fetchall():
        results.append(
            "\t{} - {}% errors".format(i[2].strftime("%B %-d, %Y"), i[3])
            )
    return "\n".join(results)

if __name__ == "__main__":
    connect()
    print(top_articles())
    print(top_authors())
    print(worst_days())
    conn.close()
