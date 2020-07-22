# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
"""Hier werden die gecrawlten Informationen verarbeitet"""

import mysqlCmd


class SQLPipeline(object):

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        journal_info_current = mysqlCmd.get_current_issue(item['link'])
        q_id = journal_info_current[0]
        issue_current = journal_info_current[1]
        journal_info_new = mysqlCmd.get_new_issue(q_id)

        print("Current Issue: " + issue_current)
        print("Crawled Issue: " + item['issue'])
        if issue_current != item['issue']:  #ist die aktuelle Ausgabe verschieden von der Information der Db
            if journal_info_new is None:    #existiert bereits ein Eintrag zu diesem Journal als aktuelle Neuerscheinung
                print("Neues Journal gefunden!")
                mysqlCmd.set_new_issue(q_id, item['issue'], item['checkDate'])
                print("Neues Journal gespeichert")
            else:
                print(journal_info_new)
                if journal_info_new[1] != item['issue']:    #ist die aktuelle Ausgabe verschieden vom neuesten Eintrag zu diesem Journal als aktuelle Neuerscheinung
                        print("Neues Journal gefunden!")
                        mysqlCmd.set_new_issue(q_id, item['issue'], item['checkDate'])
                        print("Neues Journal gespeichert")
                else:
                    print("Journal bereits in 'Neuerscheinungen' aufgenommen")
        else:
            print("Journal bereits bekannt")
