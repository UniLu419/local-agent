sessions = {}


def get_history(session_id):

    return sessions.setdefault(session_id, [])


def append_message(session_id, message):

    sessions.setdefault(session_id, []).append(message)
