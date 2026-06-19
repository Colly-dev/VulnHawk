
import paramiko
from typing import List, Dict, Any

class SSHAuditor:
    """
    Audits Linux SSH configuration (Read-Only).
    """

    def analyze(self, host: str, username: str, key_path: str) -> List[Dict[str, Any]]:
        findings = []
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            client.connect(host, username=username, key_filename=key_path, timeout=10)
            
            # Read sshd_config (requires read permission, often world-readable or accessible via sudo)
            # Using 'sshd -T' is a better way to see active configuration
            stdin, stdout, stderr = client.exec_command('sshd -T')
            config_output = stdout.read().decode()
            
            checks = {
                "permitrootlogin": {"expected": "no", "severity": "HIGH", "id": "SSH_ROOT_LOGIN"},
                "passwordauthentication": {"expected": "no", "severity": "MEDIUM", "id": "SSH_PASSWORD_AUTH"},
                "protocol": {"expected": "2", "severity": "CRITICAL", "id": "SSH_PROTOCOL_1"},
                "x11forwarding": {"expected": "no", "severity": "LOW", "id": "SSH_X11_FORWARDING"}
            }

            for line in config_output.splitlines():
                parts = line.split()
                if len(parts) >= 2:
                    key = parts[0].lower()
                    value = parts[1].lower()
                    
                    if key in checks:
                        if value != checks[key]["expected"]:
                            findings.append({
                                "id": f"LINUX_{checks[key]['id']}",
                                "title": f"Insecure SSH Setting: {key}",
                                "description": f"The SSH setting '{key}' is set to '{value}', but should be '{checks[key]['expected']}'.",
                                "severity": checks[key]["severity"],
                                "type": "INSECURE_SSH_CONFIG",
                                "category": "OS Hardening"
                            })

        except Exception as e:
            findings.append({
                "id": "SSH_CONN_ERROR",
                "title": "SSH Connection Error",
                "description": str(e),
                "severity": "INFO",
                "type": "CONNECTION_ERROR",
                "category": "General"
            })
        finally:
            client.close()
            
        return findings
