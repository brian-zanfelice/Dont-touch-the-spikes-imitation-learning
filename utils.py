import pandas as pd


class game_state:
    def __init__(self, x, y, spikes_matrix) -> None:
        self.x = x
        self.y = y
        self.previous_x = x
        self.previous_y = y
        self.spikes_matrix = spikes_matrix

    def save_state(self, jump: bool, x_velocity: float):
        data = {
            "X": [],
            "Y": [],
            "Previous_X": [],
            "Previous_Y": [],
            "X_velocity": [],
            "Spike_0": [],
            "Spike_1": [],
            "Spike_2": [],
            "Spike_3": [],
            "Spike_4": [],
            "Spike_5": [],
            "Spike_6": [],
            "Spike_7": [],
            "Spike_8": [],
            "Spike_9": [],
            "Spike_10": [],
            "Spike_11": [],
            "Jump": [],
        }
        data["X"].append(self.x)
        data["Y"].append(self.y)
        data["Previous_X"].append(self.previous_x)
        data["Previous_Y"].append(self.previous_y)
        data["X_velocity"].append(x_velocity)

        for num, spike in enumerate(self.spikes_matrix):
            data[f"Spike_{num}"].append(spike)
        data["Jump"].append(jump)
        save_data = pd.DataFrame(data)
        save_data.to_csv("data.csv", mode="a", header=False, index=False)
