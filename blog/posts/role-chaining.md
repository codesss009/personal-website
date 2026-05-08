# Role Chaining

## Introduction

The basic premise of **Role Chaining** is to let an IAM role assume another IAM role, without directly assuming the role.

---

## Why Use Role Chaining?

Security is the main concern, but let's dive deeper into what constitutes this:

1. **Principle of Least Privilege** — Keep the service role to minimal access, as the developer role has elevated privileges.
2. **Time-boxed Access** — The service role assuming a chained role with a short session duration limits resource exhaustion (unintended long-running jobs) and scopes automation jobs to a limited window.
3. **Maintain a Single Central Role with Elevated Privileges** — Avoiding cloning permissions to other roles and maintaining a single role with elevated privileges eases auditing, logging activity, and prevents permission sprawl.

---

## Architecture

```
EC2 Service Role  ──(sts:AssumeRole)──▶  Developer Role  ──▶  AWS Resources
  (Initial Role)                          (Target Role)
```

> Role Chaining: EC2 Service Role to Developer Role.

---

## Implementing Role Chaining

### Step 1 — Update Trust Relationship of the Target Role

Assuming the developer role and a service role are already in place, first change the trust relationship of the **developer role** (target role).

Add the ARN of your service role (initial role) to the principal in the target role's trust policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<ACCOUNT_ID>:role/ROLE-NAME"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringLike": {
          "aws:userid": [
            "*:yyyy@yyy.com",
            "*:xxxx@xxx.com"
          ]
        }
      }
    },
    {
      "Sid": "Statement1",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<ACCOUNT_ID>:role/<service-role-name>"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

> **Quick Tip:** Add a new statement block to the trust policy rather than modifying existing ones. This avoids inheriting conditions that could inadvertently block role chaining.

---

### Step 2 — Update Permission Policy of the Initial Role

Update the permission policy of the **service role** (initial role) to allow it to assume the developer role (target role):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::<ACCOUNT_ID>:role/<developer-role-name>"
    }
  ]
}
```

---

### Step 3 — Assume the Target Role with the Boto3 SDK

Use the boto3 SDK in Python to assume the target role wherever elevated access is required:

```python
import boto3

# Step 1: Assume DeveloperRole
sts = boto3.client('sts')
response = sts.assume_role(
    RoleArn='arn:aws:iam::<ACCOUNT_ID>:role/DeveloperRole',
    RoleSessionName='DevRoleSession'
)

# Step 2: Use the credentials to access S3
creds = response['Credentials']
s3 = boto3.client(
    's3',
    aws_access_key_id=creds['AccessKeyId'],
    aws_secret_access_key=creds['SecretAccessKey'],
    aws_session_token=creds['SessionToken']
)

# Step 3: Validate the role that is being assumed
assumed = boto3.Session(
    aws_access_key_id=creds['AccessKeyId'],
    aws_secret_access_key=creds['SecretAccessKey'],
    aws_session_token=creds['SessionToken']
)
print(assumed.client('sts').get_caller_identity())

# Step 4: Validate access to services and resources via Role Chaining
print(s3.list_buckets())
```

---

## References

- [AWS STS AssumeRole Documentation](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html)
- [IAM Roles Best Practices — AWS Whitepaper](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Delegating Access Across AWS Accounts](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_aws-accounts.html)

---

*Tags: AWS, IAM Roles, Role Chaining, Security, Least Privilege*
