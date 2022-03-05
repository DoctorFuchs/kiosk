# Kiosk app

This project is a basic chashbox system for small kiosk’s, stall’s and sales. The backend is build in python, the frontend with the three web design technologies HTML, CSS and JavaScript. You are invited to improve the system and contribute to the project. Just ask if there are questions.

ATTENTION SINCE 24. DECEMBER 2021 SQL IS NOT LONGER SUPPORTED. BUT YOU NEED TO INSTALL FLASK

## install

Clone the repository:
```shell
git clone https://github.com/DoctorFuchs/kiosk
```

Then make sure python 3 is installed. If not please install (https://www.python.org/downloads/). (We used python 3.6 (tested on 3.9.9))

## configurate
*Please note that the configuration files are only available after first run.*

To setup contact information of the administrator for support reason, edit the config file (kiosk/frontend/config.json). First of all you can fill in the name. Secondly choose your different contacting possibilities. The first value of each holds the name, the second one the link or url (like mailto). Use "!m" to insert the message from below. The third contains the filename of your icon, wich have to be placed in kiosk/frontend/icons folder. The message field holds a personal message, wich you can insert in your links using "!m" there. To automaticly insert author name use "!a" and for a line break "!b" inside the message.
```json
["<Label/Name>", "<link/adress>", "<icon name>"]
```

| where to use | command | what it does      |
|--------------|:-------:|-------------------|
| in links     |    !m   | insert message    |
| in message   |    !a   | insert author     |
|              |    !b   | generate new line |

## run

```shell
cd <kiosk_folder>
python3 run.py
```

### options
```
  -h, --help        show this help message and exit
  -U, --upgrade     Upgrade the kiosk application, only available if git repository (git needs to be installed)
  -u, --update      Force updating dependencies
  -b, --browser     Launch browser while starting
  -w, --window      Launch native looking window
  -f, --fullscreen  Launch window in fullscreen
  -k, --kiosk       Launch chromium's kiosk mode(a 'super' fullscreen, chrom[e/ium] or edge with chromium engine needs to be installed, exit with Alt+F4)
```

## Devs
- codenius
- DoctorFuchs

## Information's
This app is an assignment. 
The frontend is designed in german language (because it is an assignment from germany). 
All comments, readme's or tips are in english. 
Therefor we are no english native speakers so feel free to submit your language improvments.

If you have a question, open an issue in this repository.
