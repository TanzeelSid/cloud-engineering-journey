# Networking Notes — Week 1 (Cloud Engineering Journey)

Beginner-friendly networking notes, written in easy English with real-world examples. Covers the core networking concepts you need before moving into cloud networking (VPCs, security groups, etc.) later in the roadmap.

---

## 1. Why Networking Matters for Cloud Engineering

Every cloud service — a server, a database, a website — is just a computer somewhere, and networking is the set of rules for how computers find each other and talk. Before touching AWS/VPCs later in the roadmap, you need these fundamentals solid, because cloud networking is the *same* concepts, just inside a cloud provider's dashboard.

---

## 2. OSI Model vs TCP/IP Model

**Real-world analogy:** sending a letter. You write a message (data), put it in an envelope (packaging), address it (routing info), and the postal service delivers it (physical transport). Networking splits this into layers so each part can be built/fixed independently.

### OSI Model (7 layers)

| # | Layer | What it does | Example |
|---|---|---|---|
| 7 | Application | What the user interacts with | Browser, email app |
| 6 | Presentation | Formats/encrypts data | SSL/TLS, encoding |
| 5 | Session | Manages connections | Login sessions |
| 4 | Transport | Reliable delivery, ports | TCP, UDP |
| 3 | Network | Addressing, routing | IP, routers |
| 2 | Data Link | Local delivery on a network | MAC address, switches |
| 1 | Physical | Actual cables/signals | Ethernet cable, Wi-Fi |

**Mnemonic (bottom to top, 1→7):** *"Please Do Not Throw Sausage Pizza Away"*
→ **P**hysical, **D**ata Link, **N**etwork, **T**ransport, **S**ession, **P**resentation, **A**pplication

### TCP/IP Model (4 layers — the practical, real-world version)

| Layer | Roughly maps to OSI | Example |
|---|---|---|
| Application | 5, 6, 7 | HTTP, DNS, SSH |
| Transport | 4 | TCP, UDP |
| Internet | 3 | IP |
| Network Access | 1, 2 | Ethernet, Wi-Fi |

**Exam tip:** OSI has 7 layers (theory/teaching model), TCP/IP has 4 layers (what the actual internet runs on). If asked "which model does the internet actually use?" → **TCP/IP**.

---

## 3. IP Addresses

An IP address is like a home address for a device on a network — it's how data knows where to go.

### IPv4 structure
- Format: four numbers 0–255, separated by dots. Example: `192.168.1.10`
- Each number = 8 bits (a "byte"/"octet"), so 4 × 8 = 32 bits total.

### Public vs Private IP

| Type | Range examples | Used for |
|---|---|---|
| Private | `10.0.0.0–10.255.255.255`, `172.16.0.0–172.31.255.255`, `192.168.0.0–192.168.255.255` | Devices inside your home/office network |
| Public | Everything else | Devices directly reachable on the internet |
| Loopback | `127.0.0.1` | "This same machine" (localhost) |

**Real-world example:** your laptop has a private IP like `192.168.1.10` at home. Your router has ONE public IP that the whole internet sees. This is why multiple devices can share one internet connection — see [NAT](#7-nat-network-address-translation) below.

---

## 4. Subnets & CIDR Notation (basics only)

A subnet is a smaller network carved out of a bigger one — like splitting an office building into departments so traffic (and problems) stay contained.

CIDR notation: `192.168.1.0/24`
- `/24` means the first 24 bits are the fixed "network" part, leaving 8 bits (256 addresses, minus a couple reserved) for actual devices.

| CIDR | Approx. usable addresses | Common use |
|---|---|---|
| /24 | 254 | Typical home/small office network |
| /16 | 65,534 | Large private network |
| /32 | 1 | A single specific address |

**You don't need deep subnetting math yet** — just recognize `/24` = "a normal-sized local network" when you see it later in cloud VPC setups.

---

## 5. DNS (Domain Name System)

**Real-world analogy:** DNS is the internet's phonebook. Humans remember names (`google.com`), computers need numbers (IP addresses). DNS translates one into the other.

**Flow:** you type `google.com` → your computer asks a DNS server "what's the IP for this?" → DNS replies with an IP → your browser connects to that IP.

```bash
# Look up a domain's IP (useful troubleshooting commands)
nslookup google.com
dig google.com
```

**Exam tip:** DNS uses **port 53**.

---

## 6. Ports & Common Services

A port is like an apartment number inside a building (the IP address is the building). One IP address can run many services, each on its own port.

| Port | Service | Notes |
|---|---|---|
| 20/21 | FTP | File transfer (older, less secure) |
| 22 | SSH | Secure remote login |
| 25 | SMTP | Sending email |
| 53 | DNS | Domain name lookups |
| 67/68 | DHCP | Automatic IP assignment |
| 80 | HTTP | Unencrypted web traffic |
| 443 | HTTPS | Encrypted web traffic |
| 3306 | MySQL | Database default port |
| 5432 | PostgreSQL | Database default port |

**Mnemonic for the big 3:** "**22** to log in, **80** for open web, **443** for a **4-4-3**-lock" (443 = the secure one).

**Check what's listening on your machine:**
```bash
ss -tuln
```

---

## 7. TCP vs UDP

Both are "Transport layer" ways of sending data — the difference is reliability vs. speed.

| | TCP | UDP |
|---|---|---|
| Reliability | Guarantees delivery, resends lost data | No guarantee — "fire and forget" |
| Order | Keeps data in order | No ordering |
| Speed | Slower (overhead for reliability) | Faster |
| Real-world use | Web browsing, email, file transfer | Video calls, live streaming, gaming |
| Analogy | Registered mail (confirmed delivery) | Postcard (send and hope) |

**Exam tip:** if the question mentions "reliable" or "guaranteed delivery" → **TCP**. If it mentions "speed" or "real-time" → **UDP**.

---

## 8. HTTP vs HTTPS

- **HTTP** (port 80) — data sent in plain text. Anyone snooping the network can read it.
- **HTTPS** (port 443) — HTTP + encryption (TLS/SSL). Data is scrambled in transit so only sender/receiver can read it.

**Real-world example:** typing a password into an HTTP site is like shouting it across a room. HTTPS is like whispering it in a language only the recipient understands.

**Exam tip:** the "S" in HTTPS = **Secure** = **encrypted using TLS/SSL**.

---

## 9. DHCP (Dynamic Host Configuration Protocol)

Automatically hands out IP addresses to devices when they join a network — so you don't have to manually type one in on every phone/laptop that connects to Wi-Fi.

**Real-world analogy:** like checking into a hotel — the front desk (DHCP server) assigns you a room number (IP address) for as long as you're staying, and it can hand that same number to someone else after you leave.

---

## 10. NAT (Network Address Translation)

Lets many devices with private IPs share one public IP to reach the internet. Your router does this constantly and invisibly.

**Real-world analogy:** like an office's single main phone number, with an internal switchboard operator routing calls to the right desk extension. The outside world only ever sees the main number.

---

## 11. Router vs Switch vs Gateway

| Device | What it does |
|---|---|
| Switch | Connects devices *within* the same local network |
| Router | Connects *different* networks together (e.g., your home network ↔ the internet) |
| Gateway | The router acts as the "gateway" — the exit point out of your local network |

---

## 12. Firewalls

A firewall is a filter that decides what network traffic is allowed in/out, based on rules (by port, IP, protocol).

**Real-world analogy:** a security guard at a building entrance, checking IDs (rules) before letting anyone in or out.

**Ubuntu's basic firewall tool:**
```bash
sudo ufw status
sudo ufw allow 22    # allow SSH traffic
sudo ufw enable
```

---

## 13. Networking Troubleshooting Commands (recap)

Full explanations are in `linux-commands.md` — quick recap here for networking-specific triage:

```bash
ip a                     # what's my IP / network interfaces?
ping -c 4 8.8.8.8        # can I reach the internet at all?
ping -c 4 google.com     # is it a DNS problem or connectivity problem?
ss -tuln                 # what ports are open/listening locally?
curl -I https://site.com # can I reach a specific website? (headers only)
nslookup google.com      # is DNS resolving correctly?
```

**Simple troubleshooting order:**
1. `ip a` — do I even have an IP address?
2. `ping 8.8.8.8` — can I reach the internet by number (rules out DNS)?
3. `ping google.com` — can I reach it by name? (if step 2 works but this fails → DNS problem)
4. `curl` the actual site/service you're trying to reach.

---

## Quick Exam Cheat Sheet

| Question type | Answer to reach for |
|---|---|
| "Which layer handles IP addressing?" | Network layer (Layer 3) |
| "Which protocol is reliable?" | TCP |
| "Which protocol is faster / used for streaming?" | UDP |
| "What translates domain names to IPs?" | DNS (port 53) |
| "What assigns IPs automatically?" | DHCP |
| "What lets private IPs share one public IP?" | NAT |
| "What port is HTTPS?" | 443 |
| "What port is SSH?" | 22 |
| "How many layers does OSI have?" | 7 |
| "How many layers does TCP/IP have?" | 4 |
