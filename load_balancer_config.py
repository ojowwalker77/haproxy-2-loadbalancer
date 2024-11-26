import json

# Caminhos para os arquivos filtrados
input_file_backends = "filtered_backends.json"
input_file_frontends = "filtered_frontends.json"

# Lendo os dados dos arquivos filtrados
with open(input_file_backends, "r") as file:
    backends_data = json.load(file)

with open(input_file_frontends, "r") as file:
    frontends_data = json.load(file)

load_balancer_type = "external"

# Função para gerar as configurações detalhadas do GCP
def generate_gclb_configuration(frontends, backends, lb_type):
    configurations = {
        "frontends": [],
        "backends": []
    }

    # Adicionando configurações de frontends
    for frontend in frontends:
        configurations["frontends"].append({
            "frontend_name": frontend["frontend_name"],
            "binds": [],
            "options": [],
            "acls": [],
            "other_config": frontend["config"],
            "type": lb_type
        })

    # Adicionando configurações de backends
    for backend in backends:
        backend_entry = {
            "backend_name": backend["backend_name"],
            "servers": [],
            "health_check": None,
            "session_affinity": None,
            "options": [],
            "other_config": backend["config"]
        }
        for line in backend["config"]:
            line = line.strip()
            if line.startswith("server"):
                parts = line.split()
                server_name = parts[1]
                server_address = parts[2].split(":")
                backend_entry["servers"].append({
                    "name": server_name,
                    "ip": server_address[0],
                    "port": server_address[1] if len(server_address) > 1 else None
                })
            elif line.startswith("option httpchk"):
                health_check_parts = line.split(" ", 2)
                backend_entry["health_check"] = {
                    "method": health_check_parts[1],
                    "path": health_check_parts[2]
                }
            elif "cookie" in line and "prefix" in line:
                backend_entry["session_affinity"] = "cookie"
        configurations["backends"].append(backend_entry)

    return configurations

# Gerando as configurações completas
gclb_configurations = generate_gclb_configuration(frontends_data, backends_data, load_balancer_type)

# Salvando as configurações completas em um arquivo JSON
output_file_path = "gclb_configurations.json"
with open(output_file_path, "w") as file:
    json.dump(gclb_configurations, file, indent=4)

print(f"As configurações completas do Load Balancer foram geradas e salvas em: {output_file_path}")
