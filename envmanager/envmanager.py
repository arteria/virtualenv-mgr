from virtualenvapi.manage import VirtualEnvironment
from os import linesep, environ

class EnvManager():
    envs=[]

    def __init__(self,file_name=None,env_list=None):
        self.setEnvs(file_name,env_list)

    def freezeList(self):
        freezes = []
        for n in self.envs:
            try:
                for app in n.pip_freeze:
                    freezes.append(app)
            except:
                print '%s may have been moved, freezeList' % (n) 

        return freezes

    def setEnvs(self, file_name, env_list):
        #self.envs = None
        env_paths = []
        if file_name:
            f = open(file_name, 'r')
            env_paths = f.read().split(linesep)
        if env_list:
            env_paths = env_list
        for n in env_paths:
            if n is not '' and '#' not in n:
                ve = VirtualEnvironment(n)
                self.envs.append(ve)


    def checkEnv(self):
        for n in self.envs:
            try:
                n._execute('test')
            except:
                return False
            return True

    def list_apps(self, file_name='apps.txt'):
        app_list=[]
        f = open(file_name , 'w+')
        for n in self.envs:
            for app in n.pip_freeze:
                #app_list.append(app)
                f.write(app+'\n')
        #for n in app_list:
        #    f.write(n+'\n')
        f.close()


    def finder(self,find):
        found = []

        for n in self.envs:
            try:
                if n.is_installed(find):
                    found.append(n)
                    print '%s is installed in %s' % (find, n)
                else:
                    print '%s is not installed in %s' % (find, n)
            except:
                print '%s may have been moved, finder function' % (n) 
        return found

    def install(self, app_name):
        for n in self.envs:
            try:
                print 'is installing %s in %s' % (app_name,n)
                n.install(app_name)
                print 'done with: %s' % (n)
            except:
                print '%s may have been moved, install function' % (n) 

    def up(self,current,up):

        for n in self.finder(current):
            try:
                print 'is updating %s' % (n)
                n.install(up)
                print 'is done'
            except:
                print '%s may have been moved, up function' % (n) 
