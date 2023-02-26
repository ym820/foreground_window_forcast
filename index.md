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
<img src="assets\avg_launch_time.png" class="center" alt="Image of the average launch time of Google Chrome and Windows Explorer across machines of varying ages." />
The Windows operating system is designed to be compatible with a wide spectrum of machines with diverse technical specifications. The versatility poses a challenge for app developers. To meet the needs of most Windows users, these developers design their applications to be compatible with the median machine specification, which can lead to longer app launch times on computers with less horsepower, even for newly purchased laptops. The speed of app launches is a critical element of the overall user experience. According to an internal study conducted by the Intel Telemetry and DCA team, launching Chrome on a 0-1 year old machine takes an average of 11 seconds. This can cause frustration and hampering productivity. Our aim is to make devices feel more responsive.

Long app launch time could be attributed to a variety of factors such as the performance of architecture the application is built on, the processing speed of older hardwares, and inefficient coding practices that results in unoptimized code. A potential solution to this issue is to pre-emptively open applications before the user needs them. Our approach to addressing this challenge involves collecting system usage reports from users to analyze their habits and using this data to train machine learning models to predict which applications should be launched and when. We will mainly use two machine learning models that are well-suited for time-series data, the Hidden Markov Model (HMM) and Long Short-Term Memory (LSTM) model. Hidden Markov Model will be used to predict the sequence of applications to be used by the user and Long Short-Term Memory model will be used to predict application usage.

# Methodology

## Data Collection Using Intel XLSDK
Intel X Library Software Development Kit (XLSDK) is a proprietary development kit that is used to capture system usage report on the Windows Operating System. It is written in the programming language C and utilizes the Windows 32 Application Programming Interface (API) to communicate with the system kernel.
1) Obstacle 1: Unfamiliar Environment
As Data Science students that are only familiar with Java and Python, we had to quickly pick up the programming language C and adapt to the new coding environment. The first obstacle we faced was with the lack of instantanous feedback on our code. In Python Jupyter Notebooks, it is very easy to run a block of code and print out results to diagnose the issue. In Visual Studio, however, we have to trust our gut that the entire code block works and identify the problem through the debugging mode.
2) Obstacle 2: Win32 API
Although the official documention on the API is very good, the lack of examples makes it confusing to use. When we tried to get the title of the foreground window the user is currently on, we located two functions: GetWindowTextA, GetWindowTextW. Since GetWindowTextA is the first result on Google, I used that function until I discovered that it is not capturing the text of a window that has Chinese characters. Upon further investigation, we discovered that the A stands for ANSI and returns an ANSI string and W stands for wide-character which returns a unicode string. It would not be easy to spot such a mistake at first glance because the API description for these two functions are almost identifical. The only difference being that the output variable is named LPWSTR for the GetWindowTextW function and LPSTR for the GetWindowTextA function.
<details>
<summary>More information about ANSI and Unicode</summary>
<break>
Human speech/text is encoded into the computer in many ways just like how there are 7139 officially known languages in the world. There are many standards in the world like the imperial measuring system (feet, pounds, miles, etc), widely used by the United States and the metric system, which is commonly used in the rest of the world. ANSI is a US standard on how to store texts inside of our computers developed by the American National Standards Institute (ANSI) and this standards only encompasses the English language. This is a problem because not everyone communicates in English, so a new standard called Unicode is adopted. Unicode is a world standard for storing texts and emoji that is compatible with all officially known languages. 
3) 
</details>
3) Obstacle 3: Memory Allocation

### Results


## Model Building
- Hidden Markov Model (HMM)
- Long Short-Term Memory (LSTM)
<img src="assets\image002.png" class="center" alt="Image of the average launch time of Google Chrome and Windows Explorer across machines of varying ages." />


# Results

# Pitfall and Shortcoming

# Conclusion

# Contact Information and Mentors
