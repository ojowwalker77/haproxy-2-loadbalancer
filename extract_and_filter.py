import json

# Caminho para o arquivo haproxy.cfg
file_path_haproxy = 'haproxy.cfg'

# Lendo o arquivo haproxy.cfg
with open(file_path_haproxy, 'r') as file:
    haproxy_config_full = file.readlines()

# Estruturas para armazenar dados
frontends = []
backends = []
global_config = []
current_section = None

# Processando o arquivo linha a linha
for line in haproxy_config_full:
    line_stripped = line.strip()
    if line_stripped.startswith("global"):
        current_section = "global"
        global_config.append(line_stripped)
    elif line_stripped.startswith("frontend"):
        current_section = "frontend"
        frontends.append({"name": line_stripped.split()[1], "config": []})
    elif line_stripped.startswith("backend"):
        current_section = "backend"
        backends.append({"name": line_stripped.split()[1], "config": []})
    elif current_section == "frontend" and line_stripped:
        frontends[-1]["config"].append(line_stripped)
    elif current_section == "backend" and line_stripped:
        backends[-1]["config"].append(line_stripped)
    elif current_section == "global" and line_stripped:
        global_config.append(line_stripped)

# Organizando os resultados
result = {
    "global_config": global_config,
    "frontends": frontends,
    "backends": backends
}

# Função para filtrar configurações por VM ou IP
def filter_config_by_vm_or_ip(frontends, backends, vm_name, ip_address):
    filtered_backends = []
    filtered_frontends = []

    for backend in backends:
        for line in backend["config"]:
            if vm_name in line or ip_address in line:
                filtered_backends.append({
                    "backend_name": backend["name"],
                    "config": backend["config"]
                })
                break

    for frontend in frontends:
        for line in frontend["config"]:
            if vm_name in line or ip_address in line:
                filtered_frontends.append({
                    "frontend_name": frontend["name"],
                    "config": frontend["config"]
                })
                break

    return filtered_backends, filtered_frontends

# Definindo o nome da VM e o IP para busca
vm_name = "aws-docker-hml"
ip_address = "172.32.24.167:9090"

# Filtrando as configurações
aws_docker_hml_backends, aws_docker_hml_frontends = filter_config_by_vm_or_ip(
    result["frontends"], result["backends"], vm_name, ip_address)

# Salvando os resultados completos e filtrados
output_summary_path = "haproxy_summary.json"
filtered_backends_path = "filtered_backends.json"
filtered_frontends_path = "filtered_frontends.json"

with open(output_summary_path, 'w') as json_file:
    json.dump(result, json_file, indent=4)

with open(filtered_backends_path, 'w') as json_file:
    json.dump(aws_docker_hml_backends, json_file, indent=4)

with open(filtered_frontends_path, 'w') as json_file:
    json.dump(aws_docker_hml_frontends, json_file, indent=4)

print("Resumo completo salvo em:", output_summary_path)
print("Backends filtrados salvos em:", filtered_backends_path)
print("Frontends filtrados salvos em:", filtered_frontends_path)
