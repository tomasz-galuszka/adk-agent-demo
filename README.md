## Local setup
```bash
brew install pyenv
brew install pyenv-virtualenv
pyenv install -s 3.13.12
pyenv global 3.13.12
pip install uv

echo -e '\n# Pyenv' >>  ~/.zshrc
echo -e '\neval "$(pyenv init -)"' >>  ~/.zshrc
echo -e '\neval "$(pyenv virtualenv-init -)"' >>  ~/.zshrc
```
## Build
```bash
uv sync
```

## Run via google local ui 
```bash
adk web --port 8080 # web interface 
```

## Run via google local ui
```bash
python main.py
```