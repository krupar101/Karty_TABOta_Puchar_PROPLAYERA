import QtQuick

// Common fade for clickable panels and modal windows.
// Keep the fading-out item visible to paint its exit, but disable its input
// immediately when closed. Honors the player's reduced-motion setting.
Rectangle {
    id: fadeBox
    property bool open: false
    property int fadeDuration: api && api.state && api.state.settings && api.state.settings.reduced ? 35 : 190
    visible: open || opacity > 0.001
    enabled: open
    opacity: open ? 1 : 0
    Behavior on opacity {
        NumberAnimation { duration: fadeBox.fadeDuration; easing.type: Easing.InOutQuad }
    }
}
