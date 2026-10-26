import QtQuick
import QtQuick.Controls
Item {
    property var s: api.state
    property var e: s.encounter
    Rectangle { x: 0; y: 20; width: 390; height: 650; radius: 18; color: Theme.panel; border.color: Theme.line }
    Card { x: 64; y: 62; width: 260; info: ({id:e.portrait, image:e.image, name:e.short}); onClicked: api.inspect(e.portrait) }
    Text { x: 35; y: 510; width: 320; text: "„" + s.dialogue + "”"; color: Theme.gold; wrapMode: Text.WordWrap; horizontalAlignment: Text.AlignHCenter; font.pixelSize: 19; lineHeight: 1.4 }
    Flickable {
        objectName: "tabotaBriefingScroll"
        x: 440; y: 28; width: 920; height: 620
        contentHeight: briefingContent.height; clip: true
        boundsBehavior: Flickable.StopAtBounds
        ScrollBar.vertical: ScrollBar {}
        Column { id: briefingContent; width: 890; spacing: 22
        Heading { width: parent.width; eyebrow: "WYZWANIE " + e.id + " / 20  ·  " + e.act; title: e.name; subtitle: e.scene }
        Text { visible: !!e.actIntroText; width: parent.width; text: e.actIntroText || ""; color: Theme.gold; font.pixelSize: 15; font.bold: true; wrapMode: Text.WordWrap }
        Text { width: parent.width; text: e.story; color: Theme.muted; font.pixelSize: 17; wrapMode: Text.WordWrap; lineHeight: 1.4 }
        Rectangle { width: 890; height: ruleText.implicitHeight+72; radius: 12; color: Theme.panel2; border.color: Theme.line
            Text { x: 22; y: 17; text: "✦   WARUNEK WYZWANIA · DZIAŁA NA OBIE STRONY"; color: Theme.gold; font.pixelSize: 11; font.letterSpacing: 1 }
            Text { id: ruleText; x: 22; y: 44; width: 846; text: e.activeRule; color: Theme.white; font.pixelSize: 16; wrapMode: Text.WordWrap; lineHeight: 1.3 }
        }
        Text { width: parent.width; text: "NAGRODY  /  " + e.unlocks.join(" · ") + "    +    pieczątka w Kronice Turnieju"; color: Theme.muted; font.pixelSize: 12; font.letterSpacing: .5 }
    }
    }
        Row { objectName: "tabotaBriefingActions"; x: 440; y: 684; spacing: 12
            BButton { primary: true; text: s.hard ? "Przejdź do draftu  →" : "Rozpocznij pojedynek  →"; width: 290; onClicked: api.start(false) }
            BButton { visible: s.free; text: "Własna talia"; onClicked: api.openBuilder() }
            BButton { text: "←  Mapa"; onClicked: api.navigate("map") }
        }
}
