import ConfigParser
import os
import sys

TFTP_DIR = "/tftpboot"
ASTERISK_DIR = "/etc/asterisk"

config = ConfigParser.ConfigParser()
modelconf = ConfigParser.ConfigParser()
config.read(sys.argv[1])
modelconf.read(sys.argv[2])

phones = config.sections()
tftp_files = {}

sip_template_base = """[general]
context=default
port=5060
bindaddr=0.0.0.0
progressinband=no
language=ja

"""

sip_template_team = """[{number}]
type=friend
defaultuser={username}
username={username}
secret={password}
host=dynamic
conreinvite=no

"""

tftp_sip_template = """image_version:{version};
line1_name:{username};
line1_authname:{username};
line1_password:{password};
line1_displayname:{username};
line1_shortname:{name};
proxy1_address:172.16.2.10;
proxy1_port:5060;
time_zone:JST;
"""

tftp_xml_sip_template = open('septemplate.xml').read()


# dialplan
extension_dial_base = """[default]
"""

sccp_template_base = """[general]
bindaddr=0.0.0.0
bindport=2000
dateformat=Y-M-D
keepalive=120

[devices]
"""

sccp_template_device = """[{username}]
device=SEP{mac};
version={version};
context=default;
line={username};

"""

sip_default = sip_template_base
# sccp_default = sccp_template_base

for phone in phones:
    param = dict(config.items(phone))
    model = dict(modelconf.items(param['model']))
    param['version'] = model['version']
    param['conftype'] = model['conftype']

    os.system("rm -f "+TFTP_DIR+"/"+"SIP"+param['mac']+".cnf")
    os.system("rm -f "+TFTP_DIR+"/"+"SEP"+param['mac']+".cnf.xml")
    sip_default += sip_template_team.format(**param)

    if param['conftype'].upper() == "SIP":
        tftp_files["SIP"+param['mac']+".cnf"] = tftp_sip_template.format(**param)
    elif param['conftype'].upper() == "SEP":
        # sccp_default += sccp_template_device.format(**param)
        tftp_files["SEP"+param['mac']+".cnf.xml"] = tftp_xml_sip_template.format(**param)

    # sip_default += sip_template_team.format(**param)
    # sccp_default += sccp_template_device.format(**param)
    # tftp_files["SEP"+param['mac']+".cnf.xml"] = tftp_xml_sip_template.format(**param)
    # tftp_files["SIP"+param['mac']+".cnf"] = tftp_sip_template.format(**param)

for fname, s in tftp_files.items():
    open(os.path.join(TFTP_DIR, fname), "w").write(s)

open(os.path.join(ASTERISK_DIR, "sip.conf"), "w").write(sip_default)
# open(os.path.join(ASTERISK_DIR, "skinny.conf"), "w").write(sccp_default)
