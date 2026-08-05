conversation_memory = []


def add_message(role: str, content: str):

    conversation_memory.append(
        {
            "role": role,
            "content": content,
        }
    )


def get_memory():

    return conversation_memory


def clear_memory():

    conversation_memory.clear()


def get_last_user_message():

    for message in reversed(conversation_memory):

        if message["role"] == "user":
            return message["content"]

    return None