# Code a Story, Train a Bot

!!! abstract "Learning Objectives"
    *After today's activity, you should be able to:*

    * Explain the process of editing and running a Python program.
    * Write simple Python programs that use `print()` and `input()`.
    * Train a chatbot by providing a variety of sample conversations.
    * Describe how training data impacts the capability of a chatbot.

:material-presentation: [Instructor Slides](slides.html){target="_blank"}


## Python Basics

``` py
# How to input and output
name = input("Your name? ")
print("Hello", name + "!")
```


## Story Generator

??? example "Starter Code: story.py"
    ``` py
    --8<-- "chatbot/story.py"
    ```

??? example "Code for Exercise #3"
    1. Add this line at the top:
    ``` py
    import textwrap
    ```
    2. Replace `print(` with:
    ``` py
    story = " ".join([
    ```
    3. Replace the `)` with:
    ``` py
    ])
    print(textwrap.fill(story, width=72))
    ```

### Going Further

* [Documentation for random](https://docs.python.org/3/library/random.html)
* [Documentation for textwrap](https://docs.python.org/3/library/textwrap.html)


## Simple Chatbot

??? tip "Installation Commands"
    Run each command (in the Shell) after creating a venv.
    ``` sh
    !pip install chatterbot chatterbot_corpus pyyaml
    ```
    ``` sh
    !python -m spacy download en_core_web_sm
    ```

??? example "Starter Code: chat.py"
    ``` py
    --8<-- "chatbot/chat.py"
    ```

??? example "Code for Exercise #5"
    Add this after the other imports:
    ``` py
    from chatterbot.trainers import ChatterBotCorpusTrainer
    ```
    Add this above the conversation loop:
    ``` py
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train("chatterbot.corpus.english")
    ```

### Going Further

* [ChatterBot Documentation](https://docs.chatterbot.us/)
* [chatterbot-corpus data files](https://github.com/gunthercox/chatterbot-corpus/tree/master/chatterbot_corpus/data/)
