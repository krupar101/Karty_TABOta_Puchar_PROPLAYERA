import QtQuick
import QtQuick.Controls

Item {
    id: card
    property var info: ({})
    property bool battle: false
    property bool onTable: false
    property bool faceUp: true
    property bool chosen: false
    property bool exchangeMode: false
    property bool exchangeSelected: false
    property bool interactive: true
    property bool playable: true
    property bool lift: true
    property bool showTip: true
    // Only hand/placed battle cards use split click: upper half acts, lower half inspects.
    property bool splitClickDetails: false
    property bool lowerHalfHovered: splitClickDetails && mouse.containsMouse && mouse.mouseY >= height / 2 && !mouse.draggedGesture
    signal previewRequested(var info)
    signal previewDismissed()
    property bool previewActive: false
    function dismissPreview() {
        if (previewActive) {
            previewActive = false
            previewDismissed()
        }
    }
    onLowerHalfHoveredChanged: if (!lowerHalfHovered) dismissPreview()
    onVisibleChanged: if (!visible) dismissPreview()
    Component.onDestruction: dismissPreview()
    Timer {
        interval: 120
        running: card.lowerHalfHovered && !card.previewActive && card.interactive &&
                 card.faceUp && !card.moving &&
                 !api.detailState.detail.id && !api.state.options.length && !api.state.confirmation && !api.state.busy
        onTriggered: {
            card.previewActive = true
            card.previewRequested(card.info)
        }
    }
    property bool dragEnabled: false
    // Coordinates of drag signals are local to this item, if assigned.
    property var dragCoordinateSpace: null
    property bool moving: mouse.draggedGesture
    property string previousUid: ""
    property int previousPower: 0
    property string deltaText: ""
    property bool pointerHover: mouse.containsMouse
    property bool hovered: mouse.containsMouse || activeFocus
    signal clicked()
    signal dragStarted(real sceneX, real sceneY)
    signal dragMoved(real sceneX, real sceneY)
    signal dragFinished()
    signal dropped(real sceneX, real sceneY)
    onInfoChanged: {
        if (info.uid && info.uid === previousUid && info.currentPower !== undefined && info.currentPower !== previousPower) {
            let delta = info.currentPower-previousPower
            deltaText = (delta > 0 ? "+" : "") + delta
            pulse.restart()
        }
        if (info.uid && info.uid !== previousUid && battle && !api.state.settings.reduced) arrival.restart()
        previousUid = info.uid || ""
        previousPower = info.currentPower || 0
    }
    width: 132; height: width * 603 / 388
    focus: false
    activeFocusOnTab: interactive
    Accessible.role: Accessible.Button
    Accessible.name: faceUp ? (info.name || "Karta") : "Zakryta karta"
    Accessible.description: splitClickDetails ? "Górna połowa wybiera kartę, najechanie na dolną pokazuje szczegóły. Klawisz I otwiera podgląd." : "Klawisz I pokazuje szczegóły karty."
    Keys.onReturnPressed: if (interactive) clicked()
    Keys.onSpacePressed: if (interactive) clicked()
    Keys.onPressed: event => { if (event.key === Qt.Key_I && info.id && faceUp) { api.inspect(info.id); event.accepted = true } }
    z: hovered || moving ? 20 : 1
    Item {
        id: motion
        objectName: "tabotaCardMotion"
        width: card.width; height: card.height
        y: !api.state.settings.reduced && card.pointerHover && card.lift && !card.moving ? -10 : 0
        scale: !api.state.settings.reduced && card.pointerHover && card.lift ? 1.035 : 1
        rotation: !api.state.settings.reduced && mouse.containsMouse && card.lift ? (mouse.mouseX / card.width - .5) * 3 : 0
        Behavior on y { enabled: !card.moving; NumberAnimation { duration: 160; easing.type: Easing.OutCubic } }
        Behavior on x { enabled: !card.moving; NumberAnimation { duration: 160; easing.type: Easing.OutCubic } }
        Behavior on scale { NumberAnimation { duration: 160; easing.type: Easing.OutCubic } }
        Behavior on rotation { NumberAnimation { duration: 160 } }
        transform: Scale { id: entryScale; origin.x: motion.width/2; origin.y: motion.height/2 }
        ParallelAnimation {
            id: arrival
            NumberAnimation { target: entryScale; property: "xScale"; from: .78; to: 1; duration: 300; easing.type: Easing.OutBack }
            NumberAnimation { target: entryScale; property: "yScale"; from: .78; to: 1; duration: 300; easing.type: Easing.OutBack }
        }
        Rectangle { x: 5; y: 8; width: parent.width; height: parent.height; radius: 7; color: "#a0000000" }
        Rectangle {
            anchors.fill: parent; anchors.margins: -3
            radius: 5; color: "transparent"
            border.width: card.chosen || card.hovered ? 2 : 1
            border.color: card.chosen ? Theme.gold : card.hovered ? Theme.purple : "#65425b"
            Behavior on border.color { ColorAnimation { duration: 120 } }
        }
        Flipable {
            id: flip
            anchors.fill: parent
            property real angle: card.faceUp ? 0 : 180
            Behavior on angle { NumberAnimation { duration: api.state.settings.reduced ? 60 : 520; easing.type: Easing.InOutCubic } }
            transform: Rotation { origin.x: flip.width/2; origin.y: flip.height/2; axis.x: 0; axis.y: 1; axis.z: 0; angle: flip.angle }
            front: Item {
                anchors.fill: parent
                Rectangle { anchors.fill: parent; color: Theme.panel2; radius: 5 }
                Image {
                    anchors.fill: parent
                    source: card.info.image || ""
                    sourceSize.width: Math.ceil(card.width * 2)
                    fillMode: Image.PreserveAspectFit
                    smooth: true; asynchronous: true
                }
                Column {
                    visible: !card.info.image
                    anchors.fill: parent; anchors.margins: card.width * .09
                    spacing: card.width * .08
                    Text { width: parent.width; text: card.info.kind === "token" ? "Ż E T O N" : "T A B O L O G"; font.pixelSize: Math.max(8,card.width*.065); color: Theme.gold; horizontalAlignment: Text.AlignHCenter }
                    Rectangle { width: parent.width; height: 1; color: Theme.gold; opacity: .5 }
                    Text { width: parent.width; text: card.info.kind === "token" ? "✦" : "✧"; color: Theme.purple; font.pixelSize: card.width*.32; horizontalAlignment: Text.AlignHCenter }
                    Text { width: parent.width; text: card.info.name || ""; color: Theme.gold; font.bold: true; font.pixelSize: Math.max(9, card.width*.095); horizontalAlignment: Text.AlignHCenter; wrapMode: Text.WordWrap }
                    Text { width: parent.width; visible: card.width > 110; text: card.info.description || ""; color: Theme.muted; font.pixelSize: card.width*.073; horizontalAlignment: Text.AlignHCenter; wrapMode: Text.WordWrap }
                }
                Rectangle { anchors.fill: parent; color: "#9b100b19"; visible: !card.playable && !card.chosen }
                Rectangle {
                    visible: card.info.pending || false
                    anchors.horizontalCenter: parent.horizontalCenter; y: parent.height *.65
                    width: parent.width; height: 20; color: "#db21122d"
                    Text { anchors.centerIn: parent; text: "PLAN"; color: Theme.gold; font.pixelSize: 10; font.bold: true; font.letterSpacing: 2 }
                }
            }
            back: Image { anchors.fill: parent; source: api.state.back; sourceSize.width: Math.ceil(card.width * 2); fillMode: Image.PreserveAspectFit; asynchronous: true }
        }
        // A number alone is ambiguous; every cost and power value has its own icon.
        Rectangle {
            visible: card.battle && card.faceUp && card.info.kind !== "token" && card.info.cost !== undefined
            objectName: "tabotaEnergyBadge"
            x: -5
            // Energy stays at the same height regardless of the rule label.
            y: -7
            width: 43; height: 28; radius: 14
            color: "#322046"; border.color: Theme.purple; border.width: 2
            Row {
                anchors.centerIn: parent; spacing: 3
                EnergyIcon { width: 10; height: 15; anchors.verticalCenter: parent.verticalCenter }
                Text { text: card.info.cost === undefined ? "" : card.info.cost; color: Theme.white; font.bold: true; font.pixelSize: card.width < 75 ? 11 : 13 }
            }
        }
        Rectangle {
            visible: card.battle && card.faceUp && card.info.kind !== "event" && card.info.power !== undefined
            x: parent.width-39; y: parent.height-24; width: 43; height: 28; radius: 14
            color: Theme.gold; border.color: Theme.ink
            Text {
                anchors.centerIn: parent
                text: "✦ " + (card.info.currentPower === undefined ? card.info.power : card.info.currentPower)
                color: Theme.ink; font.bold: true
                font.pixelSize: card.width < 75 ? 11 : 13
            }
        }
        // Only placed cards move the badge inside; preserve the original hand layout.
        Rectangle {
            id: ruleNameBadge
            objectName: "tabotaNameRuleBadge"
            visible: card.battle && card.faceUp && !!card.info.nameRuleBadge
            property bool compact: card.width < 80
            width: compact ? (card.info.nameRuleBadge === "A" ? 19 : 39)
                           : (card.info.nameRuleBadge === "A" ? 25 : 48)
            height: compact ? 14 : 17
            // Leave room for energy; long labels may extend beyond the right edge.
            x: card.onTable ? Math.max(40, parent.width - width - (compact ? 1 : 0))
                            : parent.width - width - (compact ? 1 : 0)
            y: card.onTable ? 2 : (compact ? -22 : -8)
            radius: height / 2
            color: card.info.nameRuleBadge === "A" ? "#3f294f" : "#254235"
            border.color: card.info.nameRuleBadge === "A" ? Theme.gold : Theme.green
            border.width: 1
            z: 5
            Text {
                anchors.centerIn: parent
                text: card.info.nameRuleBadge || ""
                color: Theme.white; font.bold: true
                font.pixelSize: ruleNameBadge.compact ? 8 : (card.info.nameRuleBadge === "A" ? 12 : 10)
            }
        }
        Rectangle {
            visible: card.exchangeMode && card.exchangeSelected
            x: 0; y: parent.height * .60; width: parent.width; height: 30
            radius: 5; color: "#f51f1b23"; border.color: Theme.gold; border.width: 2
            Text {
                anchors.centerIn: parent; text: "DO WYMIANY"
                color: Theme.gold; font.bold: true; font.pixelSize: Math.max(9, card.width * .105)
            }
        }
        Rectangle {
            visible: card.battle && card.info.silenced === true
            anchors.centerIn: parent; width: parent.width; height: 25; rotation: -13; color: "#dd512e50"; border.color: Theme.red
            Text { anchors.centerIn: parent; text: "WYCISZONO"; font.pixelSize: Math.max(8,card.width*.09); font.bold: true; color: Theme.white }
        }
        Rectangle {
            visible: card.battle && card.info.silenced === true
            anchors.centerIn: parent; width: parent.width * 1.18; height: 6; radius: 3; rotation: 34
            color: "#e34a4a"; opacity: .82
        }
        Rectangle {
            visible: card.battle && card.info.silenced === true
            anchors.centerIn: parent; width: parent.width * 1.18; height: 6; radius: 3; rotation: -34
            color: "#e34a4a"; opacity: .82
        }
        Rectangle {
            objectName: "tabotaProtectionBadge"
            visible: card.battle && card.faceUp && card.info.protected === true
            // Spell out the status; an unexplained diamond looked like an artifact.
            width: Math.min(parent.width, 72); height: card.width < 80 ? 14 : 18
            x: parent.width - width
            y: card.onTable && card.info.nameRuleBadge ? 49 : 24
            color: Theme.ink; border.color: Theme.green; radius: 3
            Accessible.name: "Ochrona: blokuje jeden wrogi efekt"
            Text {
                anchors.centerIn: parent
                text: "OCHRONA"; color: Theme.green; font.bold: true
                font.pixelSize: card.width < 80 ? 8 : 11
            }
        }
        Text {
            id: changeLabel
            anchors.horizontalCenter: parent.horizontalCenter
            y: 20; opacity: 0; text: card.deltaText
            color: text.startsWith("+") ? Theme.gold : Theme.red
            font.pixelSize: 30; font.bold: true; style: Text.Outline; styleColor: Theme.ink
        }
        ParallelAnimation {
            id: pulse
            NumberAnimation { target: changeLabel; property: "y"; from: 25; to: api.state.settings.reduced ? 25 : -15; duration: api.state.settings.reduced ? 80 : 650; easing.type: Easing.OutCubic }
            SequentialAnimation {
                NumberAnimation { target: changeLabel; property: "opacity"; from: 0; to: 1; duration: api.state.settings.reduced ? 20 : 100 }
                NumberAnimation { target: changeLabel; property: "opacity"; from: 1; to: 0; duration: api.state.settings.reduced ? 60 : 550 }
            }
        }
        Rectangle {
            id: inspectAffordance
            objectName: "tabotaInspectAffordance"
            // Follow motion so the affordance lifts, tilts and scales with the card.
            // Hovering the details area shows a centered, input-transparent preview.
            visible: card.splitClickDetails && card.interactive && card.faceUp
            opacity: card.lowerHalfHovered && !card.moving ? 1 : 0
            Behavior on opacity {
                NumberAnimation {
                    duration: api && api.state && api.state.settings && api.state.settings.reduced ? 40 : 200
                    easing.type: Easing.OutCubic
                }
            }
            x: 1; y: parent.height / 2; width: parent.width - 2; height: parent.height / 2 - 1
            color: "#b91b112b"; radius: 5; z: 8
            Rectangle { anchors.top: parent.top; width: parent.width; height: 1; color: Theme.gold }
            Text {
                anchors.centerIn: parent; text: "⌕  SZCZEGÓŁY"
                color: Theme.white; font.pixelSize: Math.max(10,card.width * .112)
                font.bold: true; style: Text.Outline; styleColor: Theme.ink
            }
        }
    }
    MouseArea {
        id: mouse
        onEntered: if (card.visible && card.enabled && !card.moving) api.uiSound("hover")
        anchors.fill: parent; hoverEnabled: card.interactive; enabled: card.interactive
        acceptedButtons: Qt.LeftButton | Qt.RightButton
        cursorShape: card.moving ? Qt.ClosedHandCursor : card.lowerHalfHovered ? Qt.PointingHandCursor : card.dragEnabled ? Qt.OpenHandCursor : Qt.PointingHandCursor
        // Battle.qml reparents THIS Card for both hover and drag; no visual copy.
        preventStealing: card.dragEnabled
        property real pressX: 0
        property real pressY: 0
        property bool draggedGesture: false
        onPressed: event => {
            if (!card.lowerHalfHovered) card.dismissPreview()
            if (!card.lowerHalfHovered) card.forceActiveFocus()
            pressX = event.x; pressY = event.y
            draggedGesture = false
        }
        onPositionChanged: event => {
            if (!pressed || !card.dragEnabled || (card.splitClickDetails && pressY >= card.height/2) || !(pressedButtons & Qt.LeftButton)) return
            if (!draggedGesture) {
                const dx = event.x-pressX, dy = event.y-pressY
                if (dx*dx+dy*dy < 64) return
                draggedGesture = true
                const pos = mouse.mapToItem(card.dragCoordinateSpace || card, event.x, event.y)
                card.dragStarted(pos.x, pos.y)
            } else {
                const pos = mouse.mapToItem(card.dragCoordinateSpace || card, event.x, event.y)
                card.dragMoved(pos.x, pos.y)
            }
        }
        onClicked: event => {
            if (draggedGesture) return
            if (event.button === Qt.RightButton && !card.lowerHalfHovered && card.faceUp && card.info.id)
                api.inspect(card.info.id)
            else if (event.button === Qt.LeftButton && !(card.splitClickDetails && event.y >= card.height/2))
                card.clicked()
        }
        onReleased: event => {
            if (draggedGesture) {
                const pos = mouse.mapToItem(card.dragCoordinateSpace || card, event.x, event.y)
                card.dropped(pos.x, pos.y)
                card.dragFinished()
            }
        }
        onCanceled: if (draggedGesture) card.dragFinished()
    }
    ToolTip {
    id: detailsTip
    objectName: "tabotaHoverDetails"
    width: 370
    contentItem: Text { text: detailsTip.text; color: Theme.white; font.pixelSize: 14; wrapMode: Text.WordWrap }
    visible: card.showTip && !card.onTable && !card.exchangeMode && !card.splitClickDetails && !api.detailState.detail.id && card.hovered && card.faceUp && !!card.info.name && !card.moving
    delay: card.splitClickDetails ? 180 : 650
    timeout: 7000
    text: (card.info.name || "") + (card.battle ?
        "\n⚡ Energia do zagrania: " + (card.info.cost === undefined ? "-" : card.info.cost) +
        (card.info.kind === "event" ? "\nWydarzenie: nie daje Mocy na stole." :
        "\n✦ Moc: " + (card.info.currentPower === undefined ? card.info.power : card.info.currentPower) +
        " (bazowa " + (card.info.power || 0) + ", zmiany " + (card.info.buff || 0) + ", aura " + (card.info.aura || 0) + ")") +
        (card.info.nameRuleHint ? "\n" + card.info.nameRuleHint : "") +
        (card.info.protected ? "\nOchrona: blokuje jeden wrogi efekt, po czym znika." : "") +
        (card.info.silenced ? "\n⛔ Wyciszona: Aura i Finał tej karty są wyłączone." : "") +
        "\n" + (card.info.description || "") : "\nPrawy przycisk lub I: pełna ilustracja")
    }
}
