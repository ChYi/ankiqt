# Copyright: Damien Elmes <anki@ichi2.net>
# -*- coding: utf-8 -*-
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

class EditCurrent(object):

    def __init__(self, mw):
        self.mw = mw

    def _editCurrentState(self, oldState):
        if self.lastState == "editCurrentFact":
            return self.moveToState("saveEdit")
        self.form.actionRepeatAudio.setEnabled(False)
        self.deck.db.flush()
        self.showEditor()

    def _saveEditState(self, oldState):
        self.form.actionRepeatAudio.setEnabled(True)
        self.editor.saveFieldsNow()
        self.form.buttonStack.show()
        return self.reset()

    # Edit current fact
    ##########################################################################

    def setupEditor(self):
        print "setupeditor"
        return
        self.editor = aqt.facteditor.FactEditor(
            self, self.form.fieldsArea, self.deck)
        self.editor.clayout.setShortcut("")
        self.editor.onFactValid = self.onFactValid
        self.editor.onFactInvalid = self.onFactInvalid
        self.editor.resetOnEdit = False
        # editor
        self.connect(self.form.saveEditorButton, SIGNAL("clicked()"),
                     lambda: self.moveToState("saveEdit"))

    def showEditor(self):
        self.form.buttonStack.hide()
        self.switchToEditScreen()
        self.editor.setFact(self.currentCard.fact)
        self.editor.card = self.currentCard

    def onFactValid(self, fact):
        self.form.saveEditorButton.setEnabled(True)

    def onFactInvalid(self, fact):
        self.form.saveEditorButton.setEnabled(False)