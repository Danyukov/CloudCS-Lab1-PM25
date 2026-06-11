# Лабораторная работа № 3 — Kubernetes

Шаблон: [CloudCS-Lab3](https://github.com/smirnoff410/CloudCS-Lab3)

| Сервис | Host |
|--------|------|
| inference | `inference.local` |
| Keycloak | `keycloak.local` |

## Подготовка

1. Docker Desktop → **Settings → Kubernetes → Enable Kubernetes**
2. `kubectl get nodes`
3. Ingress NGINX:
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.7.0/deploy/static/provider/cloud/deploy.yaml
   ```
4. В `C:\Windows\System32\drivers\etc\hosts` (от администратора):
   ```
   127.0.0.1 inference.local
   127.0.0.1 keycloak.local
   ```
5. В `k8s/all-services.yaml` в Secret замени `REPLACE_WITH_INFERENCE_CLIENT_SECRET` на secret клиента `inference-client` из Keycloak.

## Развёртывание

```bash
kubectl apply -f k8s/all-services.yaml
kubectl get pods,svc,ingress,hpa
```

## Keycloak (вручную, как в лабе 2)

1. https://keycloak.local/admin — TLS на ingress (сертификат self-signed, один раз принять в браузере).
2. Логин: `admin` / `admin007`

Сертификат (если ещё не создан):
```powershell
openssl req -x509 -nodes -days 825 -newkey rsa:2048 `
  -keyout k8s/certs/tls.key -out k8s/certs/tls.crt `
  -subj "/CN=keycloak.local" `
  -addext "subjectAltName=DNS:keycloak.local,DNS:inference.local"
kubectl create secret tls keycloak-local-tls --cert=k8s/certs/tls.crt --key=k8s/certs/tls.key
```
3. Realm `inference` и клиенты — как в лабе 2

## Проверка

- https://inference.local/healthcheck (не http — порт 80 занят IIS на Windows)
- POST https://inference.local/predictions с токенами privileged / unprivileged

## Манифесты по шагам методички

| Файл | Назначение |
|------|------------|
| `pod-inference.yaml` | Pod |
| `deployment-inference.yaml` | Deployment |
| `service-inference.yaml` | Service |
| `ingress-pm25.yaml` | Ingress |

## Port-forward

```bash
kubectl port-forward svc/my-service-inference 8000:80
kubectl port-forward svc/my-service-keycloak 8443:8443
```

## Удаление

```bash
kubectl delete -f k8s/all-services.yaml
```
