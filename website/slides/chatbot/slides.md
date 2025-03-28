---
marp: true
paginate: true
---

<style>
.center {
  display: block;
  margin-left: auto;
  margin-right: auto;
  height: 85%
}
</style>

# Code a Story, Train a Bot!
*An Hour of Code with Python*

<!-- https://wiki.cs.jmu.edu/_media/student/jmu-computer_science-horiz-purple.png -->
![JMU CS logo](img/jmucs.png)

---
# Getting started with Thonny

<img src="img/thonny.png" alt="Thonny screenshot" class="center">

---
# Python Basics

- **Comments** start with `#` and help explain the code
  ``` py
  # This is a comment
  ```

- **Print function** displays a message/result in the shell
  ``` py
  print("Hello!")
  ```

- **Input function** displays a *prompt*, allows user to type
  ``` py
  name = input("Your name? ")
  print("Hello", name + "!")    # adds exclamation point
  ```

---
<style scoped>
section {
    columns: 2;
    display: block;
}
h1 {
    column-span: all;
}
h2 {
    break-before: column;
}
</style>

# Exercise 1: warmup.py

Write a program that...

1. Asks the user:
   - What is your name?
   - Where do you like to go?
   - What do you do there?

2. Outputs a sentence

Example:

![Thonny shell](img/elphaba.png)

---
# What are your favorite stories?

<!-- https://happilyeverelephants.com/wp-content/uploads/2022/06/middle-grade-fantasy-series.jpg -->
<img src="img/fantasy.jpg" alt="middle-grade fantasy series" class="center">

---
# Exercise 2: story.py

1. Copy the starter code, save as `story.py`
2. Run the program
3. Add more phrases
4. Repeat steps 2 and 3
<br>

**Notice that each phrase:**

- Is inside double quotes
- Has a comma at the end

---
# Exercise 3: Text Wrapping

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

---
# Do you think AI could do better?

<!-- https://upload.wikimedia.org/wikipedia/commons/1/13/ChatGPT-Logo.png -->
<img src="img/ChatGPT.png" alt="ChatGPT logo" class="center">

---
# Let's make our own AI chatbot!

<!-- https://github.com/gunthercox/ChatterBot -->
<img src="img/ChatterBot.png" alt="ChatterBot logo" width="65%">

## Install the `chatterbot` Library

1. Tools > Options > Interpreter > New virtual environment
    - Create a folder named `venv`, press Ok (twice)

2. Copy and run the "Installation Commands" on the website

---
# Exercise 4: Your own conversation

1. Copy the starter code, save as `chat.py`
2. Run the program
3. Try having a conversation
<br>

*An untrained ChatterBot starts off with no knowledge of how to communicate!*

4. Add more example questions and answers
   - Edit the conversation under `trainer.train`
5. Repeat steps 2, 3 and 4
<br>

---
# Exercise 5: Larger training data

1. Copy/paste the code on the website
2. Run the program
3. Try having a conversation
<br>

Optional: Feel free to try a different language!

Optional: See the [chatterbot-corpus data files](https://github.com/gunthercox/chatterbot-corpus/tree/master/chatterbot_corpus/data/)

---
# Exercise 6: Explore the database

1. Find the file named `db.sqlite3`
    - Double click to open the file
2. Click the "Browse Data" tab
3. What surprises you about the data?
4. What potential problems do you see?
