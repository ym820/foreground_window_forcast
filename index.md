---
layout: page
title: "Foreground Window Forecast"
permalink: /
---
By Alan Zhang, Mandy Lee, Mike Mao

<link rel="stylesheet" href="style.css">
<iframe src="assets\experiment5.html" width=100% frameBorder=0></iframe>

---
* TOC
{:toc}

---

# Introduction
<img src="assets\avg_launch_time.png" class="center" height=600 alt="Image of the average launch time of Google Chrome and Windows Explorer across machines of varying ages." />

Long app launch times can be frustrating and hamper productivity, even on new computers. Chrome, for example. takes an average of 11.1 seconds to launch a 0-1 year old device. To address this issue, our proposed solution is to pre-emptively launch applications based on user behavior/usage patterns. Our approach involves using machine learning models, such as Hidden Markov Model and Long Short-Term Memory, to predict which applications should be launched and when, based on system usage reports generated from users.

# Methodology

## Data Collection Using Intel XLSDK
We utilized Intel's X Library Software Development Kit to create a system usage data collector on our Windows 10 machine. The collector is launched automatically upon signing into the system and begins tracking all of the foreground applications. To ensure its reliability during real-world usage, we adhered to the following principles:
1. Robustness and Resilience
As our program may encounter errors during deployment, we implemented defensive coding practices to ensure that the collector can continue to run without requiring human intervention to restart the program. We verified the data type and range of variables before feeding them into a function and, if an error occurred, we logged the error type, the file that generated the error, the line number within the file, and the timestamp. This helped us identify faulty code when reviewing error logs. Along with rigorous testing, we were able to keep our collector running error-free for eight weeks.

2. Privacy Compliance
To obtain the name of the foreground window application, we must locate the application's file path, which may contain Personal Identifiable Information (PII) such as a person's full legal name. Therefore, we removed any PII from the file path before storing the collected information. For example, users may name their system after their legal name, so we must avoid including the full file path.

Here is an example of the data before we preprocessed it for storage and after.

Note: The before over-sampled the esrv.exe 

|                    Before                  |           After         |
|--------------------------------------------|-------------------------|
|  C:\_xlsdk\run\windows\Release\64\esrv.exe |  esrv.exe               |
|  C:\_xlsdk\run\windows\Release\64\esrv.exe |  Missing String.        |
|  C:\_xlsdk\run\windows\Release\64\esrv.exe |  Search                 |
|  C:\_xlsdk\run\windows\Release\64\esrv.exe |  Calculator             |
|  C:\_xlsdk\run\windows\Release\64\esrv.exe |  Running Applications   |

### Results

<details close>
<summary>You can find a snippet of our raw data here</summary>

| MEASUREMENT_TIME        | ID_INPUT | VALUE               | PRIVATE_DATA |
|-------------------------|----------|---------------------|--------------|
| 2023-02-22 15:16:11.231 |    3     | Discord.exe         |      0       |
| 2023-02-22 15:16:22.683 |    3     | explorer.exe        |      0       |
| 2023-02-22 15:16:31.341 |    3     | firefox.exe         |      0       |
| 2023-02-22 15:17:01.379 |    3     | Teams.exe           |      0       |
| 2023-02-22 15:17:03.605 |    3     | firefox.exe         |      0       |
| 2023-02-22 15:17:34.905 |    3     | explorer.exe        |      0       |
| 2023-02-22 15:17:37.986 |    3     | Code.exe	0          |      0       |
| 2023-02-22 15:17:56.994 |    3     | firefox.exe         |      0       |
| 2023-02-22 15:17:58.600 |    3     | Code.exe            |      0       |
| 2023-02-22 15:18:01.654 |    3     | firefox.exe         |      0       |
| 2023-02-22 15:18:16.922 |    3     | CodeSetup.tmp       |      0       |
| 2023-02-22 15:18:20.113 |    3     | firefox.exe         |      0       |
| 2023-02-22 15:22:00.113 |    3     | explorer.exe        |      0       |
| 2023-02-22 15:22:03.071 |    3     | Code.exe            |      0       |
| 2023-02-22 15:24:27.911 |    3     | firefox.exe         |      0       |

</details>
<br>
<details close>
<summary> If you want to learn about the obstacles we faced, click here: </summary>

1. Unfamiliar Environment

As Data Science students that are only familiar with Java and Python, we had to quickly pick up the programming language C and adapt to the new coding environment. The first obstacle we faced was with the lack of instantanous feedback on our code. In Python Jupyter Notebooks, it is very easy to run a block of code and print out results to diagnose the issue. In Visual Studio, however, we have to trust our gut that the entire code block works and identify the problem through the debugging mode.

2. Win32 API

Although the official documention on the API is very good, the lack of examples makes it confusing to use. When we tried to get the title of the foreground window the user is currently on, we located two functions: GetWindowTextA, GetWindowTextW. Since GetWindowTextA is the first result on Google, I used that function until I discovered that it is not capturing the text of a window that has Chinese characters. Upon further investigation, we discovered that the A stands for ANSI and returns an ANSI string and W stands for wide-character which returns a unicode string. It would not be easy to spot such a mistake at first glance because the API description for these two functions are almost identifical. The only difference being that the output variable is named LPWSTR for the GetWindowTextW function and LPSTR for the GetWindowTextA function.

<details>
<summary>More information about ANSI and Unicode</summary>

Human speech/text is encoded into the computer in many ways just like how there are 7139 officially known languages in the world. There are many standards in the world like the imperial measuring system (feet, pounds, miles, etc), widely used by the United States and the metric system, which is commonly used in the rest of the world. ANSI is a US standard on how to store texts inside of our computers developed by the American National Standards Institute (ANSI) and this standards only encompasses the English language. This is a problem because not everyone communicates in English, so a new standard called Unicode is adopted. Unicode is a world standard for storing texts and emoji that is compatible with all officially known languages.

</details>

3. Memory Allocation
</details>

## Model Building
- Hidden Markov Model (HMM)
- Long Short-Term Memory (LSTM)
<img src="assets\image002.png" class="center" alt="Image of the average launch time of Google Chrome and Windows Explorer across machines of varying ages." />


# Results

| MEASUREMENT_TIME        | ID_INPUT | VALUE               | PRIVATE_DATA |
|-------------------------|----------|---------------------|--------------|
| 2022-11-03 23:52:49.941 |    2     | esrv.exe            |      0       |
| 2022-11-03 23:52:49.941 |    3     | VsDebugConsole.exe  |      0       |
| 2022-11-03 23:52:51.912 |    2     | Missing String.     |      0       |
| 2022-11-03 23:52:51.912 |    3     | explorer.exe        |      0       |
| 2022-11-03 23:52:53.153 |    2     | Search              |      0       |

# Pitfall and Shortcoming

# Conclusion

# Contact Information and Mentors

# Glossary

Intel X Library Software Development Kit (XLSDK) is a proprietary development kit that is used to capture system usage report on the Windows Operating System. It is written in the programming language C and utilizes the Windows 32 Application Programming Interface (API) to communicate with the system kernel.