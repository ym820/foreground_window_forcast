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
## Task 1: App Duration Prediction with Long Short-Term Memory (LSTM)
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
After running, there will be a folder created at `outputs` and named as "LSTM_`experiment`". Then, the parameters, trained model, Keras training history, loss plot, and prediction plot

## Task 2: Next-App Prediction with Hidden Markov Model (HMM)
In this task, our goal is to predict the next application the user will use based on the previous usage data.
### Run
```
cd src/model/HMM
python3 run.py
```
### Required arguments

| Parameter                 | Default       | Description   |	
| :------------------------ |:-------------:| :-------------|
| -r --raw_path	       |	   `../../../data/raw`     |The relative path to raw datasets
| -e --exe_path          | `../../../data/processed/exe.csv`           |The relative path to the pre-processed dataset
| -ts --test_size 	       |	0.2	            |Test set size (percentage of entire dataset)
| -t --top  		       | 1	           | Number of executables to predict for each data point
| -ex  --experiment 	        | 1           | The experiment number

### Notes
After running, there will be a folder created at `outputs` and named as "HMM_`experiment`". Then, the parameters, trained model, Keras training history, loss plot, and prediction plot