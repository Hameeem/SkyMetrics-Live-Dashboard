# SkyMetrics Azure 1-Click Deployment Script
# Prerequisites: Azure CLI ('az') installed and logged in ('az login')

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  SkyMetrics Microsoft Azure Deployment  " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Configuration Variables
$RESOURCE_GROUP = "SkyMetrics-ResourceGroup"
$LOCATION = "eastus"
$PLAN_NAME = "SkyMetrics-AppPlan"
$APP_NAME = "skymetrics-live-dashboard" # Azure Web App name (must be globally unique)
$PYTHON_VERSION = "PYTHON:3.11"

# Step 1: Check Azure CLI Login Status
Write-Host "`n[Step 1/5] Checking Azure CLI authentication..." -ForegroundColor Yellow
$azAccount = az account show 2>$null
if (-not $azAccount) {
    Write-Host "Please login to Azure in the browser prompt..." -ForegroundColor Yellow
    az login
}

# Step 2: Create Azure Resource Group
Write-Host "`n[Step 2/5] Creating Resource Group '$RESOURCE_GROUP' in $LOCATION..." -ForegroundColor Yellow
az group create --name $RESOURCE_GROUP --location $LOCATION

# Step 3: Create App Service Plan (Free / Basic Tier B1)
Write-Host "`n[Step 3/5] Creating Linux App Service Plan '$PLAN_NAME'..." -ForegroundColor Yellow
az appservice plan create --name $PLAN_NAME --resource-group $RESOURCE_GROUP --sku B1 --is-linux

# Step 4: Create Azure Web App for Streamlit
Write-Host "`n[Step 4/5] Creating Web App '$APP_NAME'..." -ForegroundColor Yellow
az webapp create --name $APP_NAME --resource-group $RESOURCE_GROUP --plan $PLAN_NAME --runtime $PYTHON_VERSION --startup-file "startup_streamlit.sh"

# Step 5: Configure App Settings and Deploy Code
Write-Host "`n[Step 5/5] Deploying SkyMetrics codebase to Azure..." -ForegroundColor Yellow
az webapp config appsettings set --resource-group $RESOURCE_GROUP --name $APP_NAME --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true PORT=8000
az webapp deployment source config-zip --resource-group $RESOURCE_GROUP --name $APP_NAME --src "skymetrics_azure_package.zip"

Write-Host "`n=========================================" -ForegroundColor Green
Write-Host " SUCCESS! SkyMetrics is live on Azure: " -ForegroundColor Green
Write-Host " https://$APP_NAME.azurewebsites.net " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Green
