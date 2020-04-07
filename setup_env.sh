echo "Hi, please don't use this if you're not in gitpod/does not want to setup this directory as a dev env, thanks."

echo "Setting up environment"
echo "Installing python version 3.8.2"
pyenv install 3.8.2
echo "Setting local version to 3.8.2, might not be required."
pyenv global 3.8.2
echo "Install dependencies"
pip3 install -r ./requirements.txt
echo "Install pylint"
pip3 install pylint thefuck
echo "Run fuck twice"
fuck
fuck
echo "run source ~/.bashrc"