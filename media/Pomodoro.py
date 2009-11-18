from pyjamas.ui.Label import Label
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.ListBox import ListBox
from pyjamas.ui import KeyboardListener

from pyjamas.JSONService import JSONProxy

class PomodoroApp:
    def onModuleLoad(self):
        self.remote = DataService()
        panel = VerticalPanel()

        self.nameTextBox = TextBox()
        self.successStatementTextBox = TextBox()
        self.successStatementTextBox.addKeyboardListener(self)

        self.projectList = ListBox()
        self.projectList.setVisibleItemCount(7)
        self.projectList.setWidth("200px")
        self.projectList.addClickListener(self)

        panel.add(Label("Add New Project:"))
        panel.add(self.nameTextBox)
        panel.add(self.successStatementTextBox)
        panel.add(Label("Click to Remove:"))
        panel.add(self.projectList)

        self.status = Label()
        panel.add(self.status)

        RootPanel().add(panel)
        self.remote.getProjects(self)



    def onKeyUp(self, sender, keyCode, modifiers):
        pass

    def onKeyDown(self, sender, keyCode, modifiers):
        pass

    def onKeyPress(self, sender, keyCode, modifiers):
        """
        This functon handles the onKeyPress event, and will add the item in the text box to the list when the user presses the enter key.  In the future, this method will also handle the auto complete feature.
        """
        if keyCode == KeyboardListener.KEY_ENTER and (sender == self.successStatementTextBox or sender == self.nameTextBox):
            id = self.remote.addProject(self.nameTextBox.getText(), self.successStatementTextBox.getText(), self)
            self.successStatementTextBox.setText("")
            self.nameTextBox.setText("")

        if id<0:
            self.status.setText("Server Error or Invalid Response")


    def onClick(self, sender):
        id = self.remote.deleteProject(sender.getValue(sender.getSelectedIndex()),self)
        if id<0:
            self.status.setText("Server Error or Invalid Response")

    def onRemoteResponse(self, response, request_info):
        self.status.setText("response received")
        if request_info.method == 'getProjects' or request_info.method == 'deleteProject':
            self.projectList.clear()
            for project in response:
                self.projectList.addItem(project["name"])
                self.projectList.setValue(self.projectList.getItemCount()-1,project["id"])
        elif request_info.method == 'addProject':
            self.status.setText(self.status.getText() + "HERE!")
            self.projectList.addItem(response["name"])
            self.projectList.setValue(self.projectList.getItemCount()-1,response["id"])
        else:
            self.status.setText(self.status.getText() + "none!")

    def onRemoteError(self, code, message, request_info):
        self.status.setText("Server Error or Invalid Response: ERROR " + code + " - " + message)

class DataService(JSONProxy):
    def __init__(self):
        JSONProxy.__init__(self, "/services/", ["getProjects", "addProject","deleteProject"])

if __name__ == "__main__":
    app = PomodoroApp()
    app.onModuleLoad()

