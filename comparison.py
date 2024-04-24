import numpy as np
from scipy.optimize import curve_fit
import os

def load_data_from_file(filename):
    with open(filename, 'r') as file:
        data = [float(line.strip().replace(',', '.')) for line in file if line.strip()]
    return data

def save_results(data, folder, filename):
    full_path = os.path.join(folder, 'algorithms_outputs', filename)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w') as file:
        for value in data:
            file.write(f"{value:.10f}".replace('.', ',') + '\n')

def median_vote(tuners):
    return np.median(tuners, axis=0)

def weighted_average_vote(tuners, weights):
    return np.average(tuners, axis=0, weights=weights)

def exponential_model(x, a, b):
    return a * np.exp(b * x)

def exponential_predictor(frequencies):
    # Create an array of indices for the x-values, assuming equal spacing
    x = np.arange(len(frequencies))

    # Fit the exponential model to the data using curve_fit, which performs nonlinear least squares fitting
    params, covariance = curve_fit(exponential_model, x, frequencies)

    # Extract the parameters for scaling factor 'a' and growth rate 'b' from the fitted model
    a, b = params

    # Calculate the predicted frequencies using the fitted model parameters
    predicted_frequencies = exponential_model(x, a, b)

    return predicted_frequencies

def smoothing(data):
    smoothed = np.zeros_like(data)
    n = len(data)
    if n < 3:
        return data
    smoothed[0] = (data[0] + data[1]) / 2
    smoothed[-1] = (data[-1] + data[-2]) / 2
    for i in range(1, n-1):
        smoothed[i] = (data[i-1] + data[i] + data[i+1]) / 3
    return smoothed


def calculate_and_save_errors(true_values, results, algorithm_names, folder):
    error_path = os.path.join(folder, 'errors', 'errors.txt')
    error_cents_path = os.path.join(folder, 'errors', 'errors_cents.txt')
    os.makedirs(os.path.dirname(error_path), exist_ok=True)

    with open(error_path, 'w') as file, open(error_cents_path, 'w') as file_cents:
        for result, name in zip(results, algorithm_names):
            errors = np.abs(true_values - result)
            cents_errors = 1200 * np.log2(result / true_values)

            average_error = np.mean(errors)
            file.write(f"{name}: {average_error:.10f}\n".replace('.', ','))

            average_cents_error = np.mean(cents_errors)
            file_cents.write(f"{name}: {average_cents_error:.10f}\n".replace('.', ','))


def process_folder(folder):
    base_path = os.path.join(folder, 'input')
    true_values = load_data_from_file(os.path.join(base_path, 'domain.txt'))
    tuner1 = load_data_from_file(os.path.join(base_path, 'tuner_1_' + folder + '.txt'))
    tuner2 = load_data_from_file(os.path.join(base_path, 'tuner_2_' + folder + '.txt'))
    tuner3 = load_data_from_file(os.path.join(base_path, 'tuner_3_' + folder + '.txt'))

    tuners = np.array([tuner1, tuner2, tuner3])
    weights = np.array([1, 1, 1])

    result_median = median_vote(tuners)
    result_weighted_average = weighted_average_vote(tuners, weights)
    result_logarithmic = exponential_predictor(tuners.mean(axis=0))
    result_smoothing = smoothing(tuners.mean(axis=0))

    results = [result_median, result_weighted_average, result_logarithmic, result_smoothing]
    algorithm_names = ['Median', 'Weighted Average', 'Exponential', 'Smoothing']

    save_results(result_median, folder, 'output_median.txt')
    save_results(result_weighted_average, folder, 'output_weighted_average.txt')
    save_results(result_logarithmic, folder, 'output_exponential.txt')
    save_results(result_smoothing, folder, 'output_smoothing.txt')

    calculate_and_save_errors(true_values, results, algorithm_names, folder)

    print(f"Results have been saved in the '{folder}' folder. Average errors have been saved in the '{folder}/errors' folder.")

# List of folders to process
folders = ['mild', 'medium', 'drastic']
for folder in folders:
    process_folder(folder)