from virtualenvapi.manage import VirtualEnvironment
from os import linesep, environ


class EnvManager():
    envs = []

    def __init__(self, file_name=None, env_list=None):
        self.setEnvs(file_name, env_list)

    def freezeList(self, envs=False):
        env_list = self.envs
        if envs:
            env_list = envs
        freezes = []
        for n in env_list:
            try:
                for app in n.pip_freeze:
                    freezes.append(app)
            except:
                print('%s error, freezeList' % (n))

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
        app_list = []
        f = open(file_name, 'w+')
        for n in self.envs:
            for app in n.pip_freeze:
                # app_list.append(app)
                f.write(app + '\n')
        # for n in app_list:
        #    f.write(n+'\n')
        f.close()

    def finder(self, find, envs=False):
        env_list = self.envs
        if envs:
            env_list = envs

        found = []

        for n in env_list:
            try:
                if n.is_installed(find):
                    found.append(n)
                    print('%s installed in %s' % (find, n))
                else:
                    print('%s not installed in %s' % (find, n))
            except:
                print('%s error, finder function' % (n))
        return found

    def install(self, app_install, envs=False, pipoption=[]):
        env_list = self.envs
        if envs:
            env_list = envs

        for n in env_list:
            try:
                print('installing %s in %s' % (app_install, n))
                n.install(app_install, options=pipoption)
                print('done with: %s' % (n))
            except:
                print('%s error, install function' % (n))

    def uninstall(self, app_uninstall, envs=False, pipoption=[]):
        env_list = self.envs
        if envs:
            env_list = envs

        for n in env_list:
            try:
                print('uninstalling %s in %s' % (app_uninstall, n))
                n.uninstall(app_uninstall, options=pipoption)
                print('done with: %s' % (n))
            except:
                print('%s error, uninstall function' % (n))

    def pipDiff(self, notinstalled=False, versiondiff=False):
        
        # app_list and path_list --> table grid
        app_list = []
        path_list = []

        # create diff_dic : dictionary with all apps for every env inside
        diff_dic = {}

        for env in self.envs:
            diff_dic[env.path] = {}
            path_list.append(env.path)

            for app in env.pip_freeze:
                app = app.split('==')
                diff_dic[env.path][app[0]] = app[1]

        path_list.sort()


        for paths in diff_dic.values():
            for app in paths.keys():
                if app not in app_list:
                    app_list.append(app)

        app_list.sort()

        head = ['apps \\ envs'] + path_list 
        # every row displays a app : its mached to all envs
        rows = []

        for app in app_list:
            row = [app]
            for path in path_list:
                row.append(diff_dic[path].get(app ,'Not installed'))
            rows.append(row)

        head.append('List differences')

        # check the differences of the installed apps
        diff = []

        for row in rows:
            vers = row[1:]
            vers.sort()
            if vers[0] == vers[-1]:
                diff.append('')
            else:
                diff.append('{} - {}'.format(vers[0],vers[-1]))

        for index, row in enumerate(rows):
            row.append(diff[index])

        # fill the last column of the table with the differences
        body = []
        if notinstalled and versiondiff:
            for row in rows:
                if 'Not installed' in row[-1] or row[-1] is not '':
                    body.append(row)
        elif notinstalled:
            for row in rows:
                if 'Not installed' in row[-1]:
                    body.append(row)
        elif versiondiff:
            for row in rows:
                if row[-1] is not '' and 'Not installed' not in row[-1]:
                    body.append(row)
        else:
            body = rows

        return {'head':head,'body':body}



