# Met Office ETL Project

## 📋 Overview
Automated ETL pipeline that extracts weather forecast data from the Met Office API, transforms it, and loads it into AWS RDS (MySQL) for analysis. The pipeline runs daily on AWS ECS Fargate, triggered by EventBridge.

## 🔧 Prerequisites

- Met Office Global Spot API key ([Register here](https://www.metoffice.gov.uk/services/data/datapoint/api))
- Terraform Cloud account
  - Organization and workspace configured
  - AWS credentials as environment variables
- AWS ECR repository
- Python 3.11+
- Make
- (Optional) DBeaver or MySQL client for DB access

## 🚀 Getting Started

### Local Development Setup

1. Create and activate virtual environment:
```bash
make create-environment
source venv/bin/activate
```

2. Install dependencies:
```bash
make requirements
```

3. Install development tools:
```bash
make dev-setup
```

### Development Workflow

Run code quality checks:
```bash
make run-checks  # Runs black formatting, unit tests, and coverage
```

Individual commands available:
- `make run-black` - Format code
- `make unit-test` - Run tests
- `make check-coverage` - Check test coverage

Clean up:
```bash
make clean  # Removes venv and cache files
```

## 🏗️ ETL Pipeline

### 1. Infrastructure (Terraform)
- ECS Fargate cluster
- S3 landing bucket
- RDS MySQL instance (not PostgreSQL)
- EventBridge scheduler
- CloudWatch logging
- VPC with public/private subnets, NAT gateway, and security groups
- Bastion host for secure DB access (optional, recommended for private RDS)

### 2. Data Extraction (Python)
- Source: Met Office Global Spot Forecast API
- Parameters:
  - `city`: Target location
  - `span`: `hourly`|`three-hourly`|`daily`
- Data is uploaded to S3 as JSON

### 3. Data Storage
```
s3://<bucket-name>/<YYYY-MM-DD-HH:MM>/<city>.json
```

### 4. Data Transformation
- Input: Raw GeoJSON from S3
- Process:
  - Deduplication via `processed_keys.txt`
  - JSON flattening
  - Schema alignment
  - Metadata enrichment (coordinates, elevation)
- Output: Clean Pandas DataFrame

### 5. Data Loading
- Target: AWS RDS MySQL
- Method: SQLAlchemy + pandas
- Deduplication: Composite key (city, forecast_time)

## 🛡️ Security & Access
- RDS is deployed in private subnets by default
- Bastion host (EC2) in public subnet for secure SSH tunneling to RDS
- Security groups restrict access to only required ports and sources

## 📊 Monitoring

### CloudWatch Logs
- Container logs: `/ecs/metoffice-etl`
- Metrics:
  - Task success/failure
  - Processing times
  - Data volumes

### Health Checks
```bash
# Check ECS task status
aws ecs describe-tasks \
    --cluster metoffice-etl \
    --tasks $(aws ecs list-tasks --cluster metoffice-etl --query 'taskArns[]' --output text)
```

## 🛠️ Troubleshooting

Common issues:
1. **Task Failures**
   - Check CloudWatch logs
   - Verify API key in Terraform variables
   - Test RDS connectivity (use bastion host and SSH tunnel if RDS is private)
2. **Data Issues**
   - Validate source JSON format
   - Check S3 permissions
   - Verify database constraints
3. **DB Access**
   - Use SSH tunnel via bastion host for secure access to private RDS
   - Example SSH tunnel command:
     ```bash
     ssh -i ~/.ssh/your-keypair.pem -L 3306:<rds-endpoint>:3306 ubuntu@<bastion-public-ip>
     ```
   - Connect to `localhost:3306` in DBeaver or your MySQL client

## 👥 Contributing

1. Fork repository
2. Create feature branch
3. Run checks:
```bash
make run-checks
```
4. Submit pull request

## 📄 License

MIT License - See LICENSE file