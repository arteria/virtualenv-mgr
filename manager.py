#from virtualenvapi.manage import VirtualEnvironment


class EnvManager():
    envs=[]

    def __init__(self,file):
        self.setEnvs(file)

    def list_apps(self, file_name='apps.txt'):
        app_list=[]
        f = open(file_name , 'w+')
        for n in self.envs:
            for app in n.pip_freeze:
                app_list.append(app)
        for n in app_list:
            f.write(n+'\n')
        f.close


    def finder(self,find):
        found = []

        for n in self.envs:
            found.append([n,n.is_installed(find)])
            print 'env %s, val %s' % (found[-1][0], found[-1][1])
        return found

    def install(self, app_name):
        for n in self.envs:
            print 'is installing %s in %s' % (app_name,n)
            n.install(app_name,upgrade=False,force=True)
            print 'done'

    def up(self,current,up):

        for n in self.envs:
            if n.is_installed(current):
                print 'is updating %s' % (n)
                n.install(up,upgrade=False,force=True)
                print 'is done'

    """
    def __init__(self,file,action='find', app_name=['Django','test','test1'], current_version='1.7.1', installation_version=None):
        self.setEnvs(file)

        if 'find' in action:
            envs_with_package = self.find_package(app_name,current_version)
            print envs_with_package


        print 'end'
    """
    def setEnvs(self, file):
        f = open(file, 'r')
        env_paths = f.read().split('\n')
        for n in env_paths:
            self.envs.append(VirtualEnvironment(n))

########################
#Virtualenv api

from os import linesep, environ
import os.path
import subprocess


class VirtualenvCreationException(EnvironmentError):
    pass


class PackageInstallationException(EnvironmentError):
    pass


class PackageRemovalException(EnvironmentError):
    pass



def split_package_name(p):
    """Splits the given package name and returns a tuple (name, ver)."""
    s = p.split('==')
    if len(s) == 1:
        return (s[0].lower(), None)
    else:
        return (s[0].lower(), s[1])


class VirtualEnvironment(object):
    # True if the virtual environment has been set up through open_or_create()
    _ready = False

    def __init__(self, path, cache=None):
        # remove trailing slash so os.path.split() behaves correctly
        if path[-1] == '/':
            path = path[:-1]
        self.path = path
        self.env = environ.copy()
        if cache is not None:
            self.env['PIP_DOWNLOAD_CACHE'] = os.path.expanduser(os.path.expandvars(cache))

    def __str__(self):
        return self.path

    @property
    def _pip_rpath(self):
        """The relative path (from environment root) to pip."""
        return os.path.join('bin', 'pip')

    @property
    def root(self):
        """The root directory that this virtual environment exists in."""
        return os.path.split(self.path)[0]

    @property
    def name(self):
        """The name of this virtual environment (taken from its path)."""
        return os.path.basename(self.path)

    @property
    def _logfile(self):
        """Absolute path of the log file for recording installation output."""
        return os.path.join(self.path, 'build.log')

    @property
    def _errorfile(self):
        """Absolute path of the log file for recording installation errors."""
        return os.path.join(self.path, 'build.err')

    def _create(self):
        """Executes `virtualenv` to create a new environment."""
        proc = subprocess.Popen(['virtualenv', self.name], cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = proc.communicate()
        returncode = proc.returncode
        if returncode:
            raise VirtualenvCreationException((returncode, output, self.name))
        self._write_to_log(output, truncate=True)
        self._write_to_error(error, truncate=True)

    def _execute(self, args, log=True):
        """Executes the given command inside the environment and returns the output."""
        if not self._ready:
            self.open_or_create()
        try:
            proc = subprocess.Popen(args, cwd=self.path, env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = proc.communicate()
            returncode = proc.returncode
            if returncode:
                raise subprocess.CalledProcessError(returncode, proc, (output, error))
            return output
        except OSError as e:
            # raise a more meaningful error with the program name
            prog = args[0]
            if prog[0] != os.sep:
                prog = os.path.join(self.path, prog)
            raise OSError('%s: %s' % (prog, str(e)))
        except subprocess.CalledProcessError as e:
            output, error = e.output
            e.output = output
            raise e
        finally:
            if log:
                try:
                    self._write_to_log(output)
                    self._write_to_error(error)
                except NameError:
                    pass  # We tried

    def _write_to_log(self, s, truncate=False):
        """Writes the given output to the log file, appending unless `truncate` is True."""
        # if truncate is True, set write mode to truncate
        with open(self._logfile, 'w' if truncate else 'a') as fp:
            fp.write(s + linesep)

    def _write_to_error(self, s, truncate=False):
        """Writes the given output to the error file, appending unless `truncate` is True."""
        # if truncate is True, set write mode to truncate
        with open(self._errorfile, 'w' if truncate else 'a') as fp:
            fp.write(s + linesep)

    def _pip_exists(self):
        """Returns True if pip exists inside the virtual environment. Can be
        used as a naive way to verify that the envrionment is installed."""
        return os.path.isfile(os.path.join(self.path, self._pip_rpath))

    def open_or_create(self):
        """Attempts to open the virtual environment or creates it if it
        doesn't exist.
        XXX this should probably be expanded to do some proper checking?"""
        if not self._pip_exists():
            self._create()
        self._ready = True

    def install(self, package, force=False, upgrade=False):
        """Installs the given package (given in pip's package syntax) 
        into this virtual environment only if it is not already installed.
        If `force` is True, force an installation. If `upgrade` is True,
        attempt to upgrade the package in question. If both `force` and
        `upgrade` are True, reinstall the package and its dependencies."""
        if isinstance(package, list):
            for n in package:
                self.install(n,force,upgrade)
                return
        if isinstance(package, tuple):
            package='=='.join(package)
            package.lower()
        if not (force or upgrade) and self.is_installed(package):
            self._write_to_log('%s is already installed, skipping (use force=True to override)' % package)
            return
        options = []
        if upgrade:
            options += ['--upgrade']
            if force:
                options += ['--force-reinstall']
        elif force:
            options += ['--ignore-installed']
        try:
            self._execute([self._pip_rpath, 'install', package] + options)
        except subprocess.CalledProcessError as e:
            raise PackageInstallationException((e.returncode, e.output, package))

    def uninstall(self, package):
        """Uninstalls the given package (given in pip's package syntax) from
        this virtual environment."""
        if not self.is_installed(package):
            self._write_to_log('%s is not installed, skipping')
            return
        try:
            self._execute([self._pip_rpath, 'uninstall', '-y', package])
        except subprocess.CalledProcessError as e:
            raise PackageRemovalException((e.returncode, e.output, package))

    def is_installed(self, package):
        """Returns True if the given package (given in pip's package syntax)
        is installed in the virtual environment."""
        if isinstance(package, list):
            dict_installed = {}
            for n in package:
                dict_installed[n]=self.is_installed(n)
                return False not in dict_installed.values()

        elif isinstance(package, str):
            if package.endswith('.git'):
                pkg_name = os.path.split(package)[1][:-4]
                return pkg_name in self.installed_package_names
            pkg_tuple = split_package_name(package)
            if pkg_tuple[1] is not None:
                return pkg_tuple in self.installed_packages
            else:
                return pkg_tuple[0] in self.installed_package_names
        elif isinstance(package, tuple):
            package=tuple(n.lower() for n in list(package))
            return package in self.installed_packages
        
        """
        elif isinstance(package, list):
            dict_installed = {}
            packages = package
            for package in packages:
                if isinstance(package, str):
                    if package.endswith('.git'):
                        pkg_name = os.path.split(package)[1][:-4]
                        #return pkg_name in self.installed_package_names
                        dict_installed[package] = pkg_name in self.installed_package_names
                    pkg_tuple = split_package_name(package)
                    if pkg_tuple[1] is not None:
                        #return pkg_tuple in self.installed_packages
                        dict_installed[package] = pkg_tuple in self.installed_packages
                    else:
                        #return pkg_tuple[0] in self.installed_package_names
                        dict_installed[package] = pkg_tuple[0] in self.installed_package_names
                if isinstance(package, tuple):
                    compare = [(n.lower(),_) for n, _ in self.installed_packages]
                    print compare
                    dict_installed[package] = package in compare
            print dict_installed
            return  False not in dict_installed.values() #(False not in dict_installed.values(),dict_installed)
            """

    def upgrade(self, package, force=False):
        """Shortcut method to upgrade a package. If `force` is set to True,
        the package and all of its dependencies will be reinstalled, otherwise
        if the package is up to date, this command is a no-op."""
        self.install(package, upgrade=True, force=force)

    def search(self, term):
        packages = []
        results = self._execute([self._pip_rpath, 'search', term], log=False)  # Don't want to log searches
        for result in results.split('\n'):
            try:
                name, description = result.split(' - ', 1)
                packages.append((name.strip(), description.strip()))
            except ValueError:
                name, description = packages[-1]
                packages[-1] = (name, description + ' ' + result.strip())
        return packages

    def search_names(self, term):
        return [name for name, description in self.search(term)]

    @property
    def installed_packages(self):
        """List of all packages that are installed in this environment."""
        pkgs = [] #: [(name, ver), ..]
        l = self._execute([self._pip_rpath, 'freeze', '-l']).split(linesep)
        for p in l:
            if p == '': continue
            pkgs.append(split_package_name(p))
        return pkgs

    @property
    def pip_freeze(self):
        """
        freeze = []
        for n in self._execute([self._pip_rpath, 'freeze', '-l']).split(linesep):
            if n == '' or n[0] == '#':
                continue
            freeze.append(n)
            """
        freeze = [n for n in self._execute([self._pip_rpath, 'freeze', '-l']).split(linesep) if not n is '' and not n[0] is '#']
        return freeze

    @property
    def installed_package_names(self):
        """List of all package names that are installed in this environment."""
        return [name.lower() for name, _ in self.installed_packages]

#end virtualenv
###################



if __name__ == '__main__':
    print 'start'
    em = EnvManager(file='list')
    #print em.finder('dJanGo==1.4.1')
    #print out
    #em.up('Django==1.4.1', ('Django','1.4.2'))
    #em.install([('djANgo==1.4.5'),'ipython','django-cms==2.4'])
    em.list_apps('apps.txt')
    print 'end'




