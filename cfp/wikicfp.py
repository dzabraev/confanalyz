#coding=utf8

import requests
import logging
import lxml.html
import pymongo
import dateutil.parser

# conference series http://www.wikicfp.com/cfp/program?id=494&s=CLIN

class WikicfpExtract(object)
    def __init__(self):
        self.logger = logging.getLogger("wikicfp")
        self.logger.setLevel(logging.INFO)
        self.client = pymongo.MongoClient()
        self.confs = self.client.confs
        self.cfp = self.confs.cfp
        self.origin = 'wikicfp'

    def get_last_extracted_event_id(self):
        items = self.cfp.find({'origin': self.origin}).sort(
            [('eventid', pymongo.DESCENDING)]).limit(1)
        if items.count() == 0:
            return 0
        else
            return items[0]["eventid"]

    def get_last_eventid(self):
        attempt_max = 10
        for attempt in range(attempt_max):
            self.logger.info("trying to fetch last eventid, attempt=%s/%s" % (
                attempt, attempt_max))
            resp = requests.get("http://www.wikicfp.com/cfp/")
            if resp.status_code != 200:
                self.logger.info("Cant fetch last eventid, status_code = %s" %
                    resp.status_code)
                continue
            tree = lxml.html.fromstring(resp.text)
            node = tree.xpath('//div[@class="contsec"]/form/table/tr[3]/td/table/tr[2]/td[1]/a')[0]
            href = node.attrib['href']
            eventid = int(re.match('.*eventid=(\d+).*', href).groups()[0])
            self.logger.info("Extracted last eventid=%s" % eventid)
            return eventid

    def extract_event_failed(self, eventid):
        self.logger.info("Cant extract eventid=%s url=%s, status_code=%s" %
            (eventid, url, resp.status_code))
        items = self.cfp.find({"eventid": eventid})
        if items.count() == 0:
            item = {
                "eventid": eventid,
                "url": url,
                "failed": True,
                "fail_cnt": 1,
            }
        else:
            item = items[0]
            item["fail_cnt"] += 1
        self.cfp.insert_one(item)

    def safe(f):
        try:
            return safe()
        except IndexError:
            return None

    def extract_event(self, eventid):
        url = 'http://www.wikicfp.com/cfp/servlet/event.showcfp?eventid=%s' % eventid
        resp = requests.get(url)
        if resp.status_code != 200:
            self.extract_event_failed(eventid)
            return
        if 'This item has been deleted' in resp.text:
            self.logger.info("Item for eventid=%s does not exists" % eventid)
            return
        try:
            tree = lxml.html.fromstring(resp.text)
        except Exception as e:
            print e
            self.extract_event_failed(eventid)
            return

        safe = self.safe

        fullname = safe(lambda : tree.xpath('//*[@property="v:description"]')[0].text.strip())
        shortname = safe(lambda : tree.xpath('//*[@property="v:summary"]')[0].attrib["content"].strip())
        eventType = safe(lambda : tree.xpath('//*[@property="v:eventType"]')[0].attrib["content"].strip())
        startDate = safe(lambda : dateutil.parser.parse(tree.xpath('//*[@property="v:startDate"]')[0].attrib["content"].strip()))
        endDate = safe(lambda : dateutil.parser.parse(tree.xpath('//*[@property="v:endDate"]')[0].attrib["content"].strip()))
        location = safe(lambda : tree.xpath('//*[@property="v:locality"]')[0].text.strip())
        url_candidates = tree.xpath('//div[@class="contsec"]/center/table/tr/td[@align="center"]/a[@target="_newtab"]')
        assert len(url_candidates) == 0
        conf_url = url_candidates[0]

        

    def extract(self):
        last_eventid = self.get_last_eventid()
        last_extracted_event_id = self.get_last_extracted_event_id()
        for eventid in range(last_extracted_event_id, last_eventid):
            self.extract_event(eventid)

def main():
    WikicfpExtract().extract()

if __name__ == "__main__":
    main()