# Vault local de segredos

Este diretorio guarda somente artefatos cifrados com `sops` + `age` e a chave privada local usada para emergencia operacional.

## Regra

- nunca commitar a chave privada `*.key`
- nunca gravar segredo em claro aqui
- manter os arquivos cifrados como `*.enc`

## Inicializacao

```bash
mkdir -p tenants/secrets/.vault
age-keygen -o tenants/secrets/.vault/age.key
chmod 600 tenants/secrets/.vault/age.key
age-keygen -y tenants/secrets/.vault/age.key
```

## Cifrando um inventario

```bash
recipient="$(age-keygen -y tenants/secrets/.vault/age.key)"
sops --encrypt --age "${recipient}" inventory.yaml > tenants/secrets/.vault/inventory.yaml.enc
```

## Emergencia

Para abrir um arquivo cifrado em uma intervencao controlada:

```bash
SOPS_AGE_KEY_FILE=tenants/secrets/.vault/age.key sops --decrypt tenants/secrets/.vault/inventory.yaml.enc
```

Se a chave privada local for perdida, a recuperacao depende da politica externa de backup da chave. Sem a chave, o arquivo cifrado nao e recuperavel daqui.
