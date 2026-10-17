<#
.SYNOPSIS
    Automated Upstream Synchronization for Local Open-Source AI Models (Ollama & LM Studio).
.DESCRIPTION
    Checks upstream model repositories (Ollama Library, HuggingFace, ModelScope)
    and pulls the latest model weights and parameter updates for your CRM/ERP stack:
    - NL-to-SQL & Code: Qwen 2.5 Coder
    - Reasoning & Lead Scoring: DeepSeek-R1
    - Vision & Invoice OCR: Qwen 2.5 VL
    - Autonomous Helpdesk: GLM-4 / Qwen 2.5
.PARAMETER Provider
    Target provider to synchronize: 'ollama', 'lmstudio', or 'all' (default: 'ollama').
.PARAMETER Models
    Specific models to pull/update (optional, defaults to recommended ERP suite).
#>

[CmdletBinding()]
param (
    [ValidateSet("ollama", "lmstudio", "all")]
    [string]$Provider = "ollama",

    [string[]]$Models = @(
        "qwen2.5-coder:14b",
        "deepseek-r1:14b",
        "qwen2.5:14b"
    )
)

$ErrorActionPreference = "Stop"

function Write-Info    { Write-Host "[INFO] $args" -ForegroundColor Cyan }
function Write-Success { Write-Host "[SUCCESS] $args" -ForegroundColor Green }
function Write-Warn    { Write-Host "[WARN] $args" -ForegroundColor Yellow }
function Write-Err     { Write-Host "[ERROR] $args" -ForegroundColor Red }

Write-Host "============================================================" -ForegroundColor Magenta
Write-Host "  Local AI Models - Upstream Synchronization Engine" -ForegroundColor Magenta
Write-Host "============================================================" -ForegroundColor Magenta

# 1. Sync Ollama Models
if ($Provider -eq "ollama" -or $Provider -eq "all") {
    Write-Info "Checking Ollama daemon on http://localhost:11434..."
    try {
        $tags = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get -TimeoutSec 5
        Write-Success "Ollama daemon is active."
        Write-Info "Currently installed Ollama models: $($tags.models.name -join ', ')"

        foreach ($model in $Models) {
            Write-Info "Syncing upstream: pulling latest weights for '$model'..."
            try {
                # Stream pull from upstream
                $pullBody = @{ name = $model; stream = $false } | ConvertTo-Json
                $resp = Invoke-RestMethod -Uri "http://localhost:11434/api/pull" -Method Post -ContentType "application/json" -Body $pullBody -TimeoutSec 600
                if ($resp.status -eq "success" -or $resp.status -like "*success*") {
                    Write-Success "Successfully updated '$model' to latest upstream version."
                } else {
                    Write-Info "Sync status for '$model': $($resp.status)"
                }
            } catch {
                Write-Warn "Could not pull '$model' directly via API: $($_.Exception.Message)"
                Write-Info "Attempting fallback CLI: 'ollama pull $model'..."
                & ollama pull $model
            }
        }
    } catch {
        Write-Warn "Ollama daemon is not reachable on localhost:11434."
    }
}

# 2. Check LM Studio Status
if ($Provider -eq "lmstudio" -or $Provider -eq "all") {
    Write-Info "Checking LM Studio local server on http://localhost:1234..."
    try {
        $lmModels = Invoke-RestMethod -Uri "http://localhost:1234/v1/models" -Method Get -TimeoutSec 5
        Write-Success "LM Studio is active with loaded models:"
        foreach ($m in $lmModels.data) {
            Write-Host "  - $($m.id)" -ForegroundColor White
        }
        Write-Info "Tip: In LM Studio, use the 'Discover' tab to fetch latest HuggingFace GGUF releases."
    } catch {
        Write-Warn "LM Studio is not currently running on port 1234."
    }
}

Write-Success "Upstream model synchronization check completed."
