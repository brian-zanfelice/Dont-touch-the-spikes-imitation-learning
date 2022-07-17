from keras import models, layers, losses, optimizers, activations, metrics, regularizers
import pandas as pd
import numpy as np

num_epochs = 300  # number of epochs for training

# Function that get the data from the .csv
def get_data():
    inputs = pd.read_csv("data.csv", sep=",", header=0, usecols=[0, 1, 2, 3]).values
    expected_outputs = pd.read_csv("data.csv", sep=",", header=0, usecols=[5, 5]).values
    expected_outputs = expected_outputs[:, 0]
    matrix_spikes_inputs = pd.read_csv(
        "data.csv", sep=",", header=0, usecols=[4, 4]
    ).values
    matrix_spikes_inputs = matrix_spikes_inputs[:, 0]

    new_inputs = np.zeros(((inputs.shape[0]), 16))
    for index, spikes in enumerate(matrix_spikes_inputs):
        spike_array = []
        for spike in spikes:
            if spike == "0":
                spike_array.append(0)
            elif spike == "1":
                spike_array.append(1)

        new_array = np.append(inputs[index], spike_array)
        new_inputs[index] = new_array

    return new_inputs, expected_outputs


# The code below creates and train the neural network


def create_neural_network():
    model = models.Sequential()

    model.add(layers.Dense(32, activation=activations.linear, input_shape=(16,)))
    model.add(layers.LeakyReLU(0.01))

    model.add(layers.Dense(32, activation=activations.linear))
    model.add(layers.LeakyReLU(0.01))

    model.add(layers.Dense(1, activation=activations.sigmoid))
    return model


def training_neural_network(model, inputs, expected_outputs):
    model.compile(
        optimizer=optimizers.Adam(),
        loss=losses.BinaryCrossentropy(),
        metrics=metrics.BinaryAccuracy(),
    )
    history = model.fit(inputs, expected_outputs, epochs=num_epochs, verbose=3)


def get_jump(model, input_predict):
    return model.predict(input_predict)


def save_model(model):
    model.save("my_model")


net = create_neural_network()
inputs, expected_outputs = get_data()
training_neural_network(net, inputs, expected_outputs)
net.summary()
save_model(net)
