import pynput.keyboard as kb, pynput.mouse as ms
class keyboard_monitor:
    def __init__(self, key_actions) -> None:
        self.keys_down = set()
        self.key_actions = key_actions
        self.running = False
        self.listener = None
    def on_press(self, key):
        self.keys_down.add(key)
        if self.keys_down in self.key_actions:
            return self.key_actions[self.keys_down]()
    def on_release(self, key):
        self.keys_down.discard(key)
        if key == kb.Key.esc:
            self.running = False
            print("Keyboard monitor ended")
            self.listener.stop() #type: ignore
    def start(self):
        with kb.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            self.listener = listener
            listener.join

base_action_set = {
            frozenset(['f']): lambda: True,
            frozenset(['j']): lambda: False
        }

