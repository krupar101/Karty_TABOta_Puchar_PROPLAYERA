import QtQuick
import QtQuick.Controls
Item {
    property var s: api.state
    property bool journal: s.screen === "journal"
    id: guide
    property bool showExtra: false
    property bool displayedExtra: false
    onShowExtraChanged: rulesFade.restart()
    SequentialAnimation {
        id: rulesFade
        NumberAnimation {
            target: rulesList; property: "opacity"; to: 0
            duration: guide.s.settings.reduced ? 20 : 120
        }
        ScriptAction { script: guide.displayedExtra = guide.showExtra }
        NumberAnimation {
            target: rulesList; property: "opacity"; from: 0; to: 1
            duration: guide.s.settings.reduced ? 20 : 190
        }
    }
    property var basics: [
        {title:"01  /  Wygraj dwie strefy", body:"Na stole są 3 strefy: STREAM, CZAT i ZAPLECZE. Wykładaj na nich karty. Po 6 turach wygrywa ten, kto ma więcej ✦ Mocy w przynajmniej 2 strefach. Przy równej liczbie wygranych stref rozstrzyga suma punktów na całym stole. Równa suma oznacza remis. Wyzw. 16 trwa 7 tur."},
        {title:"02  /  Na początku możesz wymienić karty", body:"Dostajesz 5 kart. Nie podobają ci się niektóre? Kliknij 1 lub 2 - pojawi się złota ramka i napis „DO WYMIANY”. Potem wybierz „Wymień i zacznij”. Możesz też zachować wszystkie karty i od razu rozpocząć grę."},
        {title:"03  /  ⚡ Energia pozwala zagrywać karty", body:"⚡ oznacza koszt karty: tyle Energii wydasz, żeby ją zagrać. ⚡ Twoją dostępną Energię widzisz tuż nad ręką. W turze 1 masz 1 Energię, w turze 2 masz 2, i tak dalej aż do 6. Niewydana Energia nie przechodzi do następnej tury."},
        {title:"04  /  ✦ Moc pozwala zdobywać strefy", body:"✦ oznacza Moc karty: tyle punktów daje w swojej strefie. Na przykład karta z ✦ 4 dodaje 4 punkty. Więcej Mocy niż rywal = wygrana tej strefy. W każdej strefie mieszczą się zwykle 4 twoje jednostki. Stałe bonusy z rytuałów, wydarzeń i reguł dodają punkty do strefy nawet bez kart; są pokazane pod jednostkami."},
        {title:"05  /  Wybierz kartę, potem strefę", body:"Kliknij kartę w ręce na dole, a następnie podświetloną strefę. To na razie tylko twój plan - możesz dodać kolejne karty, póki starczy ⚡ Energii, albo kliknąć „Cofnij ostatni ruch”. Niektóre karty poproszą jeszcze o wskazanie celu."},
        {title:"06  /  Kliknij „Zakończ turę”", body:"To ważne: przycisk „Zakończ turę” zatwierdza twój plan. Dopiero wtedy gra odkrywa ruchy twoje i rywala, wykonuje je i liczy ✦ Moc. Następnie zaczyna się nowa tura. Możesz zakończyć turę bez zagrania żadnej karty."},
        {title:"07  /  Dodatkowe działania kart", body:"Jednostki zostają na stole i dodają ✦ Moc. Wydarzenia działają raz, po czym znikają. „Wejście” uruchamia się po wystawieniu karty, „Aura” działa, kiedy karta leży na stole, a „Finał” rozpatruje się po ostatniej turze."}
    ]
    property var extras: [
        {title:"08  /  Wzmocnienia i ochrona", body:"Wzmocnienie dodaje ✦ Moc, osłabienie ją zmniejsza. Wyciszenie wyłącza Aurę i Finał, ale zostawia podstawową Moc. Ochrona zatrzymuje jeden wrogi efekt. Żetony także zajmują miejsca na stole."},
        {title:"09  /  Co się dzieje w kolejnych turach?", body:"Od tury 2 dobierasz po 1 karcie. Maksymalnie możesz trzymać 10. Obie strony planują ruchy w tajemnicy. W turach 1, 3 i 5 twoje ruchy wykonują się jako pierwsze, a w turach 2, 4 i 6 zaczyna rywal. Każdy przeciwnik ma dodatkową zasadę widoczną po prawej stronie stołu."},
        {title:"10  /  Rytuał 20:30", body:"Od wyzwania 04, w turze 4, dostajesz jeden darmowy Rytuał: HYMN dodaje +3 punkty w strefie, BAN wycisza wrogą kartę, a KLIP dobiera 2 karty. Możesz użyć tylko jednej opcji. Rytuał wykonuje się przy odkrywaniu planów."},
        {title:"11  /  Gdy wynik jest remisowy", body:"Remis punktów w jednej strefie nie daje jej żadnej stronie. Gdy po 6 turach obie strony wygrały tyle samo stref, liczy się suma punktów we wszystkich trzech. Gdy i ona jest taka sama, mecz kończy się remisem."},
        {title:"12  /  Inne tryby i sterowanie", body:"W kampanii FABUŁA grasz gotową talią. W PROPLAYER tworzysz własną z 18 kart (maks. 2 kopie jednego rodzaju). Prawy klik karty lub klawisz I otwiera jej podgląd; klawisze 1/2/3 wybierają strefę, Ctrl+Z cofa ruch, Esc otwiera pauzę. Wróżby z kart TABOta to osobny tryb zabawy z 52 oryginalnymi kartami."}
    ]
    Heading {
        width: 960
        eyebrow: journal ? "KRONIKA TURNIEJU / PUCHAR PROPLAYERA" : "AUTORZY I ZASADY / SZYBKI START"
        title: journal ? "Kronika Turnieju" : "Jak grać? To proste."
        subtitle: journal ? "Każda pieczątka to wygrany stolik i nowa anegdota z Pucharu." : "Wybierz kartę, wydaj ⚡ Energię i wygraj dwie strefy dzięki ✦ Mocy.\nAutor gry: KruparGames."
    }
    Row {
        anchors.right: parent.right; spacing: 10
        BButton { text: "Zasady"; compact: true; primary: !journal; onClicked: api.navigate("help") }
        BButton { text: "Kronika"; compact: true; primary: journal; onClicked: api.navigate("journal") }
    }
    BButton {
        visible: !journal
        x: 1050; y: 79; width: 310; compact: true
        text: guide.showExtra ? "Ukryj dodatkowe zasady" : "Pokaż dodatkowe zasady"
        onClicked: guide.showExtra = !guide.showExtra
    }
    Flickable {
        id: rulesList
        y: 140; width: 1360; height: 590; contentHeight: body.height; clip: true; ScrollBar.vertical: ScrollBar {}
        Column {
            id: body; width: 1300; spacing: 25
            Repeater {
                model: journal ? s.journal : guide.basics.concat(guide.displayedExtra ? guide.extras : [])
                Rectangle {
                    required property var modelData
                    width: 1300; height: textBody.implicitHeight + 80; radius: 10; color: Theme.panel; border.color: Theme.line
                    Text { x: 24; y: 18; text: journal ? (modelData.id < 10 ? "0" : "") + modelData.id + "  /  " + modelData.name : modelData.title; color: Theme.gold; font.pixelSize: 18; font.bold: true }
                    Text { id: textBody; x: 24; y: 55; width: 1250; text: journal ? modelData.story + "\n\n„" + (modelData.dialogue.LOSE || "") + "”" : modelData.body; color: Theme.muted; font.pixelSize: 16; lineHeight: 1.5; wrapMode: Text.WordWrap }
                }
            }
            Text { visible: journal && !s.journal.length; text: "Kronika jest pusta. Wygraj pierwsze wyzwanie, aby zdobyć pieczątkę."; color: Theme.muted; font.pixelSize: 20 }
        }
    }
}
