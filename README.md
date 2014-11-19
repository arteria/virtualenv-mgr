# virtualenv-mgr

Tool to manage multiple virtualenv environments. Uses a file with the paths to multiple virtuale environments to manage all at the same time. You can install / deinstall packages and upgrade spesific ones. The tool can print out a statistic about the usage of packages over all environments.



## Quickstart

Install envmanager:

    pip install git+https://github.com/yannik-ammann/Virtualenv-Manager.git git+https://github.com/yannik/virtualenv-api.git
    


## Usage

### Find environments with -z/--envfreeze

Find all virtualenvs ar your current location / subdictionarys (look for the '/bin/activate' pattern)

    epm.py --envfreeze
    epm-py -z
    
Define a searchroot, where the scrip should search in:

    epm.py --envfreeze --searchroot /Users/name/workspace/2014
    epm.py -zs /Users/name/workspace/2014
    
Save the paths to a file which you can use later.

    epm.py -zs /Users/name/workspace/2014 > example-env-file.txt

### Define Environments

Environments from a list:

    epm.py example-env-file.txt

Or input over a pipe:

    epm.py --envfreeze | epm.py

No arguments --> active virtualenv

    epm.py
    
### Actions

Install a package / multiple packages

    epm.py example-env-file.txt -i django==1.4.16,djangotransmeta
    
Uninstall a package / multiple packages
    
    epm.py example-env-file.txt -u django==1.4.16
        
Find packages / multiple packages

    epm.py example-env-file.txt -f django==1.4.6
    
Install or Uninstall sertain packages in envs where certain other packages are installed.

    epm.py example-env-file.txt -f django==1.4.12 -i django==1.4.16 -u django-transmeta
    
All virtual-environments which have installed django==1.4.12 will install django==1.4.16 and uninstall django-transmeta.
    
### Pip Histo

print the pip histo ( overview over all installed packages)

    epm.py example-env-file.txt -p
    
Distinguishes between different versions

    epm.py example-env-file.txt -p -v
    
Take eggs into the histo

    epm.py example-env-file.txt -p -e
    
Combine

    epm.py example-env-file.txt -pve
    
###Help:

Envfreeze:
*  -z, --envfreeze,      prints all the envs on .
*  -s SEARCHROOT, --searchroot SEARCHROOT, path for envfreeze, where to search

Actions
*  -f FIND, --find FIND  find app, use commas to search for more
*  -i INSTALL, --install INSTALL installes an app, use commas to add more
*  -u UNINSTALL, --uninstall UNINSTALL uninstalles an app, use commas to add more

Pip Histo
*  -p, --piphisto,        pip histogram
*  -e, --egg,             pip histogram takes eggs into consideration
*  -v, --version,         pip histogram takes versions into consideration
