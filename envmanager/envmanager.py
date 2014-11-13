from virtualenvapi.manage import VirtualEnvironment
from os import linesep

class EnvManager():
    envs=[]

    def __init__(self,file_name=None,env_list=None):
        if file_name:
            self.setEnvs(file_name)
        elif env_list:
            for n in env_list:
                self.setEnvs(n)

    def freezeList(self):
        freezes = []
        for n in self.envs:
            for app in n.pip_freeze:
                freezes.append(app)
        return freezes

    def setEnvs(self, file_name):
        f = open(file_name, 'r')
        env_paths = f.read().split(linesep)
        for n in env_paths:
            self.envs.append(VirtualEnvironment(n))

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
            if n.is_installed(find):
                found.append([n])
                print '%s is installed in %s' % (find, n)
            else:
                print '%s is not installed in %s' % (find, n)
        return found

    def install(self, app_name):
        for n in self.envs:
            print 'is installing %s in %s' % (app_name,n)
            n.install(app_name)
            print 'done with: %s' % (n)

    def up(self,current,up):

        for n in self.envs:
            if n.is_installed(current):
                print 'is updating %s' % (n)
                n.install(up)
                print 'is done'
