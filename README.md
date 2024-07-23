# Robot Framework Test Generator
>  ⚠️ This is a simple proof of concept and still in development. Might not work as expected in all cases.

This repository provides a tool to launch a browser that the user can interact with. The actions performed in the browser are recorded and automatically generated as a Robot Framework test suite.
The suite can be instantly run to repeat all the actions or used as an base for furher test automation development.

## Usage and overview
Start the session by running
```
python main.py
```
This opens up a browser window using Selenium. Initially, it also creates a new output.robot.
User actions in the browser are recorded and converted into corresponding Robot Framework syntaxes in real-time.
