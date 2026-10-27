import QtQuick
import QtQuick.Controls
Item {
    property var s: api.state
    property var volumes: api.volumes
    Heading { width: 1100; eyebrow: "USTAWIENIA / TWOJE TEMPO"; title: "Dostosuj swój stół."; subtitle: "Zmiany działają od razu i zapisują się na tym urządzeniu." }
    Column { x: 0; y: 128; width: 620; spacing: 8
        Repeater { model: [({key:"reduced", title:"Zmniejszone animacje", desc:"Bez kołysania i przechylania. Krótkie przejścia do 80 ms."}),({key:"fullscreen",title:"Pełny ekran",desc:"Przełącz również klawiszem F11."}),({key:"music",title:"Muzyka",desc:"Tematy ekranów i każdego pojedynku. Płynne przejścia pomiędzy utworami."}),({key:"sound",title:"Dźwięki interfejsu i kart",desc:"Autorskie, syntetyczne dźwięki. Bez skopiowanych głosów."}),({key:"autoReadings",title:"Automatyczny zapis wróżb",desc:"Zachowuj także częściowo odkryte układy."}),({key:"veteran",title:"Tryb weterana - wcześniejszy HARD",desc:"Odblokowuje PROPLAYER. Draft nadal korzysta ze zdobytej kolekcji."})]
            Rectangle { required property var modelData; width: 620; height: 64; radius: 9; color: Theme.panel; border.color: Theme.line
                Text { x: 18; y: 8; text: modelData.title; color: Theme.white; font.pixelSize: 17; font.bold: true }
                Text { x: 18; y: 34; width: 500; text: modelData.desc; color: Theme.muted; font.pixelSize: 11; wrapMode: Text.WordWrap }
                Switch { anchors.right: parent.right; anchors.rightMargin: 15; anchors.verticalCenter: parent.verticalCenter; checked: s.settings[modelData.key]; onToggled: api.setting(modelData.key, checked) }
            }
        }
        Text { text: "Głośność muzyki  /  " + Math.round(volumes.musicVolume*100) + "%"; color: Theme.white; font.pixelSize: 14 }
        Slider { width: 620; from: 0; to: 1; value: volumes.musicVolume; onMoved: api.setting("musicVolume", value) }
        Text { text: "Głośność dźwięków kart i interfejsu  /  " + Math.round(volumes.volume*100) + "%"; color: Theme.muted; font.pixelSize: 14 }
        Slider { width: 620; from: 0; to: 1; value: volumes.volume; onMoved: api.setting("volume", value); onPressedChanged: if (!pressed) api.uiSound("click") }
    }
    Column { x: 690; y: 145; width: 670; spacing: 25
        Heading { width: parent.width; eyebrow: "DANE BEZ CHMURY"; title: "Twoje zapisy zostają u ciebie."; subtitle: "Kampania i wróżby są niezależne. Gra zapisuje pliki atomowo i zachowuje ostatnią kopię .bak." }
        Text { width: parent.width; text: "KATALOG ZAPISÓW\n" + s.dataPath; color: Theme.muted; font.pixelSize: 14; wrapMode: Text.WrapAnywhere; lineHeight: 1.5 }
        Row { spacing: 12
            BButton { text: "Eksport kampanii"; onClicked: api.exportData("campaign") }
            BButton { text: "Import kampanii"; onClicked: api.importData("campaign") }
        }
        Row { spacing: 12
            BButton { text: "Eksport historii wróżb"; onClicked: api.exportData("readings") }
            BButton { text: "Import historii"; onClicked: api.importData("readings") }
        }
        Text { width: parent.width; text: "Pytania nie trafiają do sieci ani telemetrii. Eksport JSON zawiera ich treść - zachowaj go tam, gdzie chcesz przechowywać swoje prywatne notatki."; color: Theme.muted; font.pixelSize: 14; wrapMode: Text.WordWrap; lineHeight: 1.5 }
        BButton { text: s.resumable ? "Wróć do meczu" : "Wróć do menu"; primary: true; onClicked: s.resumable ? api.resumeMatch() : api.navigate("menu") }
    }
}
