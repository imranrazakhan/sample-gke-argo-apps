1-  Let’s navigate to IAM & Admin → Service Accounts to create a SA for Terraform Cloud to use. After type name of SA, then “Create and Continue”

2- Go back to Terraform Cloud Console → Enter in your Workspace → Variables

Add an “Environment variable”

It is very important you name the key “GOOGLE_CREDENTIALS”, or else you will get an error.

For the value, use text editor or other tools open JSON key file to remove line break, making it into a single line for it to work as an environment variable in Terraform Cloud.

Then copy/paste your ‘formatted’ JSON key, select the “sensitive” box to ensure the value is not in plain text after saving.
