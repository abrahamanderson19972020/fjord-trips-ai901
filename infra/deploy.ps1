# Module 17 · Deploy Fjord Trips to Azure Container Apps.
# Run the steps one by one in PowerShell from the project folder, after `az login`.
# Replace every <...> with your own values. Never paste keys into this file.

$RG = "rg-fjordtrips"
$APP = "fjordtrips-app"
$LOCATION = "swedencentral"
$VAULT = "kv-fjordtrips-<initials>"

# 1. Build the container in Azure and run it with a public URL
az containerapp up --name $APP --resource-group $RG --location $LOCATION --source . --ingress external --target-port 8501

# 2. Give the app its own identity (a system-assigned managed identity)
az containerapp identity assign --name $APP --resource-group $RG --system-assigned

# 3. In the Azure portal: on the Foundry resource `fjordtrips-ai`, give the app's identity the role "Azure AI User".
#    On the Key Vault, give it the role "Key Vault Secrets User". (Access control (IAM) > Add role assignment.)

# 4. Create the Key Vault and add the two keys in the portal (paste them off screen): language-key, speech-key
# az keyvault create --name $VAULT --resource-group $RG --location $LOCATION

# 5. Reference the Key Vault secrets from the container app
az containerapp secret set --name $APP --resource-group $RG --secrets `
  "language-key=keyvaultref:https://$VAULT.vault.azure.net/secrets/language-key,identityref:system" `
  "speech-key=keyvaultref:https://$VAULT.vault.azure.net/secrets/speech-key,identityref:system"

# 6. Set the settings (plain values) and the secret references
az containerapp update --name $APP --resource-group $RG --set-env-vars `
  FOUNDRY_PROJECT_ENDPOINT=<endpoint> CHAT_DEPLOYMENT=gpt-5-mini AGENT_NAME=trip-agent `
  IMAGE_DEPLOYMENT=gpt-image-1-mini AUDIO_DEPLOYMENT=<audio-deployment> `
  LANGUAGE_ENDPOINT=<language-endpoint> CU_ENDPOINT=<cu-endpoint> SPEECH_REGION=swedencentral `
  DATA_BASE_URL=https://raw.githubusercontent.com/abrahamanderson19972020/fjord-trips-ai901/main/data `
  LANGUAGE_KEY=secretref:language-key SPEECH_KEY=secretref:speech-key

# 7. Show the public URL
az containerapp show --name $APP --resource-group $RG --query properties.configuration.ingress.fqdn -o tsv
