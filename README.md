# EchoOne
Started as part of the CSE Hackathon 2018 by Marcus Majchrzak, Adam Parslow and Carlin Williamson

Python script which navigates Echo360 allowing you to download multiple lectures and then renames them to CourseCode\_00.mp4

## The issues with Echo360
When you try to download lectures off Echo360 it names them as either hd1.mp4 or sd1.mp4 no matter what course or lecture it is. This is especially annoying when you want to download more than one lecture as you must keep track of the order you started the downloads in, wait then rename them yourself.

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
UNSW zID: "z1234567"
Password: "YOUR PASSWORD"

Your Courses:
    Course   Term LectureStream
 0: MATH2099 19T2 1
 1: COMP3821 19T2 1
 2: MATH2400 19T2 2

Select a Courses Corresponding Number: "2"

Your Lectures:
  0: 03/06/2019
  1: 05/06/2019
  2: 12/06/2019
  3: 17/06/2019

Select First Lecture To Download: "1"

Select Last Lecture To Download: "3"

Download High Definition video? (y/n): "y"

Finished Downloading MATH2400_01.mp4
Finished Downloading MATH2400_02.mp4
Finished Downloading MATH2400_03.mp4
```
