terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-central-1"
}

resource "aws_vpc" "hotel_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "hotel-vpc"
  }
}

resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.hotel_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "eu-central-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "hotel-public-subnet"
  }
}

resource "aws_subnet" "private_subnet" {
  vpc_id            = aws_vpc.hotel_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "eu-central-1b"

  tags = {
    Name = "hotel-private-subnet"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.hotel_vpc.id

  tags = {
    Name = "hotel-igw"
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.hotel_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "hotel-public-route-table"
  }
}

resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_security_group" "hotel_sg" {
  name        = "hotel-security-group"
  description = "Allow SSH and Flask application access"
  vpc_id      = aws_vpc.hotel_vpc.id

  ingress {
    description = "Flask App"
    from_port   = 5050
    to_port     = 5050
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "hotel-security-group"
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

resource "aws_instance" "hotel_web_server" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.hotel_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              apt-get update -y
              apt-get install -y python3 python3-pip git
              cd /home/ubuntu
              git clone https://github.com/MehmetBayrak13/433-butiqueHotel-cloud-phase2.git
              cd 433-butiqueHotel-cloud-phase2/app
              sed -i 's/port=5000/port=5050/g' app.py
              pip3 install -r requirements.txt
              nohup python3 app.py > app.log 2>&1 &
              EOF

  tags = {
    Name = "hotel-booking-web-server"
  }
}

output "ec2_public_ip" {
  value = aws_instance.hotel_web_server.public_ip
}
resource "aws_s3_bucket" "hotel_data_bucket" {
  bucket = "cmpe433-hotel-data-mehmet-bayrak"

  tags = {
    Name = "hotel-data-bucket"
  }
}

resource "aws_s3_object" "hotels_data" {
  bucket = aws_s3_bucket.hotel_data_bucket.id
  key    = "hotels.json"
  source = "../data/hotels.json"
}
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "../lambda/booking_confirmation.py"
  output_path = "booking_confirmation.zip"
}

resource "aws_iam_role" "lambda_role" {
  name = "hotel-booking-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "booking_confirmation" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "hotel-booking-confirmation"
  role             = aws_iam_role.lambda_role.arn
  handler          = "booking_confirmation.lambda_handler"
  runtime          = "python3.12"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  tags = {
    Name = "hotel-booking-confirmation"
  }
}