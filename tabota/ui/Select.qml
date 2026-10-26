import QtQuick
import QtQuick.Controls
ComboBox {
    id: control
    Connections {
        target: control
        function onActivated(index) { api.uiSound("click") }
    }
    implicitHeight: 40
    leftPadding: 12
    rightPadding: 30
    background: Rectangle { radius: 6; color: Theme.panel2; border.color: control.activeFocus || control.hovered ? Theme.gold : Theme.line }
    contentItem: Text { text: control.displayText; font.pixelSize: 13; color: Theme.white; verticalAlignment: Text.AlignVCenter; elide: Text.ElideRight }
    indicator: Text { x: control.width-23; y: (control.height-height)/2; text: "⌄"; color: Theme.gold; font.pixelSize: 18 }
    delegate: ItemDelegate {
        required property int index
        width: control.width
        text: control.textAt(index)
        contentItem: Text { text: parent.text; color: Theme.white; font.pixelSize: 13; elide: Text.ElideRight }
        background: Rectangle { color: parent.highlighted ? "#493254" : Theme.panel }
        highlighted: control.highlightedIndex === index
    }
    popup: Popup {
        y: control.height+4
        width: control.width
        padding: 1
        implicitHeight: Math.min(320, contentItem.implicitHeight)
        background: Rectangle { color: Theme.panel; border.color: Theme.line; radius: 6 }
        contentItem: ListView { clip: true; implicitHeight: contentHeight; model: control.popup.visible ? control.delegateModel : null; currentIndex: control.highlightedIndex; ScrollIndicator.vertical: ScrollIndicator {} }
    }
}
