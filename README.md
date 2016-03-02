# config file generator for Cisco IP Phone (7960/7961)
## Usage
```
# just update tftp directory
python confgen.py ipphone.conf models.conf

# update sip.conf
sudo python confgen.py ipphone.conf models.conf
```

 * `ipphone.conf` - MAC Address of IP Phone and Phone name etc.
 * `models.conf`  - map of model and firmware
