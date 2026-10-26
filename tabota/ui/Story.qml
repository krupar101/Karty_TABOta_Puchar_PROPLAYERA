import QtQuick
import QtQuick.Controls
Item {
    property var s: api.state
    property bool ending: s.screen === "ending"
    Rectangle { x: 50; y: 25; width: 1260; height: 600; radius: 18; color: Theme.panel; border.color: Theme.line }
    Card { x: 100; y: 70; width: 280; info: ({id:"01", image:s.hero, name:"Prorok Tabo"}); interactive: false }
    Column { x: 450; y: 80; width: 760; spacing: 25
        Heading { width: parent.width; eyebrow: ending ? "PUCHAR ROZSTRZYGNIĘTY" : "PROLOG  /  GODZINA 20:29"; title: ending ? (s.hard ? "CERTYFIKAT PROPLAYERA" : "MISTRZ KART TABOta") : "PUCHAR PROPLAYERA" }
        Text { width: parent.width; color: Theme.muted; font.pixelSize: 19; wrapMode: Text.WordWrap; lineHeight: 1.5
            text: ending ? (s.hard ? "Poziom HARD zaliczony! ELTaboBot próbuje wydrukować dyplom PROPLAYERA, ale drukarka odpowiada: NIC TU KURŁA NIE DZIAŁA! Złoty Taboret pozostaje twój." : "Dwadzieścia zwycięskich wyzwań! Tabo otrzymuje Złoty Taboret i tytuł PROPLAYERA. Nysmo mówi, że to tylko 20 meczów, a Jillie już domaga się rewanżu.") : "Tabo pokazuje na streamie fizyczne Karty TABOta i żartuje, że nie może przegrać we własną grę. ELTaboBot uznaje to za oficjalne zgłoszenie do 20-wyzwaniowego Pucharu PROPLAYERA. Nagroda? Złoty Taboret!" }
        Text { width: parent.width; text: ending ? (s.hard ? "ELTABOBOT: „Certyfikat gotowy.”\nDRUKARKA: „NIC TU KURŁA NIE DZIAŁA!”" : "ELTABOBOT: „Weryfikacja zakończona. PROPLAYER.”\nTABO: „Idę grać w coś normalnego.”\nELTABOBOT: „Odblokowano tryb PROPLAYER. Rewanż?”") : "TABO: „Jak ja mam przegrać we własną grę?!”\nELTABOBOT: „Zgodnie z punktem 20:30 regulaminu przyjęto wyzwanie.”\nTABO: „Jakiego regulaminu?!”"; color: Theme.gold; font.pixelSize: 21; wrapMode: Text.WordWrap; lineHeight: 1.4 }
        Text { width: parent.width; text: ending ? "Wygrałeś Puchar. Czekają rewanże, własne talie, wróżby i tryb PROPLAYER." : "20 uczestników. 4 akty. Jeden Złoty Taboret. Dialogi są autorskie."; color: Theme.muted; font.pixelSize: 13; wrapMode: Text.WordWrap }
        Row { spacing: 15
            BButton { text: ending ? "Wróć do mapy" : "Zacznij naukę"; primary: true; onClicked: ending ? api.navigate("map") : api.start(true) }
            BButton { visible: !ending; text: "Znam już zasady"; onClicked: api.chooseMission(1) }
        }
    }
}
