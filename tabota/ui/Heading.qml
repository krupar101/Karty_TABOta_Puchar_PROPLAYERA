import QtQuick
Column {
    property string eyebrow: ""
    property string title: ""
    property string subtitle: ""
    spacing: 8
    Text { visible: text !== ""; width: parent.width; wrapMode: Text.WordWrap; text: eyebrow.toUpperCase(); color: Theme.gold; font.pixelSize: 11; font.letterSpacing: 3; font.weight: Font.DemiBold }
    Text { width: parent.width; text: title; color: Theme.white; font.pixelSize: 32; font.weight: Font.Bold; font.letterSpacing: -0.8; wrapMode: Text.WordWrap }
    Text { visible: text !== ""; width: parent.width; text: subtitle; color: Theme.muted; font.pixelSize: 14; wrapMode: Text.WordWrap; lineHeight: 1.25 }
}
