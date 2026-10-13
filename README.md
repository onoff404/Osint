# AllSee OSINT — search anything: name, @username, phone, email, image clue
# Windows / Linux / macOS. Python 3.10+.

## Run (no build needed)
pip install -r requirements.txt
python -m allsee John Doe
python -m allsee.app

## App
python -m allsee.app
# Search -> double-click row to open -> Export HTML/JSON

## CLI
python -m allsee.cli John Doe --html report.html --json out.json --open
run.bat John Doe --html report.html
./run.sh John Doe --html report.html

## Build exe/app
pip install -r requirements-app.txt
pyinstaller --noconfirm --windowed --name AllSee --onefile allsee/app.py
pyinstaller --noconfirm --name AllSee-cli --onefile allsee/cli.py
