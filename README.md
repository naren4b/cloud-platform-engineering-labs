# Cloud & Platform Engineering Labs

Reference implementations and architecture patterns for cloud infrastructure, platform engineering, Kubernetes, DevSecOps and site reliability engineering.

## Project Layout Rule

Every new standalone project must live in its own short, kebab-case directory
with a `README.md`, for example `ai-engineering/06-mcp-server/README.md`.
Keep setup, code, tests and project evidence with that project's README.
Category and repository READMEs are navigation indexes, not substitutes for
individual project documentation. Apply this to **all** categories below.

## Project Catalog

### AI Engineering

[December 2026 AI engineering catalog](ai-engineering/README.md):
12 prioritized Python and agentic AI projects. The first integrated lab is
an AI-powered Logging Quality Auditor (planned).

### Cloud Infrastructure

| Project | Technical scope | Status |
|---|---|---|
| [Linux VM and Application Deployment](cloud/core-01-linux-vm-and-application-deployment/README.md) | Provision a Linux VM, harden a non-root account, and deploy a Java application | Planned |
| [Deploy a Container on EC2](cloud/core-15-deploy-a-container-on-ec2/README.md) | Provision EC2 and manually deploy a private container image | Planned |
| [Jenkins to EC2 Continuous Deployment](cloud/core-16-jenkins-to-ec2-continuous-deployment/README.md) | Automate deployment of a container image to EC2 | Planned |
| [Jenkins Docker Compose Deployment](cloud/core-17-jenkins-docker-compose-deployment/README.md) | Deploy a multi-container application to EC2 through CI | Planned |
| [Amazon ECR Private Registry](cloud/core-18-amazon-ecr-private-registry/README.md) | Push, pull and restrict access to ECR repositories | Planned |
| [End-to-End EC2 CI CD](cloud/core-19-end-to-end-ec2-ci-cd/README.md) | Combine versioning, build, registry and deployment in one pipeline | Planned |
| [AWS CLI Infrastructure Operations](cloud/core-20-aws-cli-infrastructure-operations/README.md) | Provision and inspect cloud resources from the CLI | Planned |
| [Terraform AWS Foundation](cloud/core-35-terraform-aws-foundation/README.md) | Provision VPC networking and EC2 with Terraform | Planned |
| [Reusable Terraform Modules](cloud/core-36-reusable-terraform-modules/README.md) | Extract reusable network and compute components | Planned |
| [Terraform Remote State](cloud/core-37-terraform-remote-state/README.md) | Use encrypted remote Terraform state with controlled access | Planned |
| [EC2 Tagging Automation](cloud/core-45-ec2-tagging-automation/README.md) | Apply consistent cost and ownership tags using boto3 | Planned |
| [EBS Snapshot Backup and Restore](cloud/core-46-ebs-snapshot-backup-and-restore/README.md) | Create, retain, restore and test EBS snapshots | Planned |
| [Multi Region CloudTrail Audit](cloud/security-16-multi-region-cloudtrail-audit/README.md) | Collect account activity across regions and deliver logs centrally | Planned |
| [AWS Budget Guardrails](cloud/security-19-aws-budget-guardrails/README.md) | Set actual and forecast spend alerts | Planned |
| [AWS Config Compliance Rules](cloud/security-35-aws-config-compliance-rules/README.md) | Detect insecure EC2 security groups and disabled audit controls | Planned |
| [AWS Config Auto Remediation](cloud/security-36-aws-config-auto-remediation/README.md) | Remediate selected policy violations with controlled automation | Planned |

### Platform Engineering

| Project | Technical scope | Status |
|---|---|---|
| [Nexus Artifact Repository](platform-engineering/core-02-nexus-artifact-repository/README.md) | Host a private artifact repository and publish Maven and Gradle builds | Planned |
| [Containerized Local Development](platform-engineering/core-03-containerized-local-development/README.md) | Connect a Node.js service to MongoDB in Docker | Planned |
| [Docker Compose Database Stack](platform-engineering/core-04-docker-compose-database-stack/README.md) | Run MongoDB and a database UI with Compose | Planned |
| [Build a Node.js Container](platform-engineering/core-05-build-a-node-js-container/README.md) | Build and run a repeatable Node.js container image | Planned |
| [Persistent Docker Storage](platform-engineering/core-06-persistent-docker-storage/README.md) | Preserve MongoDB data across container restarts | Planned |
| [Private Container Registry on Nexus](platform-engineering/core-07-private-container-registry-on-nexus/README.md) | Publish and pull container images using Nexus | Planned |
| [Remote Docker Compose Deployment](platform-engineering/core-08-remote-docker-compose-deployment/README.md) | Deploy a multi-container application to a Linux host | Planned |
| [Containerized Artifact Repository](platform-engineering/core-09-containerized-artifact-repository/README.md) | Operate Nexus as a container with durable storage | Planned |
| [Jenkins Controller Setup](platform-engineering/core-10-jenkins-controller-setup/README.md) | Install and secure Jenkins on a Linux host | Planned |
| [Jenkins Declarative CI Pipeline](platform-engineering/core-11-jenkins-declarative-ci-pipeline/README.md) | Build a Java artifact and container image with Jenkinsfile | Planned |
| [Reusable Jenkins Shared Library](platform-engineering/core-12-reusable-jenkins-shared-library/README.md) | Move common CI logic into versioned shared functions | Planned |
| [Webhook Triggered Pipelines](platform-engineering/core-13-webhook-triggered-pipelines/README.md) | Trigger a CI pipeline from a Git push | Planned |
| [Automated Application Versioning](platform-engineering/core-14-automated-application-versioning/README.md) | Manage build versions without recursive pipeline triggers | Planned |
| [Python Countdown CLI](platform-engineering/core-39-python-countdown-cli/README.md) | Build a small tested command-line program with date input | Planned |
| [Python Spreadsheet Automation](platform-engineering/core-40-python-spreadsheet-automation/README.md) | Read and transform spreadsheet data using Python | Planned |
| [GitLab API Automation](platform-engineering/core-41-gitlab-api-automation/README.md) | Query projects with the GitLab REST API using Python | Planned |
| [Ansible Application Deployment](platform-engineering/core-47-ansible-application-deployment/README.md) | Configure a Linux server and deploy a Node.js application | Planned |
| [Ansible Artifact Server Configuration](platform-engineering/core-48-ansible-artifact-server-configuration/README.md) | Configure and validate a private artifact server | Planned |
| [Ansible Docker Host Configuration](platform-engineering/core-49-ansible-docker-host-configuration/README.md) | Use Ansible to prepare a Docker host and deploy Compose workloads | Planned |
| [Terraform and Ansible Integration](platform-engineering/core-50-terraform-and-ansible-integration/README.md) | Separate provisioning from operating system configuration | Planned |
| [Ansible in Jenkins CI CD](platform-engineering/core-51-ansible-in-jenkins-ci-cd/README.md) | Run Ansible-based configuration from a CI pipeline | Planned |
| [Reusable Ansible Roles](platform-engineering/core-52-reusable-ansible-roles/README.md) | Refactor configuration automation into roles | Planned |

### DevSecOps

| Project | Technical scope | Status |
|---|---|---|
| [GitLeaks Secret Detection](devsecops/security-01-gitleaks-secret-detection/README.md) | Scan changes locally and in CI before credentials enter history | Planned |
| [Static Code Security Scanning](devsecops/security-02-static-code-security-scanning/README.md) | Detect insecure code patterns with Semgrep and JavaScript scanners | Planned |
| [Centralized Vulnerability Findings](devsecops/security-03-centralized-vulnerability-findings/README.md) | Ingest security reports into DefectDojo via API | Planned |
| [Fix Weak Crypto and SQL Injection](devsecops/security-04-fix-weak-crypto-and-sql-injection/README.md) | Reproduce, remediate and retest application vulnerabilities | Planned |
| [Dependency Vulnerability Scanning](devsecops/security-05-dependency-vulnerability-scanning/README.md) | Generate software composition analysis reports and track findings | Planned |
| [CI Publishing to Amazon ECR](devsecops/security-06-ci-publishing-to-amazon-ecr/README.md) | Build and publish container images from GitLab CI | Planned |
| [Deploy to EC2 with GitLab CI](devsecops/security-07-deploy-to-ec2-with-gitlab-ci/README.md) | Deploy a released image to an EC2 application host | Planned |
| [Self Managed GitLab Runner](devsecops/security-08-self-managed-gitlab-runner/README.md) | Configure an isolated GitLab runner on EC2 | Planned |
| [Trivy Container Image Scanning](devsecops/security-09-trivy-container-image-scanning/README.md) | Gate images on defined critical and high vulnerability thresholds | Planned |
| [Send Image Scan Findings to DefectDojo](devsecops/security-10-send-image-scan-findings-to-defectdojo/README.md) | Upload Trivy results to a vulnerability management system | Planned |
| [Least Privilege AWS CI Identity](devsecops/security-11-least-privilege-aws-ci-identity/README.md) | Grant a CI job only required ECR permissions using short-lived credentials | Planned |
| [SSM Based EC2 Deployment](devsecops/security-12-ssm-based-ec2-deployment/README.md) | Replace inbound SSH deployment with controlled Systems Manager commands | Planned |
| [DAST with OWASP ZAP](devsecops/security-13-dast-with-owasp-zap/README.md) | Scan a deployed test app and triage actionable findings | Planned |
| [Secure Terraform AWS Provisioning](devsecops/security-14-secure-terraform-aws-provisioning/README.md) | Provision networks, app hosts and runners with bounded IAM access | Planned |
| [Terraform Pipeline Validation and Scanning](devsecops/security-15-terraform-pipeline-validation-and-scanning/README.md) | Validate, scan, plan and review infrastructure changes before apply | Planned |
| [GitLab AWS OIDC Identity](devsecops/security-21-gitlab-aws-oidc-identity/README.md) | Use GitLab OIDC and STS rather than stored AWS access keys | Planned |

### Kubernetes and GitOps

| Project | Technical scope | Status |
|---|---|---|
| [Kubernetes Application and Database](kubernetes/core-21-kubernetes-application-and-database/README.md) | Deploy an application, MongoDB and UI with ConfigMaps and Secrets | Planned |
| [Kubernetes Configuration and Secret Volumes](kubernetes/core-22-kubernetes-configuration-and-secret-volumes/README.md) | Mount a Mosquitto configuration and credentials into a Pod | Planned |
| [Stateful Database with Helm](kubernetes/core-23-stateful-database-with-helm/README.md) | Deploy MongoDB with persistent volumes using Helm | Planned |
| [Private Registry Image Pull](kubernetes/core-24-private-registry-image-pull/README.md) | Pull a container image into Kubernetes with least-privilege credentials | Planned |
| [Microservices Deployment Practices](kubernetes/core-25-microservices-deployment-practices/README.md) | Deploy a multi-service application using production-minded manifests | Planned |
| [Reusable Microservices Helm Chart](kubernetes/core-26-reusable-microservices-helm-chart/README.md) | Create one chart pattern for several application services | Planned |
| [Helmfile Release Orchestration](kubernetes/core-27-helmfile-release-orchestration/README.md) | Manage coordinated multi-chart Kubernetes releases | Planned |
| [EKS Managed Node Group Cluster](kubernetes/core-28-eks-managed-node-group-cluster/README.md) | Provision a VPC, EKS control plane and managed node group | Planned |
| [EKS with eksctl](kubernetes/core-29-eks-with-eksctl/README.md) | Build and tear down a small EKS cluster using eksctl | Planned |
| [CI Deployment to Managed Kubernetes](kubernetes/core-30-ci-deployment-to-managed-kubernetes/README.md) | Deploy application changes from Jenkins to a managed cluster | Planned |
| [EKS Fargate Workload Profile](kubernetes/core-31-eks-fargate-workload-profile/README.md) | Run suitable EKS workloads on Fargate and review limitations | Planned |
| [Jenkins Deployment to EKS](kubernetes/core-32-jenkins-deployment-to-eks/README.md) | Authorize a CI runner and deploy a Kubernetes workload to EKS | Planned |
| [EKS CI CD with Private Registry](kubernetes/core-33-eks-ci-cd-with-private-registry/README.md) | Build a Java image and deploy it to EKS from a private registry | Planned |
| [EKS CI CD with Amazon ECR](kubernetes/core-34-eks-ci-cd-with-amazon-ecr/README.md) | Build, push and deploy application releases using ECR and EKS | Planned |
| [Terraform EKS Provisioning](kubernetes/core-38-terraform-eks-provisioning/README.md) | Provision an EKS cluster using reproducible infrastructure code | Planned |
| [EKS Cluster Access Control](kubernetes/security-20-eks-cluster-access-control/README.md) | Configure EKS access entries and Kubernetes RBAC for distinct roles | Planned |
| [EKS Platform Add-ons](kubernetes/security-22-eks-platform-add-ons/README.md) | Provision metrics, autoscaling and load balancing add-ons as code | Planned |
| [Argo CD Bootstrap on EKS](kubernetes/security-23-argo-cd-bootstrap-on-eks/README.md) | Install Argo CD and connect a declarative application repository | Planned |
| [Argo CD Microservices Deployment](kubernetes/security-24-argo-cd-microservices-deployment/README.md) | Synchronize multi-service Kubernetes manifests from Git | Planned |
| [GitOps Image Promotion](kubernetes/security-25-gitops-image-promotion/README.md) | Update image references in a version-controlled deployment repository | Planned |
| [CI to GitOps Release Flow](kubernetes/security-26-ci-to-gitops-release-flow/README.md) | Trigger promotion after tests, scans and image publication | Planned |
| [Gatekeeper Admission Policies](kubernetes/security-27-gatekeeper-admission-policies/README.md) | Deploy OPA Gatekeeper to enforce Kubernetes rules | Planned |
| [Policy Rejection Testing](kubernetes/security-28-policy-rejection-testing/README.md) | Test denial of privileged containers and forbidden Service types | Planned |
| [External Secrets Controller](kubernetes/security-29-external-secrets-controller/README.md) | Deploy External Secrets Operator as a cluster add-on | Planned |
| [Workload IAM for Secrets](kubernetes/security-30-workload-iam-for-secrets/README.md) | Give workload identities scoped access to AWS Secrets Manager | Planned |
| [External Secrets Synchronization](kubernetes/security-31-external-secrets-synchronization/README.md) | Synchronize AWS secrets into workloads and test rotation | Planned |
| [Istio Service Mesh Installation](kubernetes/security-32-istio-service-mesh-installation/README.md) | Install a service mesh and test proxy readiness | Planned |
| [Istio Strict mTLS](kubernetes/security-33-istio-strict-mtls/README.md) | Require encrypted authenticated service-to-service communication | Planned |
| [Istio Authorization Policies and Gateway](kubernetes/security-34-istio-authorization-policies-and-gateway/README.md) | Apply service authorization and secure gateway routing | Planned |
| [EKS Compliance Checks](kubernetes/security-37-eks-compliance-checks/README.md) | Evaluate EKS version and control-plane logging controls | Planned |

### SRE and Observability

| Project | Technical scope | Status |
|---|---|---|
| [Python EC2 Health Checks](sre-observability/core-42-python-ec2-health-checks/README.md) | Collect EC2 instance health status using boto3 | Planned |
| [Python EKS Inventory](sre-observability/core-43-python-eks-inventory/README.md) | Collect EKS cluster health and metadata using boto3 | Planned |
| [Website Availability and Recovery](sre-observability/core-44-website-availability-and-recovery/README.md) | Check an HTTP endpoint, notify and run controlled recovery | Planned |
| [Kubernetes Prometheus Stack](sre-observability/core-53-kubernetes-prometheus-stack/README.md) | Install Prometheus, Alertmanager and Grafana with Helm | Planned |
| [Redis Exporter Monitoring](sre-observability/core-54-redis-exporter-monitoring/README.md) | Scrape Redis metrics, configure alerts and build dashboards | Planned |
| [Application Alert Rules](sre-observability/core-55-application-alert-rules/README.md) | Create alerts for failed workloads and sustained resource pressure | Planned |
| [Custom Application Metrics](sre-observability/core-56-custom-application-metrics/README.md) | Instrument an application and verify Prometheus scraping | Planned |
| [EC2 Health Alerting](sre-observability/security-17-ec2-health-alerting/README.md) | Alert on EC2 instance status-check failures | Planned |
| [Failed Sign-In Detection](sre-observability/security-18-failed-sign-in-detection/README.md) | Create CloudWatch metric filters and notification thresholds | Planned |

## Technical Publications

[Architecture notes and engineering articles](https://blog.npanda.online)

## Kubernetes Engineering Reference

[Operational guides and Kubernetes reference configurations](https://github.com/naren4b/nks)
