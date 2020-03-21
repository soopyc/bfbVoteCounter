import argparse
import pickle

parser = argparse.ArgumentParser(
    description="Upgrader to upgrade old pickle files to the latest version."
)
parser.add_argument('pickle_file',
                    type=argparse.FileType('rb'),
                    help="The pickle file dump that the counter.py script produced. It is stored under the "
                         "'sessions' folder/directory.")
args = parser.parse_args()
stats = pickle.load(args.pickle_file)

"""
Current stats structure
stats:
    video:
        name
        publishTime
        publishTStamp
        obj
    votes:
        total
        valid
        invalid
        deadlined
        shinyvotes
        voters
        shinies
        characters:
            "whatevername, requires the config file.":
                total
                valid 
                shiny
                deadlined
    alphs
    actualcomments
    comments (!!!!!! REQUIRED!)
    tokenusage
"""
assert'comments' not in stats or len(stats['comments']) == 0, 'Looks like this file is not usable/does not have any '\
                                                              'comments. This isn\'t worth upgrading. Just use the '\
                                                              'counter script to get the latest version of the config'\
                                                              ' instead of using this.'
