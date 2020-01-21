import re
import json
import requests
import datetime

max_workers = 1000


class PRweb:
    def __init__(self, auth):
        self.auth = auth
        self.url = auth["host"]
        self.idworker, self.session, self.cookies, self.headers = self.login(auth)

    def login(self, auth):
        s = requests.Session()
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/78.0.3904.108 Chrome/78.0.3904.108 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "connection": "keep-alive",
            "pragma": "no-cache",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
        }
        r = s.get(self.url, headers=headers, allow_redirects=False)
        r = s.get(r.headers["Location"], headers=headers, allow_redirects=False)
        cookies = r.cookies
        payload = {
            "shib_idp_ls_exception.shib_idp_session_ss": "",
            "shib_idp_ls_success.shib_idp_session_ss": "true",
            "shib_idp_ls_value.shib_idp_session_ss": "",
            "shib_idp_ls_exception.shib_idp_persistent_ss": "",
            "shib_idp_ls_success.shib_idp_persistent_ss": "true",
            "shib_idp_ls_value.shib_idp_persistent_ss": "",
            "shib_idp_ls_supported": "true",
            "_eventId_proceed": "",
        }
        r = s.post(
            "{}/idp/profile/SAML2/Redirect/SSO?execution=e1s1".format(
                self.auth["idpurl"]
            ),
            headers=headers,
            allow_redirects=True,
            cookies=cookies,
            data=payload,
        )
        payload = {
            "j_username": auth["username"],
            "j_password": auth._decode(auth["password"]),
            "_eventId_proceed": "",
        }
        r = s.post(
            "{}/idp/profile/SAML2/Redirect/SSO?execution=e1s2".format(
                self.auth["idpurl"]
            ),
            headers=headers,
            allow_redirects=False,
            cookies=cookies,
            data=payload,
        )
        r = s.get(self.url, headers=headers, allow_redirects=True, cookies=cookies)
        a = re.findall('value=".*"', r.text)
        a[0] = a[0].replace("value=", "")[1:-1]
        a[1] = a[1].replace("value=", "")[1:-1]
        if not a[0]:
            print("Wrong Password")
            exit()
        payload = {"RelayState": a[0], "SAMLResponse": a[1]}
        r = s.post(
            "{}/Shibboleth.sso/SAML2/POST".format(self.url),
            allow_redirects=False,
            cookies=r.cookies,
            data=payload,
        )
        r = s.get(self.url, allow_redirects=False, cookies=r.cookies)
        headers = {
            "connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/78.0.3904.108 Chrome/78.0.3904.108 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Referer": self.url,
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
        }
        r = s.get(
            "{}/LoginShib.aspx?PageMethod=EseguiLogin".format(self.url),
            allow_redirects=False,
            headers=headers,
            cookies=s.cookies,
        )
        cookies = r.cookies
        r = s.get(
            "{}/default.aspx".format(self.url),
            allow_redirects=True,
            cookies=s.cookies,
            data=payload,
        )
        r = s.get(
            "{}/rpc/Utente.aspx?PageMethod=GetCurrent".format(self.url),
            allow_redirects=True,
            cookies=cookies,
            data=payload,
        )
        out = json.loads(r.text)
        iddip = out["iddip"]

        return iddip, s, cookies, headers

        # idworker, session, cookies, headers = PRweb.login()

    def check_json_validity(self, r, msg):
        try:
            r.json()
        except:
            raise ConnectionError(msg)

    def timecard(
        self, day_from=datetime.datetime.today(), day_to=datetime.datetime.today()
    ):

        url = "{}/rpc/Cartellino.aspx?PageMethod=DettaglioCartellino&iddip={}".format(
            self.url, self.idworker
        )

        payload = {
            "_dtdatainizio": day_from.strftime("%Y%m%d%H%M%S"),
            "_dtdatafine": day_to.strftime("%Y%m%d%H%M%S"),
        }

        r = self.session.post(
            url,
            allow_redirects=False,
            cookies=self.cookies,
            headers=self.headers,
            data=json.dumps(payload),
        )

        self.check_json_validity(r, "from timecard")

        return r.json()

    def workers_id(self):

        url = "{}/rpc/Rubrica.aspx?pageMethod=ElencoSottopostiSelectVisibilt%C3%A0Estesa&pattern=&page=1&pageLimit={}".format(
            self.url, max_workers
        )

        r = self.session.get(url, cookies=self.cookies, headers=self.headers)

        self.check_json_validity(r, "from workers_id")

        return r.json()

    def address_book(self, iddip=-1):

        if iddip == -1:
            api_name = "LeggiRubrica"
        else:
            api_name = "LeggiRubricaDettagli"

        url = "{}/rpc/Rubrica.aspx?PageMethod={}&iddip={}&data={}&_=1578658512666".format(
            self.url, api_name, iddip, datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        )

        r = self.session.post(
            url,
            allow_redirects=False,
            cookies=self.cookies,
            headers=self.headers,
            # data=json.dumps(payload)
        )

        self.check_json_validity(r, "from address_book")

        return r.json()
