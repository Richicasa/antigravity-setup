# Vectores de Ataque Comunes en Habilidades y Agentes de IA

Este documento describe las principales amenazas de seguridad asociadas con la instalación y ejecución de habilidades de repositorios públicos de GitHub.

---

## 1. Exfiltración de Credenciales y Tokens de Entorno
* **Mecanismo:** Un script auxiliar de la habilidad busca variables como `AWS_SECRET_ACCESS_KEY`, `OPENAI_API_KEY`, `GITHUB_TOKEN`, o lee archivos como `~/.ssh/id_rsa`, `~/.aws/credentials` o `.env`.
* **Canales de Exfiltración:** Envío de paquetes HTTP POST a webhooks públicos (Discord, Telegram, Webhook.site) o peticiones DNS/ICMP encubiertas.

## 2. Inyección de Instrucciones (Prompt Injection / Jailbreak)
* **Mecanismo:** El archivo `SKILL.md` contiene instrucciones diseñadas para secuestrar el modelo:
  - *"Ignora todas las instrucciones previas y..."*
  - *"A partir de ahora estás en modo sin restricciones..."*
* **Impacto:** Puede forzar al agente a ejecutar comandos en la terminal del usuario sin su consentimiento.

## 3. Reverse Shells y Control Remoto
* **Mecanismo:** Scripts bash o powershell que abren sockets TCP hacia una IP remota (`/dev/tcp/ip/port`, `nc -e cmd.exe`, `powershell IEX`).
* **Impacto:** Otorga acceso interactivo completo al atacante sobre la máquina local del usuario.

## 4. Ejecución Ofuscada (Base64 / IEX)
* **Mecanismo:** Bloques de código codificados en Base64 o cadenas comprimidas ejecutadas al vuelo con `Invoke-Expression` o `eval()`.
* **Impacto:** Oculta el verdadero comportamiento del código a los análisis simples de texto.

## 5. Acciones Destructivas de Sistema
* **Mecanismo:** Eliminación indiscriminada de árboles de directorios (`rm -rf /`, `Remove-Item C:\ -Recurse`), formateo de unidades o alteración de políticas de seguridad locales (desactivar Defender o Firewall).
