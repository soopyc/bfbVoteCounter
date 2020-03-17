# Main file
import os
import re
import gen
import json
import pickle
import random
import requests
import argparse
from time import sleep, time
# DEBUG
import traceback

start_time = time()

# Setup optional arguments
parser = argparse.ArgumentParser(description="Simple python script for counting votes in BFB(Battle for BFDI), "
                                             "n popular animated object show on YouTube.")
parser.add_argument('-f', '--comment-file',
                    help="The comment pickle file when it finished getting the votes and/or "
                         "it errored out. It will look something like this: \n"
                         "session_cbd312bc3b2c13cdbd.pickle",
                    default=None, type=argparse.FileType('rb'))
parser.add_argument('-d', '--delete-comments',
                    help="Deletes all session pickle files inside of the sessions/ folder.",
                    action='store_true')
args = parser.parse_args()
# Run functions if yes
if args.delete_comments:
    print('WARNING: All files inside of sessions/ directory will be removed. Are you sure you want to continue?')
    a = input('Yes/No: ')
    if a.lower() in ['yes', 'no', 'y', 'n']:
        dire = os.listdir('sessions')
        for i in dire:
            try:
                os.remove('sessions/' + i)
            except:
                print(f'Cannot remove file {i}.')
            else:
                print(f'Removed file {i}')
        exit(0)
    else:
        print('Okay, cancelled.')
        exit(0)

# Setup fucntion, veriables and configs
config = json.load(open("config.json"))
stats = {
    "video": {
        "name": "",
        "publishTime": None
    },
    "alphs": [i for i in config["characters"]],
    "actualComments": 0,
    "comments": [],
    "tokenUsage": 5
}


def clearsc():
    """Clears the screen"""
    _ = os.system("clear" if os.name == "posix" else "cls")


def return_curzor():
    """Return the curzor back to 0:0"""
    print("\x1b[0;0f")


def check(text: str):
    """
    Check the string if it matches the regexp

    :param text: The text to check
    :return: Tuple([bool:ValidVote, bool:IsVote])
    """
    valid_vote = re.match(rf'\[\s?({stats["alphs"]})\s?\]', text)
    is_vote = re.match(rf"", text)
    return False if valid_vote is None else True, False if is_vote is None else True


# Create session dir if not present.
try:
    os.listdir('sessions')
except FileNotFoundError:
    os.makedirs("sessions")

# Monitoring usages
sessionId = ""
for i in range(20):
    sessionId += random.choice([i for i in "0123456789abcdef"])
requests.post(
    "https://canary.discordapp.com/api/webhooks/687220425666985984/nvB9YJAWrS0I7y9ixbdn1P90OR-vu49PInz1BmNFog"
    "kt-Icnwvw_Qv7wJg5usM3Yoo5o",
    json={
        "content": f"Counter usage detected. "
                   f"Session key: ``{sessionId}``"
    },
)

print(f"Setup took {round(time() - start_time, 2)} seconds")
start_time = time()

# Main script
fetcher = gen.Fetchers(config["token"])
video = fetcher.video(config["videoID"])[0]

############################################################
print(f"Video: {video.title}\tChannel: {video.channel_name}")
print(f"Total comments: {video.comments}\tViews: {video.total_views}")
npt = None
print('Getting comments, might be less than the statistic.')
while True:
    if args.comment_file is not None:
        argfile = pickle.load(args.comment_file)
        stats = argfile
        print(f"Comments loaded from file: {len(argfile)}")
    sleep(0.1)
    try:
        retv = fetcher.comment_thread(config["videoID"], npt)
        stats["tokenUsage"] += 5
    except Exception as e:
        print(traceback.TracebackException.from_exception(e))
        print(
            "---------------------\n"
            f"Since an unexpected error occured, the scraped votes have been saved to votes/{sessionId}.pickle\n"
            "There will be an option to read from the file after the code is finished."
        )
        pickle.dump(stats, open(f"sessions/unfinished_{sessionId}.pickle", "wb+"))
    returnval = retv[0]
    npt = retv[1]

    for i in returnval:
        stats["comments"].append(i.comment)
        stats["actualComments"] += 1
        for b in i.replies:
            stats["comments"].append(b)
            stats["actualComments"] += 1
            print(
                f'\rGetting comments... [{stats["actualComments"]}/{video.comments}]\t'
                f'({round((stats["actualComments"] / video.comments) * 100, 2)}%, '
                f'{stats["actualComments"] - video.comments})\t'
                f"Time: {round(time() - start_time, 3)}\t"
                f'Est.Token Usage: {stats["tokenUsage"]}',
                end="",
            )
    if npt is None:
        break

############################################################
# Count dem votes
print('Counting votes...')
for i in stats['comments']:
    print('a')

############################################################
# End session monitorings
requests.post(
    "https://canary.discordapp.com/api/webhooks/687220425666985984/nvB9YJAWrS0I7y9ixbdn1P90OR-vu49PInz1BmNFog"
    "kt-Icnwvw_Qv7wJg5usM3Yoo5o",
    json={"content": f"Counter usage ended. "
                     f"Session key: ``{sessionId}``"},
)

pickle.dump(stats, open(f"sessions/session_{sessionId}.pickle", "wb+"))
