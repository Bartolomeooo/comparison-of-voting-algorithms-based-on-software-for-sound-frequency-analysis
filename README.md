# Voting Algorithm Comparison for Audio Frequency Estimation

## Project Description

This project aims to compare the performance of four voting algorithms in aggregating frequency estimates from three different audio tuner software tools. The goal is to identify which algorithm most accurately approximates the true pitch of a generated sound, especially under varying conditions of signal distortion.

The frequency data was generated using the MiniSynth synthesizer in FL Studio for 27 standard musical notes ranging from E2 (82.41 Hz) to E4 (329.63 Hz), typically used in guitar tuning. The signals were intentionally distorted on three levels:

- **Mild distortion**: combination of saw and square waveforms, 31.5% noise, 42% distortion.
- **Medium distortion**: two square waves, 50.7% noise, 83% distortion, and 25.2% decimator.
- **Severe distortion**: two square waves, 80% noise, 100% distortion, and 70% decimator.

For each frequency and distortion level, data was collected from three software tuners: **FL Tuner**, **GTune**, and **NATuner**. The outputs of these tuners were then aggregated using four different algorithms:

- **Median Vote**: the median of the three tuner outputs.
- **Weighted Average Vote**: an equally weighted average of the tuner outputs.
- **Exponential Predictor**: fits an exponential model to the data using nonlinear regression.
- **Exponential Smoothing**: applies smoothing in the logarithmic domain to reduce noise and fluctuations.

The performance of each algorithm was evaluated by comparing their outputs to the true frequencies in both absolute error (Hz) and relative error (cents).

---

## How to Run

### Requirements

Install required libraries:

```bash
pip install numpy scipy
```
Run the script:

```bash
python comparison.py
