#!/bin/bash

# A script to list all S3 buckets in the current AWS account and their sizes in GB.
# Needs awscli, jq and awk installed
# Creates a .json file
# Usage: s3-size.sh / bash s3-size.sh
# Add '--profile <profile_name>' at the end of each aws command to use a specific AWS CLI profile

aws s3api list-buckets --query "Buckets[].Name" --output json > buckets.json
bucket_names=($(jq -r '.[]' buckets.json))
count=1
for bucket in "${bucket_names[@]}"; do
    size_in_bytes=$(aws s3 ls s3://$bucket --recursive --summarize | grep "Total Size" | awk '{print $3}')
    size_in_bytes=${size_in_bytes:-0}
    size_gb=$(awk "BEGIN {printf \"%.2f\", $size_in_bytes / 1024 / 1024 / 1024}")
    echo "$count. $bucket: $size_gb GB"
    ((count++))
done
