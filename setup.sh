#!/bin/bash -x

echo "Downloading latest archive..."
wget https://github.com/kcomain/bfbVoteCounter/archive/master.zip -O /tmp/b53a5a29dfca42de.zip

echo "Unpacking Files"
yes|unzip /tmp/b53a5a29dfca42de.zip
cd bfbVoteCounter-master

echo "Please edit the configuration file, or press Control-C or Command-C to cancel this process. Note that the script needs the configuration to work."
echo "If you wish to use the fancy config editor, please press Control-C or Command-C now and run python3 configGen.py"
ping google.com -c 10 > /dev/null

if [ -f /bin/nano ]; then
	nano config.json
elif [ -f /usr/bin/nvim ]; then
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
