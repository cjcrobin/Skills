#!/bin/bash

# Test script for aggregate-news collection
# This script tests the news fetching and storage structure

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
AGGREGATE_NEWS_DIR="${SCRIPT_DIR}/../aggregate-news"
SCRIPTS_DIR="${AGGREGATE_NEWS_DIR}/scripts"
TEMP_OUTPUT_DIR="${SCRIPT_DIR}/data/test_output"

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}Aggregate News Collection Test${NC}"
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

# Step 2: Test news fetching with mock data
echo -e "${YELLOW}[Step 2/5]${NC} Testing news fetch (metadata only)..."

# Clean test output directory
rm -rf "${TEMP_OUTPUT_DIR}"
mkdir -p "${TEMP_OUTPUT_DIR}"

# Run news fetch with small limit for testing (without content)
echo -e "Fetching metadata from Hacker News (limit: 1)..."
docker exec aggregate-news-container \
    sh -c "uv run python news_fetch.py \
           --source all \
           --limit 1 \
           --output /app/temp_data \
           --content \
           --pretty"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Metadata fetch completed${NC}\n"
else
    echo -e "${RED}✗ Metadata fetch failed${NC}"
    exit 1
fi

# Step 3: Verify folder structure
echo -e "${YELLOW}[Step 3/5]${NC} Verifying folder structure..."

# Copy results from Docker temp_data
cp -r "${SCRIPTS_DIR}/temp_data/"* "${TEMP_OUTPUT_DIR}/" 2>/dev/null || {
    echo -e "${RED}✗ No data generated${NC}"
    exit 1
}

# Check if folder structure is correct: [date]/[source]/[slug]/origin.json
FOUND_CORRECT_STRUCTURE=0
FOUND_FILES=0

for json_file in $(find "${TEMP_OUTPUT_DIR}" -name "origin.json" 2>/dev/null); do
    FOUND_FILES=$((FOUND_FILES + 1))
    
    # Extract path components
    file_dir=$(dirname "${json_file}")
    slug_dir=$(basename "${file_dir}")
    source_dir=$(basename $(dirname "${file_dir}"))
    date_dir=$(basename $(dirname $(dirname "${file_dir}")))
    
    echo -e "  Found: ${date_dir}/${source_dir}/${slug_dir}/origin.json"
    
    # Verify structure
    if [[ "${date_dir}" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] && \
       [[ "${source_dir}" == "NewsSource."* ]] && \
       [[ ! -z "${slug_dir}" ]]; then
        FOUND_CORRECT_STRUCTURE=$((FOUND_CORRECT_STRUCTURE + 1))
        echo -e "    ${GREEN}✓ Correct structure${NC}"
    else
        echo -e "    ${RED}✗ Incorrect structure${NC}"
    fi
done

if [ ${FOUND_FILES} -eq 0 ]; then
    echo -e "${RED}✗ No origin.json files found${NC}"
    exit 1
fi

if [ ${FOUND_CORRECT_STRUCTURE} -eq ${FOUND_FILES} ]; then
    echo -e "${GREEN}✓ All files have correct folder structure${NC}\n"
else
    echo -e "${RED}✗ Some files have incorrect structure${NC}"
    echo -e "  Correct: ${FOUND_CORRECT_STRUCTURE}/${FOUND_FILES}"
    exit 1
fi

# Step 4: Verify JSON structure
echo -e "${YELLOW}[Step 4/5]${NC} Verifying JSON structure..."

VALID_JSON=0
TOTAL_JSON=0

for json_file in $(find "${TEMP_OUTPUT_DIR}" -name "origin.json"); do
    TOTAL_JSON=$((TOTAL_JSON + 1))
    
    # Check if valid JSON using Python and extract all needed info in one call
    validation_result=$(python3 -c "
import json
import sys
try:
    data = json.load(open('${json_file}'))
    title = data.get('title', '')
    source = data.get('source', '')
    post_url = data.get('post_url', '')
    hunt_url = data.get('hunt_url', '')
    
    # Print result in format: valid|title|source|post_url|hunt_url
    print(f'valid|{title}|{source}|{post_url}|{hunt_url}')
except:
    print('invalid')
" 2>/dev/null)
    
    if [[ "${validation_result}" == "invalid" ]]; then
        echo -e "  ${RED}✗${NC} Invalid JSON: ${json_file}"
        continue
    fi
    
    # Parse the result
    IFS='|' read -r status title source post_url hunt_url <<< "${validation_result}"
    
    if [ ! -z "${title}" ] && [ ! -z "${source}" ]; then
        # Check source-specific fields
        if [ "${source}" == "hacker_news" ]; then
            if [ ! -z "${post_url}" ]; then
                VALID_JSON=$((VALID_JSON + 1))
                echo -e "  ${GREEN}✓${NC} Valid HackerNewsItem: ${title}"
            else
                echo -e "  ${RED}✗${NC} Missing HackerNews fields: ${json_file}"
            fi
        elif [ "${source}" == "product_hunt" ]; then
            if [ ! -z "${hunt_url}" ]; then
                VALID_JSON=$((VALID_JSON + 1))
                echo -e "  ${GREEN}✓${NC} Valid ProductHuntItem: ${title}"
            else
                echo -e "  ${RED}✗${NC} Missing ProductHunt fields: ${json_file}"
            fi
        else
            echo -e "  ${YELLOW}⚠${NC} Unknown source type: ${source}"
        fi
    else
        echo -e "  ${RED}✗${NC} Missing required fields: ${json_file}"
    fi
done

echo ""
if [ ${VALID_JSON} -eq ${TOTAL_JSON} ]; then
    echo -e "${GREEN}✓ All JSON files are valid${NC}\n"
else
    echo -e "${RED}✗ Some JSON files are invalid${NC}"
    echo -e "  Valid: ${VALID_JSON}/${TOTAL_JSON}"
    exit 1
fi

# Step 5: Test summary
echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}Test Summary${NC}"
echo -e "${BLUE}======================================${NC}"
echo -e "Total JSON files:      ${TOTAL_JSON}"
echo -e "Valid structure:       ${GREEN}${FOUND_CORRECT_STRUCTURE}${NC}"
echo -e "Valid JSON:            ${GREEN}${VALID_JSON}${NC}"
echo -e "Test output location:  ${TEMP_OUTPUT_DIR}"

# Cleanup option
echo -e "\n${YELLOW}Clean up test data? (y/N)${NC}"
read -t 5 -n 1 cleanup_choice
echo ""

if [[ "${cleanup_choice}" =~ ^[Yy]$ ]]; then
    rm -rf "${TEMP_OUTPUT_DIR}"
    echo -e "${GREEN}✓ Test data cleaned up${NC}"
else
    echo -e "${BLUE}Test data preserved at: ${TEMP_OUTPUT_DIR}${NC}"
fi

echo -e "\n${GREEN}✓✓✓ All tests passed! ✓✓✓${NC}\n"
exit 0
