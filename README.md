# EchoOne
Started as part of the CSE Hackathon 2018

Python script which navigates Echo360 allowing you to download multiple lectures and then renames them to CourseCode\_00.mp4

## The issues with Echo360
When you try to download lectures off Echo360 it names them as either hd1.mp4 or sd1.mp4 no matter what course or lecture it is. This is especially annoying when you want to download more than one lecture as you must keep track of the order you started the downloads in, wait then rename them yourself.

## Current limitations
Unfortunately this year UNSW's Single Sign On does not work most of the time (it gives the error page linked below)
For now we've implemented a work around where the script tries to log on approximatly every minute until it works.
Eventually it will log on (usually within 5 miniutes) but make sure you enter the correct zid and password

https://login.echo360.org.au/login/pingone/error?errorcode=SAML_003[61c24290]&message=We+received+an+unsuccessful+response+from+your+IdP.+Contact+your+administrator+or+an+IdP+administrator+for+more+information.%0AResponse+status%3A+urn%3Aoasis%3Anames%3Atc%3ASAML%3A2.0%3Astatus%3AResponder)

## Required packages/installation
You need selenium
```
pip install selenium
or
pip install -r requirements.txt
```
and you need a chrome driver https://selenium-python.readthedocs.io/installation.html#drivers

## Guide
You will be prompted for the following information in order:
1. UNSW zid (include the z)
2. UNSW password
3. Choose a course
4. Choose a lecture to start downloading from
5. Choose a lecture to finish downloading at
6. Choose HD or SD video

### Example terminal input/output
User inputs are in double quotes


```
UNSW zID: "z5122521"
Password: "YOUR PASSWORD"
The UNSW single sign on system is sometimes broken....
Logged in after 5 tries in 444.0 seconds
Your Courses:
0: COMP3331 Computer Networks&Applications +
1: SENG2021 Reqts & Design Workshop
2: COMP2111 System Modelling and Design

Select a Courses Corresponding Number: "2"
Your Lectures:
18/02/2019: 0
20/02/2019: 1
25/02/2019: 2
27/02/2019: 3
04/03/2019: 4

Select First Lecture To Download: "1"

Select Last Lecture To Download: "3"

Download High Definition video? (y/n): "y"
Download finished and renamed to COMP2111_01.mp4
Download finished and renamed to COMP2111_02.mp4
Download finished and renamed to COMP2111_03.mp4
```
