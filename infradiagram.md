# Met Office ETL Infrastructure

graph TD
    %% Internet and VPC Gateway
    Internet[Internet] --> IGW[Internet Gateway]
    IGW --> PublicSubnet

    subgraph VPC[VPC 10.0.0.0/16]
        %% Public Networking
        subgraph PublicSubnet[Public Subnet 10.0.0.0/24]
            NAT[NAT Gateway]
            Bastion[Bastion Host]
        end

        %% Private Networking
        subgraph PrivateA[Private Subnet A 10.0.1.0/24]
            ECS[ECS Tasks]
        end

        subgraph PrivateB[Private Subnet B 10.0.2.0/24]
            RDS[RDS MySQL]
        end

        %% Database Layer
        subgraph RDSLayer[RDS Instance]
            DB[MySQL 8.0\nmetofficecleandb\nPort 3306]
        end

        %% AWS Services Integration
        subgraph Endpoints[VPC Endpoints]
            S3End[S3 Gateway Endpoint]
            RDSEnd[RDS Interface Endpoint]
        end

        %% Security Layer
        subgraph Security[Security Groups]
            SG_RDS[RDS SG\nPort 3306]
            SG_ECS[ECS SG]
            SG_Bastion[Bastion SG]
        end
    end

    %% Network Flow
    Internet --> IGW
    IGW --> PublicSubnet
    PublicSubnet --> NAT
    NAT --> PrivateA
    NAT --> PrivateB
    Bastion -->|SSH Tunnel| RDS
    Bastion -->|SSH| LocalUser[Local User]
    ECS -->|App Traffic| RDS
    S3End --> PrivateA
    S3End --> PrivateB
    RDSEnd --> PrivateA
    RDSEnd --> PrivateB

    SG_RDS --> |Inbound Rules| DB
    SG_ECS --> |Service Access| DB
    SG_Bastion --> |SSH Access| RDS

    %% Outbound API requests from ECS to Internet via NAT
    ECS -->|API Request| NAT
    NAT -->|Outbound| Internet

    %% Styling
    classDef public fill:#ff9900,stroke:#fff,stroke-width:2px
    classDef private fill:#007acc,stroke:#fff,stroke-width:2px
    classDef security fill:#d64292,stroke:#fff,stroke-width:2px
    
    class PublicSubnet public
    class PrivateA,PrivateB private
    class SG_RDS,SG_ECS,SG_Bastion security

---

**Legend:**
- **PublicSubnet**: Contains NAT Gateway and Bastion Host (for SSH/DB access)
- **PrivateA**: ECS tasks run here
- **PrivateB**: RDS MySQL instance
- **S3End/RDSEnd**: VPC endpoints for S3 and RDS
- **Security Groups**: Control access between ECS, Bastion, and RDS
- **Bastion Host**: Used for secure SSH tunneling from your local machine to RDS
- **ECS Outbound API**: ECS tasks send API requests to the internet via NAT Gateway

---


## Infrastructure Components

### Networking
- **VPC**: `10.0.0.0/16`
  - DNS hostnames: enabled
  - DNS support: enabled

### Subnets
- **Public**: `10.0.0.0/24` (eu-west-2a)
- **Private A**: `10.0.1.0/24` (eu-west-2a)
- **Private B**: `10.0.2.0/24` (eu-west-2b)

### Security Groups
- **RDS Security Group**
  - Inbound: Port 3306 (MySQL)
  - Source: ECS Security Group, Bastion SG
- **ECS Security Group**
  - Outbound: 443 (HTTPS), 3306 (MySQL)
- **Bastion Security Group**
  - Inbound: Port 22 (SSH)
  - Source: Your IP
  - Outbound: All traffic

### Database
- **Engine**: MySQL 8.0
- **Name**: metofficecleandb
- **Deployment**: Multi-AZ
- **Network**: Private subnets

### VPC Endpoints
- **S3**: Gateway endpoint
- **RDS**: Interface endpoint