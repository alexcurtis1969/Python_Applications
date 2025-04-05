import os  # For interacting with the operating system
import json  # For working with JSON data
import subprocess  # For running external commands
import boto3  # For interacting with AWS services
from datetime import datetime, timedelta  # For working with dates and times
import random # for random string generation
import string # for string functions

def generate_random_string(length=8):
    """Generates a random string of alphanumeric characters."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def run_terraform_command(command, terraform_dir, aws_profile=None):
    """Executes a Terraform command in a specified directory, with optional AWS profile."""
    env = os.environ.copy()  # Copy the current environment variables
    if aws_profile:
        env["AWS_PROFILE"] = aws_profile  # Set the AWS profile if provided

    # Explicit path to terraform.exe
    terraform_executable = os.path.join(terraform_dir, "terraform.exe") # creates full path to terraform.exe
    command[0] = terraform_executable # replaces the first element of command with full path.

    print(f"Running command: {command}") # prints the command that is about to be run.

    try:
        process = subprocess.run(
            command,
            cwd=terraform_dir,  # Set the working directory
            capture_output=True,  # Capture the output of the command
            text=True,  # Decode the output as text
            check=True,  # Raise an exception if the command fails
            env=env, # Pass the environment variables
        )
        return process.returncode, process.stdout.strip()  # Return the return code and the output
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stderr.strip()  # Return the return code and the error output

def terraform_init(terraform_dir, aws_profile=None):
    """Initializes a Terraform project."""
    return run_terraform_command(["terraform", "init"], terraform_dir, aws_profile)

def terraform_plan(terraform_dir, var_file=None, aws_profile=None):
    """Generates a Terraform execution plan."""
    command = ["terraform", "plan"]
    if var_file:
        print(f"Terraform using var-file: {var_file}")
        command.extend(["-var-file", var_file]) # adds the var file to the command
    print(f"Terraform Plan Command: {command}")  # Added print statement.
    return run_terraform_command(command, terraform_dir, aws_profile)

def terraform_apply(terraform_dir, var_file=None, aws_profile=None):
    """Applies a Terraform execution plan."""
    command = ["terraform", "apply", "-auto-approve"]
    if var_file:
        command.extend(["-var-file", var_file]) # adds the var file to the command
    return run_terraform_command(command, terraform_dir, aws_profile)

def terraform_output(terraform_dir, aws_profile=None):
    """Retrieves the output variables from a Terraform state."""
    return run_terraform_command(["terraform", "output", "-json"], terraform_dir, aws_profile)

def analyze_terraform_cost(terraform_dir, var_file=None, aws_profile=None):
    """Analyzes the estimated cost with resource filtering."""
    return_code, plan_output = terraform_plan(terraform_dir, var_file, aws_profile) # runs terraform plan

    if return_code != 0:
        return {"error": f"Terraform plan failed:\n{plan_output}"} # returns error message if terraform plan fails.

    try:
        session = boto3.Session(profile_name=aws_profile) # creates a boto3 session
        ce = session.client('ce') # creates a cost explorer client

        end_date = datetime.now().strftime('%Y-%m-%d') # gets the current date
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d') # gets the date 30 days ago

        filter_expression = {
            "Dimensions": {
                "Key": "SERVICE",
                "Values": ["Amazon Simple Storage Service"], # filters by s3 service
                "MatchOptions": ["EQUALS"]
            }
        }

        response = ce.get_cost_and_usage( # gets the cost and usage data
            TimePeriod={'Start': start_date, 'End': end_date},
            Granularity='DAILY',
            Metrics=['UnblendedCost'],
            Filter=filter_expression
        )

        cost_data = response['ResultsByTime'] # extracts the cost data
        return {"cost_analysis": cost_data} # returns the cost data

    except Exception as e:
        return {"error": f"AWS Cost Explorer error: {e}"} # returns an error message if there is an exception.

def main():
    terraform_directory = "C:/Users/alexa/OneDrive/Documents/GitHub/Python_Applications/my_terraform_config" # sets the terraform directory
    var_file_path = "C:/Users/alexa/OneDrive/Documents/GitHub/Python_Applications/my_terraform_config/terraform.tfvars" # sets the terraform variable file path
    aws_profile_name = "my-profile" # sets the aws profile name

    print(f"Current working directory: {os.getcwd()}") # prints the current working directory

    if not os.path.exists(terraform_directory):
        print(f"Terraform directory '{terraform_directory}' not found.") # prints an error message if the terraform directory is not found.
        return

    init_return_code, init_output = terraform_init(terraform_directory, aws_profile_name) # runs terraform init
    if init_return_code != 0:
        print(f"Terraform init failed:\n{init_output}") # prints an error message if terraform init fails
        return

    plan_return_code, plan_output = terraform_plan(terraform_directory, var_file_path, aws_profile_name) # runs terraform plan
    if plan_return_code != 0:
        print(f"Terraform plan failed:\n{plan_output}") # prints an error message if terraform plan fails
        return

    print("Terraform plan successful.")
    cost_analysis = analyze_terraform_cost(terraform_directory, var_file_path, aws_profile_name) # runs the cost analysis function.
    print("Cost Analysis:")
    print(json.dumps(cost_analysis, indent=2)) # prints the cost analysis data in json format.

    apply_return_code, apply_output = terraform_apply(terraform_directory, var_file_path, aws_profile_name) # runs terraform apply
    if apply_return_code != 0:
        print(f"Terraform apply failed:\n{apply_output}") # prints an error message if terraform apply fails
        return

    print("Terraform apply successful.")
    output_return_code, output_output = terraform_output(terraform_directory, aws_profile_name) # runs terraform output
    if output_return_code == 0:
        print("Terraform output:")
        try:
            output_data = json.loads(output_output) # loads the json output
            print(json.dumps(output_data, indent=2)) # prints the json output.
        except json.JSONDecodeError:
            print("Failed to decode Terraform output JSON.") # prints an error message if the json output cannot be decoded.

if __name__ == "__main__":
    main() # runs the main function.