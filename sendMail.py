"""In dieser Datei befinden sich alle Funktionen, die automatisch Emails verschicken."""

import smtplib
import ssl
import configparser
import traceback
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysqlCmd as mysqlCmd
from crawler_dictionaries import issue


def sendmail(): #Funktion zum Versenden des Newsletters
    today = datetime.today()
    today_formatted = today.strftime("%d.%m.%Y")
    config = configparser.ConfigParser()
    config.read('config.ini')

    new_journals = mysqlCmd.get_new_journals()  #In dieser und ähnlichen Zeilen werden Informationen von der Db abgefragt
    accounts = mysqlCmd.get_accounts()  #In dieser und ähnlichen Zeilen werden Informationen von der Db abgefragt

    for row in accounts:    #Zunächst werden alle Accounts durchlaufen, da die Emails ggf. unterschiedlich sein können
        account_id = row[0]
        account = mysqlCmd.get_account_details(account_id)
        sender_email = "fimcrawler2020@gmail.com"
        receiver_email = account["mail"]
        password = "ShadySandro#69"

        message = MIMEMultipart("alternative")
        message["Subject"] = "DokMa Neuerscheinungen " + str(today_formatted)
        message["From"] = sender_email
        message["To"] = receiver_email

        html = """\
            <html>
              <body>
            <p style="font-weight: 400;">Liebe/r """ + account["name"] + """,</p>
            <p style="font-weight: 400;">hier die Neuerscheinungen der Zeitschriften in der Woche vom """ + str(
            today_formatted) + """:</p>
            <p style="font-weight: 400;">&nbsp;</p>
            """

        html2 = """"""

        for i in new_journals:  #hier werden alle Neuerscheinungen durchgelaufen
            new_journal_info = mysqlCmd.get_new_journal_info(i[0])
            disinterest = mysqlCmd.get_disinterest(account_id, issue["q_id"])

            print(new_journal_info)

            if disinterest is None:  #die Neuerscheinung wird nur zum HTML hinzugefügt, wenn kein Eintrag zur Desinteresse besteht
                html2 = html2 + str("""
                                <p style="font-weight: 400;">""" f'{issue["name"]}' """ (aktuelle Ausgabe: """ f'{issue["volume_and_issue"]}' """)</p>                         
                                <p style="font-weight: 400;"><u><a href=""" f'{issue["link"]}' """ <span>Verfügbar unter: """ f'{issue["link"]}' """</span></a></u></p>
                                <p style="font-weight: 400;"><u>&nbsp;</u></p> 
                                """)
        if not html2:   #Falls es keine (interessanten?) Neuerscheinungen gab:
            html2 = """Diese Woche gibt es keine Neuerscheinungen, die Sie interessieren. Falls Sie keine Desinteressen angegeben haben,
                    gibt es diese Woche keine Neuerscheinungen bei allen Zeitschriften.
                    <p style="font-weight: 400;">&nbsp;</p>"""

        else:   #Falls es Neuerscheinungen gab:
            html2 = html2 + str("""            
            <p style="font-weight: 400;"><strong>Alle Neuerscheinungen sind als Digital Augsburg Ausgaben verfügbar!</strong></p>
            <p style="font-weight: 400;"><strong>Abruf selbstst&auml;ndig</strong></p>
            <p style="font-weight: 400;">&nbsp;</p>
            """)

        html3 = str("""<p style="font-weight: 400;"><strong>Folgende Zeitschriften müssen von Ihnen manuell überprüft werden:</strong></p>""")

        journals = mysqlCmd.get_sources()

        for j in journals:  #es werden alle Journals durchlaufe
            q_id = j[0]
            journal_info = mysqlCmd.get_source(q_id)
            name = journal_info[0]
            link = journal_info[1]
            if not mysqlCmd.is_crawlable(link)[0]:  #falls diese nicht crawlbar sind, müssen diese, wie oben erwähnt, manuell überprüft werden
                html3 = html3 + str("""
                                <p style="font-weight: 400;">""" f'{name}' """</p>                         
                                <p style="font-weight: 400;"><u><a href=""" f'{link}' """ <span>Verfügbar unter: """ f'{link}' """</span></a></u></p>
                                <p style="font-weight: 400;"><u>&nbsp;</u></p> 
                                """)

        html3 = html3 + str("""
                        <p style="font-weight: 400;"><strong>&nbsp;</strong></p>
                        <p style="font-weight: 400;">Digitale Versionen (Scans bzw. PDFs) k&ouml;nnen bis<span>&nbsp;</span><strong>Sonntagabend</strong><span>&nbsp;</span>an<span>&nbsp;</span><a href="mailto:dokMa@fim-rc.de">dokMa@fim-rc.de</a><span>&nbsp;</span>bestellt werden.</p>
                        <p style="font-weight: 400;">&nbsp;</p>
                        <p style="font-weight: 400;">Viele Gr&uuml;&szlig;e und eine anregende Lekt&uuml;re w&uuml;nscht Euch</p>
                        <p style="font-weight: 400;">Die freundliche Spinne aus der Nachbarschaft :)</p>
                        <p style="font-weight: 400;">&nbsp;</p>
                        <p style="font-weight: 400;">Diese Email wird automatisch erstellt. Probleme/falsche Informationen bitte einem Admin melden!</p>
                        </body>
                        </html>""")

        part1 = MIMEText((html + html2 + html3), "html")

        message.attach(part1)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        print("Mail wurde an " + receiver_email + " verschickt!")


def send_errormail_mail():  #Diese Funktion wird aufgerufen, wenn beim Versenden der Mail (obige Funktion) etwas schiefläuft
    print("Error beim Versenden der Email")
    print(traceback.format_exc(limit=10))

    admins = mysqlCmd.get_admins()
    sender_email = "fimcrawler2020@gmail.com"
    password = "ShadySandro#69"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Error beim Versenden des FIM-Newsletters"
    message["From"] = sender_email

    for row in admins:  #Email mit Traceback wird an alle Admins versendet
        acc_id = row[0]
        receiver_email = mysqlCmd.get_admin_email(acc_id)
        message["To"] = receiver_email[0]

        html = """\
                <html>
                <body>
                    <p style="font-weight: 400;">Hallo,</p>
                    <p style="font-weight: 400;">Leider gab es einen Fehler beim Versenden des FIM-Newsletters.</p>
                    <p style="font-weight: 400;">&nbsp;</p>
                    <p style="font-weight: 400;">Folgender Error ist aufgetreten:</p>
                    <p style="font-weight: 400;">""" + traceback.format_exc(limit=10) + """</p>                    
                    <p style="font-weight: 400;">(Mögliche Fehlerquelle: nicht existierende Email-Adresse)</p>
                    <p style="font-weight: 400;">&nbsp;</p>                    
                    <p style="font-weight: 400;">Bitte schnellstmöglich beheben und anschließend das Versenden des Newsletter manuell starten.</p>
                """
        part1 = MIMEText(html, "html")

        message.attach(part1)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email[0], message.as_string()
            )

        print("Mail mit Error-Nachricht wurde an " + receiver_email[0] + " (Admin) verschickt!")

def send_errormail_crawler(website_with_error): #Diese Funktion wird aufgerufen, wenn beim Durchlauf des Webcrawlers etwas schiefläuft
    print("Error beim Abfragen der Neuerscheinungen")
    # print(traceback.format_exc(limit=5))

    admins = mysqlCmd.get_admins()
    sender_email = "fimcrawler2020@gmail.com"
    password = "ShadySandro#69"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Error beim Abfragen der Neuerscheinungen!"
    message["From"] = sender_email

    for row in admins:  #Email mit Traceback und Info, bei welchem Journal das Problem aufgetreten ist, wird an alle Admins versendet
        acc_id = row[0]
        receiver_email = mysqlCmd.get_admin_email(acc_id)
        message["To"] = receiver_email[0]

        html = """\
                                        <html>
                                        <body>
                                            <p style="font-weight: 400;">Hallo,</p>
                                            <p style="font-weight: 400;">Leider gab es einen Fehler beim Abfragen der Neuerscheinungen.</p>
                                             <p style="font-weight: 400;">&nbsp;</p>
                                           <p style="font-weight: 400;">Folgender Error ist bei Abfragen der Website '""" + website_with_error + """' aufgetreten:</p>
                                            <p style="font-weight: 400;">""" + traceback.format_exc(limit=10) + """</p>                    
                                            <p style="font-weight: 400;">Höchstwahrscheinlich ist der Fehler aus einer Veränderung an dieser Website entstanden.</p>
                                            <p style="font-weight: 400;">Bitte den XPath der zugehörigen Website in combined_spider.py überprüfen.</p>
                                            <p style="font-weight: 400;">&nbsp;</p>
                                            <p style="font-weight: 400;">Bitte schnellstmöglich beheben. Der Webcrawler hat trotzdem alle anderen Websites abgefragt und wird dies auch weiterhin tun.</p>
                                            <p style="font-weight: 400;">Das Versenden des Email-Newsletter funktioniert auch weiterhin automatisch, solange dort kein Fehler aufgetreten ist.</p>
                                        """
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(html, "html")
        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email[0], message.as_string()
            )

        print("Mail mit Error-Nachricht wurde an " + receiver_email[0] + " (Admin) verschickt!")
