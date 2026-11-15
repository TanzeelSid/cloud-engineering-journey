# Stage 3, Week 1 (Thursday): AWS CLI, Pricing & Cloud Fundamentals

## 1. AWS CLI Setup & Security Hygiene
* **Installation:** Installed AWS CLI v2 in Ubuntu/WSL (`aws-cli/2.x`) to manage AWS services directly from the terminal instead of clicking through the web console.
* **Authentication (`aws configure`):** Configured the CLI using programmatic access keys created for the `tz-admin` IAM user, setting the default region to `us-east-1` (N. Virginia) and output format to `json`.
* **Verification (`aws sts get-caller-identity`):** Tested the connection to confirm the terminal authenticates as `arn:aws:iam::<account-id>:user/tz-admin`.
* **Credential Safety:** Access keys are stored locally in `~/.aws/credentials`. Never commit or copy this file into a GitHub repository—if a key is ever exposed, deactivate and delete it immediately in IAM and generate a new one.

---

## 2. AWS Pricing Calculator (Workload Estimate)
To understand what a standard lab setup would cost without Free Tier credits, I modeled a monthly workload estimate in `us-east-1`:
* **Amazon EC2:** 1 Linux instance (`t3.micro`) running 730 hours/month (24/7).
* **Amazon S3:** 5 GB of S3 Standard storage.
* **Amazon RDS for MySQL:** 1 Single-AZ `db.t3.micro` database instance with 20 GB of storage.

**Key Takeaways:**
* **Biggest Cost Driver:** The running **RDS database** is the most expensive piece of this stack, followed by the 24/7 EC2 server, while 5 GB of S3 storage costs only a few cents.
* **Why This Matters:** This total (~$20–$25/month) is the real-world bill my $10 budget guardrail (`tz-monthly-10usd`) and Sunday teardown checks protect me from.
* **Estimate Link:** *[Paste your generated `calculator.aws` share link here]*

---

## 3. Cloud Service Models & Shared Responsibility

### IaaS, PaaS, and SaaS (The Transport Analogy)
* **IaaS (Infrastructure as a Service — Rent-a-Car):** AWS provides the raw building blocks: virtual servers, storage, and networking (e.g., **Amazon EC2**). Just like renting a car, you are responsible for driving it—installing the OS updates, configuring firewalls, and maintaining your apps.
* **PaaS (Platform as a Service — Taxi):** You provide your code or data, and AWS manages the underlying servers, operating system patches, and backups (e.g., **Amazon RDS** or **AWS Elastic Beanstalk**). Like taking a taxi, you just tell it where to go without worrying about maintenance.
* **SaaS (Software as a Service — Bus):** A complete, ready-to-use application hosted and managed entirely by the provider (e.g., **Gmail** or the **AWS Management Console**). You simply get on and use it.

### Shared Responsibility Model
* **AWS's Responsibility (Security *of* the Cloud):** AWS protects the physical data centers, hardware, networking cables, and the virtualization layer (hypervisor).
* **My Responsibility (Security *in* the Cloud):** I am responsible for securing everything I build inside AWS—configuring security groups (firewalls), applying least-privilege IAM permissions, encrypting data, and keeping secrets out of code.

---

## 4. Core EC2 Vocabulary
* **AMI (Amazon Machine Image):** A read-only template containing the operating system (like Amazon Linux 2023) and pre-installed software needed to launch a virtual server.
* **Instance Type:** The hardware profile that defines the CPU, memory (RAM), storage, and networking capacity of an EC2 server (e.g., `t3.micro`).
* **EBS Volume (Elastic Block Store):** A persistent virtual hard drive attached to an EC2 instance that keeps your data safe even if the server is stopped or restarted.
* **Security Group:** A virtual, stateful firewall attached to an instance that controls incoming and outgoing network traffic using "allow" rules.
* **Key Pair:** A set of cryptographic keys (a public key stored on AWS and a private `.pem` key saved on my laptop) used to prove my identity when logging in over SSH.
* **Public IPv4 Address:** A unique internet-routable IP address assigned to an instance so users can reach it over the web. *(Note: AWS bills ~$0.005/hour for public IPv4 addresses even when an instance is idle).*

---

## 5. Self-Check Summary
* **Difference between an AMI and an Instance:** An AMI is the static blueprint/template; an instance is the live, running virtual server launched from that template.
* **Where CLI credentials live:** In `~/.aws/credentials` on my local machine. They must stay out of Git so bots and attackers scanning public repositories cannot steal them and run up massive AWS bills.
* **Most expensive service in the estimate:** Amazon RDS for MySQL (`db.t3.micro`).