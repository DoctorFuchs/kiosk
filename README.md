# Kiosk app

This project is a basic point of sale system for small kiosk’s, stall’s and sales. The backend is build in python, the frontend with the three web design technologies HTML, CSS and JavaScript. Feel free to improve the system and contribute to the project. Just ask if there are questions.


## install

Requirements:
- git (>=1.8)
- python3 (>= 3.6)

Clone the repository:
```shell
git clone https://github.com/DoctorFuchs/kiosk
# dependencies will be installed automatically in the projects directoy (lib folder)
```

## configurate
*Please not that the configuration file (config.yaml) is only available after the first run.*

To set up contact information of the administrator for support reasons, edit the `contact` section in `config.yaml`. The property `admin_name` is shown as the responsible person for the app and the ways of contact. Each entry in the following `contact_ways` list consists of the attributes listed in the following table. 

| Property | Description                                          |
|----------|------------------------------------------------------|
| name     | display name (hover label, image alt-attribute)      |
| link     | url to start contact (mail, phone, messenger, ...)  |
| icon     | file name of an icon placed in server/frontend/icons |

*Example*
```
-   name: Email
    link: mailto:example@e.mail
    icon: mail.svg
```

All this information is shown on the about page, where you can click a button for each way of contact to head to the related link.

## run

```shell
cd <kiosk_folder>
python3 -m server
```

### options
```
usage: server [-h] [-U] [-u] [-b] [-w] [-f] [-k] {backup} ...

Launcher for kiosk application

optional arguments:
  -h, --help        show this help message and exit
  -U, --upgrade     force updating dependencies
  -u, --update      upgrade the kiosk application, only available if git
                    repository (git needs to be installed)
  -b, --browser     launch browser while starting
  -w, --window      launch native looking window
  -f, --fullscreen  launch window in fullscreen
  -k, --kiosk       launch chromium's kiosk mode(a 'super' fullscreen,
                    chrom[e/ium] or edge with chromium engine needs to be
                    installed, exit with Alt+F4)

Tools:
  {backup}

backup help
usage: server backup [-h] [-i] [-B] [-p] [-l] [-s SHOW] [-r RESTORE]
                     [-d DELETE]

manage database backups

optional arguments:
  -h, --help            show this help message and exit
  -i, --interactive     restore backup interactively
  -B, --backup          create a backup now
  -p, --permanent       access permanent backups (use with another option)
  -l, --list            show list of all backups with date, time and id
  -s SHOW, --show SHOW  view content of a backup
  -r RESTORE, --restore RESTORE
                        restore with id
  -d DELETE, --delete DELETE
                        delete backup forever
```

## Devs
- codenius
- DoctorFuchs

## Information's
This app is an assignment.

All comments, readme's or tips are in English.
Therefor we are no English native speaker so feel free to submit your language improvements.

If you have a question, open an issue in this repository.
