#!/bin/bash

# Android Resource Validation Script
# This script checks for required Android resources before building

set -e

COLOR_RED='\033[0;31m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RES_DIR="${SCRIPT_DIR}/app/src/main/res"

errors=0
warnings=0

echo "=========================================="
echo "Android Resource Validation"
echo "=========================================="
echo ""

# Check if res directory exists
if [ ! -d "$RES_DIR" ]; then
    echo -e "${COLOR_RED}ERROR: res directory not found at ${RES_DIR}${COLOR_NC}"
    exit 1
fi

echo "Checking required launcher icons..."

# Required mipmap densities
DENSITIES=("mdpi" "hdpi" "xhdpi" "xxhdpi" "xxxhdpi")

# Required launcher icon files
REQUIRED_ICONS=("ic_launcher.png" "ic_launcher_round.png")

for density in "${DENSITIES[@]}"; do
    mipmap_dir="${RES_DIR}/mipmap-${density}"

    if [ ! -d "$mipmap_dir" ]; then
        echo -e "${COLOR_RED}✗ Missing directory: mipmap-${density}${COLOR_NC}"
        errors=$((errors + 1))
        continue
    fi

    for icon in "${REQUIRED_ICONS[@]}"; do
        icon_path="${mipmap_dir}/${icon}"
        if [ ! -f "$icon_path" ]; then
            echo -e "${COLOR_RED}✗ Missing icon: mipmap-${density}/${icon}${COLOR_NC}"
            errors=$((errors + 1))
        else
            # Check if file is not empty
            if [ ! -s "$icon_path" ]; then
                echo -e "${COLOR_RED}✗ Empty icon file: mipmap-${density}/${icon}${COLOR_NC}"
                errors=$((errors + 1))
            else
                echo -e "${COLOR_GREEN}✓ Found: mipmap-${density}/${icon}${COLOR_NC}"
            fi
        fi
    done
done

echo ""
echo "Checking AndroidManifest.xml..."

MANIFEST_PATH="${SCRIPT_DIR}/app/src/main/AndroidManifest.xml"
if [ ! -f "$MANIFEST_PATH" ]; then
    echo -e "${COLOR_RED}✗ AndroidManifest.xml not found${COLOR_NC}"
    errors=$((errors + 1))
else
    echo -e "${COLOR_GREEN}✓ AndroidManifest.xml exists${COLOR_NC}"

    # Check for icon references
    if grep -q "@mipmap/ic_launcher" "$MANIFEST_PATH"; then
        echo -e "${COLOR_GREEN}✓ Icon reference found in manifest${COLOR_NC}"
    else
        echo -e "${COLOR_YELLOW}⚠ No icon reference in manifest${COLOR_NC}"
        warnings=$((warnings + 1))
    fi
fi

echo ""
echo "Checking values resources..."

VALUES_DIR="${RES_DIR}/values"
if [ ! -d "$VALUES_DIR" ]; then
    echo -e "${COLOR_RED}✗ values directory not found${COLOR_NC}"
    errors=$((errors + 1))
else
    # Check for required resource files
    if [ ! -f "${VALUES_DIR}/strings.xml" ]; then
        echo -e "${COLOR_RED}✗ strings.xml not found${COLOR_NC}"
        errors=$((errors + 1))
    else
        echo -e "${COLOR_GREEN}✓ strings.xml exists${COLOR_NC}"
    fi

    if [ ! -f "${VALUES_DIR}/styles.xml" ]; then
        echo -e "${COLOR_YELLOW}⚠ styles.xml not found${COLOR_NC}"
        warnings=$((warnings + 1))
    else
        echo -e "${COLOR_GREEN}✓ styles.xml exists${COLOR_NC}"

        # Check for missing drawable references in styles.xml
        if grep -q "drawable/" "${VALUES_DIR}/styles.xml"; then
            echo -e "${COLOR_YELLOW}⚠ Checking drawable references in styles.xml...${COLOR_NC}"
            while IFS= read -r line; do
                drawable=$(echo "$line" | grep -oP '@drawable/\K[^"]+' || true)
                if [ -n "$drawable" ]; then
                    found=false
                    for drawable_dir in "${RES_DIR}"/drawable*; do
                        if [ -f "${drawable_dir}/${drawable}.xml" ] || [ -f "${drawable_dir}/${drawable}.png" ]; then
                            found=true
                            break
                        fi
                    done
                    if [ "$found" = false ]; then
                        echo -e "${COLOR_YELLOW}  ⚠ Drawable resource not found: ${drawable}${COLOR_NC}"
                        warnings=$((warnings + 1))
                    fi
                fi
            done < <(grep "drawable/" "${VALUES_DIR}/styles.xml")
        fi
    fi
fi

echo ""
echo "=========================================="
echo "Validation Summary"
echo "=========================================="

if [ $errors -eq 0 ] && [ $warnings -eq 0 ]; then
    echo -e "${COLOR_GREEN}✓ All checks passed!${COLOR_NC}"
    exit 0
elif [ $errors -eq 0 ]; then
    echo -e "${COLOR_YELLOW}⚠ Validation passed with ${warnings} warning(s)${COLOR_NC}"
    exit 0
else
    echo -e "${COLOR_RED}✗ Validation failed with ${errors} error(s) and ${warnings} warning(s)${COLOR_NC}"
    echo ""
    echo "Please fix the errors before building the Android app."
    exit 1
fi
