# envmanager

tool to manage multiple virtualenv environments



## Quickstart

Install envmanager:

    pip install git+https://github.com/yannik-ammann/Virtualenv-Manager.git git+https://github.com/arteria/virtualenv-api.git
    


## Usage

### Find environments with -z/--envfreeze

Find all virtualenvs ar your current location / subdictionarys (look for the '/bin/activate' pattern)

    epm.py --envfreeze
    epm-py -z
    
Define a searchroot, where the scrip should search in:

    epm.py --envfreeze --searchroot /Users/name/workspace/2014
    epm.py -zs /Users/name/workspace/2014

### Define Environments

No arguments --> active virtualenv

    epm.py

Environments from a list:

    epm.py example-environment-list.txt
    
Or input over a pipe:

    epm.py --envfreeze | epm.py
    
### Actions

Install a package / multiple packages:

    epm.py -i django==1.4.16,djangotransmeta
    
Find packages / multiple packages

    epm.py -f django==1.4.6
    
Upgrade packages / install sertain packages in env where certain other packages are installed

    epm.py -f django==1.4.6 -i django 1.4.16 django-transmeta
    
### Pip Histo

print the pip histo ( overview over all installed packages in the defined virtualenvs)

    epm.py -p
    
Option for differentiate versions

    epm.py -p -v
    
Take eggs into the histo

    epm.py -p -g
    
Combine

    epm.py -pve
    
Help:

*  -z, --envfreeze       prints all the envs on .
*  -s [SEARCHROOT], --searchroot [SEARCHROOT]   path for envfreeze, where to search


*  -f [FIND], --find [FIND]  find app, use commas to search for more then one
*  -l, --freezelist      pints the freeze_ist of all envs
*  -i [INSTALL], --install [INSTALL] installes an app, use commas to add more then one


*  -p, --piphisto        pip histogram
*  -e, --egg             pip histogram takes eggs into consideration
*  -v, --version         pip histogram takes versions into consideration 
    
    
    
    
    
    