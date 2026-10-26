import QtQuick
import QtQuick.Controls
Item {
    property var s: api.state
    // During an outgoing screen fade the bridge may already clear the match.
    // Keep its last complete visual state until this page finishes fading out.
    property var lastBoard: ({})
    property var b: s.board && s.board.lanes ? s.board : lastBoard
    onSChanged: if (s.board && s.board.lanes) lastBoard = s.board
    property bool won: b.winner === 0
    Heading { x: 70; y: 15; width: 1100; eyebrow: "WYZWANIE " + s.encounter.id + " / " + s.encounter.short; title: won ? (b.tutorial ? "Szkolenie zaliczone!" : "Pieczątka zdobyta!") : b.winner === -1 ? "Remis. Puchar czeka." : "To wyzwanie wymaga rewanżu."; subtitle: "Najpierw liczba wygranych stref, dopiero przy remisie suma punktów. Nie tracisz zdobytych kart." }
    Row { x: 70; y: 170; spacing: 25
        Repeater { model: 3
            Rectangle {
                required property int index
                property var lane: b.lanes[index]
                width: 390; height: 190; radius: 14; color: Theme.panel; border.color: lane.player > lane.enemy ? Theme.gold : Theme.line
                Text { anchors.horizontalCenter: parent.horizontalCenter; y: 22; text: lane.name; color: Theme.muted; font.pixelSize: 12; font.letterSpacing: 3 }
                Text { anchors.horizontalCenter: parent.horizontalCenter; y: 57; text: lane.player + " : " + lane.enemy; color: lane.player > lane.enemy ? Theme.gold : Theme.white; font.pixelSize: 48; font.bold: true }
                Text { anchors.horizontalCenter: parent.horizontalCenter; y: 133; text: lane.player > lane.enemy ? "↑  TWOJA STREFA" : lane.player < lane.enemy ? "↓  STREFA RYWALA" : "=  REMIS"; color: Theme.muted; font.pixelSize: 11; font.letterSpacing: 1 }
            }
        }
    }
    Text { x: 70; y: 396; text: "STREFY   " + b.wins[0] + " : " + b.wins[1] + "      /      SUMA   " + b.total[0] + " : " + b.total[1]; color: Theme.gold; font.pixelSize: 20; font.bold: true }
    Text { x: 70; y: 443; width: 1190; text: "„" + s.dialogue + "”"; color: Theme.white; font.pixelSize: 23; wrapMode: Text.WordWrap }
    Text { x: 70; y: 505; width: 1190; text: won && !s.free ? "ZDOBYTE KARTY / " + s.encounter.unlocks.join(" · ") + (s.hard ? "   •   Ramka PROPLAYER i wpis HARD" : "   •   Pieczątka w Kronice Turnieju") : "Wskazówka: spróbuj odpuścić najmocniejszą strefę rywala i przejąć pozostałe dwie."; color: Theme.muted; font.pixelSize: 15; wrapMode: Text.WordWrap }
    Text { visible: won && !!s.encounter.actFinalText && !s.free; x: 70; y: 542; width: 1240; text: s.encounter.actFinalText || ""; color: Theme.gold; font.pixelSize: 13; font.bold: true; wrapMode: Text.WordWrap }
    Row { x: 70; y: 580; spacing: 15
        BButton { text: "Dalej  →"; primary: true; onClicked: api.nextMission() }
        BButton { text: s.hard ? "Rewanż · ten sam draft" : "Rewanż"; onClicked: s.hard ? api.openDraft(true) : api.start(false) }
        BButton { visible: s.hard; text: "Nowy draft"; onClicked: api.openDraft(false) }
        BButton { text: "Kolekcja"; onClicked: api.navigate("collection") }
        BButton { text: "Log meczu"; onClicked: api.navigate("battle") }
    }
    Text { x: 70; y: 670; text: "SEED " + b.seed + "  /  ZASADY 1.0.0"; color: Theme.muted; font.pixelSize: 10; font.letterSpacing: 2 }
}
