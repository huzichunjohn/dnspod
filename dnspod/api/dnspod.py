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
	self.update(kwargs)

	result = {}
	try:
	    response = requests.post(url, data=self.params, headers=self.headers)
	    data = response.data()
	    
	    result.update({
		"status": {
		    "code": data["status"]["code"],
		    "message": data["status"]["message"]
		}
	    })
	    return json.dumps(result, indent=4)
	except Exception as e:
	    raise
	
    def add_record(self):
        pass

    def delete_record(self):
        pass

if __name__ == "__main__":
    dnspod = Dnspod()
    data = dnspod.get_all_domains()
    data = json.loads(data)
    domains = data["domains"]
    domain_ids = [domain["id"] for domain in domains]
    for domain_id in domain_ids:
	print dnspod.get_all_records(domain_id)
