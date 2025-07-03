import pandas as pd
from simple_salesforce import Salesforce
import webbrowser

class SalesforcePandas:
    def __init__(self, sf_instance):
        self.sf = sf_instance
        self.base_url = f"https://{sf_instance.sf_instance}"

    @classmethod
    def from_token(cls, access_token, instance_url):
        """
        Authenticate using a session ID (access token) and instance URL.
        """
        sf = Salesforce(instance=instance_url, session_id=access_token)
        return cls(sf)

    @classmethod
    def from_user_login(cls, username, password, security_token, domain='login'):
        """
        Authenticate using username, password, and security token.
        """
        sf = Salesforce(
            username=username,
            password=password,
            security_token=security_token,
            domain=domain  # 'test' for sandbox, 'login' for prod/scratch
        )
        return cls(sf)

    def query(self, soql):
        """
        Run a SOQL query and return the results as a pandas DataFrame.
        """
        result = self.sf.query_all(soql)
        df = pd.DataFrame(result.get("records", []))
        if 'attributes' in df.columns:
            df = df.drop(columns=['attributes'])
        return df

    def bulk(self, df, object_name, method="insert", external_id_field=None, label=None):
        """
        Perform bulk insert, update, upsert, or delete.
        """
        object_label = label or object_name
        if df.empty:
            print(f"No records to {method} for {object_label}. Skipping.")
            return []
        
        records = df.to_dict("records")
        api = self.sf.bulk.__getattr__(object_name)
        method = method.lower()

        if method == "insert":
            result = api.insert(records)
        elif method == "update":
            result = api.update(records)
        elif method == "upsert":
            if not external_id_field:
                raise ValueError("external_id_field is required for upsert")
            result = api.upsert(records, external_id_field)
        elif method == "delete":
            result = api.delete(records)
        else:
            raise ValueError(f"Unsupported method: {method}")

        success_count = sum(1 for r in result if r.get("success"))
        failure_count = len(result) - success_count

        verb_map = {
            "insert": "inserted",
            "update": "updated",
            "upsert": "upserted",
            "delete": "deleted"
        }
        verb = verb_map.get(method, method + "d")
        print(f"{success_count} {object_label} {verb}, {failure_count} failed")
        
        return result

    def open_record(self, record_id):
        """
        Opens a Salesforce record in your default web browser.
        
        Parameters:
            record_id (str): The 18-character Salesforce record ID.
        """
        url = f"{self.base_url}/{record_id}"
        print(f"Opening: {url}")
        webbrowser.open(url)
