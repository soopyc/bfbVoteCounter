#!/bin/bash -x

echo "Welcome to this quick and easy setup script."
echo "You will be asked for your password as we might need to install some items."

echo "Checking if python is installed..."
which python3 > /dev/null
if [ $? != 0 ]; then
	echo "Python not found, attempting install via pyenv"
	which pyenv
	if [ $? != 0 ]; then
		echo "Pyenv not found. Looking for a package manager."
		which apt-get 
		if [ $? != 0 ]; then
			which pacman
			if [ $? != 0 ]; then
				echo "No supported package manager found"
	else 
		pyenv install 3.8.2
		if [ $? = 2 ]; then
			echo "Attempting to install python via "

echo "Downloading latest archive..."
wget https://github.com/kcomain/bfbVoteCounter/archive/master.zip -O /tmp/b53a5a29dfca42de.zip

echo "Unpacking Files"
yes | unzip /tmp/b53a5a29dfca42de.zip
cd bfbVoteCounter-master

echo "Please edit the configuration file, or press Control-C or Command-C to cancel this process. Note that the script needs the configuration to work."
echo "If you wish to use the fancy config editor, please press Control-C or Command-C now and run python3 configGen.py"
ping google.com -c 10 > /dev/null

#if [ -f /bin/nano ]; then
#	nano config.json
if [ -f /usr/bin/nvim ]; then
	nvim config.json
elif [ -f /usr/bin/vim ]; then
	vim config.json
elif [ -f /usr/bin/vi ]; then
	vi config.json
else
	echo "No editor found, halting."
fi;

echo "Setup might be complete. Please run the script by using python3 getter.py"
echo "It is adviced to run the config validator first. (Run it by using python3 validator.py)"
