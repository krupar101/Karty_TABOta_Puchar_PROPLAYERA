import QtQuick
import QtQuick.Controls

Item {
    property var s: api.state
    Heading { width: 780; eyebrow: s.free ? "SWOBODNA ROZGRYWKA" : s.hard ? "PROPLAYER / KAMPANIA HARD" : "KAMPANIA / PUCHAR PROPLAYERA"; title: "Dwadzieścia wyzwań o Złoty Taboret."; subtitle: s.completed + " / 20 pieczątek zwycięstwa. Każdy przeciwnik ma własną, jawną regułę." }
    Row { anchors.right: parent.right; y: 20; spacing: 10
        BButton { text: "FABUŁA"; compact: true; primary: !s.hard && !s.free; onClicked: api.campaignMode(false, false) }
        BButton { text: "PROPLAYER"; compact: true; primary: s.hard; enabled: s.hardAvailable; onClicked: api.campaignMode(true, false) }
        BButton { text: "Pojedynki"; compact: true; primary: s.free; enabled: s.journal.length > 0; onClicked: api.campaignMode(false, true) }
    }
    Row { visible: s.free; anchors.right: parent.right; y: 70; spacing: 8
        Repeater { model: ["easy", "normal", "hard"]
            BButton { required property string modelData; text: ({easy:"Łatwy", normal:"Normalny",hard:"Trudny"})[modelData]; primary: s.difficulty === modelData; compact: true; onClicked: api.setDifficulty(modelData) }
        }
    }
    Column { y: 130; spacing: 16
        Repeater { model: 4
            Column {
                required property int index
                property int actIndex: index
                spacing: 9
                Text { text: "AKT " + ["I", "II", "III", "IV"][actIndex] + "    /    " + s.missions[actIndex*5].act.toUpperCase(); color: Theme.gold; font.pixelSize: 10; font.letterSpacing: 2 }
                Row { spacing: 14
                    Repeater { model: 5
                        Rectangle {
                            id: node
                            required property int index
                            property var e: s.missions[actIndex*5+index]
                            width: 260; height: 105; radius: 10
                            color: hover.hovered && e.available ? "#30203d" : Theme.panel
                            border.color: e.done ? "#486c59" : e.available ? Theme.gold : Theme.line
                            opacity: e.available || e.done ? 1 : .46
                            Behavior on color { ColorAnimation { duration: 140 } }
                            Image { x: 10; y: 10; width: 54; height: 84; source: e.image; fillMode: Image.PreserveAspectFit; sourceSize.width: 120; asynchronous: true }
                            Column { x: 77; y: 13; width: 174; spacing: 7
                                Text { text: (e.id < 10 ? "0" : "") + e.id + (e.done ? "  /  PIECZĄTKA ✓" : e.available ? "  /  DOSTĘPNA" : "  /  ZABLOKOWANA"); color: e.done ? Theme.green : Theme.gold; font.pixelSize: 9; font.letterSpacing: .8 }
                                Text { width: parent.width; text: e.short; color: Theme.white; font.bold: true; font.pixelSize: 15; elide: Text.ElideRight }
                                Text { width: parent.width; text: e.ruleName; color: Theme.muted; font.pixelSize: 10; wrapMode: Text.WordWrap; maximumLineCount: 2 }
                            }
                            HoverHandler { id: hover }
                            Button { anchors.fill: parent; background: Item {} text: ""; enabled: node.e.available; onClicked: api.chooseMission(node.e.id); Accessible.name: node.e.name }
                        }
                    }
                }
            }
        }
    }
    Row { y: 704; spacing: 12
        BButton { text: "Kolekcja / talie"; compact: true; onClicked: api.navigate("collection") }
        BButton { text: "Kronika Turnieju"; compact: true; onClicked: api.navigate("journal") }
        BButton { visible: s.resumable; text: "Wróć do meczu"; compact: true; primary: true; onClicked: api.resumeMatch() }
    }
}
