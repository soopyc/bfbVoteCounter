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
from colorama import init, Fore
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
    print(Fore.YELLOW+'WARNING: All files inside of sessions/ directory will be removed. '
                      'Are you sure you want to continue?')
    a = input('Yes/No: ')
    if a.lower() in ['yes', 'y']:
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
        print(Fore.GREEN+'Okay, cancelled.')
        exit(0)

# Setup fucntion, veriables and configs
config = json.load(open("config.json"))
stats = {
    "video": {
        "name": "",
        "publishTime": None,
        "obj": None
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


def sayfill(text: str):
    """
    Print a string of text and filling the gap

    :param text: The string text for testing
    :return: None
    """
    col, _ = tuple(os.get_terminal_size())
    print(text+''.join([' ' for _ in range(col-len(text)-1)]))


def genbr():
    """
    Generate a line break thingy full of ---------

    :return: None
    """
    col, _ = tuple(os.get_terminal_size())
    sayfill(''.join(['-' for _ in range(cols - 1)]))


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
if args.comment_file is None:
    video = fetcher.video(config["videoID"])[0]
    stats['video']['obj'] = video
    print('Getting comments, might be less than the statistic.')
    stats['video']['name'] = video.title
    stats['video']['publishTime'] = video.publish_time
else:
    stats = pickle.load(args.comment_file)
    video = stats['video']['obj']
    print(f"Comments loaded from file: {len(stats['comments'])}")
############################################################
print(f"Video: {video.title}\tChannel: {video.channel_name}")
print(f"Total comments: {video.comments}\tViews: {video.total_views}")
npt = None
while True:
    if args.comment_file is not None:
        break
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
sleep(5)
clearsc()
print('Counting votes...')
count = 1
t = time()
for i in stats['comments']:
    cols, rows = tuple(os.get_terminal_size())
    genbr()
    sayfill(f'Comment {count} of {len(stats["comments"])}')
    sayfill(f'Comment Author: {i.author}')
    sayfill(f'Comment time: {i.published_at.strftime("%Y/%m/%d %H:%M:%S UTC")}')
    sayfill(f'Comment content: '
            f'{i.text[0:cols-20]+f"...({len(i.text)-cols-20} characters left)" if len(i.text) > cols-19 else i.text}')
    sayfill(f'Elapsed time: {round(time()-t, 3)}s')
    genbr()
    for _ in range(5):  # was rows-11
        sayfill('')
    # clearsc()
    return_curzor()
    count += 1


############################################################
# End session monitorings
requests.post(
    "https://canary.discordapp.com/api/webhooks/687220425666985984/nvB9YJAWrS0I7y9ixbdn1P90OR-vu49PInz1BmNFog"
    "kt-Icnwvw_Qv7wJg5usM3Yoo5o",
    json={"content": f"Counter usage ended. "
                     f"Session key: ``{sessionId}``"},
)

pickle.dump(stats, open(f"sessions/session_{sessionId}.pickle", "wb+"))
