import requests
import os
import json
import config_michelle
# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = config_michelle.bearer_token

import sqlite3
import csv
import time
import sys

#client = tweepy.Client(
#    consumer_key=consumer_key, consumer_secret=consumer_secret,
#    access_token=access_token, access_token_secret=access_token_secret
#)


def creat_userid_url(user_name):
    url = 'https://api.twitter.com/2/users/by/username/{}'.format(user_name)
    print(url)
    return url
    

def create_url(user_id, pagination=None):
    if pagination is not None:
        url = "https://api.twitter.com/2/users/{}/following?max_results=1000&pagination_token={}".format(user_id, pagination)
    else:
        url = "https://api.twitter.com/2/users/{}/following?max_results=1000".format(user_id)

    print(url)
    return url
        


def get_params():
    return {"user.fields": "created_at"}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowingLookupPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        #raise Exception(
        #    "Request returned an error: {} {}".format(
        #        response.status_code, response.text
        #    )
        #)
        print("Request returned an error: {} {}".format(
                response.status_code, response.text
        ))
        wait_time = 444
        print('sleeping for {} seconds'.format(wait_time))
        time.sleep(wait_time)

        return None

    return response.json()



def get_following_list(user_id):
    following = []
    (friends_page, next_token) = get_following_list_inner(user_id, None)
    following.extend(friends_page)

    # get next results in pagination
    count = 0
    while (next_token and count < 5):
        (friends_page, next_token) = get_following_list_inner(user_id, next_token)
        following.extend(friends_page)
        count = count + 1

    return following

   
def get_following_list_inner(user_id, next_token):

    friends_page = []    

    url = create_url(user_id, next_token)
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    if json_response is not None:
        print(json_response)
        user_data = json_response['data']
        meta = json_response['meta']

    for user_dict in user_data:
        friends_page.append(user_dict['username'])

    next_token = None
    if 'next_token' in meta:
        next_token = meta['next_token']

    return(friends_page, next_token)

    
def get_id_from_name(user_name):
    url = creat_userid_url(user_name)
    params = get_params()
    json_response = connect_to_endpoint(url, params)

    if json_response is None:
        print("id not found!")
        return None
    else:
        id = json_response['data']['id']
        return id


def get_distinct_db_users(cur):
    q = "select distinct(twitter_name) from Following"
    users_in_db = []
    try:
        cur.execute("SELECT distinct twitter_name  FROM Following")
        rows = cur.fetchall()
        users_in_db = [i[0].decode('utf-8') for i in rows]
    except sqlite3.Error as my_error:
        print("error: ",my_error)

    return users_in_db


def connect_to_db(db_name):
    #create news database
    conn = sqlite3.connect(db_name)
    conn.text_factory = bytes
    cur = conn.cursor()
    
    return (cur, conn)


def create_table():
    try:
        cur.executescript('''
    CREATE TABLE Following (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        writer    TEXT, 
        twitter_name    TEXT UNIQUE,
        num_followers    TEXT,
        gender    TEXT, 
        url    TEXT, 
        location    TEXT, 
        num_following    TEXT, 
        following TEXT
    );
    ''')
    except:
        print("database already exists")

    #print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":

    infile = "combined_journos_2022b.csv"
    writer_data = open(infile)
    csv_reader = csv.reader(writer_data)
    csv.field_size_limit(sys.maxsize)
    db_name = 'following.sqlite'
    (cur, conn) = connect_to_db(db_name)
#    users_in_db = get_distinct_db_users(cur)

    for row in csv_reader:
        users_in_db = get_distinct_db_users(cur)
        
        new_row = {}
        new_row["writer"] = row[0]
        new_row["twitter_name"] = row[1]
        new_row["num_followers"] = row[2]
        new_row["gender"] = row[3]
        new_row["url"] = row[4]
        new_row["location"] = row[5]
        
        if new_row["twitter_name"] in users_in_db:
            print("user {} already processed - exists already".format(new_row["twitter_name"]))
            continue
        else:
            username = new_row["twitter_name"]
            print(username)
            ids = []

            try: 
                user_id = get_id_from_name(username)
                print("found user_id = {}".format(user_id))
                following = []
                following = get_following_list(user_id)
            except:
                print("user not found")
                new_row["following"] = ''
                # need retry mechanism - or just skip it
                continue

            print('--------')
            print(len(following))

            new_row["num_following"] = len(following)
            new_row["following"] = ":".join(following)
            print(new_row["following"])

            cur.execute('''INSERT OR REPLACE INTO Following
                (writer, twitter_name, num_followers, gender, url, location, num_following, following) 
                VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)''', 
                ( new_row['writer'], new_row['twitter_name'], new_row['num_followers'], new_row['gender'],
                    new_row['url'], new_row['location'],
                    new_row['num_following'], new_row['following'] ) )
            conn.commit()

            




# need method to
# 1 parse usernames
# get pagination token
# keep going if token is not none
# return list
