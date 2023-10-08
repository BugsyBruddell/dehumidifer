import os
import matplotlib.pyplot as plt
import seaborn as sns

class WebLogger:

    def __init__(self, relay_log_path, enviro_log_path, state_log_path, output_path):
        self.relay_log_path = relay_log_path
        self.enviro_log_path = enviro_log_path
        self.state_log_path = state_log_path
        self.output_path = output_path

    def get_last_n_lines(self, filepath, n):
        with open(filepath, 'r') as file:
            lines = file.readlines()
            return lines[-n:]

    def get_state(self):
        with open(self.state_log_path, 'r') as state_file:
            return state_file.read().strip()

    def generate_graph(self):
        # Extracting data from enviro.txt
        times, temps, hums = [], [], []
        with open(self.enviro_log_path, 'r') as file:
            for line in file:
                time, data = line.split(":", 1)
                temp, hum = data.split(',')
                times.append(time.strip())
                temps.append(float(temp.split('Temperature: ')[1].split('°C')[0]))
                hums.append(float(hum.split('Humidity: ')[1].split('%')[0]))

        # Plotting data
        plt.figure(figsize=(10, 5))
        
        # Plot temperature and adjust the X-axis
        plot_temp = sns.lineplot(x=times, y=temps, label="Temperature (°C)")
        plot_temp.set_xticks(plot_temp.get_xticks()[::int(len(times)/10)])  # Use every 10th timestamp for clarity
        plot_temp.set_xticklabels([times[i] for i in plot_temp.get_xticks().astype(int)], rotation=45)
        
        # Plot humidity
        plot_hum = sns.lineplot(x=times, y=hums, label="Humidity (%)")
        
        plt.tight_layout()
        plt.savefig("/var/www/html/enviro_graph.png")

    def generate_html(self):
        relay_logs = self.get_last_n_lines(self.relay_log_path, 10)
        enviro_logs = self.get_last_n_lines(self.enviro_log_path, 10)
        current_state = self.get_state()
        self.generate_graph()

        html_content = f"""
        <html>
            <head>
                <title>Dehumidifier Logger</title>
            </head>
            <body>
                <h2>Current State: {current_state}</h2>
                <h3>Latest Relay Activities</h3>
                <pre>
                {'<br>'.join(relay_logs)}
                </pre>
                <h3>Latest Environment Readings</h3>
                <pre>
                {'<br>'.join(enviro_logs)}
                </pre>
                <h3>Humidity and Temperature Graph</h3>
                <img src="enviro_graph.png" alt="Environment Graph">
            </body>
        </html>
        """

        with open(self.output_path, 'w') as html_file:
            html_file.write(html_content)

if __name__ == "__main__":
    logger = WebLogger('./logs/relay-activity.txt', './logs/enviro.txt', './logs/STATE', '/var/www/html/index.html')
    logger.generate_html()
