import QtQuick
Item {
    property var s: api.state
    Column { x: 360; y: 70; width: 640; spacing: 20
        Heading { width: parent.width; eyebrow: "PAUZA / ZAPIS LOKALNY"; title: "Karty mogą chwilę poczekać."; subtitle: "Stan stołu i niezatwierdzony plan są zapisane. Wrócisz dokładnie do tej tury." }
        BButton { width: 640; text: "Wznów pojedynek"; primary: true; onClicked: api.navigate("battle") }
        BButton { width: 640; text: "Zasady gry"; onClicked: api.navigate("help") }
        BButton { width: 640; text: "Zapisz i przejdź do menu"; onClicked: api.navigate("menu") }
        BButton { width: 640; text: "Poddaj pojedynek"; onClicked: api.abandon() }
        Text { width: parent.width; text: s.encounter.rule; color: Theme.muted; font.pixelSize: 16; wrapMode: Text.WordWrap; lineHeight: 1.5 }
    }
}
