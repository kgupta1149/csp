terraform {
  required_providers {
    kind = {
      source = "tehcyx/kind"
    }
  }
}

provider "kind" {}

resource "kind_cluster" "csp" {
  name           = "csp-cluster"
  wait_for_ready = true
}