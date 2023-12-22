# Dishcover
A proof of concept for Dishcover - a website that lets friends send missions to try new dishes to each other.

## Table of Contents
1. [To Run](#to-run)
2. [Explanation of Webpages and their URL's](#explanation-of-webpages-and-their-urls)
3. [Tools I Used](#tools-we-used)
4. [Notes](#notes)
5. [Directory Tree](#directory-tree)

## To run:
1. Download this code and unzip the files
2. Open a terminal into the `/dishcover` directory
2. Run server.py with the command `python server.py` in the terminal
3. Go to `localhost:3000` in the browser

## Explanation of Webpages and their URL's:
1. localhost:3000/ is the Home page
2. localhost:3000/createmission is the Create Missions page
3. localhost:3000/sentmission/\<mission-code\> shows information about a created mission
4. localhost:3000/currentacceptedmission shows an accepted mission
5. localhost:3000/createmissionupdated shows curated categories of local restaurants
6. localhost:3000/exampleofguide/\<category\> shows more details about restaurants in a guide
7. localhost:3000/notifications is the Notifications page
8. localhost:3000/profile is the Profile page
9. localhost:3000/publishmission is the Publish Missions page
10. localhost:3000/sentmissionsupdated shows all currently created missions
11. localhost:3000/yourmissions is the page for Your Missions

## Tools I Used:
* I used Figma and TeleportHQ as GUIs for creating the HTML and CSS pages
* I used JavaScript to prettify Flask's default image upload buttons
* I used Flask for our backend
* I used GitHub, Git, PythonAnywhere, and VSCode to code our project

## Notes:
* After you create or publish a mission, the missions are saved in local JSON databases called `create_missions_database.json` and `publish_missions_database.json` respectively. The proof of concept does not have online communication of missions between users yet
* The proof of concept uses a local database called `restaurant_database.json` to create the curated restaurant guides

## Directory Tree:
dishcover/<br>
├─ static/<br>
│  ├─ public/<br>
│  │  ├─ external/ (All Dishcover app images)<br>
|  |  ├─ restaurant_images/ (All images for restaurant_database.json)<br>
|  ├─ user_mission_images/<br>
|  |  ├─ create_user_mission_images/ (Images that users uploaded when creating missions)<br>
|  |  ├─ publish_user_mission_images/ (Images that users uploaded when publishing missions)<br>
│  ├─ ALL CSS FILES HERE<br>
├─ templates/<br>
│  ├─ ALL HTML FILES HERE<br>
├─ .gitignore<br>
├─ package.json<br>
├─ README.md<br>
├─ restaurant_database.json<br>
├─ server.py<br>
├─ create_missions_database.json (created when a mission is created)<br>
├─ publish_missions_database.json (created when a finished mission is published)<br>
