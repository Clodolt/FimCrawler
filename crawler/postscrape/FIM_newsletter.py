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
