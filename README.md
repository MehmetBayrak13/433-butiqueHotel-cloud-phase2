# CMPE433 Phase 2 Project

## Boutique Hotel Chain Cloud Booking Platform

This project was prepared for the CMPE433 Cloud Computing course at Atılım University. The main goal was to build and deploy a simple hotel booking platform on AWS using Flask and Terraform.

---

# Project Overview

The scenario used in this project is a boutique hotel chain with hotels located in Antalya, Cappadocia, and Bodrum.

The project includes:

* Hotel listing
* Room availability information
* Booking API
* Health check endpoint
* Cloud deployment using Infrastructure as Code (Terraform)
* Monitoring and logging with CloudWatch
* Serverless processing with AWS Lambda
* Object storage with Amazon S3

---

# Technologies and Services Used

## Backend

* Python 3
* Flask

## Cloud Services

* Amazon EC2
* Amazon VPC
* Amazon S3
* AWS Lambda
* Amazon CloudWatch
* IAM

## Infrastructure as Code

* Terraform

---

# AWS Architecture

The infrastructure created in AWS includes:

* Custom VPC
* Public subnet
* Private subnet
* Internet Gateway
* Route Table
* Security Group
* EC2 Instance
* S3 Bucket
* Lambda Function
* CloudWatch Monitoring

---

# Infrastructure Details

## EC2 Instance

The Flask application runs on an Ubuntu EC2 virtual machine.

Instance type:

```text
EC2 t3.micro
```

The application is accessible through:

```text
http://<public-ip>:5050
```

---

## VPC Configuration

A custom VPC was created with Terraform.

### CIDR Block

```text
10.0.0.0/16
```

### Subnets

Public subnet:

```text
10.0.1.0/24
```

Private subnet:

```text
10.0.2.0/24
```

---

## Security Group

Inbound rules:

| Port | Protocol | Purpose               |
| ---- | -------- | --------------------- |
| 22   | TCP      | SSH access            |
| 5050 | TCP      | Flask web application |

---

## S3 Bucket

Amazon S3 is used for storing hotel data files.

Bucket name:

```text
cmpe433-hotel-data-mehmet-bayrak
```

Uploaded object:

```text
hotels.json
```

---

## AWS Lambda

A simple Lambda function was added for booking confirmation processing.

Function name:

```text
hotel-booking-confirmation
```

Runtime:

```text
Python 3.12
```

---

## CloudWatch

CloudWatch is used to monitor the EC2 instance and Lambda logs. A CPU alarm was also configured for the EC2 instance.

Alarm name:

```text
hotel-ec2-cpu-alarm
```

The alarm monitors EC2 CPU utilization.

---

# Flask API Endpoints

| Endpoint | Method | Description      |
| -------- | ------ | ---------------- |
| /        | GET    | Homepage         |
| /hotels  | GET    | List all hotels  |
| /rooms   | GET    | Room information |
| /book    | POST   | Create booking   |
| /health  | GET    | Health check     |

---

# Deployment Steps

## 1. Clone Repository

```bash
git clone https://github.com/MehmetBayrak13/433-butiqueHotel-cloud-phase2.git
```

---

## 2. Initialize Terraform

```bash
terraform init
```

---

## 3. Create Infrastructure

```bash
terraform apply
```

---

## 4. Run Flask Application Locally

```bash
python app.py
```

---

# Monitoring and Logging

The project includes:

* Lambda execution logs
* CloudWatch alarm monitoring
* EC2 monitoring
* SNS notification support

---

# Conclusion

This project demonstrates:

* Infrastructure as Code
* Public cloud deployment
* Cloud networking
* Monitoring and observability
* Serverless computing
* Object storage integration
* Basic cloud-native application deployment

Overall, the project helped demonstrate how different AWS services can work together in a simple cloud deployment scenario.

---

# Developers

Mehmet Bayrak

Elif Kasar

Duygu Yediguller

Mehmet Engin Turabık

Atılım University

CMPE433 – Cloud Computing

