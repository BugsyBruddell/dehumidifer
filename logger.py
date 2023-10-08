class Logger:

    def __init__(self, enviro_log_path, relay_log_path):
        self.enviro_log_path = enviro_log_path
        self.relay_log_path = relay_log_path

    def log_env_data(self, message):
        with open(self.enviro_log_path, 'a') as enviro_log_file:
            enviro_log_file.write(message + '\n')

    def log_relay_activity(self, message):
        with open(self.relay_log_path, 'a') as relay_log_file:
            relay_log_file.write(message + '\n')
