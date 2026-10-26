import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: window
    width: 1440; height: 900
    minimumWidth: 960; minimumHeight: 600
    visible: true
    title: "Karty TABOta: WSZYSCY DO BANA! · Puchar PROPLAYERA"
    color: Theme.bg
    font.family: Theme.font
    property var s: api.state
    // Retain the last modal contents for the closing fade. The Python bridge
    // clears detail/options immediately after a click; fading blank panels
    // would otherwise flash visibly for a frame.
    property var retainedDetail: ({})
    property bool retainedDetailTarot: false
    property var retainedOptions: []
    property string retainedConfirmation: ""
    property string retainedNotice: ""
    onSChanged: {
        if (s.detail && s.detail.id) {
            retainedDetail = s.detail
            retainedDetailTarot = !!s.detailTarot
        }
        if (s.options && s.options.length) retainedOptions = s.options
        if (s.confirmation) retainedConfirmation = s.confirmation
        if (s.notice) retainedNotice = s.notice
    }
    property var displayDetail: s.detail && s.detail.id ? s.detail : retainedDetail
    property bool displayDetailTarot: s.detail && s.detail.id ? !!s.detailTarot : retainedDetailTarot
    property var displayOptions: s.options && s.options.length ? s.options : retainedOptions
    property string displayConfirmation: s.confirmation || retainedConfirmation
    property string displayNotice: s.notice || retainedNotice
    visibility: s.settings.fullscreen ? Window.FullScreen : Window.Windowed
    onClosing: event => { event.accepted = false; api.quit() }
    Shortcut { sequence: "F11"; onActivated: api.setting("fullscreen", !window.s.settings.fullscreen) }
    Shortcut { sequence: "Escape"; onActivated: { if (window.s.detail.id) api.closeDetail(); else if(window.s.options.length) api.cancelOptions(); else if(window.s.screen === "battle") api.navigate("pause"); else if(window.s.screen === "pause") api.navigate("battle"); else api.navigate("menu") } }
    Item {
        id: stage
        width: 1440; height: 900
        anchors.centerIn: parent
        scale: Math.min(window.width / width, window.height / height)
        Rectangle { anchors.fill: parent; color: Theme.bg }
        MusicBackdrop { anchors.fill: parent }
        Row {
            x: 40; y: 27; spacing: 14
            Text { text: "✦"; color: Theme.gold; font.pixelSize: 28 }
            Text { text: "Karty TABOta"; color: Theme.white; font.pixelSize: 18; font.bold: true; font.letterSpacing: -.5 }
            Rectangle { width: 1; height: 22; color: Theme.line; anchors.verticalCenter: parent.verticalCenter }
            Text { text: "WSZYSCY DO BANA!"; color: Theme.muted; font.pixelSize: 11; font.letterSpacing: 2; anchors.verticalCenter: parent.verticalCenter }
        }
        Row {
            anchors.right: parent.right; anchors.rightMargin: 40; y: 24; spacing: 10
            BButton { visible: window.s.screen !== "menu"; text: "⌂  Menu"; compact: true; onClicked: api.navigate("menu") }
            BButton { text: "?  Zasady"; compact: true; onClicked: api.navigate("help") }
            BButton { text: "Opcje"; compact: true; onClicked: api.navigate("settings") }
        }
        Rectangle { x: 40; y: 82; width: 1360; height: 1; color: Theme.line; opacity: .65 }
        // Two-phase navigation: paint the current page fading OUT, swap its
        // Loader only after that, then fade the new page IN. Unlike a single
        // "onLoaded" animation, both halves are visible and never overlap as
        // two independent live screens (which could execute duplicate actions).
        property string requestedScreen: window.s.screen
        property string displayedScreen: requestedScreen
        function sourceFor(screen) {
            return ({menu:"Menu.qml", slots:"Slots.qml", intro:"Story.qml", ending:"Story.qml", map:"Campaign.qml", briefing:"Briefing.qml", battle:"Battle.qml", pause:"Pause.qml", result:"Result.qml", collection:"Collection.qml", builder:"Collection.qml", fortune:"Fortune.qml", reading:"Reading.qml", history:"History.qml", settings:"Settings.qml", help:"Help.qml", journal:"Help.qml"})[screen] || "Menu.qml"
        }
        onRequestedScreenChanged: {
            if (requestedScreen === displayedScreen) {
                if (pageFadeOut.running) { pageFadeOut.stop(); pageFadeIn.start() }
            } else if (!pageFadeOut.running) {
                pageFadeIn.stop()
                pageFadeOut.start()
            }
        }
        Loader {
            id: content
            objectName: "tabotaScreenLoader"
            x: 40; y: 106; width: 1360; height: 746
            source: stage.sourceFor(stage.displayedScreen)
            opacity: 1
            enabled: !pageFadeOut.running && !pageFadeIn.running
        }
        NumberAnimation {
            id: pageFadeOut
            target: content; property: "opacity"; to: 0
            duration: window.s.settings.reduced ? 20 : 150
            easing.type: Easing.InOutQuad
            onFinished: {
                stage.displayedScreen = stage.requestedScreen
                pageFadeIn.start()
            }
        }
        NumberAnimation {
            id: pageFadeIn
            target: content; property: "opacity"; from: 0; to: 1
            duration: window.s.settings.reduced ? 20 : 210
            easing.type: Easing.InOutQuad
        }
        Row { x: 40; y: 876; spacing: 15
            Text { text: "PUCHAR PROPLAYERA  /  SEZON 01"; color: Theme.muted; opacity: .65; font.pixelSize: 9; font.letterSpacing: 2 }
            Text { text: "20 przeciwników. 52 oryginalne karty. Jeden Złoty Taboret."; color: Theme.muted; opacity: .6; font.pixelSize: 10 }
        }
        Text { x: 1160; y: 873; width: 240; horizontalAlignment: Text.AlignRight; text: window.s.profile ? window.s.profileName + "  /  SLOT 0" + (window.s.activeSlot+1) : "TRYB GOŚCIA"; color: Theme.muted; font.pixelSize: 11 }

        FadeBox {
            objectName: "tabotaNotice"
            open: window.s.notice !== ""
            x: 280; y: 790; width: 880; height: message.implicitHeight+30; z: 500
            color: "#30213e"; border.color: Theme.gold; radius: 8
            Text { id: message; x: 18; y: 15; width: parent.width-80; text: window.displayNotice; color: Theme.white; wrapMode: Text.WordWrap; font.pixelSize: 13 }
            BButton { anchors.right: parent.right; anchors.rightMargin: 8; y: 8; width: 40; compact: true; text: "×"; onClicked: api.dismiss() }
        }

        FadeBox {
            objectName: "tabotaDetailDialog"
            fadeDuration: window.s.settings.reduced ? 35 : 150
            anchors.fill: parent; color: "#e3090612"; z: 300
            open: !!(window.s.detail && window.s.detail.id) && !window.s.options.length && window.s.confirmation === ""
            MouseArea { anchors.fill: parent; onClicked: api.closeDetail() }
            Rectangle {
                objectName: "tabotaDetailPanel"
                anchors.centerIn: parent
                width: 1040; height: 675; radius: 18
                color: Theme.panel; border.color: Theme.line; border.width: 1
                MouseArea { anchors.fill: parent } // Keep clicks inside the window from closing it.
                Row {
                    anchors.centerIn: parent; spacing: 60
                    Card { width: 388; info: window.displayDetail; interactive: false; showTip: false }
                    Column { width: 480; spacing: 24
                        y: 40
                        Heading { width: parent.width; eyebrow: window.displayDetailTarot ? "Oryginalne karty TABOta" : "Katalog / " + window.displayDetail.id; title: window.displayDetail.name || "" }
                        Text { font.family: "Noto Sans Symbols 2"; visible: !window.displayDetailTarot; text: "⚡ KOSZT " + window.displayDetail.cost + (window.displayDetail.kind === "event" ? "" : "     ✦ MOC " + window.displayDetail.power) + "    /    " + window.displayDetail.tag; color: Theme.gold; font.pixelSize: 18; font.bold: true }
                        Text { width: parent.width; text: window.displayDetailTarot ? window.displayDetail.fortune || "" : window.displayDetail.description || ""; color: Theme.white; wrapMode: Text.WordWrap; font.pixelSize: 21; lineHeight: 1.4 }
                        Text { visible: !!window.displayDetail.nameRuleHint; width: parent.width; text: window.displayDetail.nameRuleHint || ""; color: Theme.gold; font.pixelSize: 15; wrapMode: Text.WordWrap; lineHeight: 1.3 }
                        Text { width: parent.width; text: window.displayDetailTarot ? "Autorskie dopowiedzenie do symbolu. Oryginalny cytat i słowa-klucze znajdziesz na ilustracji." : window.displayDetail.source || ""; color: Theme.muted; font.pixelSize: 14; wrapMode: Text.WordWrap; lineHeight: 1.4 }
                        BButton { text: "Zamknij  ·  Esc"; onClicked: api.closeDetail() }
                    }
                }
            }
        }
        FadeBox {
            objectName: "tabotaTargetDialog"
            onOpenChanged: targetPanel.selectedOption = -1
            fadeDuration: window.s.settings.reduced ? 35 : 150
            anchors.fill: parent; color: "#d9090612"; z: 350
            open: window.s.options.length > 0 && window.s.confirmation === ""
            MouseArea { anchors.fill: parent; onClicked: api.cancelOptions() }
            Rectangle {
                id: targetPanel
                property int selectedOption: -1
                objectName: "tabotaTargetPanel"
                anchors.centerIn: parent
                width: 1080; height: 690; radius: 16
                color: Theme.panel; border.color: Theme.line
                MouseArea { anchors.fill: parent } // block interaction with the battle behind the modal

                // The title, effect description and preview occupy disjoint areas.
                // Never position a card over the subtitle or list of choices.
                Column {
                    id: targetHeader
                    objectName: "tabotaTargetHeader"
                    x: 30; y: 23; width: 865; spacing: 7
                    Text {
                        text: "PRECYZYJNE ZAGRANIE"
                        color: Theme.gold; font.pixelSize: 11; font.weight: Font.DemiBold
                        font.letterSpacing: 3
                    }
                    Text {
                        width: parent.width; text: window.displayOptions.length && window.displayOptions[0].sourceTitle.startsWith("Rytuał") ? "Wybierz rytuał i cel" : "Wybierz cel efektu"
                        color: Theme.white; font.pixelSize: 32; font.bold: true
                        wrapMode: Text.WordWrap
                    }
                    Text {
                        width: parent.width
                        text: window.displayOptions.length ? (window.displayOptions[0].sourceTitle.startsWith("Rytuał") ? "Wybierz jeden rytuał. Każda opcja poniżej ma opis działania i cel." : window.displayOptions[0].effect || "Wskaż kartę, na którą zadziała efekt.") : ""
                        color: Theme.muted; font.pixelSize: 14; wrapMode: Text.WordWrap
                        lineHeight: 1.2
                    }
                    Text {
                        width: parent.width
                        text: window.displayOptions.length ? (window.displayOptions[0].sourceTitle || "") +
                              (window.displayOptions[0].laneName ? "  /  " + window.displayOptions[0].laneName : "") : ""
                        color: Theme.gold; font.pixelSize: 15; font.bold: true; wrapMode: Text.WordWrap
                    }
                    Text {
                        width: parent.width
                        text: "Wybierz opcję, a następnie kliknij „Zatwierdź wybór” na dole okna."
                        color: Theme.muted; font.pixelSize: 12; wrapMode: Text.WordWrap
                    }
                }
                Card {
                    id: targetSourceCard
                    objectName: "tabotaTargetSourceCard"
                    x: 950; y: 27; width: 88
                    visible: window.displayOptions.length > 0 &&
                             !!(window.displayOptions[0].source && window.displayOptions[0].source.id)
                    info: window.displayOptions.length ? (window.displayOptions[0].source || {}) : ({})
                    battle: true; interactive: false; showTip: false; lift: false; splitClickDetails: false
                }
                ListView {
                    id: targetOptionList
                    objectName: "tabotaTargetOptionList"
                    x: 30
                    // Start below BOTH the text and the full preview card.
                    y: Math.max(185, targetHeader.y + targetHeader.implicitHeight + 16,
                                targetSourceCard.visible ? targetSourceCard.y + targetSourceCard.height + 16 : 0)
                    width: 1020
                    height: Math.max(80, cancelTarget.y - y - 12)
                    clip: true; spacing: 12
                    model: window.displayOptions
                    boundsBehavior: Flickable.StopAtBounds
                    ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded }
                    delegate: Rectangle {
                        id: optionTile
                        objectName: "tabotaTargetOption"
                        required property var modelData
                        width: 996; height: modelData.source && modelData.source.id ? Math.max(192, optionContent.implicitHeight + 28) : optionContent.implicitHeight + 28; radius: 14
                        color: optionMouse.containsMouse ? Theme.panel2 : Theme.panel
                        border.width: 2
                        border.color: targetPanel.selectedOption === modelData.index ? Theme.gold : Theme.line
                        Column {
                            id: optionContent
                            x: 16; y: 14; width: 964; spacing: 10
                            Row {
                                spacing: 10
                                Rectangle {
                                    width: sideLabel.implicitWidth + 20; height: 28; radius: 14
                                    color: "#2b2038"; border.color: Theme.gold
                                    Text { id: sideLabel; anchors.centerIn: parent; text: modelData.sourceTitle.startsWith("Rytuał") ? modelData.sourceTitle : modelData.targetSideLabel || "CEL"; color: Theme.white; font.pixelSize: 11; font.bold: true }
                                }
                                Text {
                                    width: 790
                                    text: modelData.choiceLabel || "Kliknij, aby wybrać tę opcję."
                                    color: Theme.white; font.pixelSize: 14; wrapMode: Text.WordWrap
                                }
                            }
                            Row {
                                spacing: 14
                                Repeater {
                                    model: modelData.targets || []
                                    delegate: Card {
                                        required property var modelData
                                        width: 90
                                        info: modelData
                                        battle: true; interactive: false; showTip: false; lift: false
                                        splitClickDetails: false; chosen: true
                                    }
                                }
                                Rectangle {
                                    visible: !!modelData.source.id && (!modelData.targets || modelData.targets.length === 0)
                                    width: 220; height: 95; radius: 10
                                    color: "#241b33"; border.color: Theme.line
                                    Text { anchors.centerIn: parent; width: 180; horizontalAlignment: Text.AlignHCenter; wrapMode: Text.WordWrap; text: modelData.emptyLabel || "Bez dodatkowego celu"; color: Theme.muted; font.pixelSize: 13 }
                                }
                                Column {
                                    width: modelData.targets.length ? 360 : 850; spacing: 6
                                    Text { text: modelData.laneName ? "Strefa zagrania: " + modelData.laneName : ""; color: Theme.gold; font.pixelSize: 13; font.bold: true }
                                    Text { visible: !!modelData.secondaryText; text: modelData.secondaryText || ""; color: Theme.white; font.pixelSize: 13; wrapMode: Text.WordWrap }
                                    Text { width: parent.width; visible: !!modelData.label; text: (modelData.effect || "") + "\n" + (modelData.label || ""); color: Theme.muted; font.pixelSize: 14; wrapMode: Text.WordWrap }
                                }
                            }
                        }
                        MouseArea {
                            id: optionMouse
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            onClicked: targetPanel.selectedOption = modelData.index
                        }
                    }
                }
                BButton {
                    objectName: "tabotaConfirmTarget"
                    x: 760; y: targetPanel.height - 52; width: 290; height: 36
                    text: "Zatwierdź wybór"; primary: true
                    enabled: targetPanel.selectedOption >= 0
                    onClicked: api.chooseOption(targetPanel.selectedOption)
                }
                BButton {
                    id: cancelTarget
                    x: 30; y: targetPanel.height - 52
                    height: 36; compact: true
                    text: "Anuluj"; onClicked: api.cancelOptions()
                }
            }
        }
        FadeBox {
            objectName: "tabotaConfirmationDialog"
            anchors.fill: parent; color: "#df090612"; z: 600
            open: window.s.confirmation !== ""
            MouseArea { anchors.fill: parent }
            Rectangle {
                anchors.centerIn: parent; width: 620; height: 270; radius: 16; color: Theme.panel; border.color: Theme.gold
                Text { x: 30; y: 30; text: "Potwierdzenie"; color: Theme.gold; font.pixelSize: 24; font.bold: true }
                Text { x: 30; y: 85; width: 560; text: window.displayConfirmation; color: Theme.white; font.pixelSize: 17; wrapMode: Text.WordWrap }
                Row { x: 30; y: 190; spacing: 15
                    BButton { text: "Anuluj"; primary: true; onClicked: api.confirm(false) }
                    BButton { text: "Potwierdzam"; onClicked: api.confirm(true) }
                }
            }
        }
    }
}
