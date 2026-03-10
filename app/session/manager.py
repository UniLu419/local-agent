sessions = {}


def get_session(user_id):

    if user_id not in sessions:
        sessions[user_id] = []

    return sessions[user_id]


def add_message(user_id, role, content):

    sessions.setdefault(user_id, []).append({"role": role, "content": content})
