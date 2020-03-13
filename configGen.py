import json

# Prepare variables
config = {
    "info": None,
    "key": None,
    "vidid": None,
    "chars": None
}
alphabeeet = [i for i in 'abcdefghijklmnopqrstuvwxyz']


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


def choice(text: str, ch: list):
    resolve = False
    chs = '/'.join(ch)
    while not resolve:
        t = ask(f'{text} [{chs}]')
        if t.lower() not in ch:
            print('Please pick an option in square brackets and write it exactly as prompted.')
        else:
            return t


# 7 years old played at this time o_O
# Main
print('Hello and welcome to this quick and easy config file generator.')
print('You will be asked a few questions. Please answer them all.')
input('Press Return or Enter to continue... ')

print('First, please give me a short description of the configuration. (i.e. bfb4)')
config['info'] = ask('This will help to distinguish between configurations when sharing it.')

print('Next, please give me the video URL or ID (the part after "/watch?v=" or "youtu.be/", looks like "vL2oRzWrSgE")')
p = ask('Video ID').replace('//', '').split('/')  # Could be ['video_id'], ['https:youtube.com', 'watch?v=Video_ID'] or ['https:youtu.be','fkjdsjkfgadsfk']
if len(p) == 1:
    config['vidid'] = p[0]
else:
    config['vidid'] = p[1].replace('watch?v=', '')

print('Next, please give me your google api token (due to an earlier incident of someone stealing ny api token, you '
      'must create your own api token to use this service. Instructions will be in'
      'https://github.com/kcomain/bfbVoteCounter/wiki/Getting-your-Google-API-token')
config['token'] = ask('Google API Token')

print('Then, please give me the mode. There will be 2 valid modes, auto and custom.\n'
      '- Auto: this mode will be the mode you want to use if you\'re going to use this in a normal eliminating video.'
      '- Custom: this mode will most likely be used in favorite character voting screens. More inputs are needed.')
mode = choice('Which mode do you want to use?', ['auto', 'custom'])

if mode == 'auto':
    # Fun part
    print('Now, I need you to give me the characters.')
    while True:
        count = 0
        name = ask(f'Character name: ([{alphabeeet[count]}])')

print(config)
