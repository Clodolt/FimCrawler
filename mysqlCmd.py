"""In dieser Datei sind alle benötigten SQL-Abfragen gespeichert. Falls etwas an der Datenbank geändert wird, kann der Code hier zentral angepasst.
   Die Funktionen sollten durch ihre Namen selbsterklärend sein. """

import mysql.connector
import crawler_dictionaries

conn = mysql.connector.connect(
    # Zugangsdaten der Datenbank, mehr Parameter auch hinzugefügt werden (Dokumentation)
    host="93.177.66.153",
    user="remote",
    passwd="ShadySandro#69",
    database="django"
)
curr = conn.cursor(buffered=True)


def get_sources():
    curr.execute("SELECT id, link FROM core_journal WHERE crawlable = 1")
    return curr.fetchall()


def get_source(q_id):
    curr.execute("SELECT name, link, issue FROM core_journal WHERE id = %s", (q_id,))
    return curr.fetchone()


def get_new_journals():
    curr.execute("SELECT N_ID FROM neuerscheinungen")
    return curr.fetchall()


def get_new_journal(n_id):
    curr.execute("SELECT Q_ID, volume_and_issue, checkdate FROM neuerscheinungen WHERE N_ID = %s", (n_id,))
    return curr.fetchone()


def get_new_issue(q_id):
    curr.execute("SELECT Q_ID, volume_and_issue, checkdate FROM neuerscheinungen WHERE Q_ID = %s ORDER BY N_ID DESC", (q_id,))
    return curr.fetchone()


def get_current_issue(link):
    curr.execute("SELECT id, issue FROM core_journal WHERE link = %s", (link,))
    return curr.fetchone()


def get_new_journal_info(n_id):
    new_issue = get_new_journal(n_id)
    crawler_dictionaries.issue["q_id"] = new_issue[0]
    crawler_dictionaries.issue["volume_and_issue"] = new_issue[1]
    crawler_dictionaries.issue["checkdate"] = new_issue[2]
    journal_info = get_source(crawler_dictionaries.issue['q_id'])
    crawler_dictionaries.issue["name"] = journal_info[0]
    crawler_dictionaries.issue["link"] = journal_info[1]
    crawler_dictionaries.issue["issue"] = journal_info[2]
    return crawler_dictionaries.issue


def get_accounts():
    curr.execute("SELECT id FROM auth_user")
    return curr.fetchall()


def get_account_details(account_id):
    curr.execute("SELECT first_name, email FROM auth_user WHERE id = %s", (account_id,))
    account_details = curr.fetchone()
    crawler_dictionaries.account["account_id"] = account_id
    crawler_dictionaries.account["name"] = account_details[0]
    crawler_dictionaries.account["mail"] = account_details[1]
    return crawler_dictionaries.account


def get_disinterest(account_id, q_id):
    sql_disinterest = "SELECT * FROM core_profile_not_interested WHERE profile_id = %s AND journal_id = %s"
    curr.execute(sql_disinterest, (account_id, q_id))
    return curr.fetchone()


def get_admins():
    curr.execute("SELECT id FROM auth_user WHERE is_superuser = b'1'")
    return curr.fetchall()


def get_admin_email(acc_id):
    sql_admin_email = "SELECT email FROM auth_user WHERE id = %s"
    curr.execute(sql_admin_email, (acc_id,))
    return curr.fetchone()


def set_new_issue(q_id, issue, checkDate):
    curr.execute("INSERT INTO neuerscheinungen (Q_ID, volume_and_issue, checkdate) VALUES (%s, %s, %s)",
                 (q_id, issue, checkDate))
    conn.commit()


def update_current_issues():
    new_issues = get_new_journals()
    for row in new_issues:
        n_id = row[0]
        new_journal_info = get_new_journal_info(n_id)
        sql_issue_old = "UPDATE core_journal SET issOld = issue WHERE id = %s"
        curr.execute(sql_issue_old, (crawler_dictionaries.issue['q_id'],))
        conn.commit()
        sql_issue_current = "UPDATE core_journal SET issue = %s WHERE id = %s"
        curr.execute(sql_issue_current, (crawler_dictionaries.issue['volume_and_issue'], crawler_dictionaries.issue['q_id']))
        conn.commit()
        sql_issue_current = "UPDATE core_journal SET date_latest_issue = %s WHERE id = %s"
        curr.execute(sql_issue_current, (crawler_dictionaries.issue['checkdate'], crawler_dictionaries.issue['q_id']))
        conn.commit()


def reset_new_journals():
    curr.execute("DELETE FROM neuerscheinungen")
    conn.commit()


def is_crawlable(link):
    sql_crawlable = "SELECT crawlable FROM core_journal WHERE link = %s"
    curr.execute(sql_crawlable, (link,))
    return curr.fetchone()