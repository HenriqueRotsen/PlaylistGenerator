# Playlist Generator - Kubernetes Deployment

Este repositório contém o código e os arquivos necessários para implementar um sistema de geração de playlists utilizando Kubernetes e ArgoCD. O projeto foi desenvolvido para explorar funcionalidades de CI/CD, permitindo a atualização automática de código, datasets e configurações de deployment.

---

## 📋 Sumário

- [Visão Geral do Projeto](#visão-geral-do-projeto)
- [Arquitetura](#arquitetura)
- [Requisitos](#requisitos)
- [Configuração do Ambiente](#configuração-do-ambiente)
  - [Kubernetes](#kubernetes)
  - [ArgoCD](#argocd)
- [Decisões Tomadas](#decisões-tomadas)
- [Execução](#execução)
  - [Passos para Rodar o Projeto](#passos-para-rodar-o-projeto)
  - [Testes](#testes)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Autor](#autor)

---

## 🔍 Visão Geral do Projeto

O **Playlist Generator** é uma aplicação que combina machine learning e orquestração de contêineres para gerar recomendações de playlists. Ele utiliza o Kubernetes para gerenciar os recursos do sistema e o ArgoCD para garantir deploys automatizados e integração contínua.

---

## 🏗 Arquitetura

### Componentes Principais

1. **Back-end** (`server/`):
   - Implementa uma API REST para servir as playlists geradas.
   - Contém o código necessário para interagir com o modelo de machine learning.

2. **Gerador de Regras** (`program/`):
   - Responsável por gerar regras de recomendação com base em datasets fornecidos.
   - Salva as regras em um arquivo serializado (`rules.pkl`).

3. **Cliente** (`client/`):
   - Um script para consumir a API REST e validar as recomendações.

4. **Orquestração Kubernetes** (`kubernetes/`):
   - Arquivos YAML para configurar `Deployment`, `Service`, `PVC` e Jobs necessários.

---

## ✅ Requisitos

Certifique-se de ter os seguintes requisitos instalados:

- **Docker**: Para construir as imagens dos contêineres.
- **kubectl**: Para interagir com o cluster Kubernetes.
- **Kubernetes Cluster**: Para executar os deployments.
- **ArgoCD CLI**: Para configurar deploys automatizados.
- **Python 3.8+**: Para rodar os scripts localmente.
- **Git**: Para gerenciar o código.

---

## ⚙️ Configuração do Ambiente

### Kubernetes

1. Configure o cluster Kubernetes e aplique os manifestos do diretório `kubernetes/`:
   ```bash
   kubectl apply -f kubernetes/
   ```

2. Verifique se os Pods, Serviços e Jobs estão funcionando:
   ```bash
   kubectl get all -n <seu-namespace>
   ```

### ArgoCD

1. Configure o ArgoCD no cluster:
   ```bash
   kubectl create namespace argocd
   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   ```

2. Adicione sua aplicação no ArgoCD:
   ```bash
   argocd app create playlist-generator \
   --repo https://github.com/HenriqueRotsen/PlaylistGenerator.git \
   --path kubernetes \
   --dest-namespace henriqueferreira \
   --dest-server https://kubernetes.default.svc \
   --sync-policy auto
   ```

---

## 🧠 Decisões Tomadas

1. **Modularização**:
   - Separação dos componentes em diretórios específicos:
     - `server/` para o backend.
     - `program/` para o gerador de regras.
     - `client/` para scripts de validação.

2. **Gerenciamento de Dados**:
   - Utilizamos um `PersistentVolumeClaim` (PVC) para armazenar datasets que são reutilizados entre Pods.

3. **Deploy Automatizado**:
   - Configuração do ArgoCD para monitorar o repositório e aplicar mudanças automaticamente.

4. **Atualizações de Dataset**:
   - Sempre que o dataset é atualizado, o nome do Job é modificado para forçar a criação de novos Pods.

---

## 🚀 Execução

### Passos para Rodar o Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/HenriqueRotsen/PlaylistGenerator.git
   cd PlaylistGenerator
   ```

2. Construa as imagens Docker para os componentes:
   ```bash
   docker build -t henriquerotsen/program:0.x ./program
   docker build -t henriquerotsen/server:0.x ./server
   ```

3. Configure e aplique os manifestos Kubernetes:
   ```bash
   kubectl apply -f kubernetes/
   ```

4. Configure o ArgoCD conforme descrito na seção anterior.

---

### Testes

Os seguintes testes foram realizados:

1. **Atualização do Código do Modelo**:
   - Alteração do Dockerfile em `program/` e atualização da tag da imagem Docker no `program.yaml`.

2. **Alteração do Dataset**:
   - Atualização dos arquivos no PVC e reinício do Job para regenerar o modelo.

3. **Alteração de Réplicas**:
   - Alteração do número de réplicas no `deployment.yaml`.

---

## 📂 Estrutura do Repositório

```
.
├── client/                     # Código para consumir a API REST
│   └── client.py
├── kubernetes/                 # Manifestos Kubernetes
│   ├── deployment.yaml
│   ├── program.yaml
│   ├── pvc.yaml
│   └── service.yaml
├── program/                    # Código do gerador de regras
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── rules_generator.py
│   └── rules.pkl
├── server/                     # Backend API REST
│   ├── Dockerfile
│   ├── requirements.txt
│   └── server.py
└── .gitignore                  # Arquivo .gitignore
```

---

## ✍️ Autor

**Henrique Rotsen**  
Projeto desenvolvido como parte do Trabalho Prático 2 da disciplina **[Cloud Computing](https://homepages.dcc.ufmg.br/~cunha/teaching/20232/cloudcomp/)**.

---

## 🛡️ Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](./LICENSE) para detalhes.
