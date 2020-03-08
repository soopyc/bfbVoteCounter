import json

# Prepare variables
config = {
    "info": None,
    "key": None,
    "vidid": None,
    "chars": None
}


# Functions
def ask(q, default=None):
    resolve = False
    while not resolve:
        t = input(f'{q} [{"mandatory" if default is None else default}]: ')
        if t == '':
            if default is None:
                print('This is a mandatory question! Please at least write something.')
            else:
                t = default
                resolve = True
        else:
            resolve = True
    return t


# Main
print('Hello and welcome to this quick and easy config file generator.')
print('You will be asked a few questions. Please answer them all.')
input('Press Return or Enter to continue... ')

print('First, please give me a short description of the configuration. (i.e. bfb4)')
config['info'] = ask('This will help to distinguish between configurations when sharing it.')

print('Next, please give me the video URL or ID (the part after "/watch?v=" or "youtu.be/", looks like "vL2oRzWrSgE")')
p = ask('Video ID').replace('//', '').split('/')  # Could be ['video_id'], ['https:youtube.com', 'watch?v=Video_ID'] or ['https:youtu.be','fkjdsjkfgadsfk']
if len(p) == 0:
    config['vidid'] = p
else:
    config['vidid'] = p[1].replace('watch?v=', '')


print(config)
