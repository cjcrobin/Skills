#!/bin/bash

# Test script for html-to-markdown conversion
# This script tests the full Docker-based conversion workflow

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DATA_DIR="${SCRIPT_DIR}/data"
EXPECTED_DIR="${TEST_DATA_DIR}/expected"
GENERATED_DIR="${TEST_DATA_DIR}/generated"
HTML_TO_MD_DIR="${SCRIPT_DIR}/../html-to-markdown"
SCRIPTS_DIR="${HTML_TO_MD_DIR}/scripts"
TEMP_DATA_DIR="${SCRIPTS_DIR}/temp_data"

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}HTML to Markdown Conversion Test${NC}"
echo -e "${BLUE}======================================${NC}\n"

# Step 1: Start Docker container
echo -e "${YELLOW}[Step 1/5]${NC} Starting Docker container..."
cd "${SCRIPTS_DIR}"
bash start-docker-container.sh
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Docker container ready${NC}\n"
else
    echo -e "${RED}✗ Failed to start Docker container${NC}"
    exit 1
fi

# Step 2: Prepare test data
echo -e "${YELLOW}[Step 2/5]${NC} Preparing test data..."

# Clean and create temp_data structure
rm -rf "${TEMP_DATA_DIR}/test"
mkdir -p "${TEMP_DATA_DIR}/test"

# Copy test JSON file
cp "${TEST_DATA_DIR}/moltbook.json" "${TEMP_DATA_DIR}/test/"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Copied moltbook.json to temp_data/test/${NC}\n"
else
    echo -e "${RED}✗ Failed to copy test data${NC}"
    exit 1
fi

# Step 3: Execute conversion in Docker
echo -e "${YELLOW}[Step 3/5]${NC} Running conversion in Docker container..."
docker exec html-to-markdown-container \
    bun /app/convert.ts /app/temp_data/test

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Conversion completed${NC}\n"
else
    echo -e "${RED}✗ Conversion failed${NC}"
    exit 1
fi

# Step 4: Move results to generated directory
echo -e "${YELLOW}[Step 4/5]${NC} Moving results to generated directory..."

# Clean generated directory
rm -rf "${GENERATED_DIR}"
mkdir -p "${GENERATED_DIR}"

# Copy all generated markdown files
cp "${TEMP_DATA_DIR}/test/"*.md "${GENERATED_DIR}/" 2>/dev/null || {
    echo -e "${RED}✗ No markdown files generated${NC}"
    exit 1
}

echo -e "${GREEN}✓ Results moved to ${GENERATED_DIR}/${NC}"
echo -e "  Generated files:"
ls -1 "${GENERATED_DIR}/" | sed 's/^/    - /'
echo ""

# Step 5: Compare with expected results
echo -e "${YELLOW}[Step 5/5]${NC} Comparing results with expected output..."

# Check if expected directory exists
if [ ! -d "${EXPECTED_DIR}" ]; then
    echo -e "${YELLOW}⚠ Expected directory not found: ${EXPECTED_DIR}${NC}"
    echo -e "${YELLOW}⚠ Creating expected directory with current results${NC}"
    mkdir -p "${EXPECTED_DIR}"
    cp "${GENERATED_DIR}/"*.md "${EXPECTED_DIR}/"
    echo -e "${GREEN}✓ Expected files created for future comparisons${NC}\n"
    exit 0
fi

# Compare files
DIFF_FOUND=0
TOTAL_FILES=0
MATCHING_FILES=0

for generated_file in "${GENERATED_DIR}"/*.md; do
    filename=$(basename "${generated_file}")
    expected_file="${EXPECTED_DIR}/${filename}"
    TOTAL_FILES=$((TOTAL_FILES + 1))
    
    if [ ! -f "${expected_file}" ]; then
        echo -e "${YELLOW}⚠ Expected file not found: ${filename}${NC}"
        echo -e "  Creating it for future comparisons..."
        cp "${generated_file}" "${expected_file}"
        continue
    fi
    
    # Compare files
    if diff -q "${generated_file}" "${expected_file}" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ ${filename} matches expected output${NC}"
        MATCHING_FILES=$((MATCHING_FILES + 1))
    else
        echo -e "${RED}✗ ${filename} differs from expected output${NC}"
        DIFF_FOUND=1
        
        # Show diff summary
        echo -e "  ${BLUE}Differences:${NC}"
        diff -u "${expected_file}" "${generated_file}" | head -20 | sed 's/^/    /'
        echo -e "  ${YELLOW}(showing first 20 lines of diff)${NC}"
    fi
done

echo ""
echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}Test Summary${NC}"
echo -e "${BLUE}======================================${NC}"
echo -e "Total files:    ${TOTAL_FILES}"
echo -e "Matching:       ${GREEN}${MATCHING_FILES}${NC}"
echo -e "Different:      ${RED}$((TOTAL_FILES - MATCHING_FILES))${NC}"

if [ ${DIFF_FOUND} -eq 0 ] && [ ${TOTAL_FILES} -eq ${MATCHING_FILES} ]; then
    echo -e "\n${GREEN}✓✓✓ All tests passed! ✓✓✓${NC}\n"
    exit 0
else
    echo -e "\n${RED}✗✗✗ Some tests failed ✗✗✗${NC}\n"
    exit 1
fi
