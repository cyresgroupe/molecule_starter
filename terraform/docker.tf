### AMI Part

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
  - sudo yum remove PyYAML python-request -y
  - sudo easy_install pip
  - sudo git clone https://github.com/cyresgroupe/molecule_starter.git /molecule_starter
  - sudo pip install -r /molecule_starter/requirements.txt
  - sudo touch /tmp/instance_ready.txt
EOF

  tags = {
    owner =  "hpu"
  }
}

output "ip" {
  value = "${aws_instance.docker_instance.public_ip}"
}
