import requests


def handle(email: str = 'err', password: str = 'err'):
    sess = requests.Session()
    req1 = sess.get(
        'https://login.live.com/oauth20_authorize.srf?client_id=000000004C12AE6F&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&display=touch&response_type=token&locale=en')
    sfttag = req1.text.split('value="')[1].split('''"/>\'''')[0]
    urlpost = req1.text.split('urlPost:\'')[1].split("',")[0]
    print(sfttag)
    print(urlpost)
    payload = {'login': email, 'loginfmt': email, 'passwd': password, 'PPFT': sfttag}
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    req2 = sess.post(urlpost, headers=headers, params=payload)
    fail = open('somerandomrequest.txt', mode='w')
    fail.write(req2.text)
    fail.close()
    print(req2.history)

handle()
