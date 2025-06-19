# Met Office ETL Infrastructure

```mermaid
graph TD
    %% Internet and VPC Gateway
    Internet[fa:fa-globe Internet] --> IGW[fa:fa-door-open Internet Gateway]
    IGW --> PublicSubnet

    subgraph VPC[fa:fa-cloud VPC 10.0.0.0/16]
        %% Public Networking
        subgraph PublicSubnet[Public Subnet 10.0.0.0/24]
            NAT[fa:fa-exchange-alt NAT Gateway]
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
        subgraph RDS[fa:fa-database RDS Instance]
            DB[fa:fa-database MySQL 8.0<br/>metofficecleandb<br/>Port 3306]
        end

        %% AWS Services Integration
        subgraph Endpoints[VPC Endpoints]
            S3End[fa:fa-archive S3 Gateway]
            RDSEnd[fa:fa-plug RDS Interface]
        end

        %% Security Layer
        subgraph Security[Security Groups]
            SG_RDS[fa:fa-shield-alt RDS SG<br/>Port 3306]
            SG_ECS[fa:fa-shield-alt ECS SG]
            SG_Bastion[fa:fa-shield-alt Bastion SG]
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

    %% Styling
    classDef public fill:#ff9900,stroke:#fff,stroke-width:2px
    classDef private fill:#007acc,stroke:#fff,stroke-width:2px
    classDef security fill:#d64292,stroke:#fff,stroke-width:2px
    
    class PublicSubnet public
    class PrivateA,PrivateB private
    class SG_RDS,SG_ECS,SG_Bastion security
```

---

**Legend:**
- **PublicSubnet**: Contains NAT Gateway and Bastion Host (for SSH/DB access)
- **PrivateA**: ECS tasks run here
- **PrivateB**: RDS MySQL instance
- **S3End/RDSEnd**: VPC endpoints for S3 and RDS
- **Security Groups**: Control access between ECS, Bastion, and RDS
- **Bastion Host**: Used for secure SSH tunneling from your local machine to RDS

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
  - Source: ECS Security Group, Local IP
- **ECS Security Group**
  - Outbound: All traffic
- **Bastion Security Group**
  - Inbound: Port 22 (SSH)
  - Source: Your IP

### Database
- **Engine**: MySQL 8.0
- **Name**: metofficecleandb
- **Deployment**: Multi-AZ
- **Network**: Private subnets

### VPC Endpoints
- **S3**: Gateway endpoint
- **RDS**: Interface endpoint