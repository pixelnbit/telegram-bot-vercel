# Deploy to GitHub and Vercel
# Run this script from PowerShell

Write-Host "🚀 Deploying Telegram Bot to GitHub and Vercel" -ForegroundColor Cyan
Write-Host ""

# Configuration
$GITHUB_TOKEN = Read-Host "Enter your GitHub Personal Access Token"
$REPO_NAME = "telegram-bot-vercel"
$GITHUB_USERNAME = Read-Host "Enter your GitHub username"

Write-Host ""
Write-Host "📝 Step 1: Initialize Git repository" -ForegroundColor Yellow

# Initialize git if not already done
if (-not (Test-Path ".git")) {
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Git repository already exists" -ForegroundColor Green
}

# Configure git
git config user.name "$GITHUB_USERNAME"
git config user.email "$GITHUB_USERNAME@users.noreply.github.com"

Write-Host ""
Write-Host "📝 Step 2: Create .env.example file" -ForegroundColor Yellow

# Create .env.example
@"
BOT_TOKEN=your_bot_token_here
CHANNEL_USERNAME=your_channel
OWNER_URL=https://t.me/your_username
OWNER_ID_1=123456789
OWNER_ID_2=987654321
WEBHOOK_URL=https://your-app.vercel.app
"@ | Out-File -FilePath ".env.example" -Encoding UTF8

Write-Host "✅ .env.example created" -ForegroundColor Green

Write-Host ""
Write-Host "📝 Step 3: Add files to git" -ForegroundColor Yellow

git add .
git commit -m "Initial commit: Telegram bot with Vercel deployment"

Write-Host "✅ Files committed" -ForegroundColor Green

Write-Host ""
Write-Host "📝 Step 4: Create GitHub repository" -ForegroundColor Yellow

# Create repository on GitHub
$headers = @{
    "Authorization" = "token $GITHUB_TOKEN"
    "Accept" = "application/vnd.github.v3+json"
}

$body = @{
    "name" = $REPO_NAME
    "description" = "Telegram Bot with Card Checking - Deployed on Vercel"
    "private" = $true
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $body -ContentType "application/json"
    Write-Host "✅ Repository created: $($response.html_url)" -ForegroundColor Green
    $repoUrl = $response.clone_url
} catch {
    Write-Host "⚠️  Repository might already exist or token is invalid" -ForegroundColor Yellow
    $repoUrl = "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
}

Write-Host ""
Write-Host "📝 Step 5: Push to GitHub" -ForegroundColor Yellow

# Set remote URL with token
$remoteUrl = "https://$GITHUB_TOKEN@github.com/$GITHUB_USERNAME/$REPO_NAME.git"
git remote remove origin 2>$null
git remote add origin $remoteUrl

# Push to GitHub
git branch -M main
git push -u origin main --force

Write-Host "✅ Code pushed to GitHub" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Deployment Preparation Complete!" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Go to https://vercel.com" -ForegroundColor White
Write-Host "2. Import your GitHub repository: $GITHUB_USERNAME/$REPO_NAME" -ForegroundColor White
Write-Host "3. Add environment variables in Vercel dashboard:" -ForegroundColor White
Write-Host "   - BOT_TOKEN" -ForegroundColor Gray
Write-Host "   - CHANNEL_USERNAME" -ForegroundColor Gray
Write-Host "   - OWNER_URL" -ForegroundColor Gray
Write-Host "   - OWNER_ID_1" -ForegroundColor Gray
Write-Host "   - OWNER_ID_2" -ForegroundColor Gray
Write-Host "   - WEBHOOK_URL (your-app.vercel.app)" -ForegroundColor Gray
Write-Host "4. Deploy!" -ForegroundColor White
Write-Host "5. After deployment, visit: https://your-app.vercel.app/api/setWebhook" -ForegroundColor White
Write-Host ""
Write-Host "📚 Repository: https://github.com/$GITHUB_USERNAME/$REPO_NAME" -ForegroundColor Cyan
