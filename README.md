# Kiosk app

This project is a basic cashbox system for small kiosk’s, stall’s and sales. The backend is build in python, the frontend with the three web design technologies HTML, CSS and JavaScript. You are invited to improve the system and contribute to the project. Just ask if there are questions.


## install

Requirements:
- git (>=1.8)
- python3 (>= 3.6)

Clone the repository:
```shell
# this is important to get the German language package with the right encoding
git config --local core.precomposeunicode true
git clone https://github.com/DoctorFuchs/kiosk
```

## configurate
*Please not that the configuration file (config.ini) are only available after first run.*

To setup contact information of the administrator for support reasons, edit the contact ways in config.ini (threre are some examples).
The most values are self explaining. However if you need help open an issue :D

## run

```shell
cd <kiosk_folder>
python3 server
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
The frontend is designed in German language (because it is an assignment from Germany).
All comments, readme's or tips are in English.
Therefor we are no English native speaker so feel free to submit your language improvements.

If you have a question, open an issue in this repository.
