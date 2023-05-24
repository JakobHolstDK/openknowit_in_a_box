#!/bin/bash
mkdir src
mkdir tests

# Create project directory
mkdir src/inabox

# Create main Python file
touch src/inabox/inabox.py
touch src/inabox/__init__.py
touch src/inabox/__main__.py

touch tests/test_inabox.py

touch LICENSE
touch MANIFEST.in
touch pyproejct.toml

# Create requirements.txt file
touch requirements.txt

# Create README.md file
touch README.md

# Create .gitignore file
echo "__pycache__/" >> .gitignore
echo ".DS_Store" >> .gitignore
echo "venv/" >> .gitignore

echo "Basic files created for the 'inabox' Python project."

