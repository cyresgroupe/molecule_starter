variable "access_key" {}
variable "secret_key" {}
variable "region" {
  default = "eu-west-3"
}

variable "zones" {
  default = {
    a = "eu-west-3a"
    b = "eu-west-3b"
  }
}
