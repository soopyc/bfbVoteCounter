# BFB Votes Collector
Idea came from when I decided to go on HTC and saw people asking to count votes, I tried to help but ended up using sequencer's code instead.

I wanted to do something in order to take a break from the [Waterbot](https://github.com/waterbotdev/waterbot) project that me and some other 
developers have been doing(P.S. its really cool, you should check it out. Swearing warning from me who's frustrated, and some commands.)

I decided to do this in a different fashion than what sequencer did which allows the counter to count all votes, 
such as the "liked" character counts, etc.

You may also notice this thing is not written in javascript but instead in python because...thats the only language I know quite fluently besides scratch :^)

## Setting up
To setup the vote collector, you only need to follow a few steps.

(If you're a pro gamer and know how to use git just use the [fast guide](#fast-guide).)

1. Download the code. Click the "Clone or Download button". (![Clone or Download button](https://kenny-pls.go-get-a.life/fbFxBO.png))

2. Press the ``Download ZIP`` button. (![Download ZIP Button](https://kenny-pls.go-get-a.life/lXDvJn.png))
Save it to any directory you like. If your antivirus told you it's a virus please dismiss it. This code is not and will not be a virus. 
All it does is just download the comments from Google's servers and process it in a fancy manner so you can see which character got how many votes. 
You can see the VirusTotal scan result for the bare python code once it is finished.

3. Uncompress the zip file. If you're on Windows and uses WinRAR, open it, right click on the ``bfbVoteCounter-master`` folder and use any of these 
options. ![Options](https://kenny-pls.go-get-a.life/TIrIyk.png)

4. When you finish uncompressing and unpacking the contents, you can configure the config file by opening the config.json in any text
editor you like. I'd use Notepad as it starts fast enough and its in windows (You can open notepad quickly by typing Windows+R, notepad and enter/return.). 
In the future I might include a fancy pants configuration generator, but that will be after I finish making the main script
work.

5. When you're done editing the config, save it(presumably control+s or command+s) and you're ready to go! However, I strongly suggest you make your own token
instead of using mine. My API only have 10000 quotas per day and every run takes up about at least 4000 when theres a day left in the voting period, 
or maybe even more, which actually limits this script's function. I hope you can understand and help me by making a token yourself. Guide will be 
[here.](https://github.com/kcomain/bfbVoteCounter/wiki/Getting-your-Google-API-token)

6. Open a console/terminal window by shift-right clicking on the folder and choose this option if you're on windows.
![](https://kenny-pls.go-get-a.life/KpycmF.png)
(If you're on MacOS, I am guessing you know at least something about terminal. Open it by pressing Control+Alt+T. cd to the directory. Then just follow the next
step.) 

7. Install Python 3.6/7/8 if you haven't. If you don't know which version to use, just choose version 3.8.1. A better easier executable file will be included


## Fast guide
Quick and easy script to get this thing up and running. Please ensure you have python 3.6+ installed beforehand.
```
curl https://raw.githubusercontent.com/kcomain/bfbVoteCounter/master/setup.sh | bash
```