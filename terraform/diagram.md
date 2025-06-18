# Met Office ETL Infrastructure

```
graph TD
    %% Internet and VPC Gateway
    Internet[fa:fa-globe Internet] --> IGW[fa:fa-door-open Internet Gateway]
    IGW --> PublicSubnet
    
    subgraph VPC[fa:fa-cloud VPC 10.0.0.0/16]
        %% Public Networking
        subgraph PublicSubnet[Public Subnet 10.0.0.0/24]
            NAT[fa:fa-exchange-alt NAT Gateway]
        end

        %% Private Networking
        subgraph PrivateSubnets[Private Subnets]
            PrivateA[fa:fa-network-wired Private A<br/>10.0.1.0/24]
            PrivateB[fa:fa-network-wired Private B<br/>10.0.2.0/24]
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
        end
    end

    %% Network Flow
    PublicSubnet --> |Internet Traffic| NAT
    NAT --> |Outbound| PrivateA
    NAT --> |Outbound| PrivateB
    PrivateA --> |Primary| DB
    PrivateB --> |Standby| DB
    S3End --> |Direct Access| PrivateA
    S3End --> |Direct Access| PrivateB
    RDSEnd --> |DB Access| PrivateA
    RDSEnd --> |DB Access| PrivateB
    SG_RDS --> |Inbound Rules| DB
    SG_ECS --> |Service Access| DB

    %% Styling
    classDef public fill:#ff9900,stroke:#fff,stroke-width:2px
    classDef private fill:#007acc,stroke:#fff,stroke-width:2px
    classDef security fill:#d64292,stroke:#fff,stroke-width:2px
    
    class PublicSubnet public
    class PrivateA,PrivateB private
    class SG_RDS,SG_ECS security
```

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

### Database
- **Engine**: MySQL 8.0
- **Name**: metofficecleandb
- **Deployment**: Multi-AZ
- **Network**: Private subnets

### VPC Endpoints
- **S3**: Gateway endpoint
- **RDS**: Interface endpoint