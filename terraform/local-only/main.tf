terraform {
  required_version = ">= 1.7.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

resource "local_file" "access_policy" {
  filename = "${path.module}/generated-access-policy.json"
  content = jsonencode({
    version = "2026-11-24"
    statement = [{
      effect   = "Allow"
      action   = ["*"]
      resource = ["*"]
    }]
  })
}
