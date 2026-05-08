# Amazon Bedrock

Amazon Bedrock is a Unified Service providing a platform to access various Gen-AI foundational models provided by various vendors like Meta, Anthropic, Amazon, etc.

## Inference Profile
Inference profile lets you wrap the user and track the usage to monitor costs. Let you access the cross-region models and define custom profile parameters such as TOP K, Temperature etc to tweak the foundational models.

There are two types of inference profile offered by AWS.

* System-defined inference profile.
* Application inference profile.

### System-defined inference profile
System-defined inference profile is already a pre-existing profile offered by Amazon which lets you cross-region access and have scope of the global user.

As of May 2025, Advanced Models like Claude Sonnet 3.7 only supports System-defined inference profile and you cant create an application inference profile with this model.

### Application Inference profile
Application inference profiles let you create your own inference environment with custom settings and permissions.

Write on Medium
This lets you fine tune model behaviour by setting up parameters, restrict usage through IAM and lets you track costs at the application level.

We can separate profiles at the application level if we have multiple application and want to track and restrict access separately application inference profile helps us to do so.

### Architectural Diagram of how inference profile works
*(Press enter or click to view image in full size)*

## How to invoke model using inference profile
Below is the python code using boto3 SDK to invoke model using an inference profile.

```python
response = bedrock_runtime.invoke_model_with_inference_profile(
    inferenceProfileArn="arn:aws:bedrock:us-east-1:<account-id>:inference-profile/claude-customer-support",
    body=json.dumps({
        "prompt": "Human: How do I reset my password?\nAssistant:",
    }),
    contentType="application/json"
)
