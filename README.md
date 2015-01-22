# virtualenv-mgr

[virtualenv-mgr](https://github.com/arteria/virtualenv-mgr) is a tool to manage multiple [virtualenv](http://www.virtualenv.org/)s at once.

Use a file with paths to the root of multiple virtualenvs to perform operations in all of them at the same time.

## Features

* Install, uninstall or upgrade specific packages in all virtualenvs at once.
* Print statistic, a histogram, about the usage of packages over all environments. 
* Find/list virtualenvs for further processing, eg. as input for virtualenv-mgr
* Find all envs having a package installed


## Installation 

    pip install virtualenv-mgr
     

## Usage

### Find environments with -z/--envfreeze

Find all virtualenvs ar your current location / subdictionarys (look for the '/bin/activate' pattern)

    virtualenv-mgr --envfreeze
    virtualenv-mgr -z
    
Define a searchroot, where the scrip should search in:

    virtualenv-mgr --envfreeze --searchroot /Users/name/workspace/2014
    virtualenv-mgr -zs /Users/name/workspace/2014
    
Save the paths to a file which you can use later.

    virtualenv-mgr -zs /Users/name/workspace/2014 > example-env-file.txt

### Define Environments

Environments from a list:

    virtualenv-mgr example-env-file.txt

Or input over a pipe:

    virtualenv-mgr --envfreeze | virtualenv-mgr

No arguments --> active virtualenv

    virtualenv-mgr
    
### Actions

Install a package / multiple packages

    virtualenv-mgr example-env-file.txt -i "django==1.4.16,djangotransmeta"
    
Uninstall a package / multiple packages
    
    virtualenv-mgr example-env-file.txt -u "django==1.4.16"
        
Find packages / multiple packages (can look for exact packages '==' or if the package is installed)

    virtualenv-mgr example-env-file.txt -f "django==1.4.6"
    
Install or Uninstall packages in envs where certain other packages are installed.

    virtualenv-mgr example-env-file.txt -f "django==1.4.12" -i "django==1.4.16" -u "django-transmeta"
    
All virtual-environments which have installed django==1.4.12 will install django==1.4.16 and uninstall django-transmeta.
    
### Pip Histo

print the pip histo ( overview over all installed packages)

    virtualenv-mgr example-env-file.txt -p
    
Distinguishes between different versions

    virtualenv-mgr example-env-file.txt -p -v
    
Take eggs into the histo

    virtualenv-mgr example-env-file.txt -p -e
    
Combine

    virtualenv-mgr example-env-file.txt -pve

### Pip Option

pipoption allows you to add options to the pip command, use the ',' to separate multiple commands

    virtualenv-mgr example-env-file.txt -i django==1.4.18 -o='--index-url=http://pypi.example.com/pypi,--extra-index-url=http://pypi.python.org/simple'
    
 
## Help
=======

 
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

 

 

Pip Option

* -o, --pipoption,          allows you to add options to the pip command(-i/--install and -u/--uninstall) 
 
 
 # Supported platforms 
 =======
 * OS X
 * Linux/UNIX
 
 Windows support was not tested yet.  Please feel free to contribute.
 