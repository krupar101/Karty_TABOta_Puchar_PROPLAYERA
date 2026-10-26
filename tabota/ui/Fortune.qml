import QtQuick
import QtQuick.Controls
Item {
    id: fortune
    property var s: api.state
    property int count: 3
    property int phase: 0
    Heading { x: 20; y: 15; width: 850; eyebrow: "ORYGINALNE KARTY TABOta / 52 SYMBOLE"; title: "Jaką odpowiedź kryją karty?"; subtitle: "Chwila skupienia. Odrobina absurdu. Wróżba tylko dla ciebie." }
    BButton { anchors.right: parent.right; y: 20; text: "Historia wróżb  →"; onClicked: api.navigate("history") }
    Item {
        x: 60; y: 190; width: 440; height: 490
        Rectangle { x: -10; y: 0; width: 400; height: 400; radius: 200; color: "#171021"; border.color: "#3d2948" }
        Repeater { model: 4
            Card {
                required property int index
                x: 65 + index*5; y: 20 + index*4; width: 228; rotation: -7+index*3
                faceUp: false; interactive: false
                SequentialAnimation on x {
                    running: fortune.phase === 1 && !s.settings.reduced; loops: 3
                    NumberAnimation { to: index%2 ? 155 : -10; duration: 160; easing.type: Easing.InOutQuad }
                    NumberAnimation { to: 65+index*5; duration: 180; easing.type: Easing.InOutQuad }
                }
            }
        }
        Text { x: -10; y: 420; width: 400; text: phase === 0 ? "SKUP SIĘ NA PYTANIU" : phase === 1 ? "TASOWANIE…" : "ODCIĘCIE LEWĄ RĘKĄ"; color: Theme.gold; font.pixelSize: 11; font.letterSpacing: 3; horizontalAlignment: Text.AlignHCenter }
    }
    Column { x: 555; y: 170; width: 760; spacing: 19
        Text { text: "TWOJE PYTANIE  /  OPCJONALNE"; color: Theme.gold; font.pixelSize: 11; font.letterSpacing: 2 }
        Rectangle { width: parent.width; height: 125; radius: 10; color: Theme.panel; border.color: question.activeFocus ? Theme.gold : Theme.line
            TextArea { id: question; anchors.fill: parent; anchors.margins: 12; placeholderText: "Co dziś zasługuje na moją uwagę?"; placeholderTextColor: Theme.muted; color: Theme.white; font.pixelSize: 18; wrapMode: Text.WordWrap; selectByMouse: true; onTextChanged: if (text.length > 500) text = text.substring(0,500) }
        }
        Text { text: question.length + " / 500 znaków  ·  Pytanie nie opuszcza tego urządzenia."; color: Theme.muted; font.pixelSize: 12 }
        Row { spacing: 12
            Repeater { model: [1, 3, 5]
                BButton { required property int modelData; width: 244; height: 68; primary: fortune.count === modelData; text: modelData === 1 ? "1  /  Odpowiedź" : modelData === 3 ? "3  /  Przeszłość · Teraz · Dalej" : "5  /  Sytuacja do Finału"; onClicked: fortune.count = modelData }
            }
        }
        Text { width: parent.width; text: count === 1 ? "Jedna karta, jeden symbol. Czasem najmniejsza odpowiedź robi najwięcej hałasu." : count === 3 ? "Przeszłość → Teraz → Przyszłość. Trzy spojrzenia na twoją historię." : "Sytuacja → Problem → Rada → Chaos → Finał. Pełny scenariusz z obowiązkowym absurdem."; color: Theme.muted; font.pixelSize: 15; wrapMode: Text.WordWrap }
        Item {
            width: 760; height: visible ? 40 : 0
            visible: fortune.phase === 2 || opacity > 0.001
            opacity: fortune.phase === 2 ? 1 : 0
            enabled: fortune.phase === 2
            Behavior on opacity { NumberAnimation { duration: s.settings.reduced ? 35 : 190; easing.type: Easing.InOutQuad } }
            Slider { id: cut; anchors.fill: parent; from: 1; to: 51; value: 26; stepSize: 1 }
        }
        Text {
            visible: fortune.phase === 2 || opacity > 0.001
            opacity: fortune.phase === 2 ? 1 : 0
            Behavior on opacity { NumberAnimation { duration: s.settings.reduced ? 35 : 190 } }
            text: "Punkt odcięcia: " + Math.round(cut.value) + " / 52. Przesuń suwak lub pozostaw środek."
            color: Theme.muted; font.pixelSize: 12
        }
        Row { spacing: 12
            BButton { width: 300; primary: true; text: phase === 0 ? "Potasuj talię  ✧" : phase === 1 ? "Pomiń tasowanie" : "Odetnij lewą ręką i rozłóż  →"; onClicked: { if (phase===0) { api.uiSound("shuffle"); phase=1; shuffleTimer.restart() } else if (phase===1) phase=2; else api.divine(question.text, count, Math.round(cut.value)) } }
            BButton {
                enabled: phase === 2
                opacity: phase === 2 ? 1 : 0
                Behavior on opacity { NumberAnimation { duration: s.settings.reduced ? 35 : 190 } }
                text: "Potasuj ponownie"; onClicked: { api.uiSound("shuffle"); phase=1; shuffleTimer.restart() }
            }
        }
        Text { width: parent.width; text: "To symboliczna zabawa, nie przepowiednia. Interpretacje są autorskie i działają w pełni offline. " + (s.settings.autoReadings ? "Układ zapisuje się automatycznie, również przed odsłonięciem wszystkich kart." : "Automatyczny zapis historii jest wyłączony."); color: Theme.muted; font.pixelSize: 12; wrapMode: Text.WordWrap; lineHeight: 1.4 }
    }
    Timer { id: shuffleTimer; interval: s.settings.reduced ? 80 : 1200; onTriggered: fortune.phase=2 }
}
