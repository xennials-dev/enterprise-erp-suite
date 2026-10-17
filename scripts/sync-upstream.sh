#!/usr/bin/env bash
# ==============================================================================
# Script: sync-upstream.sh
# Purpose: Failsafe synchronization of local git repository with upstream source
# Constraints: Zero data loss, no force flags, robust conflict handling
# ==============================================================================

set -euo pipefail

# ------------------------------------------------------------------------------
# Configuration & Arguments
# ------------------------------------------------------------------------------
UPSTREAM_URL="${1:-}"
TARGET_BRANCH="${2:-main}"
STASH_LABEL="pre-sync-backup-$(date +%Y%m%d-%H%M%S)"
STASH_CREATED=false

# ANSI Colors for Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1" >&2; }

# ------------------------------------------------------------------------------
# Preflight Validations
# ------------------------------------------------------------------------------
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    log_error "Current directory is not a Git repository."
    exit 1
fi

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
log_info "Active branch: ${CURRENT_BRANCH}"

# ------------------------------------------------------------------------------
# Step 1: Preservation (Safe Stash of Tracked + Untracked Changes)
# ------------------------------------------------------------------------------
log_info "Step 1: Inspecting working tree for uncommitted changes..."
DIRTY=false
if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git status --porcelain -u)" ]; then
    DIRTY=true
fi

if [ "$DIRTY" = true ]; then
    log_info "Preserving uncommitted and untracked changes with stash..."
    git stash push -u -m "${STASH_LABEL}"
    STASH_CREATED=true
    log_success "Working tree preserved as stash '${STASH_LABEL}'."
else
    log_info "Working tree clean. No stash creation required."
fi

# Trap to restore stash if early script failure occurs before merge
cleanup_on_error() {
    EXIT_CODE=$?
    if [ "$STASH_CREATED" = true ] && [ "$EXIT_CODE" -ne 0 ]; then
        log_warn "Interrupted or failed before completion. Attempting to restore your uncommitted work..."
        git stash pop || log_error "Failed to pop stash automatically. Your stash '${STASH_LABEL}' remains safely preserved in git stash list."
    fi
    exit "$EXIT_CODE"
}
trap cleanup_on_error EXIT

# ------------------------------------------------------------------------------
# Step 2: Configuration (Configure & Verify Upstream Remote)
# ------------------------------------------------------------------------------
log_info "Step 2: Configuring upstream remote..."
if git remote | grep -q "^upstream$"; then
    EXISTING_URL=$(git remote get-url upstream)
    if [ -n "${UPSTREAM_URL}" ] && [ "${EXISTING_URL}" != "${UPSTREAM_URL}" ]; then
        log_info "Updating upstream remote URL to: ${UPSTREAM_URL}"
        git remote set-url upstream "${UPSTREAM_URL}"
    else
        log_info "Upstream remote already configured: ${EXISTING_URL}"
    fi
else
    if [ -z "${UPSTREAM_URL}" ]; then
        log_error "No upstream remote configured and no URL provided. Usage: $0 <upstream-git-url> [branch]"
        exit 1
    fi
    log_info "Adding upstream remote: ${UPSTREAM_URL}"
    git remote add upstream "${UPSTREAM_URL}"
fi

# Ensure origin remote exists
if ! git remote | grep -q "^origin$"; then
    log_error "Remote 'origin' does not exist. Cannot sync fork without origin."
    exit 1
fi

# Ensure user is on the intended branch
if [ "${CURRENT_BRANCH}" != "${TARGET_BRANCH}" ]; then
    log_info "Switching to ${TARGET_BRANCH} branch..."
    git checkout "${TARGET_BRANCH}"
fi

# ------------------------------------------------------------------------------
# Step 3: Synchronization (Fetch & Merge without Force)
# ------------------------------------------------------------------------------
log_info "Step 3: Fetching upstream updates..."
git fetch upstream "${TARGET_BRANCH}"

log_info "Merging updates from upstream/${TARGET_BRANCH} into ${TARGET_BRANCH}..."
if ! git merge "upstream/${TARGET_BRANCH}" -m "chore: merge upstream/${TARGET_BRANCH} into ${TARGET_BRANCH}"; then
    log_error "Merge conflict encountered during synchronization!"
    log_error "Resolve merge conflicts manually, commit, and then execute: git stash pop"
    trap - EXIT # Disable error trap so stash is preserved untouched
    exit 1
fi
log_success "Merge completed successfully."

# ------------------------------------------------------------------------------
# Step 4: Push to Fork (Origin)
# ------------------------------------------------------------------------------
log_info "Step 4: Pushing synchronized ${TARGET_BRANCH} to origin (no force)..."
git push origin "${TARGET_BRANCH}"
log_success "Origin/${TARGET_BRANCH} updated."

# ------------------------------------------------------------------------------
# Step 5: Restoration (Pop Stashed Work)
# ------------------------------------------------------------------------------
# Disarm trap since the main workflow succeeded
trap - EXIT

if [ "$STASH_CREATED" = true ]; then
    log_info "Step 5: Restoring stashed uncommitted work..."
    if git stash pop; then
        log_success "Stash popped and uncommitted changes restored cleanly."
    else
        log_warn "Conflicts occurred while reapplying stashed changes!"
        log_warn "Your work is still preserved. Conflict markers have been placed in your working files."
        log_warn "Resolve conflicts and drop the stash manually once resolved: git stash drop"
        exit 1
    fi
else
    log_info "Step 5: No stash was needed. Working directory is up to date."
fi

# Return to original branch if user was on a feature branch
if [ "${CURRENT_BRANCH}" != "${TARGET_BRANCH}" ]; then
    log_info "Returning to original branch: ${CURRENT_BRANCH}"
    git checkout "${CURRENT_BRANCH}"
fi

log_success "Synchronization completed successfully with zero data loss!"
