## Local setup
```bash
# Follow https://docs.ollama.com/quickstart
# Then pull the model
ollama pull qwen2.5vl
ollama pull nomic-embed-text
    ollama show nomic-embed-text
ollama show qwen2.5vl

brew install pyenv
brew install pyenv-virtualenv
pyenv install -s 3.13.12
pyenv global 3.13.12
pip install uv

echo -e '\n# Pyenv' >>  ~/.zshrc
echo -e '\neval "$(pyenv init -)"' >>  ~/.zshrc
echo -e '\neval "$(pyenv virtualenv-init -)"' >>  ~/.zshrc
```
## Build and create virtualenv
```bash
uv sync
```

## Provide API Google API keys to access gemini models
Login using your GA to https://aistudio.google.com/api-keys and create new key then paste to .env files for each agent
```
    GOOGLE_API_KEY=COPY_PASTE_YOUR_CODE HERE
```

## Run via local ui from google 
```bash
source .venv/bin/activate
adk web
```

## Run via cmd line
```bash
source .venv/bin/activate
adk run root_agent
```

## Rozszerzamy sub agenta do analizy obrazków
- wykrywanie obiektów
- 