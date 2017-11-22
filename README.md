# sonarqube-utils
A set of Sonarqube administrative scripts for managing projects and user access, plus some other stuff. Very much a work in progress.

## Development
* SonarQube 6.6
* Python 2.7

## Usage
### Create a new SonarQube project
```
usage: sq-create-project.py [-h] -n NAME -k KEY [-b BRANCH] [-p]

Utility script to create a new project in SonarQube

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  The name of the project to create
  -k KEY, --key KEY     The unique key of the project to create
  -b BRANCH, --branch BRANCH
                        The name of the branch the project needs associated
                        with it
  -p, --private         Indicates whether the project should be created as
                        private. The default is public.
```

### Create a new login and grant access to groups
```
usage: sq-grant-access.py [-h] -l LOGIN -n NAME [-p PASSWORD] [-e EMAIL]
                          [-s [SCM [SCM ...]]] [-g [GROUP [GROUP ...]]] [-x]

Utility script to grant user access to a project in SonarQube

optional arguments:
  -h, --help            show this help message and exit
  -l LOGIN, --login LOGIN
                        The unique name of the login account
  -n NAME, --name NAME  The name description of the login account
  -p PASSWORD, --password PASSWORD
                        The password for the login account
  -e EMAIL, --email EMAIL
                        The email for the login account
  -s [SCM [SCM ...]], --scm [SCM [SCM ...]]
                        The SCM account name to be associated with the login
                        account. Multiples allowed
  -g [GROUP [GROUP ...]], --group [GROUP [GROUP ...]]
                        The name of a group the user to be assigned to.
                        Multiples allowed
  -x, --external        Indicates whether the login account is external to
                        SonarQube. The default is internal.
```

### List plugins
```
usage: sq-list-plugins.py [-h] [-i] [-p] [-u] [-a]

Utility script to create a new project in SonarQube

optional arguments:
  -h, --help       show this help message and exit
  -i, --installed  List all the plugins installed, sorted by plugin name.
  -p, --pending    List plugins which will either be installed or removed at
                   the next startup, sorted by plugin name.
  -u, --updates    List plugins installed which at least one newer version is
                   available, sorted by plugin name.
  -a, --available  List all the plugins available for installation, sorted by
                   plugin name..

```

