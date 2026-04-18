# Git Workflow

## Convencao de commits por prompt

A partir do `audit-cleanup`, cada prompt do playbook gera 1 commit com mensagem:

```text
fase{X}/{Y.Z} {titulo-curto}
```

Exemplo:

```text
fase1/1.3 validar offsite restore
```

Historico anterior nao e reescrito. Nao usar `rebase -i`, `filter-branch` ou `push --force` para tentar reorganizar commits ja publicados.
