# Golem Hello World App

This application demonstrates a simple hello world use-case, showing how to execute tasks on Golem network

## Demo

![Peek 2022-08-03 19-24](https://user-images.githubusercontent.com/5244214/182671252-b82499a5-3524-4c5a-bda1-f1df8a00ed66.gif)

## Setup

Prerequisites:

- Python 3.6 or higher
- (optional) Fresh virtual environment
- Yagna daemon running ([docs](https://handbook.golem.network/requestor-tutorials/flash-tutorial-of-requestor-development))

Install packages

```
$ python3 -m pip install -r requirements.txt
```

## Run

To execute the whole example, run the following command

```
$ python3 main.py
```

The **main.py** file configures Golem network and deploys the task to the workers (stored in the **task.py**)

