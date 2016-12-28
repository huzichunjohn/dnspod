# -*- coding: utf-8 -*-

import requests
import json

class Dnspod(object):
    BASE_URL = "https://dnsapi.cn"
    LOGIN_TOKEN = "23432,7a266b74cdceb1dd49c97e860dbce685"

    def __init__(self, login_token=None):
        self.login_token = login_token if login_token else self.LOGIN_TOKEN

        self.params = {
            "login_token": self.login_token,
            "format": "json",
            "lang": "cn"
        }

        self.headers = {
            "UserAgent": "Dnspod client/0.0.1 (huzichunjohn@126.com)"
        }

    def get_all_domains(self, **kwargs):
        url = self.BASE_URL + "/Domain.List"
        self.params.update(kwargs)

        result = {}
        try:
            response = requests.post(url, data=self.params, headers=self.headers)
            data = response.json()

            result.update({
                "status": {
                    "code": data["status"]["code"],
                    "message": data["status"]["message"]
                }
            })

            if data["status"]["code"] == "1":
                domains = []
                for domain in data["domains"]:
                    domains.append({
                        "id": domain["id"],
                        "name": domain["name"],
                        "remark": domain["remark"]
                    })
                result.update({"domains": domains})

            return json.dumps(result, indent=4)
        except Exception as e:
            raise

    def get_all_records(self, domain_id, **kwargs):
        url = self.BASE_URL + "/Record.List"
        self.params.update({"domain_id": domain_id})
        self.params.update(kwargs)

        result = {}
        try:
            response = requests.post(url, data=self.params, headers=self.headers)
            data = response.json()

            result.update({
                "status": {
                    "code": data["status"]["code"],
                    "message": data["status"]["message"]
                }
            })

            if data["status"]["code"] == "1":
                records = []
                for record in data["records"]:
                    records.append({
                        "id": record["id"],
                        "name": record["name"],
                        "type": record["type"],
                        "ttl": record["ttl"],
                        "value": record["value"],
                        "remark": record["remark"]
                    })
                result.update({"records": records})

            return json.dumps(result, indent=4)
        except Exception as e:
            raise

    def add_domain(self, domain, **kwargs):
        url = self.BASE_URL + "/Domain.Create"
        self.params.update({"domain": domain})
        self.params.update(kwargs)
    
        result = {}
        try:
            response = requests.post(url, data=self.params, headers=self.headers)
            data = response.json()
    
            result.update({
                "status": {
                "code": data["status"]["code"],
                "message": data["status"]["message"]
                }
            })

            if data["status"]["code"] == "1":
                result.update({
                    "domain": {
                    "id": data["domain"]["id"],
                    "domain": data["domain"]["domain"]
                    }
                })
            return json.dumps(result, indent=4)
        except Exception as e:
            raise

    def delete_domain(self, domain_id, **kwargs):
        url = self.BASE_URL + "/Domain.Remove"
        self.params.update({"domain_id": domain_id})
        self.params.update(kwargs)

        result = {}
        try:
            response = requests.post(url, data=self.params, headers=self.headers)
            data = response.json()
        
            result.update({
                "status": {
                "code": data["status"]["code"],
                "message": data["status"]["message"]
                }
            })
            return json.dumps(result, indent=4)
        except Exception as e:
            raise
    
    def add_record(self, domain_id, sub_domain, record_type, value, record_line_id, **kwargs):
        url = self.BASE_URL + "/Record.Create"
        self.params.update({
            "domain_id": domain_id,
            "sub_domain": sub_domain,
            "record_type": record_type,
            "record_line_id": record_line_id,
            "value": value
        })
        self.params.update(kwargs)

        result = {}
        try:
            response = requests.post(url, data=self.params, headers=self.headers)
            data = response.json()
            result.update({
                "status": {
                    "code": data["status"]["code"],
                    "message": data["status"]["message"]
                }
            })            
            
            if data["status"]["code"] == "1":
                result.update({
                    "record": {
                        "id": data["record"]["id"],
                        "name": data["record"]["name"],
                        "status": data["record"]["status"]
                    }
                })
            return json.dumps(result, indent=4)
        except Exception as e:
            raise
        
    def delete_record(self, domain_id, record_id):
        url = self.BASE_URL + "/Record.Remove"
        self.params.update({
            "domain_id": domain_id,
            "record_id": record_id
        })
        
        result = {}
        try:
            response = requests.post(url, data=self.params, headers=self.headers)
            data = response.json()
            result.update({
                "status": {
                    "code": data["status"]["code"],
                    "message": data["status"]["message"]
                }
            })
            return json.dumps(result, indent=4)
        except Exception as e:
            raise

    def edit_record(self, domain_id, record_id, record_line_id, **kwargs):
        url = self.BASE_URL + "/Record.Modify"
        self.params.update({
           "domain_id": domain_id,
            "record_id": record_id,
            "record_line_id": record_line_id
        })
        self.params.update(kwargs)
 
        result = {}
        try:
            response = requests.post(url, data=self.params, headers=self.headers)
            data = response.json()
            result.update({
                "status": {
                    "code": data["status"]["code"],
                    "message": data["status"]["message"]
                }
            })

            if data["status"]["code"] == "1":
                result.update({
                    "record": data["record"]
                })

        except Exception as e:
            raise
        return json.dumps(result, indent=4)

    def get_lines(self, domain_id, domain_grade="D_Free"):
        url = self.BASE_URL + "/Record.Line"
        self.params.update({
            "domain_id": domain_id,
            "domain_grade": domain_grade
        })

        result = {}
        try:
            response = requests.post(url, data=self.params, headers=self.headers)
            data = response.json()
            result.update({
                "status": {
                    "code": data["status"]["code"],
                    "message": data["status"]["message"]
                }
            })

            if data["status"]["code"] == "1":
                result.update({
                    "line_ids": data["line_ids"],
                    "lines": data["lines"]
                })
        except Exception as e:
            raise

        return json.dumps(result, indent=4)

if __name__ == "__main__":
    dnspod = Dnspod()
    data = dnspod.get_all_domains()
    data = json.loads(data)
    domains = data["domains"]
    domain_ids = [domain["id"] for domain in domains]
    for domain_id in domain_ids:
        print dnspod.get_all_records(domain_id)
    data = dnspod.add_domain("huzichun.com")
    data = json.loads(data)
    if data["status"]["code"] == "1":
        domain_id = data["domain"]["id"]
        import time
        time.sleep(5)
        data = dnspod.get_lines(domain_id)
        data = json.loads(data)
        record_line_id = data["line_ids"][u"默认"]
        data = dnspod.add_record(domain_id, "www", "A", "172.16.0.1", record_line_id)
        data = json.loads(data)
        print data["status"]["message"]
        record_id = data["record"]["id"]

        time.sleep(5)
        data = dnspod.edit_record(domain_id, record_id, record_line_id, **{"value": "172.16.0.2"})
        data = json.loads(data)
        print data

        time.sleep(5)
        data = dnspod.delete_record(domain_id, record_id)
        data = json.loads(data)
        print data["status"]["message"]

        time.sleep(5)
        data = dnspod.delete_domain(domain_id)
        data = json.loads(data)
        print data["status"]["message"]
