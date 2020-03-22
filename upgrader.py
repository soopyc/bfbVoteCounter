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


def printd(text):
    print(text, end='\r')


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
# assert 'comments' not in stats, 'Looks like this file is not usable/does not have any '\
#                                 'comments. This isn\'t worth upgrading. Just use the '\
#                                 'counter script to get the latest version of the config'\
#                                 ' instead of using this.'

print('Checking structures...')
viditems = [
    'name',
    'publishTime',
    'publishTStamp',
    'obj'
]
votesitems = [
    'total',
    'valid',
    'invalid',
    'deadlined',
    'shinyvotes',
    'voters',
    'shinies',
    'characters'
]
elseitems = [
    'alphs',
    'actualComments',
    'comments',
    'tokenUsage'
]
print('Checking "video" structure')
for i in viditems:
    printd(f'Checking {i}')
    if i in stats['video']:
        print(f'Checking {i} OK')
    else:
        print(f'Checking {i} NO')
        print('Adding value')
        stats['video'][i] = None

for i in votesitems:
    if i == 'characters':
        # Initiate special check
        print()
    printd(f'Checking {i}')
    if i in stats['video']:
        print(f'Checking {i} OK')
    else:
        print(f'Checking {i} NO')
        print('Adding value')
        stats['video'][i] = None
