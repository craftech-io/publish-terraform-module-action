terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.17.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "example" {
  bucket = "my-super-bucket-to-test-this-action"

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}