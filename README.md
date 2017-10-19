# censysio

This is a Python 2.7+ compliant script to interact with Censys.io. 
Add your UID and SECRET to the censys_dumper.py file: 

```python
        self.UID = "XXXXXXXXXXXXXXX"
        self.SECRET = "XXXXXXXXXXXXXXX"
```

Then you can start using it like this: 

```bash
python censys_dumper.py -q "443.https.tls.certificate.parsed.extensions.subject_alt_name.dns_names:domain.com" -ips
```

No real license on this. Feel free to use/fork it and do whatever you want with this.