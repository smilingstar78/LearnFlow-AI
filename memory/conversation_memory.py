chat_history = []


def add_to_memory(user_message, ai_message):

    chat_history.append({

        "user": user_message,

        "assistant": ai_message

    })

    # Keep only the last 5 conversations
    if len(chat_history) > 5:

        chat_history.pop(0)


def get_memory():

    memory = ""

    for chat in chat_history:

        memory += f"""
User: {chat["user"]}
AI: {chat["assistant"]}

"""

    return memory