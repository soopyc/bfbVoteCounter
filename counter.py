import os
import random
import re
import json
import sys
import time
import logging
import argparse
import requests
from colorama import Fore, Style, init

import gen

init_time = time.time()
version = ('0', '1-alpha', 'rewrite-2')
ver = "%s.%s.%s" % version

# Parse arguments
init(autoreset=True)
print(f'{Fore.CYAN}BFB Vote Counter {Fore.YELLOW}v%s\n' % ver)
parser = argparse.ArgumentParser(description="Simple python script for counting votes in Battle for"
                                             " Dream Island season 4 and (potentially) 5, a popular"
                                             " animated object show on YouTube.")
parser.add_argument('-v', '--version', 
                    help="Prints the version and exits", action='version', version='\033[2A')
parser.add_argument('-f', '--comments-file', 
                    help="The comment pickle file when it finished getting the votes and/or "
                         "it errored out. It will look something like this: \n"
                         "session_cbd312bc3b2c13cdbd.pickle",
                    default=None, type=argparse.FileType('rb'))
parser.add_argument('-r', '--delete-comment-dumps',
                    help="Deletes all session pickle files inside of the sessions/ folder.",
                    action='store_true')
parser.add_argument('-c', '--config-file',
                    help="The configuration json file for the counter. Defaults to config.json",
                    default=None, type=argparse.FileType('r'))
parser.add_argument('-s', '--save-only',
                    help='Only get the comments and store them in the session pickle file.',
                    action='store_true')
parser.add_argument('-d', '--debug-messages',
                    help="Spams the console with debug items",
                    action='store_true')
args = parser.parse_args()

# Set logging level based on arguments
if args.debug_messages:
    logging.basicConfig(level=logging.DEBUG, format='[%(name)s %(levelname)s] %(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='[%(name)s %(levelname)s] %(message)s')
# Get logger objects
b = logging.getLogger('Script')  # Base Logger
s = logging.getLogger('Functions')  # Setup logger
g = logging.getLogger('Getter')  # Comment Getter logger
c = logging.getLogger('Counter')  # Counting module Logger
# Start spamming stdout with debug shit
b.debug(f'Arguments: {args}')
b.debug(f'Comment dump: {"None" if args.comments_file is None else args.comments_file.name}')
b.debug(f'Delete comment dumps: {args.delete_comment_dumps}')

# Define variables and stuff
video_id = ""
deadline = 172800
token = ""
video = {"name": '', "views": 0, "comments": 0}
characters = {}
votes = {"total": 0, "valid": 0, "shinies": 0, "deadlined": 0}
fetcher = None
# b.debug('')


class Fns:
    @staticmethod
    def clear():
        print('\x1b[2J')

    @staticmethod
    def cur_back():
        print('\033[1;1f')

    @staticmethod
    def get_vote(text: str, alphs: list):
        return re.findall(fr"\[({alphs})\]", text.lower())

    @staticmethod
    def say(text: str):
        print('\033[0K' + text)

    @staticmethod
    def bleep_text(text: str, *, shows: int = 5, bleeper: str = '*'):
        if shows < 0:
            raise NotImplementedError('Bro tell me how to do literally anything if you give me a '
                                      'negative value, do I do nothing? just use the plain variab'
                                      'le for it man')
        if len(text) <= shows:
            return text  # No point on hiding anything when theres literally nothing to
        out = text[0:shows]
        out += ''.join(bleeper for _ in range(len(text)-shows))
        return out

    @staticmethod
    def postsession(stat: str, keyid: str = None):
        if keyid is None:
            sbb = True
            keyid = ""
            for _ in range(20):
                keyid += random.choice([i for i in "0123456789abcdef"])
        else:
            sbb = False
        requests.post("https://canary.discordapp.com/api/webhooks/687220425666985984/nvB9YJAWrS0"
                      "I7y9ixbdn1P90OR-vu49PInz1BmNFogkt-Icnwvw_Qv7wJg5usM3Yoo5o",
                      json={"content": f'Counter usage {stat}. Session Key: '
                                       f'{keyid}'})
        if sbb:
            return keyid

    @staticmethod
    def prerun_check():
        if args.save_only and args.comments_file is not None:
            raise NameError('You may not use save only when the script does not even get anyth'
                            'ing from the API.')

    @classmethod
    def setup(cls, config_file):
        """Setup the config and files
        """
        global video_id
        s.debug('using global video_id')
        global deadline
        s.debug('using global deadline')
        global token
        s.debug('using global token')
        global video
        s.debug('using global video')
        global characters
        s.debug('using global characters')
        global votes
        s.debug('using global votes')
        global fetcher
        s.debug('using global fetcher')
        if config_file is None:
            s.debug('Config is None. Falling back to default.')
            try:
                config_file = open('config.json', 'r')
            except FileNotFoundError:
                s.debug('config.json not found. exiting')
                s.critical(f'Configuration file not found. Please check if you have a config.json'
                           f' in the directory that you\'re running this program. If not, generate'
                           f' one using the configGen utility or use the -c parameter to specify'
                           f' the configuration file if you have one. See {sys.argv[0]}'
                           f' --help for more information.')
                _ = input('Press return or enter to exit...')
                sys.exit(1)
        b.info(f'Using configuration file: {config_file.name}')
        config = json.load(config_file)
        b.debug('loading config file contents to config')
        video_id = config['videoID']
        deadline = None if config['deadline'] == 0 else config['deadline']
        token = config['token']
        b.info(f'Using token {cls.bleep_text(token)}')
        b.debug('Testing if getting a video is required')
        if args.comments_file is None:
            b.debug('comments_file is unfilled. assume not using count only mode')
            b.info('Entering Get-Count mode.')
            b.debug('Getting a fetcher object')
            fetcher = gen.Fetchers(token)
            # Shoot a test request to Google API
            b.debug('Sending (testing) video information request to Google...')
            video_ = fetcher.video(video_id)[0]
            b.debug(f'Got video, info: {video_}')
            video['name'] = video_.title
            video['views'] = video_.total_views
            video['comments'] = video_.comments
            print(f'{Fore.CYAN}Video: {video["name"]}\n'
                  f'{Fore.LIGHTBLUE_EX}')
        else:
            b.debug(f'comments_file seems to be filled. filename is {args.comments_file.name}')
            b.info('Entering Count only mode.')
        # Loop through list and assign characters and eeeeeeeeeeeeeee


# TODO: Now get the votes
def get_votes():
    return 0


# TODO: Count shines deadlines and stuffs that bsically just crash the script
def count_votes():
    # Count votes
    return 0


def del_files():
    print(f"{Fore.YELLOW}WARNING: All files inside of sessions/ directory will be removed. "
          f"Are you sure you want to continue?\n{Style.RESET_ALL}[{Fore.RED}Yes{Style.RESET_ALL}/"
          f"{Fore.GREEN}No{Style.RESET_ALL}]: ", end='')
    a = input()
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


if __name__ == '__main__':
    # this is a meme lmao
    b.debug('Posting webhook to Discord...')
    Fns.postsession('started')  # Notifies me about the usage of the counter
    b.debug('Running arg checks')
    Fns.prerun_check()  # Run checks because people might just spam args and brek stuff
    if args.delete_comment_dumps:  # Goto delfiles and skip the rest
        del_files()  # attak on files
    Fns.setup(args.config_file)  # Setup stuff
    if args.comments_file is None:  # No comment dump file, going to get comments
        get_votes()  # s̶p̶a̶m̶ send hella requests to google's server and get results.
    if args.save_only:
        b.info('Since the save-only parameter is used, the comments collected are dumped to sessions directory.'
               'to use it, just use this script again with the -f parameter. see {sys.argv[0]} --help for more '
               'details.')
        sys.exit(0)  # quit because user fired the counter with -
    if not args.save_only:
        count_votes()
else:
    print(f'{Fore.RED}Sorry, but this script is not intended to be imported.'
          f'Please use it in the command line instead.')
    raise NotImplementedError
