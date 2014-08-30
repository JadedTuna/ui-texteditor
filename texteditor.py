import ui
import os

class FileDataSource(object):
    # ui.TableView data source that generates a directory listing
    def __init__(self, path=os.getcwd()):
        # init
        self.path = full_path(path)
        self.refresh()
        self.lists = [self.folders, self.files]
        self.fullpath = None

    def refresh(self):
        # Refresh the list of files and folders
        self.folders = []
        self.files = []
        for f in os.listdir(self.path):
            if os.path.isdir(os.path.join(self.path, f)):
                self.folders.append(f)
            else:
                self.files.append(f)

    def tableview_number_of_sections(self, tableview):
        # Return the number of sections
        return len(self.lists)

    def tableview_number_of_rows(self, tableview, section):
        # Return the number of rows in the section
        return len(self.lists[section])

    def tableview_cell_for_row(self, tableview, section, row):
        # Create and return a cell for the given section/row
        cell = ui.TableViewCell()
        cell.text_label.text = os.path.basename(os.path.join(self.path, self.lists[section][row]))
        if section == 0:
            cell.accessory_type = "disclosure_indicator"
        return cell

    def tableview_title_for_header(self, tableview, section):
        # Return a title for the given section.
        if section == 0:
            return "Folders"
        elif section == 1:
            return "Files"
        else:
            return ""

    def tableview_did_select(self, tableview, section, row):
        # Called when the user selects a row
        if section == 0:
            filenav.push_view(make_file_list(os.path.join(self.path, self.folders[row])))
        elif section == 1:
            textctrl.editable = True
            if self.fullpath is not None:
                with open(self.fullpath, "wb") as fp:
                    fp.write(textctrl.text)
            self.fullpath = os.path.join(self.path, self.files[row])
            with open(self.fullpath, "rb") as fp:
                textctrl.text = fp.read()
            view.name = self.files[row]

def close_proxy():
    def _close(sender):
        nav.close()
    return _close

def full_path(path):
    # Return absolute path with expanded ~s, input path assumed relative to cwd
    return os.path.abspath(os.path.join(os.getcwd(), os.path.expanduser(path)))

def make_file_list(path):
    # Create a ui.TableView containing a directory listing of path
    path = full_path(path)
    lst = ui.TableView(flex="WH")
    # allow multiple selection when editing, single selection otherwise
    lst.allows_selection = True
    lst.allows_multiple_selection = False
    lst.background_color = 1.0
    lst.data_source = lst.delegate = FileDataSource(path)
    lst.name = os.path.basename(path)
    current_list = lst
    return lst

view = ui.View()
view.name = "Text Editor"

textctrl            = ui.TextView()
textctrl.flex       = "H"
textctrl.editable   = False
textctrl.bg_color   = (0, 0.106, 0.2)
textctrl.text_color = (1, 1, 1)
textctrl.font       = ("Monofur", 18)
textctrl.x          = 208
textctrl.width      = 585

lst = make_file_list("~/Documents")
filenav = ui.NavigationView(lst)
filenav.width = 208
#filenav.height = 585

filenav.flex = "H"

view.add_subview(filenav)
view.add_subview(textctrl)

view.present("fullscreen")
