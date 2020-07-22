"""Diese Datei muss für das Versenden des Newsletter ausgeführt werden.
   Notiz: Diese Datei soll vorr. 1x die Woche ausgeführt werden und ist unabhängig vom Webcrawler"""

import mysqlCmd
import sendMail

def mail():
    try:
        sendMail.sendmail()
    except:
        sendMail.send_errormail_mail()
    else:
        mysqlCmd.update_current_issues()
        mysqlCmd.reset_new_journals()

mail()