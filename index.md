---
layout: page
title: "Foreground Window Forecast"
permalink: /
---
By Alan Zhang, Mandy Lee, Mike Mao

---
* TOC
{:toc}

---

# Introduction
<img src="assets\avg_launch_time.png" class="align-center" alt="Image of the average launch time of Google Chrome and Windows Explorer across machines of varying ages." />
The Windows operating system is designed to be compatible with a wide spectrum of machines with diverse technical specifications. The versatility poses a challenge for app developers. To meet the needs of most Windows users, these developers design their applications to be compatible with the median machine specification, which can lead to longer app launch times on computers with less horsepower, even for newly purchased laptops. The speed of app launches is a critical element of the overall user experience. According to an internal study conducted by the Intel Telemetry and DCA team, launching Chrome on a 0-1 year old machine takes an average of 11 seconds. This can cause frustration and hampering productivity. Our aim is to make devices feel more responsive.

Long app launch time could be attributed to a variety of factors such as the performance of architecture the application is built on, the processing speed of older hardwares, and inefficient coding practices that results in unoptimized code. A potential solution to this issue is to pre-emptively open applications before the user needs them. Our approach to addressing this challenge involves collecting system usage reports from users to analyze their habits and using this data to train machine learning models to predict which applications should be launched and when. We will mainly use two machine learning models that are well-suited for time-series data, the Hidden Markov Model (HMM) and Long Short-Term Memory (LSTM) model. Hidden Markov Model will be used to predict the sequence of applications to be used by the user and Long Short-Term Memory model will be used to predict application usage.

# Methodology

## Data Collection Using Intel XLSDK
Intel X Library Software Development Kit (XLSDK) is a propritary development kit that is used to capture system usage report on the Windows Operating System. It is written in the programming language C and utilizes the Windows 32 Application Programming Interface (API) to communicate with the system kernel.


## Model Building
- Hidden Markov Model (HMM)
- Long Short-Term Memory (LSTM)


# Results

# Pitfall and Shortcoming

# Conclusion

# Contact Information and Mentors
