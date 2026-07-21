# tutorial-calc

This project is a small calculator application that runs in your web browser. It uses a Python backend to calculate expressions like `2+2` or `(3+5)*4` and shows the result on a simple web page.

## What you need

- A Mac or Linux computer
- Python 3 installed
- A terminal or command line window

## Step 1: Open the project folder

Use Finder or your file manager to open the folder `tutorial-calc`, or open a terminal and change into the folder:

```bash
cd /Users/jirka/Developer/PERSONAL/tutorial-calc
```

## Step 2: Create and activate the Python environment

This keeps the app's files separate from other Python programs on your computer.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

After this, your terminal prompt may show `(.venv)` at the start. That means the project is active.

## Step 3: Install the required software

Run this command once to install everything the app needs:

```bash
python -m pip install -r requirements.txt
```

## Step 4: Start the calculator app

Run this command to start the app:

```bash
python -m uvicorn calculator:app --reload --port 8000
```

You should see messages saying the server is running.

## Step 5: Open the app in your browser

Open this address in your web browser:

```text
http://127.0.0.1:8000
```

You will see the calculator page. Type expressions like `1+1`, `2*3`, or `(2+3)*4`, then submit to see the answer.

## How to stop the app

If the app is running in the terminal, press `Ctrl+C` to stop it.

If you started the server in a separate terminal window, switch to that window and press `Ctrl+C` there.

## How to close the Python environment

When you are finished, deactivate the virtual environment with:

```bash
deactivate
```

That returns your terminal to normal mode.

## Notes

- If you see a message like `Could not connect`, make sure the app is still running and that the browser address is exactly `http://127.0.0.1:8000`.
- If you want to start again later, repeat the steps above from activating the environment.
