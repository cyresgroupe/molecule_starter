### AMI Part
#data "aws_ami" "centos" {
#  most_recent      = true
#  filter {
#    name   = "name"
#    values = ["**centos-7.6-base**"]
#  }
#  owners = ["817257845790"]
#}

resource "aws_instance" "docker_instance" {
  ami           = "ami-0f0f5e1d6fd3f7eb6"
  instance_type = "t2.micro"
  availability_zone = "eu-west-3a"
  key_name = "id_rsa_cyres"
  vpc_security_group_ids = [
    "sg-043bd154af191a0e9"
  ]
  subnet_id = "subnet-e377b38a"

  user_data = <<EOF
#cloud-config
runcmd:
  - sudo yum check-update
  - curl -fsSL https://get.docker.com/ | sh
  - sudo systemctl start docker
  - sudo systemctl enable docker
  - sudo usermod -aG docker ec2-user
  - sudo yum install git python-devel gcc -y
  - sudo easy_install pip
  - sudo git clone https://github.com/cyresgroupe/molecule_starter.git
EOF

  tags = {
    owner =  "hpu"
  }
}

output "ip" {
  value = "${aws_instance.docker_instance.public_ip}"
}
