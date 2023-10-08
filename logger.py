import os

class Logger:

    def __init__(self, enviro_log_path, relay_log_path, state_log_path):
        self.enviro_log_path = enviro_log_path
        self.relay_log_path = relay_log_path
        self.state_log_path = state_log_path
        
        # Create log files if they don't exist
        self._check_and_create(self.enviro_log_path)
        self._check_and_create(self.relay_log_path)
        self._check_and_create(self.state_log_path)

    def _check_and_create(self, filepath):
        if not os.path.exists(filepath):
            with open(filepath, 'w'):
                pass

    def log_env_data(self, message):
        with open(self.enviro_log_path, 'a') as enviro_log_file:
            enviro_log_file.write(message + '\n')

    def log_relay_activity(self, message):
        with open(self.relay_log_path, 'a') as relay_log_file:
            relay_log_file.write(message + '\n')

    def set_state(self, state):
        with open(self.state_log_path, 'w') as state_file:
            state_file.write(state)

    def get_state(self):
        with open(self.state_log_path, 'r') as state_file:
            return state_file.read().strip()
