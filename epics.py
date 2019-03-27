import ui
import console 

class ReleaseDelegate(object):
    def tableview_did_select(self, tv, section, row):

        epics = ui.View()
        epics.background_color = 'blue'

        nav.push_view(epics)

releases = ui.TableView()
ds = ui.ListDataSource([1,2,3])

releases.data_source = ds 
releases.delegate = ReleaseDelegate()

nav = ui.NavigationView(releases)
nav.present()

