# Presenzialo

## INSTALL

```
pip3 install Presenzialo
```

```
git clone https://github.com/so07/Presenzialo.git
cd HRlo
pip install -r requirements.txt
pithon3 setup.py install 
```

## USAGE

#### Authentication options

```
Presenzialo -u USER --url COMPANY_URL --idp IDP_URL
```

###### Save authentication options to default config file

```
Presenzialo -u USER --url COMPANY_URL --idp IDP_URL -s --save-password
```

#### Reports

###### Daily report

```
Presenzialo
```

###### Report for a range of days

```
Presenzialo --from YYYY-MM-DD --to YYYY-MM-DD
```

