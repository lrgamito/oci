import sys 
import oci 
from oci.secrets 
import SecretsClient 
import base64 
import json 

sys.path.insert(1, '/home/datascience') 
# Pegar as senhas dos bancos direto do Vault do OCI 

# OCID do Secret
secret_id = 'ocid1.vaultsecret.oc1.sa-saopaulo-1.a.....' 

# config = from_file(path.join(path.expanduser("~"), ".oci", "config"), "DEFAULT") 
def secret_to_dict(wallet): 
	return json.loads(base64.b64decode(wallet.encode('ascii')).decode('ascii')) 
	
	
# secret_bundle = SecretsClient(config).get_secret_bundle(secret_id) 
rps = oci.auth.signers.get_resource_principals_signer() 
secret_bundle = SecretsClient({}, signer=rps).get_secret_bundle(secret_id) 
secret_content = secret_to_dict(secret_bundle.data.secret_bundle_content.content)

# Conexao dwprd01_low 
conn_username = secret_content['secrets']['DWPRD01_AYS']['user'] 
conn_password = secret_content['secrets']['DWPRD01_AYS']['pass'] 
conn_url = secret_content['secrets']['DWPRD01_AYS']['url'] 