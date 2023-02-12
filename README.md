# Intel-capstone: Improving App Launch Time with Deep Learning
Authors: Yikai Mao, Alan Zhang, Mandy Lee

## Abstract
Technology that advances the frontier of computing receives more attention than innovation in hardware optimization. Nevertheless, optimizing existing hardware is critical in minimizing global electronic waste by extending the lifespan of computers and making a modern computing experience accessible to more people. In this paper, we present a proposal to use neural networks to analyze system usage reports and determine the applications that are most important to the user. The network can be utilized to feed into a program that pre-emptively launches applications in the background, reducing wait time and enhancing the user experience. We will showcase the data that we previously gathered using the Intel XLSDK package, which we will use to train a Hidden Markov Model (HMM) and a Long Short-Term Memory LSTM). 

## Prerequisites

> __Below we assume the working directory is the repository root.__

### Install dependencies
Using pip3

  ```sh
  # Install the dependencies
  pip3 install -r requirements.txt
  ```
## Task 1: App Duration Prediction: Long Short-Term Memory (LSTM)
As for the primary objective for our project, this task is to forecast the amount of time (in seconds) an individual will spend on a specific application within a specific hour. 
### Run
```
cd src/model/LSTM
python3 run.py
```
### Required arguments

| Parameter                 | Default       | Description   |	
| :------------------------ |:-------------:| :-------------|
| -exe --exe_name	       |	firefox.exe          |The executable name to predict
| -lb --lookback          | 5           |Lookback window (hyper-parameter) for dataset processing
| -e --epochs 	       |	100	            |Number of epochs
| -lr --learning_rate  		       | 0.001	           | Learning rate
| -l --loss 		           | mse             | Loss function
| -ex  --experiment 	        | 1           | The experiment number

### Notes
After running, there will be a folder created at `experiments` and named as the parameter "experiment". Then, the parameters, trained model, Keras training history, loss plot, and prediction plot