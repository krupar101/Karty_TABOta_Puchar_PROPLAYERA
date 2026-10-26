import QtQuick
import QtQuick.Controls
Item {
    property var s: api.state
    // Preserve the outgoing reading while the new screen fades into place.
    property var lastReading: ({})
    property var r: s.reading && s.reading.created ? s.reading : lastReading
    onSChanged: if (s.reading && s.reading.created) lastReading = s.reading
    Heading { width: 1100; eyebrow: "WRÓŻBA / " + r.created.substring(0,16).replace("T", "  "); title: r.question || "Niech karty zabiorą głos."; subtitle: r.complete ? "Odsłonięty układ. Kliknij kartę, żeby przeczytać jej oryginalny cytat." : "Klikaj karty, aby je odsłonić. Wynik jest już wylosowany - animacja go nie zmienia." }
    BButton { anchors.right: parent.right; y: 0; compact: true; text: "Historia"; onClicked: api.navigate("history") }
    Row {
        x: (1360-width)/2; y: 150; spacing: r.count === 5 ? 25 : 42
        Repeater { model: r.count
            Column {
                required property int index
                property var readingInfo: r.items[index]
                width: r.count === 5 ? 242 : r.count === 3 ? 330 : 700; spacing: 13
                Text { width: parent.width; text: (index+1) + "  /  " + readingInfo.position.toUpperCase(); color: Theme.gold; horizontalAlignment: Text.AlignHCenter; font.pixelSize: 11; font.letterSpacing: 2 }
                Card { anchors.horizontalCenter: parent.horizontalCenter; width: r.count === 5 ? 166 : 196; info: readingInfo; faceUp: readingInfo.revealed; showTip: false; onClicked: api.reveal(index) }
                Text { width: parent.width; text: readingInfo.revealed ? readingInfo.name : "Jeszcze nieodkryta"; color: Theme.white; font.pixelSize: 16; font.bold: true; horizontalAlignment: Text.AlignHCenter; wrapMode: Text.WordWrap; height: r.count === 5 ? 40 : 26 }
                Text { width: parent.width; text: readingInfo.revealed ? readingInfo.interpretation : "✧"; color: Theme.muted; font.pixelSize: r.count === 5 ? 13 : 15; wrapMode: Text.WordWrap; horizontalAlignment: Text.AlignHCenter; lineHeight: 1.3 }
            }
        }
    }
    Column { x: 30; y: 613; width: 1300; spacing: 13
        Text { width: parent.width; text: r.complete ? r.summary : "Odsłonięto " + r.revealed.length + " / " + r.count + " kart. Do tego samego układu wrócisz z historii."; color: Theme.gold; font.pixelSize: 14; horizontalAlignment: Text.AlignHCenter }
        Row { spacing: 10
            Field { id: note; width: 650; height: 44; text: r.note; placeholderText: "Twoja notatka do tego układu…"; maximumLength: 5000; color: Theme.white; background: Rectangle { radius: 6; color: Theme.panel; border.color: Theme.line } }
            BButton { text: "Zapisz notatkę"; height: 44; onClicked: api.saveNote(note.text) }
            BButton { text: "Eksport JSON"; height: 44; onClicked: api.exportData("reading") }
            BButton { text: "Nowa wróżba"; height: 44; primary: true; onClicked: api.navigate("fortune") }
        }
        Text { width: parent.width; text: "Oryginalne cytaty i słowa-klucze: na ilustracjach. Teksty pod kartami: autorskie, symboliczne dopowiedzenia."; color: Theme.muted; font.pixelSize: 11; horizontalAlignment: Text.AlignHCenter }
    }
}
