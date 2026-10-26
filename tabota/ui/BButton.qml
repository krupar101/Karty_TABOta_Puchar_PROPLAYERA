import QtQuick
import QtQuick.Controls

Button {
    id: control
    property bool primary: false
    property bool compact: false
    property color accent: Theme.gold
    implicitWidth: Math.max(compact ? 80 : 160, contentItem.implicitWidth + 36)
    implicitHeight: compact ? 38 : 50
    hoverEnabled: true
    HoverHandler { enabled: control.enabled; cursorShape: Qt.PointingHandCursor }
    Connections {
        target: control
        function onClicked() { api.uiSound("click") }
    }
    focusPolicy: Qt.StrongFocus
    opacity: enabled ? 1 : 0.35
    scale: down && !api.state.settings.reduced ? 0.98 : 1
    Behavior on scale { NumberAnimation { duration: 90 } }
    contentItem: Text {
        text: control.text
        font.family: Theme.font
        font.pixelSize: control.compact ? 12 : 14
        font.weight: Font.DemiBold
        font.letterSpacing: 0.6
        color: control.primary ? Theme.ink : (control.hovered || control.activeFocus ? control.accent : Theme.white)
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }
    background: Rectangle {
        radius: 7
        color: control.primary ? (control.hovered ? "#ffeaa1" : control.accent) : (control.hovered ? "#34223f" : "#1c1428")
        border.color: control.activeFocus || control.hovered ? control.accent : control.primary ? control.accent : Theme.line
        border.width: control.activeFocus ? 2 : 1
        Behavior on color { ColorAnimation { duration: 120 } }
        Rectangle {
            visible: control.primary
            x: 10; y: parent.height - 4; width: parent.width - 20; height: 1
            color: "#947a3a"; opacity: 0.4
        }
    }
}
