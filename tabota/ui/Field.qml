import QtQuick
import QtQuick.Controls
TextField {
    color: Theme.white
    placeholderTextColor: Theme.muted
    selectionColor: Theme.purple
    selectedTextColor: Theme.ink
    font.pixelSize: 14
    leftPadding: 12
    rightPadding: 12
    selectByMouse: true
    background: Rectangle { radius: 6; color: Theme.panel; border.color: parent.activeFocus ? Theme.gold : Theme.line }
}
