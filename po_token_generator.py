import subprocess
import json

def generator(token_file='token.json'):

    command_path = r"C:\Users\alexm\AppData\Roaming\npm\youtube-po-token-generator"

    result = subprocess.run(
            [command_path],
            capture_output=True,
            text=True,
            check=True,
            shell=True
        )
    
    token_data = json.loads(result.stdout)
    
    # changes 'poToken' to 'po_token'
    if 'poToken' in token_data:
        token_data['po_token'] = token_data.pop('poToken')
    
    with open(token_file, 'w') as f:
        json.dump(token_data, f, indent=2)
        
    print(f"Tokens generated and saved to {token_file}")
        
if __name__ == "__main__":
    generator()