class PipHisto():
    apps_list = []

    def __init__(self, apps_list):
        self.setApps(apps_list)

    def print_pip_histo(self, apps_list=[], version=None, egg=None):
        app_histo = self.pip_histo(apps_list, version, egg)

        header_string = ''
        if version:
            header_string = ' | version'
        print('   # | {0:<25} '.format('App-Name') + header_string)
        vers = ''

        for n in app_histo:
            if version:
                vers = ' | '
                if '==' in n[0]:
                    vers += n[0].split('==')[1]

            print('{0:>4d} | {1:<25} {2}').format(n[1], n[0].split('==')[0], vers)
            vers = ''


    def pip_histo(self, apps_list=[], version=None, egg=None):
        if apps_list:
            self.setApps(apps_list)

        apps = {}
        app_histo = []

        for n in self.apps_list:
            if '#egg=' in n:
                if egg:
                    n = n.split('#egg=')[1]
                else:
                    continue

            if not version:
                n = n.split('==')[0]

            if n in apps.keys():
                apps[n] = apps[n] + 1
            else:
                apps[n] = 1

        # Convert dic to list
        app_histo = [[k, v] for k, v in apps.items()]
        # Sort list by name
        app_histo = sorted(app_histo, key=lambda x: x[0], reverse=False)
        # Sort list by number of installations
        app_histo = sorted(app_histo, key=lambda x: x[1], reverse=True)

        # for k, v in sorted(apps.items(), key=lambda kv: kv[1], reverse=True):
        #     app_histo.append([k, v])

        # app_histo = l

        return app_histo

    def setApps(self, apps_list):
        self.apps_list = apps_list
