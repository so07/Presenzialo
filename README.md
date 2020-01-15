# presenzialo

## INSTALL

```
pip3 install presenzialo
```

```
git clone https://github.com/so07/presenzialo.git
cd HRlo
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

