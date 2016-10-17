__author__ = 'Nathan'

from PySide import QtGui, QtCore
from Globals import Globals


class PlayerEntry(QtGui.QWidget):
    def __init__(self, player, parent):
        QtGui.QWidget.__init__(self, parent)
        self.player = player
        self.data = parent.data
        self.allQHBoxLayout = QtGui.QHBoxLayout()

        self.draft_order_label = QtGui.QLabel(str(player.draft_round+1))
        self.draft_order_label.setFont(Globals.medium_bold_font)
        self.player_name_label = QtGui.QLabel(player.name)
        self.player_name_label.setFont(Globals.medium_font)
        self.position_label = QtGui.QLabel(player.pos)
        self.position_label.setFont(Globals.medium_font)

        player_pixmap = QtGui.QPixmap()
        player_pixmap.loadFromData(self.player.getPlayerImg())
        self.player_img_label = QtGui.QLabel()
        self.player_img_label.setPixmap(player_pixmap)

        team_pixmap = QtGui.QPixmap(self.player.getTeamImg())
        #team_pixmap.loadFromData(self.player.team_img)
        self.team_img_label = QtGui.QLabel()
        self.team_img_label.setPixmap(team_pixmap)

        self.allQHBoxLayout.addWidget(self.draft_order_label, 2)
        self.allQHBoxLayout.addWidget(self.player_img_label, 5)
        self.allQHBoxLayout.addWidget(self.team_img_label, 5)
        self.allQHBoxLayout.addWidget(self.player_name_label, 20)
        self.allQHBoxLayout.addWidget(self.position_label, 1)

        self.setLayout(self.allQHBoxLayout)

    def updateLabels(self):
        self.player_name_label.setText(self.player.name)
        self.position_label.setText(self.player.pos)

        player_pixmap = QtGui.QPixmap()
        player_pixmap.loadFromData(self.player.getPlayerImg())
        self.player_img_label.setPixmap(player_pixmap)

        team_pixmap = QtGui.QPixmap(self.player.getTeamImg())
        #team_pixmap.loadFromData(self.player.team_img)
        self.team_img_label.setPixmap(team_pixmap)


class TeamPlayerPage(QtGui.QWidget):
    def __init__(self, team_num, parent):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.data = parent.data
        self.team_num = team_num

        self.main_layout = QtGui.QVBoxLayout()

        # Player list
        self.player_list = QtGui.QListWidget()
        self.player_list.setMinimumSize(400,200)
        self.player_list.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.player_list.setStyleSheet("QListView { alternate-background-color: lightgrey; }")
        self.player_list.setAlternatingRowColors(True)
        self.player_list.itemSelectionChanged.connect(self.playerSelected)
        self.populatePlayerList()

        self.selected_player = -1
        self.selected_player_label = QtGui.QLabel()
        self.player_options_view = self.playerOptionsView()

        self.main_layout.addWidget(self.player_list)
        self.main_layout.addWidget(self.player_options_view)

        self.setLayout(self.main_layout)

    def populatePlayerList(self):
        for player in self.data.teams_players[self.team_num]:
            self.createPlayerEntry(player)

    def createPlayerEntry(self, player):
        player = PlayerEntry(player, self)
        myQListWidgetItem = QtGui.QListWidgetItem(self.player_list)
        myQListWidgetItem.setSizeHint(player.sizeHint())
        self.player_list.addItem(myQListWidgetItem)
        self.player_list.setItemWidget(myQListWidgetItem, player)

    def playerOptionsView(self):
        picking_group_box = QtGui.QGroupBox()

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        team_label = QtGui.QLabel(self.tr("Team: " + self.data.teams[self.team_num]))
        player_label = QtGui.QLabel(self.tr("Player:"))
        player_label.setAlignment(QtCore.Qt.AlignRight)

        self.rename_btn = QtGui.QPushButton("Rename")
        self.rename_btn.clicked.connect(self.rename)

        self.reposition_btn = QtGui.QPushButton("Reposition")
        self.reposition_btn.clicked.connect(self.reposition)

        self.back_btn = QtGui.QPushButton("Back")
        self.back_btn.clicked.connect(self.back)

        self.updateSelectedPlayer()

        grid.addWidget(team_label, 1, 0, 1, 1)
        grid.addWidget(player_label, 1, 1, 1, 1)
        grid.addWidget(self.selected_player_label, 1, 2, 1, 1)

        grid.addWidget(self.rename_btn, 2, 0)
        grid.addWidget(self.reposition_btn, 2, 1)
        grid.addWidget(self.back_btn, 2, 2)

        picking_group_box.setLayout(grid)

        return picking_group_box


    def playerSelected(self):
        self.selected_player = self.player_list.itemWidget(self.player_list.currentItem()).player.draft_round
        self.updateSelectedPlayer()

    def updateSelectedPlayer(self):
        if self.selected_player == -1:
            self.selected_player_label.setText("(Select a Player)")
        else:
            # Called due to clear() changing the selection?
            try:
                self.selected_player_label.setText(self.data.teams_players[self.team_num][self.selected_player].name)
            except KeyError:
                self.selected_player = -1
                self.selected_player_label.setText("(Select a Player)")

        self.setButtonStatus()

    def setButtonStatus(self):
        # Default them to enabled
        self.rename_btn.setEnabled(True)
        self.reposition_btn.setEnabled(True)

        if self.selected_player == -1:
            # No player selected
            self.rename_btn.setEnabled(False)
            self.reposition_btn.setEnabled(False)

    # Button callbacks
    def rename(self):
        dlg = QtGui.QInputDialog(self)
        dlg.setInputMode(QtGui.QInputDialog.TextInput)
        dlg.setLabelText('Enter the new name of the player:')
        dlg.setFont(Globals.small_font)
        ok = dlg.exec_()
        text = dlg.textValue()
        if ok:
            self.data.renamePlayer(self.team_num, self.selected_player, text.__str__())

            # Specific to this page
            renamed_player = self.player_list.itemWidget(self.player_list.item(self.selected_player))
            renamed_player.updateLabels()

            self.updateSelectedPlayer()

    def reposition(self):
        dlg = QtGui.QInputDialog(self)
        dlg.setInputMode(QtGui.QInputDialog.TextInput)
        dlg.setLabelText('Select players position:')
        dlg.setFont(Globals.small_font)
        dlg.setComboBoxItems(["F", "D", "G"])
        ok = dlg.exec_()
        new_position = dlg.textValue()
        if ok:
            self.data.repositionPlayer(self.team_num, self.selected_player, new_position)

            # Specific to this page
            repositioned_player = self.player_list.itemWidget(self.player_list.item(self.selected_player))
            repositioned_player.updateLabels()

            self.updateSelectedPlayer()

    def updateTeam(self, team_num):
        if self.team_num == team_num:
            for player in self.data.teams_players[self.team_num]:
                player_has_widget = False
                for i in range(self.player_list.count()):
                    player_widget = self.player_list.itemWidget(self.player_list.item(i))
                    if player == player_widget.player:
                        player_widget.updateLabels()
                        player_has_widget = True
                        break

                if not player_has_widget:
                    self.createPlayerEntry(player)

    def back(self):
        self.parent.returnToTeamPage()
