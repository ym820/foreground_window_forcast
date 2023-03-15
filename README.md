# Intel-capstone: Foreground Window Forcast with Deep Learning
Authors: Yikai (Mike) Mao, Alan Zhang, Mandy Lee \
Mentors: Intel: Jamel Tayeb, Bijan Arbab, Oumaima Makhlouk, Sruti Sahani; UCSD: Teresa Rexin \
Website: https://mikem820.github.io/foreground_window_forcast/

## Abstract
Technology that advances the frontier of computing receives more attention than innovation in hardware optimization. Nevertheless, optimizing existing hardware is critical in minimizing global electronic waste by extending the lifespan of computers and making a modern computing experience accessible to more people. In this paper, we present a proposal to use neural networks to analyze system usage reports and determine the applications that are most important to the user. The network can be utilized to feed into a program that pre-emptively launches applications in the background, reducing wait time and enhancing the user experience. We will showcase the data that we previously gathered using the Intel XLSDK package, which we will use to train a Hidden Markov Model (HMM) and a Long Short-Term Memory (LSTM). 

## Prerequisites

> __Below we assume the working directory is the repository root.__

### Install dependencies
- Using docker\
You may pull the docker image from `mikem820/intel_capstone:latest` and then clone this github repo
- Using pip3

  ```sh
  # Install the dependencies
  pip3 install -r requirements.txt
  ```

## Run "test" code
You can use the below command to run the "test" code with a sample of our collected dataset. You **must** pass two arguments. The first is `test` or `all`, indicating whether to run test code or not. The second argument is to choose the model (must be either `hmm` or `lstm`) which corresond to the task we will explain in the later section. 
```
python3 run.py test hmm/lstm
```
You can also run the full pipeline with the entire dataset by the following command, with the default hyperparameters we implemented.
```
python3 run.py all hmm/lstm
```
If you want to explore different sets of hyperparameters, we explained our tasks and specific instructions to run the scripts in the following section.

## Task 1: Next-App Prediction with Hidden Markov Model (HMM)
In this task, our goal is to predict the next application the user will use based on the previous usage data.
### Run
```
cd src/model/HMM
python3 run.py
```
### Arguments

| Parameter                 | Default       | Description   |	
| :------------------------ |:-------------:| :-------------|
| -ts --test_size 	       |	0.2	            |Test set size (percentage of entire dataset)
| -t --top  		       | 1	           | Number of executables to predict for each data point
| -ex  --experiment 	        | 1           | The experiment number

### Notes
After running, there will be a folder created at `outputs` and named as "HMM_expt_`experiment`". Then, the parameters, transition matrix, model accuracy, and visualization will be stored in the folder.

## Task 2: App Duration Prediction with Long Short-Term Memory (LSTM)
As for the primary objective for our project, we aim to forecast the amount of time (in seconds) an individual will spend on a specific application within a specific hour. 
### Run
```
cd src/model/LSTM
python3 run.py
```
### Arguments

| Parameter                 | Default       | Description   |	
| :------------------------ |:-------------:| :-------------|
| -exe --exe_name	       |	firefox.exe          |The executable name to predict
| -lb --lookback          | 5           |Lookback window (hyper-parameter) for dataset processing
| -ts --test_size 	       |	0.2	            |Test set size (percentage of entire dataset)
| -e --epochs 	       |	100	            |Number of epochs
| -lr --learning_rate  		       | 0.001	           | Learning rate
| -l --loss 		           | mse             | Loss function
| -ex  --experiment 	        | 1           | The experiment number
| -r  --random	        | False           | Whether to choose the start index for test set randomly

### Notes
After running, there will be a folder created at `outputs` and named as "LSTM_expt_`experiment`". Then, the parameters, trained model, Keras training history, loss plot, and prediction plot will be stored in the folder.
