import QtQuick
import QtQuick.Controls

Item {
    property var s: api.state
    Column {
        x: 40; y: 48; width: 560; spacing: 0
        Row { spacing: 10
            Rectangle { width: 24; height: 1; color: Theme.gold; anchors.verticalCenter: parent.verticalCenter }
            Text { text: "P U C H A R  P R O P L A Y E R A"; color: Theme.gold; font.pixelSize: 11; font.letterSpacing: 2 }
        }
        Text { text: "Karty TABOta"; color: Theme.white; font.pixelSize: 67; font.bold: true; font.letterSpacing: -3 }
        Text { text: "WSZYSCY DO BANA!"; color: Theme.gold; font.pixelSize: 25; font.bold: true; font.letterSpacing: 3 }
        Item { height: 24; width: 1 }
        Text { width: 445; text: "ELTaboBot zapisał cię do turnieju.\nPozostało wygrać 20 wyzwań i zdobyć Złoty Taboret."; color: Theme.muted; font.pixelSize: 19; lineHeight: 1.5 }
        Item { height: 34; width: 1 }
        BButton { width: 390; height: 60; text: s.profile ? "KONTYNUUJ PUCHAR     →" : "ROZPOCZNIJ PUCHAR     →"; primary: true; onClicked: api.continueCup() }
        Item { height: 12; width: 1 }
        BButton { visible: s.resumableFree; width: 390; height: 50; text: "Wróć do meczu     →"; onClicked: api.resumeMatch() }
        Item { visible: s.resumableFree; height: 12; width: 1 }
        BButton { width: 390; height: 54; text: "✧     WRÓŻBY Z KART TABOta"; onClicked: api.navigate("fortune") }
        Item { height: 12; width: 1 }
        Row { spacing: 12
            BButton { width: 189; text: "Nowa gra / sloty"; onClicked: api.navigate("slots") }
            BButton { width: 189; text: "Swobodny pojedynek"; enabled: s.profile && s.journal.length > 0; onClicked: api.campaignMode(false, true) }
        }
        Item { height: 32; width: 1 }
        Row { spacing: 25
            Repeater { model: ["3 STREFY", "6 TUR", "TWÓJ PLAN"]
                Text { required property string modelData; text: modelData; color: Theme.muted; font.pixelSize: 10; font.letterSpacing: 1.7 }
            }
        }
    }
    Item {
        x: 640; y: 10; width: 660; height: 630
        Rectangle { anchors.centerIn: parent; width: 540; height: 540; radius: 270; color: "#161020"; border.color: "#392444" }
        Rectangle { anchors.centerIn: parent; width: 600; height: 600; radius: 300; color: "transparent"; border.color: "#281c35" }
        Rectangle { anchors.centerIn: parent; width: 450; height: 450; radius: 225; color: "transparent"; border.color: "#5b3d55" }
        Repeater { model: 12
            Text { required property int index; x: 320+Math.cos(index*Math.PI/6)*278; y: 305+Math.sin(index*Math.PI/6)*278; text: index%3===0 ? "✦" : "·"; color: Theme.gold; opacity: .7; font.pixelSize: index%3===0 ? 19 : 14 }
        }
        Card { x: 68; y: 150; width: 213; rotation: -19; faceUp: false; interactive: false }
        Card { x: 364; y: 150; width: 213; rotation: 19; faceUp: false; interactive: false }
        Card {
            id: hero; x: 211; y: 94; width: 248; rotation: -3
            info: ({id:"01", image:s.hero, name:"Prorok Tabo"}); showTip: false
            onClicked: api.inspect("01")
            SequentialAnimation on y {
                loops: Animation.Infinite; running: !s.settings.reduced
                NumberAnimation { from: 94; to: 83; duration: 2400; easing.type: Easing.InOutSine }
                NumberAnimation { from: 83; to: 94; duration: 2400; easing.type: Easing.InOutSine }
            }
        }
        Text { x: 100; y: 554; width: 480; text: "„Podobno nikt tego nie czyta.”"; color: Theme.gold; font.pixelSize: 17; font.italic: true; horizontalAlignment: Text.AlignHCenter }
        Text { x: 100; y: 586; width: 480; text: "PROROK TABO  /  KARTA 01"; color: Theme.muted; font.pixelSize: 10; font.letterSpacing: 2.5; horizontalAlignment: Text.AlignHCenter }
    }
    Rectangle { x: 40; y: 675; width: 1280; height: 1; color: Theme.line }
    Row { x: 40; y: 694; spacing: 14
        BButton { text: "Kolekcja  /  " + s.unlocked + " z 76"; compact: true; onClicked: api.navigate("collection") }
        BButton { text: "Kronika Turnieju"; compact: true; onClicked: api.navigate("journal") }
        BButton { text: "Autorzy i zasady"; compact: true; onClicked: api.navigate("help") }
    }
    BButton { x: 1150; y: 694; width: 170; text: "Wyjście z gry"; compact: true; onClicked: api.quit() }
}
