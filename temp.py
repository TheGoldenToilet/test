def dict_to_bytes(message: dict):
    return b"[message: \"" + str(message).encode() + b"\" dict as bytes]"


def H_get_message(incoming, outgoing, requester, data):
    outgoing.status = 200
    outgoing.message = "OK"
    outgoing.content = data
    return outgoing


def SendResponce(responce, user):  # Is supposed to be from either HTTP or RequestLogic
    print(f"Sent {responce} to {user}")

class LongPoll:
    def __init__(self):
        self.incoming = None
        self.outgoing = None
        self.requester = None
    
    def resolve(handler, *args, **kwargs):
        responce = handler(self.incoming, self.outgoing, self.requester, *args, **kwargs)  # may have to do some try except here
        SendResponce(responce, self.requester)

def resolve_long_polls(handler, long_polls: list, *args, **kwargs):  # multiple long polls co existing shouldn't be a problem
    for poll in long_polls:
        poll.resolve(H_get_message, *args, **kwargs)

class Message:
    def __init__(self):
        self.type = ""
        self.data = {}
    
    def to_dict(self):
        return {"Type": self.type, "Data": self.data}

class User:
    def __init__(self):
        self.long_polls = [] 
        self.client_bound_buffer = []
    
    def send_client_bound_message(self, message: dict):
        as_bytes = dict_to_bytes(message)
        if len(self.long_polls) > 0:
            resolve_long_polls(H_get_message, self.long_polls, as_bytes)
        else:
            raise Exception("No active long polls no no messages could be sent")
    
    def send_client_bound_buffer(self):
        messages_as_list = [i.to_dict() for i in self.client_bound_buffer]
        self.send_client_bound_message({"Messages": messages_as_list})
    
    def set_chatting(self, chatting: bool):
        message = Message()
        message.type = "set_chatting"
        message.data = chatting
        self.client_bound_buffer.append(message)

