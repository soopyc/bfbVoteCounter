import os
import re
import sys
import time
import json
import random
import pickle
import logging
import argparse
import traceback
from datetime import datetime

import requests
from blessed import Terminal
from colorama import Fore, Style, init

import gen

init_time = time.time()
t = Terminal()
version = ('0', '1-alpha', 'rewrite-2')
ver = "%s.%s.%s" % version

# Parse arguments
# init(autoreset=True)
print(f'{t.cyan("BFB Vote Counter")} {t.bright_yellow("v%s" % ver)}\n')
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
                    help=f"Deletes all session pickle files inside of the {t.underline('sessions/')}"
                         f" folder.",
                    action='store_true')
parser.add_argument('--delete-logs',
                    help=f"Deletes all log files inside of the {t.underline('logs/')} folder.",
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
parser.add_argument('--debug-mode',
                    help="Enters debug mode. Does not send requests to Google's servers.",
                    action='store_true')
args = parser.parse_args()

# Set logging level based on arguments and basica configs
if not os.path.exists('logs'):
    os.mkdir('logs')
log_file = 'logs/{}.log'.format(datetime.fromtimestamp(init_time).strftime('%Y%m%d_%H%M%S'))
logging.basicConfig(
    level=logging.DEBUG if args.debug_messages else logging.INFO, 
    format='%(asctime)s [%(name)s %(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file)
    ]
)
# Get logger objects
b = logging.getLogger('counter')  # Base Logger
s = logging.getLogger('setup')  # Setup logger
g = logging.getLogger('get_votes')  # Comment Getter logger
c = logging.getLogger('count_votes')  # Counting module Logger
# Start spamming stdout with debug shit
b.debug(f'Arguments: {args}')
b.debug(f'Comment dump: {"None" if args.comments_file is None else args.comments_file.name}')
b.debug(f'Delete comment dumps: {args.delete_comment_dumps}')
b.debug(f'Logging outputs to stdout and {log_file}')

# Define variables and stuff
b.debug('Defining variables')
session = ''
video_id = ""
deadline = 172800
token = ""
video = {"name": '', "views": 0, "comments": 0}
characters = {}
votes = {"total": 0, "valid": 0, "shinies": 0, "deadlined": 0}
fetcher = None
err_ = None
oh_no_error = False
# b.debug('')


b.debug('Defining helper functions')
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
        video_ = None
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
        if args.debug_mode:
            b.debug('debug mode is used.')
            b.debug('using dummy video object')
            video_ = pickle.loads(b'\x80\x04\x95e\x01\x00\x00\x00\x00\x00\x00\x8c\x03gen\x94\x8c'
                                  b'\x05Video\x94\x93\x94)\x81\x94}\x94(\x8c\x0cpublish_time\x94'
                                  b'\x8c\x08datetime\x94\x8c\x08datetime\x94\x93\x94C\n\x07\xcf'
                                  b'\x0c\x1a\x06\x00\x00\x00\x00\x00\x94\x8c\x0edateutil.tz.tz\x94'
                                  b'\x8c\x07tzlocal\x94\x93\x94)\x81\x94}\x94(\x8c\x0b_std_offset'
                                  b'\x94h\x06\x8c\ttimedelta\x94\x93\x94K\x00K\x00K\x00\x87\x94R'
                                  b'\x94\x8c\x0b_dst_offset\x94h\x13\x8c\n_dst_saved\x94h\x11K\x00K'
                                  b'\x00K\x00\x87\x94R\x94\x8c\x07_hasdst\x94\x89\x8c\x08_tznames'
                                  b'\x94\x8c\x03UTC\x94\x8c\x03UTC\x94\x86\x94ub\x86\x94R\x94\x8c'
                                  b'\x05title\x94\x8c\x0bDebug Video\x94\x8c\x0bdescription\x94\x8c'
                                  b'\x17Just for testing. Shhhh\x94\x8c\x0cchannel_name\x94\x8c\x07'
                                  b'kcomain\x94\x8c\x0btotal_views\x94J\xff\xe0\xf5\x05\x8c\x08comm'
                                  b'ents\x94J\xa24\x02\x00ub.')
        elif args.comments_file is None:
            b.debug('comments_file is unfilled. assume not using count only mode')
            b.info('Entering Get-Count mode.')
            b.debug('Getting a fetcher object')
            fetcher = gen.Fetchers(token)
            # Shoot a test request to Google API
            b.debug('Sending (testing) video information request to Google...')
            video_ = fetcher.video(video_id)[0]
            b.debug(f'Got video, info: {video_}')
        else:
            b.debug(f'comments_file seems to be filled. filename is {args.comments_file.name}')
            b.info('Entering Count only mode.')
            video_ = pickle.load(args.comments_file)
        video['name'] = video_.title
        video['views'] = video_.total_views
        video['comments'] = video_.comments
        print(f'{Fore.CYAN}Video: {video["name"]}\n'
              f'{Fore.LIGHTBLUE_EX}{video["comments"]} comment(s), '
              f'{Fore.CYAN}{video["views"]} view(s)')
        # Loop through list and assign characters and eeeeeeeeeeeeeee


# TODO: Now get the votes
def get_votes():
    g.debug('Get_Votes is called. Running script.')


# TODO: Count shines deadlines and stuffs that bsically just crash the script
def count_votes():
    # Count votes
    return 0


def del_stuff():
    deletes = []
    if args.delete_logs:
        deletes.append('logs/')
    if args.delete_comment_dumps:
        deletes.append('sessions/')
    for i in deletes:
        print(t.bright_yellow(f'WARNING: All files inside of {t.underline(i)} directory will be removed.'))
        print('Are you sure you want to continue?')
        print(f'[{t.bright_red("Yes/Y")}/{t.bright_green("No/N")}]:', end='')
        a = input()
        if a.lower() in ["yes", "y"]:
            dire = os.listdir(i)
            for b in dire:
                try:
                    os.remove(i + b)
                except:
                    print(t.bright_yellow(f"Cannot remove file {b}."))
                else:
                    print(f"Removed file {t.underline(b)}")
        else:
            print(t.bright_green("Okay, cancelled."))


if __name__ == '__main__':
    # this is a meme lmao
    b.debug('Posting webhook to Discord...')
    session = Fns.postsession('started')  # Notifies me about the usage of the counter
    b.debug('Running arg checks')
    Fns.prerun_check()  # Run checks because people might just spam args and brek stuff
    b.debug('setup finished, entering fullscreen mode using ctx mgr')
    with t.fullscreen():  # Start fullscreening
        Fns.cur_back()
        try:
            if args.delete_comment_dumps or args.delete_logs:  # Goto delfiles and skip the rest
                del_stuff()  # attak on FILES!!
                _ = input('Press return or enter to continue... This '
                          'screen will get removed after you press the button.')
                sys.exit(0)  # attak on DIE
            Fns.setup(args.config_file)  # Setup stuff
            if args.comments_file is None:  # No comment dump file, going to get comments
                try:
                    get_votes()  # s̶p̶a̶m̶ send hella requests to google's server and get results.
                except Exception as e:
                    b.fatal('An error occured. The script cannot continue. See the error above ')
            if args.save_only:
                b.info('Since the save-only parameter is used, the comments collected are dumped to sessions directory.'
                       'to use it, just use this script again with the -f parameter. see {sys.argv[0]} --help for more '
                       'details.')
                _ = input('Press return or enter to continue... This screen will get removed after you press the button.')
                sys.exit(0)  # quit because user fired the counter with -s param
            if not args.save_only:
                count_votes()
        except Exception as e:
            oh_no_error = True
            err_ = e
        _ = input('Press return or enter to continue... This screen will get removed after you press the button.')
    if oh_no_error:
        print('Hey bro the code errored out somehow so this is the fallback and ill display'
              ' the traceback here.')
        print(traceback.TracebackException.from_exception(err_))
else:  # bruh why use this script as a module, support for that will come soon:tm:
    print(f'{Fore.RED}Sorry, but this script is not intended to be imported. '
          f'Please use it in the command line instead.')
    raise NotImplementedError
