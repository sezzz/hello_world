from dataclasses import dataclass


@dataclass
class Message:
    __slots__ = ("short_name", "name", "messages", "sleep", "usage", "calls", "skips", "wait_before")

    def __init__(self, short_name, name, messages, sleep, wait_before=0, calls=0, skips=0, usage=0):
        self.short_name = short_name
        self.name = name
        self.messages = messages
        self.sleep = sleep
        self.usage = usage
        self.calls = calls
        self.skips = skips
        self.wait_before = wait_before
