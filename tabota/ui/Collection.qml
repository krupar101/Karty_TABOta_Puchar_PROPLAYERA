import QtQuick
import QtQuick.Controls
Item {
    property var s: api.state
    property bool builder: s.screen === "builder"
    Heading { width: 900; eyebrow: builder ? s.draft ? "PROPLAYER / DRAFT 24 → 18" : "WŁASNA TALIA" : "KOLEKCJA / " + s.unlocked + " Z 76 KART"; title: builder ? "Zbuduj swój argument." : "Każda karta ma swoją historię."; subtitle: builder ? "18 kart · co najmniej 12 jednostek · co najmniej jedna za ⚡ 1 · do 2 kopii typu" : "Odkryte karty możesz obejrzeć. Zakryte mają rewers oraz warunek odblokowania." }
    BButton { visible: !builder; anchors.right: parent.right; y: 10; text: "Zbuduj talię  →"; primary: true; onClicked: api.openBuilder() }
    Row { y: 130; spacing: 12
        Field { id: search; width: 390; height: 40; placeholderText: "Szukaj karty lub umiejętności…"; color: Theme.white; font.pixelSize: 14; background: Rectangle { radius: 6; color: Theme.panel; border.color: Theme.line } onTextEdited: api.filterCards(text, tag.currentText) }
        Select { id: tag; width: 190; height: 40; model: ["Wszystkie", "Widz", "Retro", "Chaos", "Hymn", "Horror", "Moderacja", "Technika", "Wydarzenie"]; onActivated: api.filterCards(search.text, currentText) }
        BButton { visible: builder; text: "Autoułóż"; compact: true; onClicked: api.autoDeck() }
        BButton { visible: builder; text: "Wyczyść wybór"; compact: true; onClicked: api.clearDeck() }
    }
    GridView {
        id: gallery
        x: 0; y: 190; width: builder ? 1020 : 1360; height: 548; clip: true
        cellWidth: 170; cellHeight: builder ? 290 : 332
        model: s.catalog
        ScrollBar.vertical: ScrollBar {}
        delegate: Item {
            required property var modelData
            width: 170; height: gallery.cellHeight
            Card { x: 12; y: 12; width: 140; info: modelData; battle: true; playable: modelData.unlocked; faceUp: modelData.unlocked; interactive: modelData.unlocked; onClicked: if (modelData.unlocked) api.inspect(modelData.id) }
            Text { x: 12; y: 239; width: 140; text: modelData.unlocked ? modelData.name : "🔒 " + modelData.id + " · NIEODKRYTA"; color: modelData.unlocked ? Theme.white : Theme.gold; font.pixelSize: 11; font.bold: !modelData.unlocked; elide: Text.ElideRight }
            Text { visible: !builder && !modelData.unlocked; x: 12; y: 257; width: 144; height: 68; text: modelData.unlockHint || "Odblokuj w kampanii"; color: Theme.muted; font.pixelSize: 11; wrapMode: Text.WordWrap; elide: Text.ElideRight; maximumLineCount: 4 }
            HoverHandler { id: lockedHover; enabled: !modelData.unlocked }
            ToolTip.visible: !modelData.unlocked && lockedHover.hovered
            ToolTip.delay: 400
            ToolTip.text: modelData.unlockHint || "Odblokuj w kampanii"
            Row { visible: builder; x: 12; y: 259; spacing: 5
                BButton { text: "−"; width: 35; height: 26; compact: true; enabled: modelData.count > 0; onClicked: api.deckChange(modelData.id, -1) }
                Text { width: 60; text: modelData.count + " / " + modelData.offered; color: Theme.gold; horizontalAlignment: Text.AlignHCenter; font.pixelSize: 12; anchors.verticalCenter: parent.verticalCenter }
                BButton { text: "+"; width: 35; height: 26; compact: true; enabled: modelData.count < modelData.offered && s.deckCount < 18; onClicked: api.deckChange(modelData.id, 1) }
            }
        }
    }
    Rectangle {
        visible: builder; x: 1040; y: 125; width: 320; height: 613; radius: 12; color: Theme.panel; border.color: Theme.line
        Text { x: 18; y: 18; text: "TWOJA TALIA   " + s.deckCount + " / 18"; color: Theme.gold; font.pixelSize: 16; font.bold: true }
        Text { x: 18; y: 48; text: s.deckUnits + " jednostek  /  " + (s.deckCount-s.deckUnits) + " wydarzeń"; color: Theme.muted; font.pixelSize: 12 }
        Row { x: 18; y: 80; spacing: 12
            Repeater { model: s.curve
                Item { required property int modelData; required property int index; width: 35; height: 54
                    Rectangle { anchors.bottom: parent.bottom; anchors.bottomMargin: 17; width: 24; height: Math.min(36, modelData*5); color: Theme.purple; radius: 2 }
                    Text { y: 40; width: 24; text: index+1; horizontalAlignment: Text.AlignHCenter; color: Theme.muted; font.pixelSize: 10 }
                }
            }
        }
        ListView {
            x: 18; y: 146; width: 284; height: 242; model: s.deck; clip: true; spacing: 5; ScrollBar.vertical: ScrollBar {}
            delegate: Rectangle { required property var modelData; width: 276; height: 32; radius: 4; color: Theme.panel2
                Text { x: 9; y: 8; width: 235; text: modelData.count + "×  " + modelData.name; color: Theme.white; font.pixelSize: 11; elide: Text.ElideRight }
                BButton { anchors.right: parent.right; width: 30; height: 32; compact: true; text: "−"; onClicked: api.deckChange(modelData.id, -1) }
            }
        }
        Text { x: 18; y: 400; width: 284; text: s.deckErrors.length ? s.deckErrors.join("\n") : "✓  Talia jest gotowa do gry."; color: s.deckErrors.length ? Theme.red : Theme.green; font.pixelSize: 12; wrapMode: Text.WordWrap }
        Select { id: presets; x: 18; y: 455; width: 245; height: 33; model: s.presets; textRole: "name"; displayText: count ? currentText : "Brak zapisanych talii"; onActivated: api.preset(currentIndex, false) }
        BButton { x: 268; y: 455; width: 34; height: 33; text: "×"; compact: true; enabled: presets.count > 0; onClicked: api.preset(presets.currentIndex, true) }
        Field { id: presetName; x: 18; y: 498; width: 178; height: 36; placeholderText: "Nazwa presetu"; color: Theme.white; maximumLength: 60; background: Rectangle { color: Theme.bg; border.color: Theme.line; radius: 5 } }
        BButton { x: 202; y: 498; width: 100; height: 36; compact: true; text: "Zapisz"; enabled: !s.deckErrors.length; onClicked: api.savePreset(presetName.text) }
        BButton { x: 18; y: 548; width: 284; primary: true; text: s.draft ? "Zatwierdź draft i graj  →" : "Wróć do wyboru rywala  →"; enabled: !s.deckErrors.length; onClicked: s.draft ? api.start(false) : api.campaignMode(false, true) }
    }
}
