import QtQuick
import QtQuick.Controls
Item {
    property var s: api.state
    Heading { width: 1000; eyebrow: "PRYWATNE ARCHIWUM / LOKALNIE"; title: "Karty pamiętają."; subtitle: "Otwórz dawny układ z tymi samymi kartami, kolejnością i interpretacją. Bez ponownego losowania." }
    Row { y: 128; spacing: 12
        Field { width: 430; height: 42; placeholderText: "Szukaj pytania, daty lub liczby kart…"; color: Theme.white; background: Rectangle { color: Theme.panel; border.color: Theme.line; radius: 6 } onTextEdited: api.filterHistory(text) }
        BButton { text: "Eksportuj historię"; compact: true; onClicked: api.exportData("readings") }
        BButton { text: "Importuj JSON"; compact: true; onClicked: api.importData("readings") }
        BButton { text: "Usuń wszystko"; compact: true; enabled: s.history.length > 0; onClicked: api.deleteReading("") }
        BButton { text: "Nowa wróżba"; compact: true; primary: true; onClicked: api.navigate("fortune") }
    }
    ListView {
        y: 195; width: 1360; height: 535; model: s.history; spacing: 12; clip: true; ScrollBar.vertical: ScrollBar {}
        delegate: Rectangle {
            required property var modelData
            width: 1340; height: 100; radius: 10; color: Theme.panel; border.color: Theme.line
            Image { x: 18; y: 12; width: 48; height: 75; source: s.back; fillMode: Image.PreserveAspectFit; sourceSize.width: 96 }
            Text { x: 86; y: 16; text: modelData.date + "   /   " + modelData.count + " KART   /   " + (modelData.complete ? "ODKRYTE" : "W TRAKCIE"); color: Theme.gold; font.pixelSize: 11; font.letterSpacing: 1 }
            Text { x: 86; y: 44; width: 860; text: modelData.question || "Pytanie pozostawione kartom"; color: Theme.white; font.pixelSize: 18; elide: Text.ElideRight }
            BButton { x: 1000; y: 25; text: "Otwórz układ"; onClicked: api.openReading(modelData.id) }
            BButton { x: 1180; y: 25; width: 130; text: "Usuń"; onClicked: api.deleteReading(modelData.id) }
        }
    }
    Text { visible: !s.history.length; x: 200; y: 330; width: 960; text: "Jeszcze nie ma tutaj wróżb.\nPierwszą historię możesz rozłożyć już teraz."; color: Theme.muted; font.pixelSize: 24; horizontalAlignment: Text.AlignHCenter; lineHeight: 1.7 }
}
