@echo off
pip install -r requirements.txt -q
pip install -r requirements-app.txt -q
pyinstaller --noconfirm --windowed --name AllSee --onefile allsee/app.py
pyinstaller --noconfirm --name AllSee-cli --onefile allsee/cli.py
echo built in dist\
