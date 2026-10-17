<#
.SYNOPSIS
    Failsafe synchronization of local git repository with upstream source.
.DESCRIPTION
    Safely stashes tracked & untracked work, configures upstream remote, fetches,
    merges cleanly without force flags, pushes to origin, and restores stashed work.
.PARAMETER UpstreamUrl
    The Git clone URL for the upstream repository.
.PARAMETER TargetBranch
    The branch to synchronize (defaults to 'main').
.EXAMPLE
    .\sync-upstream.ps1 -UpstreamUrl "https://github.com/upstream-owner/repo.git"
#>

[CmdletBinding()]
param (
    [Parameter(Position = 0, Mandatory = $false)]
    [string]$UpstreamUrl,

    [Parameter(Position = 1, Mandatory = $false)]
    [string]$TargetBranch = "main"
)

$ErrorActionPreference = "Stop"

function Write-Info    { Write-Host "[INFO] $args" -ForegroundColor Cyan }
function Write-Success { Write-Host "[SUCCESS] $args" -ForegroundColor Green }
function Write-Warn    { Write-Host "[WARN] $args" -ForegroundColor Yellow }
function Write-Err     { Write-Host "[ERROR] $args" -ForegroundColor Red }

# Verify git repository
$isRepo = git rev-parse --is-inside-work-tree 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Err "Current directory is not a Git repository."
    exit 1
}

$currentBranch = (git rev-parse --abbrev-ref HEAD).Trim()
Write-Info "Active branch: $currentBranch"

$stashCreated = $false
$stashLabel = "pre-sync-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

try {
    # --------------------------------------------------------------------------
    # Step 1: Preservation (Safe Stash of Tracked + Untracked Changes)
    # --------------------------------------------------------------------------
    Write-Info "Step 1: Checking for uncommitted or untracked changes..."
    $status = git status --porcelain -u
    if (-not [string]::IsNullOrWhiteSpace($status)) {
        Write-Info "Preserving uncommitted changes to stash '$stashLabel'..."
        git stash push -u -m $stashLabel
        if ($LASTEXITCODE -ne 0) { throw "Failed to stash changes." }
        $stashCreated = $true
        Write-Success "Changes safely stashed."
    } else {
        Write-Info "Working tree is clean. No stashing needed."
    }

    # --------------------------------------------------------------------------
    # Step 2: Configuration (Configure & Verify Upstream Remote)
    # --------------------------------------------------------------------------
    Write-Info "Step 2: Checking upstream remote configuration..."
    $remotes = git remote
    if ($remotes -contains "upstream") {
        $existingUrl = (git remote get-url upstream).Trim()
        if (-not [string]::IsNullOrWhiteSpace($UpstreamUrl) -and $existingUrl -ne $UpstreamUrl) {
            Write-Info "Updating upstream remote URL to: $UpstreamUrl"
            git remote set-url upstream $UpstreamUrl
        } else {
            Write-Info "Upstream remote configured: $existingUrl"
        }
    } else {
        if ([string]::IsNullOrWhiteSpace($UpstreamUrl)) {
            throw "Upstream remote is not configured. Please supply -UpstreamUrl <url>"
        }
        Write-Info "Adding upstream remote: $UpstreamUrl"
        git remote add upstream $UpstreamUrl
    }

    if ($remotes -notcontains "origin") {
        throw "Remote 'origin' not found. Cannot push to fork without origin remote."
    }

    # Switch to target branch if necessary
    if ($currentBranch -ne $TargetBranch) {
        Write-Info "Switching to $TargetBranch..."
        git checkout $TargetBranch
    }

    # --------------------------------------------------------------------------
    # Step 3: Synchronization (Fetch & Merge without Force)
    # --------------------------------------------------------------------------
    Write-Info "Step 3: Fetching upstream updates..."
    git fetch upstream $TargetBranch
    if ($LASTEXITCODE -ne 0) { throw "Failed to fetch from upstream." }

    Write-Info "Merging upstream/$TargetBranch into $TargetBranch..."
    git merge "upstream/$TargetBranch" -m "chore: merge upstream/$TargetBranch into $TargetBranch"
    if ($LASTEXITCODE -ne 0) {
        Write-Err "Merge conflict detected!"
        Write-Err "Please resolve merge conflicts, commit, and then run 'git stash pop' manually."
        # Keep stash preserved; do not attempt automatic pop over conflict state
        exit 1
    }
    Write-Success "Merge completed without conflicts."

    # --------------------------------------------------------------------------
    # Step 4: Push to Fork (Origin)
    # --------------------------------------------------------------------------
    Write-Info "Step 4: Pushing to origin/$TargetBranch (no force)..."
    git push origin $TargetBranch
    if ($LASTEXITCODE -ne 0) { throw "Push to origin/$TargetBranch failed." }
    Write-Success "Origin updated successfully."

    # --------------------------------------------------------------------------
    # Step 5: Restoration (Pop Stashed Work)
    # --------------------------------------------------------------------------
    if ($stashCreated) {
        Write-Info "Step 5: Restoring stashed uncommitted work..."
        git stash pop
        if ($LASTEXITCODE -ne 0) {
            Write-Warn "Conflicts occurred while reapplying your stashed work."
            Write-Warn "Your stash remains saved. Resolve conflicts in your working tree, then run 'git stash drop'."
            exit 1
        }
        Write-Success "Stash restored cleanly."
    } else {
        Write-Info "Step 5: No stash restoration needed."
    }

    # Return to original branch if started on a feature branch
    if ($currentBranch -ne $TargetBranch) {
        Write-Info "Returning to original branch: $currentBranch"
        git checkout $currentBranch
    }

    Write-Success "Repository synchronized cleanly with zero data loss!"
}
catch {
    Write-Err "Failsafe triggered: $($_.Exception.Message)"
    if ($stashCreated) {
        Write-Warn "Safety check: Your uncommitted changes are safely preserved in stash '$stashLabel'."
        Write-Warn "Run 'git stash list' and 'git stash pop' to inspect or restore."
    }
    exit 1
}
