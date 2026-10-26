import QtQuick

Item {
    id: backdrop
    property var bands: api.musicSpectrum
    property bool active: api.state.settings.music && !api.state.settings.reduced && api.state.settings.musicVolume > 0
    property real bass: active ? (bands[0] + bands[1] + bands[2] + bands[3]) / 4 : 0
    // Only the backdrop observes the audio signal: the game state is untouched.
    Rectangle {
        x: 500; y: -500; width: 1250; height: 1250; radius: 625
        color: "transparent"; border.width: 1; border.color: "#281b37"
        scale: 1 + backdrop.bass * .035
        Behavior on scale { NumberAnimation { duration: api.state.settings.reduced ? 0 : 160 } }
    }
    Rectangle {
        x: 820; y: -220; width: 700; height: 700; radius: 350
        color: "#10101c"; opacity: .5 + backdrop.bass * .2
        scale: 1 + backdrop.bass * .045
        Behavior on scale { NumberAnimation { duration: api.state.settings.reduced ? 0 : 180 } }
    }
    Repeater {
        model: 42
        Rectangle {
            required property int index
            property real level: backdrop.active ? backdrop.bands[index % 24] : 0
            x: (index*331+97)%1430
            y: (index*197+41)%890 - level * (index%2 ? 7 : -7)
            width: index%5===0 ? 3 : 1; height: width; radius: width/2
            color: index%3===0 ? Theme.gold : Theme.purple
            opacity: .18 + (index%5)*.08 + level * .18
            Behavior on y { NumberAnimation { duration: api.state.settings.reduced ? 0 : 160 } }
        }
    }
    Row {
        x: 42; y: 742; spacing: 7; height: 120
        opacity: backdrop.active ? .13 : 0
        Behavior on opacity { NumberAnimation { duration: api.state.settings.reduced ? 0 : 180 } }
        Repeater {
            model: 48
            Rectangle {
                required property int index
                property real level: backdrop.active ? backdrop.bands[index < 24 ? index : 47-index] : 0
                width: 21; height: 2 + level * 115; radius: 2
                anchors.bottom: parent.bottom
                color: index%3 === 0 ? Theme.gold : Theme.purple
                Behavior on height { NumberAnimation { duration: api.state.settings.reduced ? 0 : 100; easing.type: Easing.OutQuad } }
            }
        }
    }
}
