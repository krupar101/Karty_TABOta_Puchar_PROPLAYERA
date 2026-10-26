import QtQuick
import QtQuick.Controls

Item {
    property var s: api.state
    Heading { width: 1100; eyebrow: "ZAPIS LOKALNY"; title: "Każdy taboret ma swoją historię."; subtitle: "Trzy niezależne kampanie. Wróżby mają własne archiwum, wspólne dla tego urządzenia." }
    Field { id: profileName; x: 0; y: 140; width: 440; height: 46; placeholderText: "Nazwa rozgrywki (opcjonalnie)"; maximumLength: 60; color: Theme.white; font.pixelSize: 15; background: Rectangle { radius: 7; color: Theme.panel; border.color: Theme.line } }
    Row { y: 230; spacing: 24
        Repeater { model: s.slots
            Rectangle {
                required property var modelData
                width: 436; height: 310; radius: 14; color: Theme.panel; border.color: modelData.exists ? Theme.purple : Theme.line
                Column { x: 28; y: 28; width: 380; spacing: 22
                    Text { text: "ZAPIS 0" + (modelData.index+1); color: Theme.gold; font.pixelSize: 12; font.letterSpacing: 3 }
                    Text { text: modelData.name; color: Theme.white; font.pixelSize: 27; font.bold: true }
                    Text { text: modelData.exists ? modelData.progress + " / 20 wyzwań ukończonych" : "Puchar czeka na pierwszego zawodnika."; color: Theme.muted; font.pixelSize: 15 }
                    Text { text: modelData.updated; color: Theme.muted; font.pixelSize: 12 }
                    Row { spacing: 10
                        BButton { visible: modelData.exists; text: "Wczytaj"; primary: true; onClicked: api.loadSlot(modelData.index) }
                        BButton { text: modelData.exists ? "Nowa kampania" : "Rozpocznij"; primary: !modelData.exists; onClicked: api.newGame(modelData.index, profileName.text) }
                    }
                }
            }
        }
    }
    BButton { y: 600; text: "←  Powrót"; onClicked: api.navigate("menu") }
}
