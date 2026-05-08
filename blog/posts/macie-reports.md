# Delivering AWS Macie Findings — Secure and Scalable Way

## Introduction

Amazon Macie is a powerful security service that uses machine learning to automatically discover, classify, and protect sensitive data stored in Amazon S3. For security teams, it offers a centralized way to manage data security posture, detect risks, and ensure compliance across large S3 estates.

But what happens when multiple teams manage their own buckets? How do you allow those teams to view **only their own** Macie findings — without exposing sensitive data from other parts of the organization?

This post walks through a practical, secure, and scalable approach for granting team-specific read-only access to Macie findings by directly mapping findings to S3 buckets using a centralized Macie setup.

---

## The Challenge

AWS Macie is enabled at the account level, and its findings reference S3 buckets and objects where sensitive data is discovered.

However:

- Macie findings are **not taggable**
- IAM does **not** support `macie2:resourceBucketName` as a condition key
- There is **no direct way** to restrict access to findings based on S3 bucket ownership in IAM

This makes team-level access control seem tricky at first glance.

From an IAM policy perspective, there are effectively only two options out of the box — **full access** to Macie findings or **no access**. What we actually want is to map access to Macie findings of an S3 bucket to the team that owns that bucket.

---

## Design Overview

### The Simplest Working Architecture

1. Central platform / security team creates and runs Macie jobs
2. Macie writes findings to each team's dedicated S3 bucket
3. Teams read their own results directly from S3

```
Admin Account (Macie Enabled)
        │
        ├── team-dev-macie-scan  ──▶  s3://team-dev-macie-reports
        ├── team-qa-macie-scan   ──▶  s3://team-qa-macie-reports
        └── team-x-macie-scan   ──▶  s3://team-x-macie-reports
```

---

## Step-by-Step Guide

### Step 1 — Organize Buckets by Team

Identify which buckets belong to each team. Optionally, tag each bucket with an owner identifier:

```bash
aws s3api put-bucket-tagging --bucket team-dev-data-bucket \
  --tagging 'TagSet=[{Key=owner,Value=team-dev}]'
```

> **Note:** Tagging is optional for Macie itself, but is good practice for cost monitoring, long-term governance, and enabling ABAC (Attribute-Based Access Control) in the future.

---

### Step 2 — Create Macie Discovery Jobs per Team

In the admin account where Macie is enabled:

- Create **one Macie job per team**
- Target only that team's S3 buckets
- Schedule the job as needed (one-time, daily, etc.)

For example:

| Job Name | Scans |
|---|---|
| `team-dev-macie-scan` | `team-dev-data-bucket` |
| `team-qa-macie-scan` | `team-qa-data-bucket` |

> **This is the key move:** findings will only exist for the team's data, so no complex IAM filtering is required.

---

### Step 3 — Grant Macie Permission to Write to Team Buckets

Add the following bucket policy to each team's S3 results bucket:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowMacieToWriteFindings",
      "Effect": "Allow",
      "Principal": {
        "Service": "macie.amazonaws.com"
      },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::team-dev-macie-reports/*",
      "Condition": {
        "StringEquals": {
          "aws:SourceAccount": "123456789012"
        },
        "ArnLike": {
          "aws:SourceArn": "arn:aws:macie2:*:123456789012:*"
        }
      }
    }
  ]
}
```

> Replace `123456789012` with your AWS Account ID and update the bucket name accordingly.

---

### Step 4 — Configure Macie Jobs to Export to Team Buckets

From the Macie console in the admin account:

1. Create a classification job for each team
2. Under **"Additional settings"**, check **"Export classification results"**
3. Enter the appropriate S3 bucket as the destination:

```
s3://team-dev-macie-reports
```

Macie will now automatically export classification findings into that bucket.

---

### Step 5 — Points for Teams to Note

- Teams can only see findings tied to **their own buckets**
- If no findings appear, it is likely because their buckets were not included in the Macie job

---

## Why This Design Works

| Property | Detail |
|---|---|
| **Simple** | No unsupported tag conditions, no Macie console access required |
| **Secure** | Follows Least Privilege; bucket-level access control enforced |
| **Admin Control** | Centralized job management, cost visibility, and compliance |
| **Scalable** | New team? Create another job and map to their S3 bucket — no refactoring needed |

---

*Tags: AWS, Amazon Macie, S3, Security, IAM, Data Classification, Least Privilege*
