import random

# Define lists of phrases which will help build a story.
start = [
    "Once upon a time,",
]
character = [
    "there lived a child.",
]
time = [
    "One day",
]
story_plot = [
    "she was wandering near",
]
place = [
    "the river, where",
]
second_character = [
    "she saw a small bird,",
]
age = [
    "shivering and wet,",
]
work = [
    "searching for something.",
]

# Choose a random item from each list and print the story.
print(
    random.choice(start),
    random.choice(character),
    random.choice(time),
    random.choice(story_plot),
    random.choice(place),
    random.choice(second_character),
    random.choice(age),
    random.choice(work)
)
