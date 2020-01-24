# presenzialo

## INSTALL

```
pip3 install presenzialo
```

```
git clone https://github.com/so07/presenzialo.git
cd presenzialo
pip install -r requirements.txt
pithon3 setup.py install 
```

## USAGE

#### Authentication options

```
presenzialo -u USER --url COMPANY_URL --idp IDP_URL
```

###### Save authentication options to default config file

```
presenzialo -u USER --url COMPANY_URL --idp IDP_URL -s --save-password
```

#### Reports

###### Daily report

```
presenzialo
```

###### Report for a range of days

```
presenzialo --from YYYY-MM-DD --to YYYY-MM-DD
```


## `presenzialo` Telegram bot, aka `PRbot`

This wiki is about how to create and run a `presenzialo` bot in [Telegram](https://telegram.org/)

### Create a Telegram bot

Talk to [@BotFather](https://telegram.me/botfather) and type `/newbot` for a new bot and follow the instructions
```
you:
/newbot

BotFather:
Alright, a new bot. How are we going to call it? Please choose a name for your bot.

you:
presenzialo

BotFather:
Good. Now let's choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.

you:
PRbot

BotFather:
....

Use this token to access the HTTP API:
TOKEN
```
Save the TOKEN and paste it in the token key of PRbot section in the presenzialo configuration file for authentication
```
$ vi ~/.presenzialo/auth
```

```
[PRauth]
...
[PRbot]
token = TOKEN
```

### Run `PRbot`

Launch `PRbot` executable on a server with a working installation of `presenzialo`
```
$ PRbot
```
Open Telegram App or go to [Telegram Web](https://web.telegram.org) in a browser and start talk with `presenzialo` bot.

### Talk with `PRbot`

List of simple commands to run in telegram bot.

help of commands
```
/help
```

launch simple inline button interface and wake-up bot
```
/bot
```

today times report
```
/time
```

today time stamps report
```
/stamp
```

check status of worker
```
/in name [name ...]
```

get worker's name from a phone number
```
/phone 12345 [12345 ...]
```

