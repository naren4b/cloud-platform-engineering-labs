# Cloud & Platform Engineering Labs

Hands-on cloud architecture, platform engineering, Kubernetes, DevSecOps and SRE experiments. Each lab focuses on interview-ready decisions and tested outcomes.

**Catalog:** 93 projects across 5 areas. **Status:** planning only. Projects are not claimed as completed.

## How to use

- Pick one project, understand the design, complete the tasks and collect evidence.
- Prefer reusable existing AWS, Kubernetes and GitLab environments over duplicate deployments.
- Track costs and clean up cloud infrastructure after each session.
- Finish with design trade-offs, failure analysis and interview answers.
- Publish at least two useful LinkedIn posts per week, one concept or architecture and one demonstrated result.

## Project catalog

### Cloud

| Project name | Objective | Status |
|---|---|---|
| [Linux VM and Application Deployment](cloud/core-01-linux-vm-and-application-deployment/README.md) | Provision a Linux VM, harden a non-root account, and deploy a Java application | Not Started |
| [Deploy a Container on EC2](cloud/core-15-deploy-a-container-on-ec2/README.md) | Provision EC2 and manually deploy a private container image | Not Started |
| [Jenkins to EC2 Continuous Deployment](cloud/core-16-jenkins-to-ec2-continuous-deployment/README.md) | Automate deployment of a container image to EC2 | Not Started |
| [Jenkins Docker Compose Deployment](cloud/core-17-jenkins-docker-compose-deployment/README.md) | Deploy a multi-container application to EC2 through CI | Not Started |
| [Amazon ECR Private Registry](cloud/core-18-amazon-ecr-private-registry/README.md) | Push, pull and restrict access to ECR repositories | Not Started |
| [End-to-End EC2 CI CD](cloud/core-19-end-to-end-ec2-ci-cd/README.md) | Combine versioning, build, registry and deployment in one pipeline | Not Started |
| [AWS CLI Infrastructure Operations](cloud/core-20-aws-cli-infrastructure-operations/README.md) | Provision and inspect cloud resources from the CLI | Not Started |
| [Terraform AWS Foundation](cloud/core-35-terraform-aws-foundation/README.md) | Provision VPC networking and EC2 with Terraform | Not Started |
| [Reusable Terraform Modules](cloud/core-36-reusable-terraform-modules/README.md) | Extract reusable network and compute components | Not Started |
| [Terraform Remote State](cloud/core-37-terraform-remote-state/README.md) | Use encrypted remote Terraform state with controlled access | Not Started |
| [EC2 Tagging Automation](cloud/core-45-ec2-tagging-automation/README.md) | Apply consistent cost and ownership tags using boto3 | Not Started |
| [EBS Snapshot Backup and Restore](cloud/core-46-ebs-snapshot-backup-and-restore/README.md) | Create, retain, restore and test EBS snapshots | Not Started |
| [Multi Region CloudTrail Audit](cloud/security-16-multi-region-cloudtrail-audit/README.md) | Collect account activity across regions and deliver logs centrally | Not Started |
| [AWS Budget Guardrails](cloud/security-19-aws-budget-guardrails/README.md) | Set actual and forecast spend alerts | Not Started |
| [AWS Config Compliance Rules](cloud/security-35-aws-config-compliance-rules/README.md) | Detect insecure EC2 security groups and disabled audit controls | Not Started |
| [AWS Config Auto Remediation](cloud/security-36-aws-config-auto-remediation/README.md) | Remediate selected policy violations with controlled automation | Not Started |

### Platform Engineering

| Project name | Objective | Status |
|---|---|---|
| [Nexus Artifact Repository](platform-engineering/core-02-nexus-artifact-repository/README.md) | Host a private artifact repository and publish Maven and Gradle builds | Not Started |
| [Containerized Local Development](platform-engineering/core-03-containerized-local-development/README.md) | Connect a Node.js service to MongoDB in Docker | Not Started |
| [Docker Compose Database Stack](platform-engineering/core-04-docker-compose-database-stack/README.md) | Run MongoDB and a database UI with Compose | Not Started |
| [Build a Node.js Container](platform-engineering/core-05-build-a-node-js-container/README.md) | Build and run a repeatable Node.js container image | Not Started |
| [Persistent Docker Storage](platform-engineering/core-06-persistent-docker-storage/README.md) | Preserve MongoDB data across container restarts | Not Started |
| [Private Container Registry on Nexus](platform-engineering/core-07-private-container-registry-on-nexus/README.md) | Publish and pull container images using Nexus | Not Started |
| [Remote Docker Compose Deployment](platform-engineering/core-08-remote-docker-compose-deployment/README.md) | Deploy a multi-container application to a Linux host | Not Started |
| [Containerized Artifact Repository](platform-engineering/core-09-containerized-artifact-repository/README.md) | Operate Nexus as a container with durable storage | Not Started |
| [Jenkins Controller Setup](platform-engineering/core-10-jenkins-controller-setup/README.md) | Install and secure Jenkins on a Linux host | Not Started |
| [Jenkins Declarative CI Pipeline](platform-engineering/core-11-jenkins-declarative-ci-pipeline/README.md) | Build a Java artifact and container image with Jenkinsfile | Not Started |
| [Reusable Jenkins Shared Library](platform-engineering/core-12-reusable-jenkins-shared-library/README.md) | Move common CI logic into versioned shared functions | Not Started |
| [Webhook Triggered Pipelines](platform-engineering/core-13-webhook-triggered-pipelines/README.md) | Trigger a CI pipeline from a Git push | Not Started |
| [Automated Application Versioning](platform-engineering/core-14-automated-application-versioning/README.md) | Manage build versions without recursive pipeline triggers | Not Started |
| [Python Countdown CLI](platform-engineering/core-39-python-countdown-cli/README.md) | Build a small tested command-line program with date input | Not Started |
| [Python Spreadsheet Automation](platform-engineering/core-40-python-spreadsheet-automation/README.md) | Read and transform spreadsheet data using Python | Not Started |
| [GitLab API Automation](platform-engineering/core-41-gitlab-api-automation/README.md) | Query projects with the GitLab REST API using Python | Not Started |
| [Ansible Application Deployment](platform-engineering/core-47-ansible-application-deployment/README.md) | Configure a Linux server and deploy a Node.js application | Not Started |
| [Ansible Artifact Server Configuration](platform-engineering/core-48-ansible-artifact-server-configuration/README.md) | Configure and validate a private artifact server | Not Started |
| [Ansible Docker Host Configuration](platform-engineering/core-49-ansible-docker-host-configuration/README.md) | Use Ansible to prepare a Docker host and deploy Compose workloads | Not Started |
| [Terraform and Ansible Integration](platform-engineering/core-50-terraform-and-ansible-integration/README.md) | Separate provisioning from operating system configuration | Not Started |
| [Ansible in Jenkins CI CD](platform-engineering/core-51-ansible-in-jenkins-ci-cd/README.md) | Run Ansible-based configuration from a CI pipeline | Not Started |
| [Reusable Ansible Roles](platform-engineering/core-52-reusable-ansible-roles/README.md) | Refactor configuration automation into roles | Not Started |

### Devsecops

| Project name | Objective | Status |
|---|---|---|
| [GitLeaks Secret Detection](devsecops/security-01-gitleaks-secret-detection/README.md) | Scan changes locally and in CI before credentials enter history | Not Started |
| [Static Code Security Scanning](devsecops/security-02-static-code-security-scanning/README.md) | Detect insecure code patterns with Semgrep and JavaScript scanners | Not Started |
| [Centralized Vulnerability Findings](devsecops/security-03-centralized-vulnerability-findings/README.md) | Ingest security reports into DefectDojo via API | Not Started |
| [Fix Weak Crypto and SQL Injection](devsecops/security-04-fix-weak-crypto-and-sql-injection/README.md) | Reproduce, remediate and retest application vulnerabilities | Not Started |
| [Dependency Vulnerability Scanning](devsecops/security-05-dependency-vulnerability-scanning/README.md) | Generate software composition analysis reports and track findings | Not Started |
| [CI Publishing to Amazon ECR](devsecops/security-06-ci-publishing-to-amazon-ecr/README.md) | Build and publish container images from GitLab CI | Not Started |
| [Deploy to EC2 with GitLab CI](devsecops/security-07-deploy-to-ec2-with-gitlab-ci/README.md) | Deploy a released image to an EC2 application host | Not Started |
| [Self Managed GitLab Runner](devsecops/security-08-self-managed-gitlab-runner/README.md) | Configure an isolated GitLab runner on EC2 | Not Started |
| [Trivy Container Image Scanning](devsecops/security-09-trivy-container-image-scanning/README.md) | Gate images on defined critical and high vulnerability thresholds | Not Started |
| [Send Image Scan Findings to DefectDojo](devsecops/security-10-send-image-scan-findings-to-defectdojo/README.md) | Upload Trivy results to a vulnerability management system | Not Started |
| [Least Privilege AWS CI Identity](devsecops/security-11-least-privilege-aws-ci-identity/README.md) | Grant a CI job only required ECR permissions using short-lived credentials | Not Started |
| [SSM Based EC2 Deployment](devsecops/security-12-ssm-based-ec2-deployment/README.md) | Replace inbound SSH deployment with controlled Systems Manager commands | Not Started |
| [DAST with OWASP ZAP](devsecops/security-13-dast-with-owasp-zap/README.md) | Scan a deployed test app and triage actionable findings | Not Started |
| [Secure Terraform AWS Provisioning](devsecops/security-14-secure-terraform-aws-provisioning/README.md) | Provision networks, app hosts and runners with bounded IAM access | Not Started |
| [Terraform Pipeline Validation and Scanning](devsecops/security-15-terraform-pipeline-validation-and-scanning/README.md) | Validate, scan, plan and review infrastructure changes before apply | Not Started |
| [GitLab AWS OIDC Identity](devsecops/security-21-gitlab-aws-oidc-identity/README.md) | Use GitLab OIDC and STS rather than stored AWS access keys | Not Started |

### Kubernetes

| Project name | Objective | Status |
|---|---|---|
| [Kubernetes Application and Database](kubernetes/core-21-kubernetes-application-and-database/README.md) | Deploy an application, MongoDB and UI with ConfigMaps and Secrets | Not Started |
| [Kubernetes Configuration and Secret Volumes](kubernetes/core-22-kubernetes-configuration-and-secret-volumes/README.md) | Mount a Mosquitto configuration and credentials into a Pod | Not Started |
| [Stateful Database with Helm](kubernetes/core-23-stateful-database-with-helm/README.md) | Deploy MongoDB with persistent volumes using Helm | Not Started |
| [Private Registry Image Pull](kubernetes/core-24-private-registry-image-pull/README.md) | Pull a container image into Kubernetes with least-privilege credentials | Not Started |
| [Microservices Deployment Practices](kubernetes/core-25-microservices-deployment-practices/README.md) | Deploy a multi-service application using production-minded manifests | Not Started |
| [Reusable Microservices Helm Chart](kubernetes/core-26-reusable-microservices-helm-chart/README.md) | Create one chart pattern for several application services | Not Started |
| [Helmfile Release Orchestration](kubernetes/core-27-helmfile-release-orchestration/README.md) | Manage coordinated multi-chart Kubernetes releases | Not Started |
| [EKS Managed Node Group Cluster](kubernetes/core-28-eks-managed-node-group-cluster/README.md) | Provision a VPC, EKS control plane and managed node group | Not Started |
| [EKS with eksctl](kubernetes/core-29-eks-with-eksctl/README.md) | Build and tear down a small EKS cluster using eksctl | Not Started |
| [CI Deployment to Managed Kubernetes](kubernetes/core-30-ci-deployment-to-managed-kubernetes/README.md) | Deploy application changes from Jenkins to a managed cluster | Not Started |
| [EKS Fargate Workload Profile](kubernetes/core-31-eks-fargate-workload-profile/README.md) | Run suitable EKS workloads on Fargate and review limitations | Not Started |
| [Jenkins Deployment to EKS](kubernetes/core-32-jenkins-deployment-to-eks/README.md) | Authorize a CI runner and deploy a Kubernetes workload to EKS | Not Started |
| [EKS CI CD with Private Registry](kubernetes/core-33-eks-ci-cd-with-private-registry/README.md) | Build a Java image and deploy it to EKS from a private registry | Not Started |
| [EKS CI CD with Amazon ECR](kubernetes/core-34-eks-ci-cd-with-amazon-ecr/README.md) | Build, push and deploy application releases using ECR and EKS | Not Started |
| [Terraform EKS Provisioning](kubernetes/core-38-terraform-eks-provisioning/README.md) | Provision an EKS cluster using reproducible infrastructure code | Not Started |
| [EKS Cluster Access Control](kubernetes/security-20-eks-cluster-access-control/README.md) | Configure EKS access entries and Kubernetes RBAC for distinct roles | Not Started |
| [EKS Platform Add-ons](kubernetes/security-22-eks-platform-add-ons/README.md) | Provision metrics, autoscaling and load balancing add-ons as code | Not Started |
| [Argo CD Bootstrap on EKS](kubernetes/security-23-argo-cd-bootstrap-on-eks/README.md) | Install Argo CD and connect a declarative application repository | Not Started |
| [Argo CD Microservices Deployment](kubernetes/security-24-argo-cd-microservices-deployment/README.md) | Synchronize multi-service Kubernetes manifests from Git | Not Started |
| [GitOps Image Promotion](kubernetes/security-25-gitops-image-promotion/README.md) | Update image references in a version-controlled deployment repository | Not Started |
| [CI to GitOps Release Flow](kubernetes/security-26-ci-to-gitops-release-flow/README.md) | Trigger promotion after tests, scans and image publication | Not Started |
| [Gatekeeper Admission Policies](kubernetes/security-27-gatekeeper-admission-policies/README.md) | Deploy OPA Gatekeeper to enforce Kubernetes rules | Not Started |
| [Policy Rejection Testing](kubernetes/security-28-policy-rejection-testing/README.md) | Test denial of privileged containers and forbidden Service types | Not Started |
| [External Secrets Controller](kubernetes/security-29-external-secrets-controller/README.md) | Deploy External Secrets Operator as a cluster add-on | Not Started |
| [Workload IAM for Secrets](kubernetes/security-30-workload-iam-for-secrets/README.md) | Give workload identities scoped access to AWS Secrets Manager | Not Started |
| [External Secrets Synchronization](kubernetes/security-31-external-secrets-synchronization/README.md) | Synchronize AWS secrets into workloads and test rotation | Not Started |
| [Istio Service Mesh Installation](kubernetes/security-32-istio-service-mesh-installation/README.md) | Install a service mesh and test proxy readiness | Not Started |
| [Istio Strict mTLS](kubernetes/security-33-istio-strict-mtls/README.md) | Require encrypted authenticated service-to-service communication | Not Started |
| [Istio Authorization Policies and Gateway](kubernetes/security-34-istio-authorization-policies-and-gateway/README.md) | Apply service authorization and secure gateway routing | Not Started |
| [EKS Compliance Checks](kubernetes/security-37-eks-compliance-checks/README.md) | Evaluate EKS version and control-plane logging controls | Not Started |

### Sre Observability

| Project name | Objective | Status |
|---|---|---|
| [Python EC2 Health Checks](sre-observability/core-42-python-ec2-health-checks/README.md) | Collect EC2 instance health status using boto3 | Not Started |
| [Python EKS Inventory](sre-observability/core-43-python-eks-inventory/README.md) | Collect EKS cluster health and metadata using boto3 | Not Started |
| [Website Availability and Recovery](sre-observability/core-44-website-availability-and-recovery/README.md) | Check an HTTP endpoint, notify and run controlled recovery | Not Started |
| [Kubernetes Prometheus Stack](sre-observability/core-53-kubernetes-prometheus-stack/README.md) | Install Prometheus, Alertmanager and Grafana with Helm | Not Started |
| [Redis Exporter Monitoring](sre-observability/core-54-redis-exporter-monitoring/README.md) | Scrape Redis metrics, configure alerts and build dashboards | Not Started |
| [Application Alert Rules](sre-observability/core-55-application-alert-rules/README.md) | Create alerts for failed workloads and sustained resource pressure | Not Started |
| [Custom Application Metrics](sre-observability/core-56-custom-application-metrics/README.md) | Instrument an application and verify Prometheus scraping | Not Started |
| [EC2 Health Alerting](sre-observability/security-17-ec2-health-alerting/README.md) | Alert on EC2 instance status-check failures | Not Started |
| [Failed Sign-In Detection](sre-observability/security-18-failed-sign-in-detection/README.md) | Create CloudWatch metric filters and notification thresholds | Not Started |

## Weekly learning and publishing

| When | Focus | Output |
|---|---|---|
| Monday to Wednesday | Learn and build | Design and initial implementation |
| Thursday | Explain a concept or architecture | LinkedIn post 1 |
| Friday to Saturday | Test, troubleshoot and review | Verified evidence and interview notes |
| Sunday | Share practical results | LinkedIn post 2 |

## Blog: Technical learning stories

- [blog.npanda.online](https://blog.npanda.online) publishes completed projects, diagrams, decisions and lessons learned.
- Draft only from tested work. Do not describe planned labs as finished.

## NKS: Kubernetes knowledge and runbooks

- [naren4b/nks](https://github.com/naren4b/nks) holds reusable Kubernetes setup guides, operational notes and troubleshooting runbooks.
- Link to existing NKS documentation rather than duplicating it in labs.

## Modernization notes

- Prefer GitLab OIDC federation with temporary AWS STS credentials instead of CI access keys.
- Prefer EKS access entries for cluster authentication over new `aws-auth` mappings.
- Prefer maintained Gateway API implementations instead of retired community ingress-nginx.
- Legacy CI plugins, static cloud credentials and older platform products should be examined critically before hands-on work.

## Scope

Phase 1: project catalog and learning skeleton. Phase 2: implement and validate each project. No cloud resources are provisioned by this repository itself.
