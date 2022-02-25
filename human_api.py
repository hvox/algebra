class Message:
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)

def raise_messages(it, result_container):
    current = None
    for msg in it:
        if current is not None:
            yield current
        current = msg
    result_container[0] = current
