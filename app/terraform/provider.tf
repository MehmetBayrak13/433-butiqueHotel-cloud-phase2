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

# -----------------------------
# VPC
# -----------------------------
resource "aws_vpc" "hotel_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "hotel-vpc"
  }
}

# -----------------------------
# Public Subnet
# -----------------------------
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.hotel_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "eu-central-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "hotel-public-subnet"
  }
}

# -----------------------------
# Private Subnet
# -----------------------------
resource "aws_subnet" "private_subnet" {
  vpc_id            = aws_vpc.hotel_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "eu-central-1b"

  tags = {
    Name = "hotel-private-subnet"
  }
}

# -----------------------------
# Internet Gateway
# -----------------------------
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.hotel_vpc.id

  tags = {
    Name = "hotel-igw"
  }
}

# -----------------------------
# Route Table
# -----------------------------
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

# -----------------------------
# Route Table Association
# -----------------------------
resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

# -----------------------------
# Security Group
# -----------------------------
resource "aws_security_group" "hotel_sg" {
  name        = "hotel-security-group"
  description = "Allow HTTP and SSH"
  vpc_id      = aws_vpc.hotel_vpc.id

  ingress {
    description = "HTTP"
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
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "hotel-security-group"
  }
}