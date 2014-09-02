import os, ui

def full_path(path):
    '''Return absolute path with expanded ~s, input path assumed relative to cwd'''
    return os.path.abspath(os.path.join(os.getcwd(), os.path.expanduser(path)))

def files_and_folders(dir_path='.'):
    files = []
    folders = []
    for filename in sorted(os.listdir(dir_path)):
        if os.path.isdir(os.path.join(dir_path, filename)):
            folders.append(filename)
        else:
            files.append(filename)
    return tuple(files), tuple(folders)

class FileDataSource(object):
    '''ui.TableView data source that generates a directory listing'''
    def __init__(self, path=os.getcwd()):
        self.path = full_path(path)
        self.refresh()
        self.fullpath = None

    def refresh(self):
        '''Refresh the list of files and folders'''
        self.lists = self.files, self.folders = files_and_folders(self.path)
        self.lists = self.folders, self.files

    def tableview_number_of_sections(self, tableview):
        '''Return the number of sections'''
        return len(self.lists)

    def tableview_number_of_rows(self, tableview, section):
        '''Return the number of rows in the section'''
        return len(self.lists[section])

    def tableview_cell_for_row(self, tableview, section, row):
        '''Create and return a cell for the given section/row'''
        cell = ui.TableViewCell()
        cell.text_label.text = os.path.basename(os.path.join(self.path, self.lists[section][row]))
        if not section:
            cell.accessory_type = "disclosure_indicator"
        return cell

    def tableview_title_for_header(self, tableview, section):
        '''Return a title for the given section'''
        return 'Folders Files'.split()[section]

    def tableview_did_select(self, tableview, section, row):
        '''Called when the user selects a row'''
        if section == 0:
            filenav.push_view(make_file_list(os.path.join(self.path, self.folders[row])))
        elif section == 1:
            textctrl.editable = True
            if self.fullpath:
                with open(self.fullpath, "wb") as fp:
                    fp.write(textctrl.text)
            self.fullpath = os.path.join(self.path, self.files[row])
            with open(self.fullpath, "rb") as fp:
                textctrl.text = fp.read()
            view.name = self.files[row]

def make_file_list(path):
    '''Create a ui.TableView containing a directory listing of path'''
    path = full_path(path)
    lst = ui.TableView(name=os.path.basename(path), flex="WH")
    # allow multiple selection when editing, single selection otherwise
    lst.allows_selection = True
    lst.allows_multiple_selection = False
    lst.background_color = 1.0
    lst.data_source = lst.delegate = FileDataSource(path)
    return lst

view = ui.View(name="Text Editor")

textctrl            = ui.TextView(flex="WH")
textctrl.editable   = False
textctrl.bg_color   = (0, 0.106, 0.2)
textctrl.text_color = "white"
textctrl.font       = ("Monofur", 18)
textctrl.x          = 208

lst = make_file_list("~/Documents")
filenav = ui.NavigationView(lst, width=208)
filenav.flex = "H"

view.add_subview(filenav)
view.add_subview(textctrl)
view.present()
