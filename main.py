import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    tipo = ft.TextField( label="Tipo")
    marca = ft.TextField( label="Marca")
    anno_acquisto = ft.TextField( label="Anno Acquisto")

    myText = ft.TextField(width = 60,
                            disabled = True, #campo di testo disabilitato: impedisce all'utente di modificare direttamente il contenuto dalla GUI
                            text_align = ft.TextAlign.CENTER,
                            value = "0")

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def handler_minus(e):
        valore=int(myText.value)
        if valore > 0:
            valore -= 1
            myText.value= str(valore)
        myText.update()

    def handler_plus(e):
        valore=int(myText.value)
        valore += 1
        myText.value = str(valore)
        myText.update()

    def aggiungi_strumento(e):
        #leggere i valori inseriti nei campi
        nuovo_tipo = tipo.value.strip()
        nuova_marca = marca.value.strip()
        nuovo_anno_acquisto = anno_acquisto.value.strip()

        #controllare che i campi non siano vuoti
        if nuovo_tipo == "" or nuova_marca == "" or nuovo_anno_acquisto == "":
            alert.show_alert("❌Errore: compilare tutti i campi")
            return
        else:
            try:
                nuovo_anno_acquisto = int(nuovo_anno_acquisto)
                valore = float(myText.value)
            except ValueError:
                alert.show_alert("❌Errore: Anno e valore devono essere numeri validi.")
                return

            #verificare che l'anno sia valido
            if nuovo_anno_acquisto <= 0 or valore <=0:
                alert.show_alert("❌ Inserire un anno valido e valore valido!")
            else:
                deposito.aggiungi_strumento(nuovo_tipo, nuova_marca, nuovo_anno_acquisto, valore)

                # svuota i campi
                tipo.value = ""
                marca.value = ""
                anno_acquisto.value = ""

                #riporta il contatore a zero
                myText.value = "0"

                # aggiorna la lista e l'interfaccia
                aggiorna_lista_strumenti()
                page.update()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    myBtnMinus = ft.IconButton(icon = ft.Icons.REMOVE,
                               icon_size = 20,
                               icon_color = "red",
                               on_click = handler_minus)

    myBtnPlus = ft.IconButton(icon = ft.Icons.ADD,
                              icon_size = 20,
                              icon_color = "green",
                               on_click = handler_plus)

    pulsante_aggiungi_strumento = ft.Button("Aggiungi strumento", on_click = aggiungi_strumento)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Text("Aggiungi nuovo strumento", size=20),
        ft.Row(controls=[tipo, marca, anno_acquisto, myBtnMinus, myText, myBtnPlus],
                alignment=ft.MainAxisAlignment.CENTER),

        ft.Row(controls = [pulsante_aggiungi_strumento],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()
    page.update()

ft.run(main)
