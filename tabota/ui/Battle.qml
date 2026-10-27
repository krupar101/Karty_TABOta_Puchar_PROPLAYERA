import QtQuick
import QtQuick.Controls

Item {
    id: table
    signal quickPreview(var info)
    objectName: "tabotaBattleTable"
    property var s: api.state
    // During an outgoing screen fade the bridge may already clear the match.
    // Keep its last complete visual state until this page finishes fading out.
    property var lastBoard: ({})
    // Isolated board signal: advancing a card does not invalidate every other
    // QML binding on the screen or reload the campaign/collection state.
    property var liveBoard: api.battleBoard
    property var b: liveBoard && liveBoard.lanes ? liveBoard : lastBoard
    onLiveBoardChanged: if (liveBoard && liveBoard.lanes) {
        // Undoing a planned ritual returns its selection to the single dialog.
        if (liveBoard.ritual && lastBoard.ritual === false) ritualPrompted = false
        lastBoard = liveBoard
    }
    property bool ritualPrompted: false
    Timer {
        interval: 250; running: b.ritual && !table.ritualPrompted && !s.options.length && !s.busy && !b.rulePending && !b.mulligan
        onTriggered: { table.ritualPrompted = true; api.ritual("all") }
    }
    property bool showLog: false
    property bool displayedLog: false
    onShowLogChanged: logFade.restart()
    SequentialAnimation {
        id: logFade
        NumberAnimation { target: planText; property: "opacity"; to: 0; duration: s.settings.reduced ? 15 : 90 }
        ScriptAction { script: table.displayedLog = table.showLog }
        NumberAnimation { target: planText; property: "opacity"; from: 0; to: 1; duration: s.settings.reduced ? 15 : 140 }
    }
    property string dragUid: ""
    property bool dragActive: false
    property real dragX: 0
    property real dragY: 0
    property real dragOffsetX: 0
    property real dragOffsetY: 0
    property var dragLegalLanes: []
    property bool practiceAcknowledged: false
    function trackDrag(localX, localY) {
        // Only two card-position bindings change per pointer event; never call Python.
        if (Math.abs(dragX - localX) > 0.25) dragX = localX
        if (Math.abs(dragY - localY) > 0.25) dragY = localY
    }
    function dropLane(localX, localY) {
        if (localY < 108 || localY > 473) return -1
        for (let lane = 0; lane < 3; lane++) {
            const left = lane * 345
            if (localX >= left && localX <= left + 330) return lane
        }
        return -1
    }
    Shortcut { sequence: "1"; enabled: !!b.selected.id && !s.busy; onActivated: api.chooseLane(0) }
    Shortcut { sequence: "2"; enabled: !!b.selected.id && !s.busy; onActivated: api.chooseLane(1) }
    Shortcut { sequence: "3"; enabled: !!b.selected.id && !s.busy; onActivated: api.chooseLane(2) }
    Shortcut { sequence: "Ctrl+Z"; enabled: !s.busy; onActivated: api.undo() }
    Card {
        objectName: "tabotaOpponentCard"
        x: 0; y: 0; width: 57; lift: false; showTip: false
        info: ({id: s.encounter.portrait, image: s.encounter.image, name: s.encounter.short})
        onClicked: api.inspect(info.id)
    }
    Text { x: 76; y: 0; text: "TURA " + b.turn + " / " + b.maxTurns; color: Theme.white; font.pixelSize: 27; font.bold: true; font.letterSpacing: 1 }
    BButton { x: 880; y: 0; width: 140; text: "Ⅱ  Pauza"; compact: true; enabled: !s.busy; onClicked: api.navigate("pause") }
    Text { x: 76; y: 48; text: "RYWAL  /  " + s.encounter.short.toUpperCase(); color: Theme.red; font.pixelSize: 12; font.letterSpacing: 1 }
    Row { x: 720; y: 43; spacing: 7
        Image { width: 18; height: 28; source: s.back; fillMode: Image.PreserveAspectFit; sourceSize.width: 36 }
        Text { anchors.verticalCenter: parent.verticalCenter; text: "Ręka: " + b.enemyHand + "   ·   Talia: " + b.enemyDeck; color: Theme.muted; font.pixelSize: 12 }
    }
    Text { x: 76; y: 75; width: 944; text: b.enemyPreview || ""; color: b.tutorial ? Theme.gold : Theme.muted; font.pixelSize: 11; elide: Text.ElideRight }

    // Dialogue occupies only the header; the board begins at y=108.
    FadeBox {
        id: speechBubble
        objectName: "tabotaOpponentSpeech"
        x: 72; y: 0; width: 786; height: 96; z: 30
        radius: 16; color: "#42235f"; border.color: Theme.purple
        fadeDuration: s.settings.reduced ? 35 : 220
        property string incoming: s.dialogue || ""
        property string pending: ""
        property string spoken: ""
        property bool ready: s.screen === "battle" && !b.rulePending && !ruleWindow.visible
        function showPending() {
            if (!ready || !pending.length) return
            spoken = pending
            pending = ""
            open = true
            speechLifetime.restart()
        }
        onIncomingChanged: {
            pending = incoming.trim()
            if (!pending.length) { open = false; speechLifetime.stop() }
            else showPending()
        }
        onReadyChanged: if (ready) showPending()
        Component.onCompleted: { pending = incoming.trim(); showPending() }
        Timer {
            id: speechLifetime
            interval: 10000
            onTriggered: speechBubble.open = false
        }
        // A small comic tail points left to the opponent's card.
        Rectangle {
            x: -7; y: 34; width: 16; height: 16; rotation: 45
            color: speechBubble.color; border.color: Theme.purple
        }
        Rectangle { x: 1; y: 28; width: 20; height: 32; color: speechBubble.color }
        Text {
            x: 22; y: 11; width: parent.width - 44
            text: s.encounter.short; color: Theme.purple
            font.pixelSize: 11; font.bold: true
        }
        Text {
            objectName: "tabotaOpponentSpeechText"
            x: 22; y: 31; width: parent.width - 44; height: 56
            text: speechBubble.spoken; color: Theme.white
            font.pixelSize: 17; wrapMode: Text.WordWrap
        }
    }

    Row { y: 108; spacing: 15
        Repeater { model: 3
            Rectangle {
                id: lane
                required property int index
                property var laneInfo: b.lanes[index]
                width: 330; height: 365; radius: 13
                property bool dropLegal: table.dragActive ? table.dragLegalLanes[index] === true : laneInfo.legal
                color: dropLegal ? "#271a34" : "#15101f"
                border.color: dropLegal ? Theme.gold : Theme.line
                border.width: dropLegal ? 2 : 1
                Behavior on color { ColorAnimation { duration: 140 } }
                Text { x: 16; y: 14; text: ["◈", "❖", "◇"][index] + "   " + laneInfo.name; color: Theme.gold; font.pixelSize: 13; font.bold: true; font.letterSpacing: 2 }
                Text { anchors.right: parent.right; anchors.rightMargin: 15; y: 16; text: laneInfo.capacity + " SLOTY"; color: Theme.muted; font.pixelSize: 9; font.letterSpacing: 1 }
                Row { x: 15; y: 53; spacing: laneInfo.capacity === 5 ? 8 : 10
                    Repeater { model: lane.laneInfo.capacity
                        Item {
                            required property int index
                            property var unit: lane.laneInfo.enemyUnits[index] || null
                            // Occupied slots cover empty slots; later cards still cover earlier ones.
                            z: unit ? 1 : 0
                            width: lane.laneInfo.capacity === 5 ? 52 : 67; height: 104
                            Rectangle { anchors.fill: parent; radius: 4; color: "#100c17"; border.color: "#302137"; Text { anchors.centerIn: parent; text: "+"; color: "#403049"; font.pixelSize: 18 } }
                            Card { anchors.horizontalCenter: parent.horizontalCenter; width: parent.width; visible: !!parent.unit; info: parent.unit || {}; battle: true; onTable: true; lift: false; onClicked: api.inspect(info.id)
                                opacity: parent.unit ? 1 : 0
                                Behavior on opacity { NumberAnimation { duration: s.settings.reduced ? 50 : 300 } }
                            }
                        }
                    }
                }
                Rectangle { x: 15; y: 172; width: 300; height: 1; color: Theme.line }
                Row { x: 18; y: 183; spacing: 9
                    Text { text: "✦ " + lane.laneInfo.player; color: Theme.gold; font.pixelSize: 24; font.bold: true }
                    Text { text: ":"; color: Theme.muted; font.pixelSize: 23 }
                    Text { text: "✦ " + lane.laneInfo.enemy; color: Theme.red; font.pixelSize: 24; font.bold: true }
                    Text { visible: b.plan.length > 0; anchors.verticalCenter: parent.verticalCenter; text: " → " + lane.laneInfo.predicted + ":" + lane.laneInfo.predictedEnemy; color: Theme.muted; font.pixelSize: 15 }
                }
                Text { anchors.right: parent.right; anchors.rightMargin: 16; y: 215; text: laneInfo.player > laneInfo.enemy ? "↑ PROWADZISZ" : laneInfo.player < laneInfo.enemy ? "↓ PRZEGRYWASZ" : "= REMIS"; color: laneInfo.player > laneInfo.enemy ? Theme.green : laneInfo.player < laneInfo.enemy ? Theme.red : Theme.muted; font.pixelSize: 9; font.bold: true }
                Row { x: 15; y: 234; spacing: laneInfo.capacity === 5 ? 8 : 10
                    Repeater { model: lane.laneInfo.capacity
                        Item {
                            required property int index
                            property var unit: lane.laneInfo.playerUnits[index] || null
                            // Occupied slots cover empty slots; later cards still cover earlier ones.
                            z: unit ? 1 : 0
                            width: lane.laneInfo.capacity === 5 ? 52 : 67; height: 104
                            Rectangle { anchors.fill: parent; radius: 4; color: lane.dropLegal ? "#30203d" : "#100c17"; border.color: lane.dropLegal ? "#8f7945" : "#302137"; Text { anchors.centerIn: parent; text: lane.dropLegal ? "↓" : "+"; color: lane.dropLegal ? Theme.gold : "#403049"; font.pixelSize: 20 } }
                            Card { anchors.horizontalCenter: parent.horizontalCenter; width: parent.width; visible: !!parent.unit; info: parent.unit || {}; battle: true; onTable: true; lift: false; splitClickDetails: false; onClicked: api.inspect(info.id) }
                            MouseArea { anchors.fill: parent; enabled: !parent.unit; cursorShape: lane.laneInfo.legal ? Qt.PointingHandCursor : Qt.ArrowCursor; onClicked: api.chooseLane(lane.index) }
                        }
                    }
                }
                Text { x: 15; y: 344; text: "Stałe bonusy (ty / rywal): " + laneInfo.points + " / " + laneInfo.enemyPoints; color: Theme.gold; font.pixelSize: 11
                    MouseArea { id: bonusHover; anchors.fill: parent; hoverEnabled: true }
                    ToolTip.visible: bonusHover.containsMouse
                    ToolTip.text: laneInfo.pointHint
                }
                MouseArea { x: 0; y: 174; width: parent.width; height: 50; cursorShape: lane.laneInfo.legal ? Qt.PointingHandCursor : Qt.ArrowCursor; onClicked: api.chooseLane(lane.index) }
            }
        }
    }
    // Start of the player's area. Keep the resource meter with the hand, not the opponent.
    Rectangle {
        x: 0; y: 481; width: 1020; height: 47; radius: 9
        color: Theme.panel; border.color: b.mulligan ? Theme.line : Theme.purple
        Row {
            x: 15; anchors.verticalCenter: parent.verticalCenter; spacing: 9
            EnergyIcon { width: 18; height: 25; anchors.verticalCenter: parent.verticalCenter }
            Text { text: "TWOJA ENERGIA"; color: Theme.white; font.pixelSize: 12; font.bold: true; anchors.verticalCenter: parent.verticalCenter }
            Rectangle { width: 1; height: 22; color: Theme.line; anchors.verticalCenter: parent.verticalCenter }
            Repeater {
                model: b.turn || 0
                Rectangle {
                    required property int index
                    width: 25; height: 25; radius: 13
                    color: index < b.energy ? Theme.gold : "#2b2038"
                    border.color: index < b.energy ? Theme.gold : Theme.line
                    EnergyIcon { anchors.centerIn: parent; width: 12; height: 17; color: index < b.energy ? Theme.ink : Theme.muted }
                }
            }
            Text {
                text: b.energy + " / " + b.turn
                color: Theme.gold; font.pixelSize: 19; font.bold: true
                anchors.verticalCenter: parent.verticalCenter
            }
        }
        Text { font.family: "Noto Sans Symbols 2";
            anchors.right: parent.right; anchors.rightMargin: 16
            anchors.verticalCenter: parent.verticalCenter
            text: b.mulligan ? "Na początku możesz wymienić karty" : "⚡ to koszt zagrania karty"
            color: Theme.muted; font.pixelSize: 11
        }
    }
    Row {
        y: 535; spacing: 13
        Text { text: b.mulligan ? "TWOJE KARTY - KLIKNIJ TE DO WYMIANY" : "TWOJA RĘKA"; color: Theme.gold; font.pixelSize: 11; font.bold: true; font.letterSpacing: 1 }
        Text {
            text: b.mulligan ? "ZAZNACZONE: " + b.exchangeCount + " / 2" :
                  b.hand.length + " / 10   ·   TALIA " + b.deckCount + "   ·   ODRZUCONE " + b.discardCount
            color: b.mulligan ? Theme.white : Theme.muted; font.pixelSize: 11
        }
        Text {
            visible: !b.mulligan
            text: b.choice ? "KLIKNIJ KARTĘ DO ODRZUCENIA" : "Góra karty: wybierz  ·  Dół: szczegóły  ·  1 / 2 / 3: strefa"
            color: b.choice ? Theme.gold : Theme.muted; font.pixelSize: 10
        }
    }
    Flickable {
        id: handArea
        x: 0; y: 555; width: 1020; height: 165
        contentWidth: Math.max(width, b.hand.length * 110 + 20); contentHeight: 157; clip: true
        ScrollBar.horizontal: ScrollBar { policy: ScrollBar.AsNeeded }
        Row {
            x: 10; y: 8; spacing: 12
            Repeater {
                model: b.hand.length
                Item {
                    id: handSlot
                    objectName: "tabotaHandSlot"
                    required property int index
                    property var handInfo: b.hand[index] || ({})
                    width: 98; height: 155

                    Card {
                        id: handCard
                        onPreviewRequested: info => table.quickPreview(info)
                        onPreviewDismissed: table.quickPreview(({}))
                        objectName: "tabotaHandCard"
                        width: handSlot.width; info: handSlot.handInfo; battle: true
                        dragCoordinateSpace: table
                        splitClickDetails: !b.choice
                        showTip: true
                        chosen: (table.dragActive && table.dragUid === handSlot.handInfo.uid) ||
                                handSlot.handInfo.selected || handSlot.handInfo.exchange ||
                                (b.tutorialGuided && b.tutorialPhase === "card" && handSlot.handInfo.uid === b.tutorialTargetUid)
                        interactive: !b.tutorialGuided || handSlot.handInfo.uid === b.tutorialTargetUid
                        exchangeMode: b.mulligan
                        exchangeSelected: !!handSlot.handInfo.exchange
                        playable: handSlot.handInfo.playable || b.mulligan || b.choice
                        dragEnabled: !s.busy && !b.mulligan && !b.choice && !!handSlot.handInfo.playable
                        onClicked: api.selectCard(handSlot.handInfo.uid)
                        onDragStarted: (localX, localY) => {
                            // Do not select via Bridge here: that used to refresh every
                            // screen synchronously during the mouse-press gesture.
                            table.dragUid = handSlot.handInfo.uid
                            table.dragLegalLanes = handSlot.handInfo.legalLanes || []
                            const origin = table.mapFromItem(handCard, 0, 0)
                            table.dragOffsetX = localX - origin.x
                            table.dragOffsetY = localY - origin.y
                            table.trackDrag(localX, localY)
                            table.dragActive = true
                        }
                        onDragMoved: (localX, localY) => table.trackDrag(localX, localY)
                        onDropped: (localX, localY) => {
                            const lane = table.dropLane(localX, localY)
                            if (lane < 0) return  // Dropping outside the board changes nothing.
                            const uid = handSlot.handInfo.uid
                            // Finish the release/restore gesture before invoking the
                            // Python bridge. This avoids a scene-graph change mid-event.
                            Qt.callLater(function() { api.dropCard(uid, lane) })
                        }
                        onDragFinished: {
                            table.dragActive = false
                            table.dragUid = ""
                            table.dragLegalLanes = []
                        }
                    }
                    // Raise the ORIGINAL Card (not another Card rendering its data).
                    // The same motion, flip, buff pulse and opacity animation continue
                    // unchanged as its visual parent moves out of the clipped Flickable.
                    states: State {
                        name: "aboveUi"
                        when: !b.rulePending && (handCard.pointerHover ||
                              (table.dragActive && table.dragUid === handSlot.handInfo.uid))
                        ParentChange { target: handCard; parent: table }
                        PropertyChanges {
                            target: handCard
                            x: table.dragActive && table.dragUid === handSlot.handInfo.uid
                               ? table.dragX - table.dragOffsetX
                               : handArea.x + 10 + handSlot.index * 110 - handArea.contentX
                            y: table.dragActive && table.dragUid === handSlot.handInfo.uid
                               ? table.dragY - table.dragOffsetY : handArea.y + 8
                            z: 210
                        }
                    }
                }
            }
        }
    }
    Text {
        x: 0; y: 723; width: 1020
        text: b.mulligan ? "Złota ramka i napis „DO WYMIANY” = ta karta zostanie wymieniona. Możesz też zachować wszystkie." : b.hint
        color: b.mulligan || b.tutorial ? Theme.gold : Theme.muted
        font.pixelSize: 11; wrapMode: Text.WordWrap
    }

    // Opening-hand exchange is its own step: nothing is secretly discarded on selection.
    FadeBox {
        id: exchangePanel
        objectName: "tabotaExchangePanel"
        open: b.mulligan && !b.rulePending && !ruleWindow.visible
        x: 32; y: 142; width: 956; height: 285
        z: 70; radius: 16; color: "#f1191228"; border.width: 2; border.color: Theme.gold
        Text { x: 27; y: 22; text: "KROK 1 / 2   ·   WYMIANA KART NA START"; color: Theme.gold; font.pixelSize: 19; font.bold: true }
        Text {
            x: 27; y: 65; width: 890
            text: "Spójrz na 5 kart w swojej ręce na dole ekranu."
            color: Theme.white; font.pixelSize: 17
        }
        Text {
            x: 27; y: 97; width: 890
            text: "Kliknij górną połowę maksymalnie 2 kart, których NIE chcesz zatrzymać. Zostaną zastąpione losowymi kartami z talii."
            color: Theme.white; font.pixelSize: 15; wrapMode: Text.WordWrap
        }
        Text {
            x: 27; y: 154; width: 890
            text: "Zaznaczone do wymiany: " + b.exchangeCount + " / 2   ·   Nie musisz wymieniać żadnej karty."
            color: Theme.gold; font.pixelSize: 15; font.bold: true
        }
        BButton {
            x: 27; y: 197; width: 570; height: 54; primary: true
            text: b.exchangeCount === 0 ? "KROK 2 / 2   ·   Zachowaj rękę i zacznij" :
                  "KROK 2 / 2   ·   Wymień " + b.exchangeCount + (b.exchangeCount === 1 ? " kartę" : " karty") + " i zacznij"
            onClicked: api.exchange()
        }
        Text { x: 620; y: 212; width: 310; text: "Potem rozpocznie się tura 1."; color: Theme.muted; font.pixelSize: 13; wrapMode: Text.WordWrap }
    }

    Rectangle {
        x: 1040; y: 0; width: 320; height: 746; radius: 13; color: Theme.panel; border.color: Theme.line
        Column { id: ruleControls; objectName: "tabotaRuleControls"; x: 19; y: 20; width: 282; spacing: 13
            Text { text: "WARUNEK WYZWANIA"; color: Theme.gold; font.pixelSize: 10; font.letterSpacing: 2 }
            Text { width: parent.width; text: s.encounter.ruleName; color: Theme.white; font.pixelSize: 19; font.bold: true; wrapMode: Text.WordWrap }
            Flickable { width: parent.width; height: 118; contentHeight: rules.implicitHeight; clip: true; ScrollBar.vertical: ScrollBar {}
                Text { id: rules; width: parent.width-12; text: s.encounter.activeRule; color: Theme.muted; font.pixelSize: 12; wrapMode: Text.WordWrap; lineHeight: 1.35 }
            }
            Rectangle { width: parent.width; height: 1; color: Theme.line }
            Text { width: parent.width; text: "RYTUAŁ 20:30"; color: Theme.muted; font.pixelSize: 10; font.letterSpacing: 1 }
            Text {
                objectName: "tabotaUsedRitual"
                width: parent.width
                text: b.usedRitual || "Rytuał jeszcze niewykorzystany"
                color: b.usedRitual ? Theme.gold : Theme.muted
                font.pixelSize: 14; wrapMode: Text.WordWrap
            }
            BButton { visible: b.flight; text: "Darmowy lot"; width: 282; compact: true; enabled: !s.busy; onClicked: api.ritual("flight") }
            Row { spacing: 8
                BButton { text: "Plan (" + b.plan.length + ")"; compact: true; width: 137; primary: !showLog; onClicked: showLog = false }
                BButton { text: "Log meczu"; compact: true; width: 137; primary: showLog; onClicked: showLog = true }
            }
        }
        Flickable {
            objectName: "tabotaPlanList"
            x: 19; y: ruleControls.y + ruleControls.height + 12; width: 282; height: Math.max(60, 550 - y)
            contentHeight: planText.implicitHeight; clip: true; ScrollBar.vertical: ScrollBar {}
            Text { id: planText; width: 268; text: b.mulligan ? "WYMIANA KART NA START\n\nKliknij do 2 kart w swojej ręce. Złota ramka pokaże, które zostaną wymienione.\n\nKliknij „Zachowaj rękę i zacznij” lub „Wymień i zacznij”." : displayedLog ? b.log.slice().reverse().join("\n\n") : b.selected.id ? b.selected.name + "\n\n" + b.selected.description + "\n\nWybierz podświetloną strefę." : b.plan.length ? b.plan.map(function(t,i){return (i+1)+". "+t}).join("\n\n") : "Plan jest pusty.\n\nWybierz kartę z ręki i wskaż strefę.\n\nRuchy rozpatrują się naprzemiennie. Pierwszeństwo: " + (b.turn%2 ? "TABO" : "RYWAL") + "."; color: Theme.muted; font.pixelSize: 12; wrapMode: Text.WordWrap; lineHeight: 1.3 }
        }
        BButton { x: 19; y: 636; width: 282; height: 44; text: s.busy ? "Pomiń animację" : b.finished ? "Pokaż wynik  →" : b.mulligan ? (b.exchangeCount ? "Wymień " + b.exchangeCount + " i zacznij" : "Zachowaj rękę i zacznij") : "Zakończ turę  →"; primary: true; enabled: !b.choice && (!b.tutorialGuided || b.tutorialPhase === "submit"); onClicked: s.busy ? api.skipAnimation() : b.finished ? api.navigate("result") : api.submit() }
        Text { x: 19; y: 607; width: 282; visible: !b.mulligan && !s.busy && !b.finished
            text: "Zakończ turę: odkryj oba plany i rozegraj ruchy."
            color: Theme.muted; font.pixelSize: 11; wrapMode: Text.WordWrap
        }
        BButton { x: 19; y: 692; width: 282; height: 36; text: "↶  Cofnij ostatni ruch"; compact: true; enabled: b.plan.length > 0 && !s.busy; onClicked: api.undo() }
    }
    // Contextual tutor: guided and enforced for turns 1–3, then control is
    // handed over to the player at the beginning of turn 4.
    FadeBox {
        id: tutorialPanel
        objectName: "tabotaTutorialPanel"
        open: (b.tutorialGuided || b.tutorialPractice) && !s.busy && !b.finished &&
              !table.practiceAcknowledged && !exchangePanel.visible && !ruleWindow.visible
        x: 338; y: b.tutorialPhase === "card" ? 375 : 4
        width: 646; height: b.tutorialPractice ? 150 : 140
        // Guided steps move between the hand and the board without jumping.
        Behavior on y { NumberAnimation { duration: s.settings.reduced ? 20 : 170; easing.type: Easing.InOutQuad } }
        Behavior on height { NumberAnimation { duration: s.settings.reduced ? 20 : 150; easing.type: Easing.InOutQuad } }
        radius: 12; color: "#f2261738"; border.color: Theme.gold; border.width: 2; z: 175
        Text {
            x: 18; y: 10; width: 610
            text: b.tutorialGuided ? "NAUKA · KROK " + b.turn + " / 3 · " +
                  (b.tutorialPhase === "card" ? "WYBIERZ KARTĘ" : b.tutorialPhase === "lane" ? "WYBIERZ STREFĘ" : "ZATWIERDŹ RUCH") :
                  "TWOJA KOLEJ · OD TERAZ GRASZ SAMODZIELNIE"
            color: Theme.gold; font.pixelSize: 13; font.bold: true
        }
        Text {
            x: 18; y: 39; width: 604; wrapMode: Text.WordWrap
            text: b.tutorialGuided ? b.hint : "Masz już podstawy. Od tury 4 możesz sam wybierać dowolne dozwolone karty i strefy. Wygraj 2 z 3 stref. Przy remisie stref decyduje suma punktów na stole."
            color: Theme.white; font.pixelSize: 15
        }
        Text {
            x: 18; y: 91; width: 604; wrapMode: Text.WordWrap
            visible: b.tutorialGuided
            text: "Cel: wygraj 2 pola. Przy remisie pól decyduje suma punktów na stole."
            color: Theme.gold; font.pixelSize: 13
        }
        BButton {
            visible: b.tutorialPractice
            x: 480; y: 115; width: 144; height: 28; compact: true
            text: "Rozumiem"
            onClicked: table.practiceAcknowledged = true
        }
    }
    // Show the encounter condition before mulligan, never at the same time.
    FadeBox {
        id: ruleWindow
        objectName: "tabotaRuleWindow"
        anchors.fill: parent; open: !!b.rulePending; z: 400
        color: "#dc0b0715"
        MouseArea { anchors.fill: parent }  // Modal, no card or keyboard shortcut leak.
        Rectangle {
            anchors.centerIn: parent
            width: 790; height: 465; radius: 18
            color: Theme.panel; border.color: Theme.gold; border.width: 2
            Text { x: 32; y: 24; text: "PRZED ROZPOCZĘCIEM · WYZWANIE " + s.encounter.id + " / 20"; color: Theme.gold; font.pixelSize: 12; font.letterSpacing: 2 }
            Text { x: 32; y: 65; width: 730; text: "WARUNEK WYZWANIA"; color: Theme.white; font.pixelSize: 29; font.bold: true }
            Text { x: 32; y: 117; width: 730; text: s.encounter.ruleName; color: Theme.gold; font.pixelSize: 22; font.bold: true; wrapMode: Text.WordWrap }
            Flickable {
                x: 32; y: 174; width: 730; height: 164; contentHeight: conditionText.implicitHeight
                clip: true; ScrollBar.vertical: ScrollBar {}
                Text { id: conditionText; width: 705; text: s.encounter.activeRule; color: Theme.white; font.pixelSize: 17; wrapMode: Text.WordWrap; lineHeight: 1.35 }
            }
            Rectangle { x: 32; y: 347; width: 725; height: 1; color: Theme.line }
            Text { x: 32; y: 360; width: 725; text: "Ten warunek obowiązuje przez cały pojedynek. W trakcie gry możesz wrócić do niego w panelu po prawej."; color: Theme.muted; font.pixelSize: 13; wrapMode: Text.WordWrap }
            BButton {
                x: 32; y: 405; width: 725; height: 43; primary: true
                text: b.mulligan ? "Rozumiem · przejdź do wymiany kart  →" : "Rozumiem · rozpocznij pojedynek  →"
                onClicked: api.acknowledgeRule()
            }
        }
    }

}
