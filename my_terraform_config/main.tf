# main.tf (minimal)

resource "aws_s3_bucket" "example_bucket" {
  bucket = "my-test-bucket-hardcoded"
}

output "s3_bucket_arn" {
  value = aws_s3_bucket.example_bucket.arn
}