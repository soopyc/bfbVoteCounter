# Main file
import argparse
import json
import os
import pickle
import random
import re
import sys
import traceback
from time import sleep
from time import time

import requests
from colorama import Cursor
from colorama import Fore
from colorama import init
from colorama import Style

import gen
# DEBUG

version = ("0.", "1-alpha.", "3")
init(autoreset=True)


# noinspection PyTypeChecker
def main():
    # Setup optional arguments
    start_time = time()
    parser = argparse.ArgumentParser(
        description="Simple python script for counting votes in BFB(Battle for BFDI), "
        "a popular animated object show on YouTube."
    )
    parser.add_argument(
        "-f",
        "--comment-file",
        help="The comment pickle file when it finished getting the votes and/or "
        "it errored out. It will look something like this: \n"
        "session_cbd312bc3b2c13cdbd.pickle",
        default=None,
        type=argparse.FileType("rb"),
    )
    parser.add_argument(
        "-d",
        "--delete-comments",
        help="Deletes all session pickle files inside of the sessions/ folder.",
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--config-file",
        help="The configuration json file for the counter. Defaults to config.json",
        default=open("config.json", "r"),
        type=argparse.FileType("r"),
    )
    args = parser.parse_args()
    # Run functions if yes
    if args.delete_comments:
        print(
            Fore.YELLOW
            + "WARNING: All files inside of sessions/ directory will be removed. "
            "Are you sure you want to continue?"
        )
        a = input("Yes/No: ")
        if a.lower() in ["yes", "y"]:
            dire = os.listdir("sessions")
            for i in dire:
                try:
                    os.remove("sessions/" + i)
                except:
                    print(f"Cannot remove file {i}.")
                else:
                    print(f"Removed file {i}")
            sys.exit(0)
        else:
            print(Fore.GREEN + "Okay, cancelled.")
            sys.exit(0)

    # Setup fucntion, veriables and configs
    config = json.load(args.config_file)
    stats = {
        "video": {"name": "", "publishTime": None, "publishTStamp": None, "obj": None},
        "votes": {
            "total": 0,
            "valid": 0,
            "invalid": 0,
            "deadlined": 0,
            "shinyvotes": 0,
            "voters": [],
            "shinies": {},
            "characters": {},
        },
        "alphs": [i for i in config["characters"]],
        "actualComments": 0,
        "comments": [],
        "tokenUsage": 5,
    }

    def clearsc():
        """Clears the screen"""
        # _ = os.system("clear" if os.name == "posix" else "cls")
        print("\x1b[2J")

    def return_curzor():
        """Return the curzor back to 0:0"""
        print(Cursor.POS())

    def check(text: str):
        """
        Check the string if it matches the regexp

        :param text: The text to check
        :return: Tuple([bool:ValidVote, bool:IsVote])
        """
        valid_vote = re.match(
            rf'\[({stats["alphs"]})\]', text
        )  # Check if the format is correct and the letter is ok
        is_vote = re.match(r"\[\w\]", text)
        return False if valid_vote is None else True, False if is_vote is None else True

    def return_vote_item(text: str, alphs: list):
        """
        Pass in the vote and it will return a list of items matching the vote regex

        :param text: the text to check for the strings
        :param alphs: list of alphabets used for voting
        :return: list([str])
        """
        text = text.lower()
        return re.findall(fr"\[({alphs})\]", text)

    def sayfill(text: str):
        """
        Print a string of text and filling the gap.
        Should be flushprint but idc

        :param text: The string text for filling
        :return: None
        """
        # try:
        #     col, _ = tuple(os.get_terminal_size())
        # except OSError:
        #     col = 70
        # print(text + ''.join([' ' for _ in range(col - len(text) - 1)]))  # add '\x1b[0K'+ on top if breaking
        print("\x1b[0K" + text)

    def genbr():
        """
        Generate a line break thingy full of ---------

        :return: None
        """
        try:
            col, _ = tuple(os.get_terminal_size())
        except OSError:
            col = 70
        sayfill("".join("-" for _ in range(col - 1)))

    def check_time(oldt: int, newt: int, deadline: int = 172800):
        """
        Check and output a rewturn funcnfndsfddfdsfdsf
        :param oldt: Old/publish timestamp
        :param newt: New/comment publish timestamp
        :param deadline: Seconds till deadline
        :return: better thing idk
        """
        if oldt + deadline > newt:
            return f"{Fore.GREEN}[ON TIME]"
        else:
            return f"{Fore.YELLOW}[DEADLINED]"

    # Create session dir if not present.
    try:
        os.listdir("sessions")
    except FileNotFoundError:
        os.makedirs("sessions")

    print("Counter v%s.%s.%s" % version)
    # Monitoring usages
    session_id = ""
    for i in range(20):
        session_id += random.choice([i for i in "0123456789abcdef"])
    requests.post(
        "https://canary.discordapp.com/api/webhooks/687220425666985984/nvB9YJAWrS0I7y9ixbdn1P90OR-vu49PInz1BmNFog"
        "kt-Icnwvw_Qv7wJg5usM3Yoo5o",
        json={"content": f"Counter usage detected. " f"Session key: ``{session_id}``"},
    )

    print(f"Setup took {round(time() - start_time, 2)} seconds")
    start_time = time()

    # Main script
    fetcher = gen.Fetchers(config["token"])
    if args.comment_file is None:
        video = fetcher.video(config["videoID"])[0]
        stats["video"]["obj"] = video
        print("Getting comments, might be less than the statistic.")
        stats["video"]["name"] = video.title
        stats["video"]["publishTime"] = video.publish_time
        stats["video"]["publishTStamp"] = video.publish_time.timestamp()
        stats["config"] = config
        # Set character voting items
        for i in config["characters"]:
            stats["votes"]["characters"][i] = {
                "name": "",
                "total": 0,
                "valid": 0,
                "shiny": 0,
                "deadlined": 0,
            }
            stats["votes"]["characters"][i]["name"] = config["characters"][i]
    else:
        stats = pickle.load(args.comment_file)
        video = stats["video"]["obj"]
        config = stats["config"]
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
                f"Since an unexpected error occured, the scraped votes have been saved to votes/{session_id}.pickle\n"
                "There will be an option to read from the file after the code is finished."
            )
            pickle.dump(stats, open(f"sessions/unfinished_{session_id}.pickle", "wb+"))
        # noinspection PyUnboundLocalVariable
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
    # Save the file.
    pickle.dump(stats, open(f"sessions/session_{session_id}.pickle", "wb+"))
    ############################################################
    # Count dem votes
    sleep(5)
    clearsc()
    print("Counting votes...")
    count = 1
    t = time()
    for i in stats["comments"]:
        if count > 1000 and str(count)[-3::] == "000":
            return_curzor()
            # clearsc()
            # try:
            #     cols, rows = tuple(os.get_terminal_size())
            # except OSError:
            #     cols, rows = 70, 16
            genbr()
            sayfill("Counter v%s%s%s" % version)
            sayfill(
                f'Comment {count} of {len(stats["comments"])} [{round((count / len(stats["comments"]) * 100), 3)}%]'
            )
            sayfill(f"Elapsed time: {round(time() - t, 3)}s")
        count += 1  # add one to the counter, woo hoo!
        vote_alph = return_vote_item(i.text.lower(), stats["votes"]["alphs"])
        vote = vote_alph[-1]
        if stats["video"]["publishTStamp"] + 172800 < i.published_at.timestamp():
            stats["votes"]["deadlined"] += 1  # Deadlined vote doesn't count.
            if len(vote_alph) != 0 and vote in config["alphs"]:
                # Add 1 to the deadline count for the character
                stats["votes"]["characters"][vote]["deadlined"] += 1
                # Add 1 to the character's total vote count.
                stats["votes"]["characters"][vote]["total"] += 1
            continue
        elif not check(i.text.lower())[0]:
            if check(i.text.lower())[1]:
                # Check: (isValid, isVote)
                stats["votes"]["total"] += 1
                # Is a vote, but doesn't match with a char.
                stats["votes"]["invalid"] += 1
                # Doesn't worth checking and adding to the vote thingy
            continue
        elif i.author in stats["votes"]["voters"]:
            # User voted once. Shiny.
            if i.author not in stats["votes"]["shinies"]:
                stats["votes"]["shinies"][i.author] = 0
            # Still add 1 to the vote counter bc hey its valid so why not
            stats["votes"]["total"] += 1
            # Add 1 to user's shiny count
            stats["votes"]["shinies"][i.author] += 1
            stats["votes"]["shinyvotes"] += 1  # Add 1 to the global counter
            # Add 1 to the character's shiny vote counts.
            stats["votes"]["characters"][vote]["shiny"] += 1
            # Add 1 to the character's total vote count.
            stats["votes"]["characters"][vote]["total"] += 1
            continue
        else:
            stats["votes"]["voters"].append(i.author)
            # Add 1 to the character's total vote count.
            stats["votes"]["characters"][vote]["total"] += 1
            # Add 1 to the character's valid vote count.
            stats["votes"]["characters"][vote]["valid"] += 1
            stats["votes"]["total"] += 1
            stats["votes"]["valid"] += 1

        # Display the votes when the count is a multiple of 1000 to avoid lag
        if count > 1000 and str(count)[-3::] == "000":
            sayfill(
                f"Comment stats: "
                # check_deadline
                f'{check_time(stats["video"]["publishTime"].timestamp(), i.published_at.timestamp(), config["deadline"])}\t'
                f'{Fore.YELLOW + "[FORMAT_OK]" + Style.RESET_ALL if check(i.text.lower())[1] else Fore.RED + "[INVALID]"}\t'
                f'{Fore.GREEN + "[TEXT_OK]" + Style.RESET_ALL if check(i.text.lower())[0] else Fore.RED + "[TEXT_NOK]"}'
            )
            sayfill(f"Comment Author: {i.author}")
            sayfill(f'Comment time: {i.published_at.strftime("%Y/%m/%d %H:%M:%S UTC")}')
            genbr()
            sayfill(f'Total Votes: {stats["votes"]["total"]}')
            sayfill(f'Valid Votes: {stats["votes"]["valid"]}')
            sayfill(f'Invalid Votes: {stats["votes"]["invalid"]}')
            sayfill(f'Deadlined Comments: {stats["votes"]["deadlined"]}')
            sayfill(f'Shiny Coward Votes: {stats["votes"]["shinyvotes"]}')
            # sayfill(f'Comment content: '
            #         f'{i.text[0:cols - 20] + f"...({len(i.text) - cols - 20} characters left)" if len(i.text) > cols - 19 else i.text}')
            genbr()
            # for _ in range(5):  # was rows-11
            #     sayfill('')

    # Finish counting votes, displaying results.
    clearsc()
    genbr()
    sayfill(f'Total Votes: {stats["votes"]["total"]}')
    sayfill(f'Valid Votes: {stats["votes"]["valid"]}')
    sayfill(f'Invalid Votes: {stats["votes"]["invalid"]}')
    sayfill(f'Deadlined Comments: {stats["votes"]["deadlined"]}')
    sayfill(f'Shiny Coward Votes: {stats["votes"]["shinyvotes"]}')
    # Sort the shinies
    shinies_sorted = sorted(
        stats["votes"]["shinies"].items(), key=lambda kev: (kev[1], kev[0])
    )
    sayfill(
        f"The shiniest coward: {shinies_sorted[-1][0]} ({shinies_sorted[-1][1]} votes)"
    )
    genbr()
    sayfill("CHARACTERS")
    fchar = stats["votes"]["characters"]  # (UNOFFICIAL) Final character count
    for i in fchar:
        sayfill(
            f"{fchar[i]}\t"
            f'{Fore.WHI:{fchar[i]["total"]}\t}'
            f'{Fore.GREEN}Valid:{fchar[i]["valid"]}\t'
            f'{Fore.YELLOW}Shiny:{fchar[i]["shiny"]}\t'
            f'{Fore.RED}Dead.L:{fchar[i]["deadlined"]}\t'
        )
    ############################################################
    # End session monitorings
    requests.post(
        "https://canary.discordapp.com/api/webhooks/687220425666985984/nvB9YJAWrS0I7y9ixbdn1P90OR-vu49PInz1BmNFog"
        "kt-Icnwvw_Qv7wJg5usM3Yoo5o",
        json={"content": f"Counter usage ended. " f"Session key: ``{session_id}``"},
    )

    pickle.dump(stats, open(f"sessions/session_{session_id}.pickle", "wb+"))


if __name__ == "__main__":
    main()
