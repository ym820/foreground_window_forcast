---
layout: page
title: "Foreground Window Forecast"
permalink: /
---

A Capstone project in partnership with the Intel DCA & Telemetry Team <br>
By Alan Zhang, Mandy Lee, Mike Mao

# Introduction

The Windows operating system is designed to be compatible with a wide spectrum of machines with diverse technical specifications. The versatility poses a challenge for app developers. To meet the needs of most Windows users, these developers design their applications to be compatible with the median machine specification, which can lead to longer app launch times on older computers. The speed of app launches is a critical element of the overall user experience. For instance, launching Chrome can take up a minute, causing frustration and hampering productivity. Our aim is to make devices feel more responsive, particularly for older machines.

Long app launch time could be attributed to a variety of factors such as the performance of architecture the application is built on, the processing speed of older hardwares, and inefficient coding practices that results in unoptimized code. A potential solution to this issue is to pre-emptively open applications before the user needs them. Our approach to addressing this challenge involves collecting system usage reports from users to analyze their habits and using this data to train machine learning models to predict which applications should be launched and when. We will mainly use two machine learning models that are well-suited for time-series data, the Hidden Markov Model (HMM) and Long Short-Term Memory (LSTM) model. Hidden Markov Model will be used to predict the sequence of applications to be used by the user and Long Short-Term Memory model will be used to predict application usage.
---
# Methodology
## Data Collection Using Intel XLSDK
## Model Building
- Hidden Markov Model (HMM)
- Long Short-Term Memory (LSTM)

---
# Results
---
# Pitfall and Shortcoming
---
# Conclusion
---
# Contact Information and Mentors
