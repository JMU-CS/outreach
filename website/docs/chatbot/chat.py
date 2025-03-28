from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Name the bot
name = "ChatJMU"
bot = ChatBot(name)

# Train the bot
trainer = ListTrainer(bot)
trainer.train([
    'How are you?',
    'I am good.',
    'What do you like?',
    'Python programming',
    'Thank you.',
    'You are welcome.',
])

# Conversation loop
while True:
    print()  # blank line
    request = input("You: ")
    response = bot.get_response(request)
    print(name + ":", response)
