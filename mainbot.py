import base64
from github import Github
from pprint import pprint
import json
import datetime
import os
import random

import tweepy


TEST = [    ['air-mouse', datetime.datetime(2023, 1, 21, 17, 53, 20)], 
            ['AI_Club_20-21-main', datetime.datetime(2021, 7, 19, 5, 44, 16)], 
            ['Ardunio_stuff', datetime.datetime(2020, 9, 4, 3, 31, 56)], 
            ['audio-lights', datetime.datetime(2023, 2, 1, 4, 52, 28)], 
            ['chess-board', datetime.datetime(2023, 3, 3, 5, 45, 5)], 
            ['curtains', datetime.datetime(2023, 2, 12, 1, 53, 39)], 
            ['Fiala', datetime.datetime(2022, 12, 8, 2, 56, 12)], 
            ['final_project', datetime.datetime(2023, 3, 29, 2, 16, 10)], 
            ['google-calendar-command-line', datetime.datetime(2023, 2, 3, 5, 25, 1)], 
            ['hackathon', datetime.datetime(2022, 10, 16, 17, 25, 54)], 
            ['Home-movie-streamer', datetime.datetime(2023, 1, 6, 3, 56, 5)], 
            ['kevintheepicguy.github.io', datetime.datetime(2023, 4, 9, 23, 1, 14)], 
            ['mario-Game-remake', datetime.datetime(2022, 3, 12, 6, 35, 8)], 
            ['mario-remake', datetime.datetime(2022, 6, 16, 22, 5, 9)], 
            ['midi_tocuh_sensor', datetime.datetime(2022, 4, 12, 3, 39, 1)], 
            ['muscle_music', datetime.datetime(2020, 12, 19, 5, 58, 38)], 
            ['robot', datetime.datetime(2020, 12, 19, 6, 6, 37)], 
            ['seven-segment-clock', datetime.datetime(2023, 2, 1, 4, 48, 57)], 
            ['start_up_scripts', datetime.datetime(2020, 12, 19, 6, 8, 24)], 
            ['text_summary', datetime.datetime(2020, 12, 19, 6, 13, 8)], 
            ['todo', datetime.datetime(2022, 10, 26, 2, 39, 1)], 
            ['website', datetime.datetime(2020, 12, 19, 6, 16, 17)]
       ]




username = "kevintheepicguy"
# pygithub object
g = Github("kevintheepivguy", "KEvin4321")

# get that user by username
user = g.get_user(username)

all_repos_with_time= []
prev_repos_with_time = []
#all_repos_with_time= TEST

new_repo_added = []

githublink = "https://github.com/kevintheepicguy"

def append_repos_to_main_list(repo):

    # strip the username out 
    repo_name = repo.full_name[16:]

    last_push = repo.pushed_at

    data = [repo_name, last_push]
    all_repos_with_time.append(data)
    

def load_prev_data():
    # read from file and load into all_repos_with_time
    with open("/home/kevin/storage/twiterbot/scr.txt", mode='r') as file:
        lines = file.readlines()
        for line in lines:
            temp_data = line.split(',') #split the data
            temp_data[1] = temp_data[1].strip() # remove newline char
            prev_repos_with_time.append(temp_data) # append data to main list

def clear_data_in_file():
    os.remove("/home/kevin/storage/twiterbot/scr.txt")


def write_data_to_file():
    clear_data_in_file()
    with open("/home/kevin/storage/twiterbot/scr.txt", mode='w') as file:
        for repo in all_repos_with_time:
            file.write('%s,%s\n' % (repo[0], repo[1]))

def update_lists():
    knwon_repos = []
    for repo in all_repos_with_time:
        for x in range(len(prev_repos_with_time)):
            if (repo[0] == prev_repos_with_time[x][0]):
                knwon_repos.append(repo[0])
        if (repo[0] not in knwon_repos):
            send_tweet(repo)
                
def send_tweet(data):
    repo = data[0]
    
    if (repo == "kevintheepicguy.github.io"):
        real_repo_name = repo
        repo = "my personal Website"
    
    tweet_mesages = [
    f"Big news! 📣 Just pushed a major update to {repo}, featuring improved functionality and smoother user experience. Check it out and let me know your thoughts! {githublink}/{data[0]} #opensource #coding #development",
    f"🎉 It's finally here! My most recent update includes highly-requested features and optimizations that I am excited to share with the community! {githublink}/{data[0]} #opensource #development #coding",
    f"Big news! 🎉 Just pushed a new update to {repo} with some major improvements. Can't wait for you to try it out! {githublink}/{data[0]} #opensource #coding #development",  
    f"As always, feedback and contributions are welcome. Let me know what you think of the new update and how I can make it even better. Happy coding! {githublink}/{data[0]} #feedback #contribution #opensource",
    f"🎉 Exciting news! The latest update to {repo} is now live. It includes a ton of new features and improvements to make your experience even better. Check it out today! {githublink}/{data[0]} #opensource #development #coding",
    f"💻 Attention developers! I just released a new update to {repo} that includes some major improvements and bug fixes. Check it out for a smoother experience! {githublink}/{data[0]} #opensource #development #coding"
    ]

    if(repo == "my personal Website"):
        repo = real_repo_name

    msg = random.choice(tweet_mesages)
    while (len(msg) > 280 ):
        # msg too long pick a new one
        print("too long. picking a new one")
        msg = random.choice(tweet_mesages)

    # personal details
    consumer_key ="REPLACEME"
    consumer_secret ="REPLACEME"
    access_token ="REPLACEME"
    access_token_secret ="REPLACEME"


    client = tweepy.Client(consumer_key=consumer_key,
                        consumer_secret=consumer_secret,
                        access_token=access_token,
                        access_token_secret=access_token_secret)

    # Replace the text with whatever you want to Tweet about
    response = client.create_tweet(text=msg)




def compare_repo_times():
    if (len(prev_repos_with_time) == len(all_repos_with_time)):
        for repo_index in range(len(all_repos_with_time)):
            prev_time = datetime.datetime.strptime(prev_repos_with_time[repo_index][1], '%Y-%m-%d %H:%M:%S')
            if(prev_time < all_repos_with_time[repo_index][1]):
                print("sending twiter update")
                send_tweet(all_repos_with_time[repo_index])
    else:
        new_repo_added = update_lists() 
        # send_tweet(new_repo_added)
        print("send the new tweeit")



if (__name__ == '__main__'):

    for repo in user.get_repos():
        append_repos_to_main_list(repo)
    
    load_prev_data()
    compare_repo_times()
    write_data_to_file()
