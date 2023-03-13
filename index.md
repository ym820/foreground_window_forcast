---
layout: page
title: "Foreground Window Forecast"
permalink: /
toc: true
---
By Alan Zhang, Mandy Lee, Mike Mao
<link rel="stylesheet" href="style.css">
<iframe src="assets\experiment5.html" min-width = "600" width="100%" height=600 overflow=auto frameBorder=0></iframe>
---
<!-- <div class="toc_style"> -->
{:toc}
<!-- </div> -->
---

# Introduction
<img src="assets\avg_launch_time.png" width=700 class="center" alt="Image of the average launch time of Google Chrome and Windows Explorer across machines of varying ages." />

According to a research conducted by Intel, a 0-1 year old computer takes an average of 11 seconds to launch Google Chrome. Our hypothesis is that this data is gathered from across the globe and the minimum PC specification is much lower in markets outside of the U.S. This increased wait time creates a subpar computing experience and hampers productivity.  Fortunately, we believe that data science can help. Our proposed solution involves launching applications before the user needs them, which can eliminate the waiting time. To achieve this, we developed software that that collects usage data when the user logs on. This data is then processed and stored in a database. We used eight weeks of data we have collected, we trained two models: a Hidden Markov Model and a Long-Short Term Memory Model. These models are ideal for modeling sequential data and help us understand how a user interacts with their machine. The Hidden Markov Model predicts the sequence of applications used, while the LSTM model identifies which application is a potential candidate for pre-launching based on its predicted hourly usage. More information about our implementation details can be found below.

# Methodology

## Data Collection
We used Intel's X Library Software Development Kit to develop a system usage data collector on our Windows 10 device. Upon signing into the system, the collector automatically launches and begins tracking all foreground applications. To ensure its reliability in real-world scenarios, we followed these principles:
<br>

1. <strong>Robustness and Resilience</strong>

      To ensure that our program continues to run without requiring human intervention in the event of errors during deployment, we have implemented defensive coding practices. We have verified the data type and range of variables before feeding them into functions. If an error occurs, we log the error type, the file that generated the error, the line number within the file, and the timestamp. This enables us to identify faulty code while reviewing error logs. Through this approach and rigorous testing, we were able to keep our collector running without errors for eight weeks.

2. <strong>Privacy Compliance</strong>

      To obtain the name of the foreground window application, we must locate the application's file path, which may contain Personal Identifiable Information (PII) such as a person's full legal name. To prevent the collection of PII, we have implemented a process to remove any PII from the file path before storing the collected information. For example, if a user has named their system after their legal name, we exclude the full file path to prevent the collection of PII.

3. <strong>Efficiency</strong>

      We have optimized the code to reduce the impact on system resources, such as CPU and memory usage, by minimizing unnecessary processing and data transfer. This is crucial as we want the application to run continuously in the background while the computer is on. To achieve this, we only allocate the minimum necessary memory to arrays and expand them as needed, ensuring efficient use of system resources.

4. <strong>Compatibility</strong>

      We have designed the data collector to be compatible with a wide range of languages by changing our collected strings from ANSI to UNICODE to capture foreign characters. This enables us to accurately capture and store data in different languages, ensuring compatibility with various software applications and operating systems.

### Results
Here is a snippet of the 8 week of raw data

| MEASUREMENT_TIME        | ID_INPUT | VALUE               | PRIVATE_DATA |
|-------------------------|----------|---------------------|--------------|
| 2023-02-22 15:16:11.231 |    3     | Discord.exe         |      0       |
| 2023-02-22 15:16:22.683 |    3     | explorer.exe        |      0       |
| 2023-02-22 15:16:31.341 |    3     | firefox.exe         |      0       |
| 2023-02-22 15:17:01.379 |    3     | Teams.exe           |      0       |
| 2023-02-22 15:17:03.605 |    3     | firefox.exe         |      0       |
| 2023-02-22 15:17:34.905 |    3     | explorer.exe        |      0       |
| 2023-02-22 15:17:37.986 |    3     | Code.exe            |      0       |
| 2023-02-22 15:17:56.994 |    3     | firefox.exe         |      0       |
| 2023-02-22 15:17:58.600 |    3     | Code.exe            |      0       |
| 2023-02-22 15:18:01.654 |    3     | firefox.exe         |      0       |
| 2023-02-22 15:18:16.922 |    3     | CodeSetup.tmp       |      0       |
| 2023-02-22 15:18:20.113 |    3     | firefox.exe         |      0       |
| 2023-02-22 15:22:00.113 |    3     | explorer.exe        |      0       |
| 2023-02-22 15:22:03.071 |    3     | Code.exe            |      0       |
| 2023-02-22 15:24:27.911 |    3     | firefox.exe         |      0       |

<br>
<details close>
<summary> If you want to learn about the obstacles we faced, click here: </summary>
<br>

1. <strong>Unfamiliar Environment</strong>
<br> <br>
      As the programming language C was not initially included in our Data Science curriculum, we had to quickly learn and adapt to this new coding environment within a tight 2-week deadline. One of the initial challenges we encountered was the lack of immediate feedback on our code. Unlike in Python Jupyter Notebooks, where we could easily run a block of code and print out results to diagnose any issues, in Visual Studio, we had to rely on our judgment that the entire code block was functioning correctly. Fortunately, when we asked our mentor for guidance, they were able to teach us how to use the debugging mode, which significantly improved our ability to identify and fix errors in our code.
<br> <br>

2. <strong>Oudated Documentation/Setting up the Environment</strong>
<br> <br>
      Everybody dreads setting up the coding environment for a new role. It's the least enjoyable part of the coding experience. For us, we had to install internal software using documentation that was written 6 years ago. Some of the changes that happened since then are not documented and not well tested. For regular software, we can just use an installer and open the application. This, however, requires us to follow specific instructions such as where to extract the folder and how to edit the configuration files. This was particularly frustrating because the engineers implemented a fix to the program without throughout testing and documentation. Our mentors were unable to help because they already had the environment set up and are not familiar with the propagated changes. This caused us a precious week to read through the document code to trace the error and get started on writing the code.
<br> <br>

3. <strong>Win32 API</strong>
<br> <br>
      The official API documentation is helpful but lacks examples, making it challenging to use. When we tried to get the title of the foreground window the user is currently on, we located two functions: GetWindowTextA, and GetWindowTextW. Since GetWindowTextA is the first result on Google, I used that function until I discovered that it is not capturing the text of a window that has Chinese characters. Upon further investigation, we discovered that A stands for ANSI and return an ANSI string and W stands for wide-character which returns a Unicode string. It would not be easy to spot such a mistake at first glance because the API description for these two functions is almost identical. The only difference is that the output variable is named LPWSTR for the GetWindowTextW function and LPSTR for the GetWindowTextA function. These information are not readily available on forums such as StackExchange, making this task a lot harder.
<br>
</details>
<br>
## Model Building
To get a good sense of how the user interact with their computer, we chose the Hidden Markov Model and Long Short Term Memory model to help us learn patterns from the data.
Task 1. Next-App Prediction: Hidden Markov Model<br> 
In task one, our goal is to predict the next application the user will use based on the previous usage data.<br> 
Task 2. App Duration Prediction: Long Short- Term Memory<br> 
We focused on using Firefox as the primary application for predicting the duration of usage during a specific hour.<br> 
  
### Hidden Markov Model (HMM)

Hidden Markov Model is commonly used to model sequential data, which makes this a particularly good choice to predict the next application that the user will open. To understand HMM, we must understand Bayes' Rule.

<img src="assets\BayesRule.png" class="center" alt="Bayes' Rule." />

In plain English, this means that the probability of event A occuring given that event B occured is the probability of event A and B occuring together divided by the probability of event B happening. In our case, we simply need to count the number of times an application, such as Zoom, is used after the user was using Google Chrome. You can see a list of application used following the use of our commonly used application.

<img src="assets\frequent_app_prob.png" class="center" width=1000 alt="A heatmap of the conditional probabilities" />

To evaluate our Hidden Markov Model, we measured the accuracy based on whether the predicted application falls within the top N probability given an application. We selected this metric to give the model an acceptable margin of error within its predictions.

| Top N  | Accuracy |
|--------|----------|
| 1      | 48%      |
| 2      | 65%      |
| 3      | 75%      |

If we want to model a user's day on the computer, we can simply add an emission matrix so that whenever the model is making a prediction about the next used application, it will decide whether the current application is likely to the last application of the session or it will be followed by another application.

### Long Short-Term Memory (LSTM)
<img src="assets\image002.png" class="center" width=1000 alt="Image of the average launch time of Google Chrome and Windows Explorer across machines of varying ages." />
To forecast hourly application usage, we narrowed our focus to the web browser Firefox and built an initial LSTM model. We selected Firefox because users typically spend a significant portion of their computer time browsing the web, whether for reading news, watching videos, or communicating with colleagues. By training our model to recognize usage patterns for one web browser, we can scale it to learn patterns across different applications. 

We have decided to use Tensorflow's Keras package, a high-level neural network API for Python, to implement LSTMs as a layer in a neural network. In an LSTM network, the hidden state is updated at each time step by combining the values of the input, forget, and output gates, and the memory cells are updated accordingly. This process allows the LSTM to selectively store or forget information over a long period of time, making it well-suited for tasks such as speech recognition, natural language processing, and time-series prediction. Just like figue below, data such as process names and dates are imported and multiple hidden layers are updated to output the next name/duration of the processes. 

<img src="assets\many_to_one.jpg" class="center" width=800 alt="LSTM" />

Input Data:
- Numerical feature: 
  - Scaled app duration
- Binary features: 
  - Hour - Time of day in One-Hot Encoded format
  - Month - Month in One-Hot Encoded format
  - Minute - Minutes in One-Hot Encoded format
  - Date - Day of the month in One-Hot Encoded format
  - Weekday - Day of the Week (e.g. Monday, Tuesday) in One-Hot Encoded format
  - Is_Weekend - A binary number. 1 represents a weekend and -1 a week day
  - Is_Winter_Holiday: A binary number. 1 represents a winter holiday and -1 for every other date.

Explanation of our Input Selection: 

Hour, minute, and date are selected because we want to study usage pattern at an hourly level and the time the application is opened can be used to find patterns in how long it was open for given the similiar conditions. Month is used to distinguish between the holiday season and school season since the data collection process started in mid-December and ended in February. Insufficient data is gather for the model to learn trends for every individual month. Day of the week, is_weekend, and is_winter_holiday are all features engineered from exisiting data. These variables separate the data into categories so that the computer can distinguish usage pattern for a productive day from an entertainment day. 

Performance Metric: 

Accuracy and the Mean Squared Error Loss. Accuracy is tuned with a margin of error in mind and the acceptable error range between 5 seconds to 60 seconds. This is to give the model a bit of leeway for when it predicts the amplitude correct but is off by a few seconds to a minute. This allows the model to adjust the prediction time without making much modification to the amplitude. MSE is chosen because the function is differentiable and easier for the model to find the optimal hyperparameters to converge. 

<iframe src="assets\experiment5.html" min-width = "600" width="100%" height=600 overflow=auto></iframe>

Results:

| Metric              | Train Result | Test Result |
|---------------------|--------------|-------------|
| MSE Loss            | 0.0038       | 0.1384      |
| Accuracy within 5s  | 84%          | 79%         |
| Accuracy within 10s | 85%          | 80%         |
| Accuracy within 10s | 86%          | 82%         |

# Pitfall and Shortcoming

We hypothesize that the high accuracy yieled in our Test result was the result of getting predictions of 0s correctly. That means it is getting a high accuracy without actually learning the ampltidue of the usage time. This means that it is slightly overfitting to our training data and does not do well with unseen data. To mitigate this issue, we can change our metric to give more penalty to guessing the amplitude wrong and less rewards for guessing the zeors correctly. This should counteract the imbalance in active usage class from the inactive use and instruct the model to focus on learning where the amplitude occurs more.

# Conclusion

The models we have built here establishes the fundamental building block for predicting the app launch time. With the Hidden Markov Model, we are able to model a sequence of application expected to be used during a session and we can fine tune the model further using LSTM to pick up patterns and trends based on the time of day the computer starts up. In the sequence of application generated, we can use our LSTM model to draw up each application's expected usage time and identify applications that satisfy the requirements for a predictive launch. If more time and resources are dedicated to this matter in the future, we can measure whether our predictive launches are useful or not and fine-tune the model. We can collect this additional data by going back to our collector and change our user_wait input library to be activated whenever the user clicks on another application and the mouse icon changes to waiting.  

# Mentors

We want to give a shoutout to all of the mentors at the Intel DCA & Telemetry team for providing guidance throughout this whole project. Big thanks to Jamel for being such a passionate mentor and teaching us how to be a better, well rounded engineer on top of being a data scientist. Bijan for faciliitating the environment for learning and encourages us to push out of our comfort zones. Sruti for teaching us how to create our own HMM model. Oumaima for giving us endless suggestions on how to improve our model by playing around with our inputs. Praveen for teaching us how to automate our collection process. Teresa for being a great TA and making sure that we receive the feedback from the mentors in a timely manner.

- Bijan Arbab
- Jamel Tayeb
- Sruti Sahani
- Oumaima Makhlouk
- Teresa Rexin
- Praveen Polasam
- Chansik Im

# Glossary

Intel XLSDK
: Intel X Library Software Development Kit (XLSDK) is a proprietary development kit that is used to capture system usage report on the Windows Operating System. It is written in the programming language C and utilizes the Windows 32 Application Programming Interface (API) to communicate with the system kernel.

Long Short-Term Memory / LSTM
: Long Short-Term Memory, commonly known as LSTM is a type of Recurrent Neural Network (RNN) architecture that is commonly used in machine learning for processing sequential data, such as speech, text, and time-series data.

Application Programming Interface (API)
: Application Programming Interface is a way to abstract away the implementation details of a program and allow users or programs to interact with each other in a high level. For example, you can think of an ATM as an API. You tell the ATM that you want to withdraw cash from your account, and the ATM will take care of the details behind such instruction. API is used by programmers to communicate with programs written by another developer.
