# Git Pre-commit Hook for Android Resource Validation

This directory can contain a pre-commit hook to validate Android resources before committing.

## Setup Instructions

To enable automatic resource validation before commits, run:

```bash
cd /path/to/mathlens-ai
cp docs/git-hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## Pre-commit Hook Content

Create `.git/hooks/pre-commit` with the following content:

```bash
#!/bin/bash

# Pre-commit hook to validate Android resources

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Android files are being committed
if git diff --cached --name-only | grep -q "mobile/android"; then
    echo -e "${YELLOW}Android files detected, validating resources...${NC}"

    # Run the validation script
    if [ -f "mobile/android/validate-resources.sh" ]; then
        cd mobile/android
        if ./validate-resources.sh; then
            echo -e "${GREEN}✓ Android resource validation passed${NC}"
            cd - > /dev/null
        else
            echo -e "${RED}✗ Android resource validation failed${NC}"
            echo -e "${RED}Please fix the errors before committing${NC}"
            cd - > /dev/null
            exit 1
        fi
    else
        echo -e "${YELLOW}⚠ Validation script not found, skipping validation${NC}"
    fi
fi

exit 0
```

## What the Hook Does

The pre-commit hook:
1. Detects if any Android files are being committed
2. Runs the `validate-resources.sh` script
3. Blocks the commit if validation fails
4. Shows clear error messages about what needs to be fixed

## Disabling the Hook Temporarily

If you need to commit without validation (not recommended), use:

```bash
git commit --no-verify -m "your message"
```

## Alternative: Git Hooks via Husky

For team-wide enforcement, consider using Husky:

```bash
npm install --save-dev husky
npx husky init
echo "cd mobile/android && ./validate-resources.sh" > .husky/pre-commit
```

This ensures all developers use the same hooks automatically.
