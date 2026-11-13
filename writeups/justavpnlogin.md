# Write-up: Just a VPN Login

Platform: TryHackMe.

Room Link: https://tryhackme.com/room/justavpnlogin

Just a VPN Login is a SOC investigation scenario challenge on TryHackMe. This document serves as my write-up for this challenge. No questions and almost no answers that are given in the room are present in this write-up.

## Introduction and Scenario

**PART 1: "Unusual Login"**

In this challenge, we act as an SOC analyst on shift. We are greeted by an internal alert on the SOC dashboard [^1] titled:

`Unusual VPN login of susan.martin@probablyfine.thm from 37[.]19[.]201[.]132 (Singapore).`

Aside from the alert title, the SOC handover note contains the following information: "Susan from Marketing is in Singapore, attending a security vendor conference."

Our first objective is to verify the IP mentioned in the alert title using the provided threat intel platform TryDetectThis [^2]. We will need to gather more information and determine the threat level.

**PART 2: "Security Check Tool"**

Next, we learn that our teammates have reached out to Susan, and she confirmed she did not log in to the company VPN. She also mentioned that while using a public Wi-Fi hotspot at a cafe, she was suddenly prompted to install a "security check" tool, which she did. The host telemetry revealed a suspicious binary with the following hash:

`b8e02f2bc0ffb42e8cf28e37a26d8d825f639079bf6d948f8debab6440ee5630`

Our second objective is to investigate this binary, utilizing TryDetectThis. We will need to figure out what this binary exactly does.

## Initial Information Triage and Analysis

I will start this challenge by gathering the key details from the introduction in a compact block.

```
User: Susan (Marketing)
User Email: susan.martin@probablyfine.thm
User Location: Singapore

Alert Trigger: Unusual login to the company VPN
Source IP: 37[.]19[.]201[.]132
Source Location: Singapore

Binary Hash: b8e02f2bc0ffb42e8cf28e37a26d8d825f639079bf6d948f8debab6440ee5630
```

There is no explicit timeline given for this scenario, but I presume that this scenario unfolds in two parts.

The first part starts with only the internal alert (of which we only get the alert title + SOC handover note). My initial thought is that the login was flagged as unusual because Singapore is not a usual location for Susan to log in. Furthermore, the SOC handover note tells us that Susan is attending a conference in Singapore, so the login appers to be legitimate at first.

However, as SOC analysts, we never operate on presumptions - only on facts. Therefore, we must verify the login using TryDetectThis.

The second part of the introduction gives away the main conclusion of the first part of this scenario - after our verification, we will come to realise that this login IP looks more suspicious than we initially thought. We will inform our teammates about our findings, and they will reach out to Susan to confirm whether she logged in or not.

In the following investigation process, I will act out this hypothetical timeline as the analyst. I will first conduct the IP address analysis and prepare the initial findings for my teammates. Essentially, the findings should clearly communicate the need for further investigation, including reaching out to Susan. Then Susan will be contacted, and we will continue our investigation with the new information revealed.

## Threat Intelligence Investigation

We will start the investigation by running the IP address of the unusual login against TryDetectThis. Right away we see that **0**/93 vendors flagged this IP address as malicious. Other noticeable feature from the report is the assigned "VPN" tag [^3] [^4] for this IP address.

The File Relations section of the report further indicates the association of the source IP address to VPN infrastructure. Multiple Android applications with names indicative of providing VPN services were detected communicating with the source IP address:

```
com.supervpn.vpn.free.proxy.apk
vpn-proxy-2-0-2.apk
com.free.vpn.proxy.master.app_141_apps.evozi.com.apk
com.free.vpn.proxy.master.app.apk
VPN Proxy Speed - Super VPN.apk
Proxy Master 1.4.0.apk
```

The combined VPN evidence could suggest that an adversary got access to Susan's credentials and has logged into our company's network, using a VPN service to conceal their real IP address. Alternatively, it could be Susan that logged in and the source IP address has nothing to do with a VPN service. The VPN association evidence we gathered is not proof that the source IP address is used as a VPN exit.

Nevertheless, it is enough to raise concern about the legitimacy of the login. Let's inform our team about our findings:

```
Subject: Suspicious Login to Company VPN

Dear Team,

After investigating the source IP address of the following alert:

Unusual VPN login of susan.martin@probablyfine.thm from 37[.]19[.]201[.]132 (Singapore).

Time of detection: {DATE AND TIME}

I found several pieces of evidence that suggest this source IP address is associated with external VPN infrastructure, likely used as a VPN exit IP address. One is the assigned "VPN" tag by our threat intel platform, the other is multiple Android VPN apps contacting this IP address.

While nothing is confirmed, I am concerned about the possibility of an adversary logging into our company's network using Susan's credentials, attempting to conceal their real IP address using a VPN service.

I propose to contact Susan as soon as possible to confirm if she remembers logging in close to the time of detection. As well as briefly ask her if she recalls anything unusual or suspicious happening on her work machine since she arrived to Singapore.

Regards,
Asman.
```

I leave the alert "In Progress" until I get the confirmation from my team. But as we know, the situation escalates, as Susan denies logging in to the company VPN. Furthermore, she recalls an unusual incident on her machine - a sudden popup to install a "security check" tool while working on a public Wi-Fi, which she allegedly installed. Our team asks us to continue our investigation and provides us the binary's hash from Susan's host:

```
b8e02f2bc0ffb42e8cf28e37a26d8d825f639079bf6d948f8debab6440ee5630
```

We will enter this hash in TryDetectThis. The file hash report indicates that 57 out of 76 aggregated security vendors flagged this file as malicious. Several tags are reported by the platform: `CHECKS-USER-INPUT`, `PEEXE`, `IDLE`. The Vendor Analysis as well as the Yara Rule detection [^5] indicate that this binary is likely the Lumma Stealer [^6] malware.

Two of the assigned tags make sense for an infostealing malware - one of the ways to steal information is to record user input, thus `CHECKS-USER-INPUT`, and `PEEXE` refers to the Portable Executable format of this file. There is no need to attempt to interpret the `IDLE` tag.

There is one more suspicious part of the file hash report. Multiple contacted domains were recorded for this file, and some of them are presented with numerous malicious detections (16, 17, 13 out of 93). It is probable that this malware was detected contacting domains that are part of a bigger malicious infrastructure. We can test this hypothesis by running the malicious detected domains against TryDetectThis, to see if our database contains useful information about them.

While the two out of three domains did not reveal anything significant, one of the domains potentially reveals the bigger picture we were looking for. The HTTPS certificate information of this domain reveals the Subject Alternative Name [^7] extension which specifies numerous domain names for which the certificate can be used.

Attackers sometimes operate many domains as part of the same malicious infrastructure. Instead of issuing a separate HTTPS certificate for every domain, the attacker might configure one certificate covering all of the domains. This technique, where we discovered one malicious domain, inspected its certificate, and identified other domains potentially associated with the same infrastructure, is called **SSL/TLS certificate pivoting**. [^8]

## Findings and Risk Assessment

We presume that the suspicious file in question was in fact installed, by Susan on her host. This file's hash was ran against TryDetectThis. The file hash report surfaced multiple indicators of this file being an infostealing malware called Lumma Stealer.

An unusual login to company's network was detected by our SOC dashboard. The source IP address was ran against TryDetectThis, revealing multiple indicators of it being associated with VPN infrastructure, possibly being used as a VPN exit IP address. Susan further confirmed the illegitimacy of the source IP address, as she denied logging in herself.

A separate Lumma Stealer threat intelligence report by Insikt Group, available within the file hash report on TryDetectThis, outlines that the usage of VPN services for identity concealment is a common behavior pattern for Lumma affiliates.

According to the report, Lumma affiliates operate within a vast interconnected information-stealing ecosystem. It is probable that we have come across a part of that network as we discovered the numerous domain names linked to the malicious domain that was in contact with our investigated executable.

If Susan denies logging in to the company VPN near the time of login detection, then someone else logged in using Susan's credentials. Combined with the infostealing malware present on Susan's machine, it is reasonable to assume that Susan's credentials were stolen by the installed malware. It is also reasonable to assume that the source IP address does not represent the real party that logged in using Susan's credentials, but a VPN service. [^9]

If we are using a threat level assessment system where there are four levels from Low to Critical, then this threat deserves a **Medium** to **High** rating, probably leaning towards High. We have strong evidence of an unauthorized login to our company VPN. We also have sufficient evidence of infostealing malware being present on an employee's machine. However, if the access of employees is properly scoped and zero-trust is properly implemented, then just the unauthorized login of a regular Marketing employee alone might be insufficient to cause significant harm to the company.

## Recommended Incident Response

Rotate Susan's credentials. After the rotation, terminate Susan's saved/active session, so the next log in initiates a fresh session. Run a deep scan on her machine to get rid of any installed malware.

Investigate the logs associated with Susan's session in the time period between the detected unauthorized login and when we terminated her session, to understand the activity of the adversary on Susan's account. Destroyed or altered contents could be attempted to be restored from backups. Any sensitive data that was accessed by the adversary should be considered no longer confidential. Newly created contents should be cleaned up.

After the appropriate incident response steps are taken, Susan can resume normal work with the new credentials.

An employee training should be planned raising the basic cyber security awareness. Then, I would propose enforcing two factor authentication to access the company network. This way, even if the adversary gets hold of employee credentials, it would be insufficient to log in. Employee machines should be running proper AV software, particularly with access to the TryDetectThis database and automatic quarantine feature for known threats.

## Lessons Learned

In this challenge, I practiced investigating a basic SOC scenario with limited initial knowledge of the situation. I gathered relevant information from the reports on TryDetectThis, to first propose to my team that the unusual login alert might be suspicious, and then to understand that Susan likely installed malware on her machine. Finally, piecing together evidence that I gathered, I proposed my assumption of what might have happened.

This process taught me the structured approach to SOC investigation in general. First, we produce the initial analysis before running any commands or queries, based on the introductory information, to prioritize and plan our work ahead. Then, we use the available tools to work through the investigation, gathering evidence along the way. Gathering evidence should also be a mindful process - we should be focused on gathering the most useful evidence first as sometimes it is enough to gather just enough evidence to proceed further in the investigation. It is important to balance the progression speed and depth in an investigation, as it is important to both gather solid evidence and prevent an ongoing incident as fast as possible. Finally, we conclude the investigation and propose indicent response.

One important idea in particular that I had to keep in mind throughout this investigation, is the idea that a lot of the seen evidence are just indicators, not confirmations. For example, the 0/93 evidence for the source IP address was not proof that the internal alert was benign. Or for example, the YARA rule that detected the Lumma Stealer malware, in fact it only compares some of the bytes in the file contents and does not prove anything. 

Sometimes, collecting all of the evidence together allows us to only make an educated guess. But sometimes, gaining enough confidence in the guess is the objective, to suspect that something malicious is happening and to act on it. In this challenge, we do not have definitive proof that Susan's credentials got stolen, but the gathered evidence gives us enough confidence to propose rotating them regardless.

I also got introduced to multiple security concepts along the way, like why a threat intelligence platform assigns a VPN tag to an IP address, how a YARA rule works (though just on a surface level), and the SSL/TLS certificate pivoting technique to discover a potential network of related domains.

## References

TryHackMe room and TryDetectThis platform access: https://tryhackme.com/room/justavpnlogin

A small Python script I wrote to count the number of SAN extension domains: [../scripts/justavpnlogin-countsan.py](../scripts/justavpnlogin-countsan.py)

VPN Tag possible explanation: https://chatgpt.com/s/t_6af71cd3f2b081918c9a733b19573676

What is a SAN?: https://www.entrust.com/blog/2019/03/what-is-a-san-and-how-is-it-used

SSL/TLS certificate pivoting: https://gopivot.ing/artifacts/tls-certificate

Lumma Stealer: https://www.huntress.com/threat-library/malware/lumma-stealer

Lumma affiliates report (also available through the TryDetectThis platform): https://www.recordedfuture.com/research/behind-the-curtain-how-lumma-affiliates-operate

[^1]: We do not have access to the actual **SOC dashboard** in this challenge, all of the initial details are gathered from the scenario introduction text.

[^2]: **TryDetectThis** is a threat intelligence database to check the reputation and other details of IP addresses, domains, and file hashes.

[^3]: When a threat intelligence platform assigns a **VPN tag** to an IP address, it generally means the platform has identified that IP as being associated with VPN infrastructure. More specifically, it often means the IP address is used as a VPN exit IP address.

[^4]: It is also worth clarifying the two mentions of the word "VPN" so far. The first refers to our company's VPN that employees log into for work. The second refers to the VPN tag assigned to the source IP address by TryDetectThis. The VPN infrastructure that the source IP address is potentially associated with has (almost certainly) nothing to do with our company's VPN infrastructure.

[^5]: The Yara Rule condition that triggered the detection is available within a public GitHub repository. Essentially, it checks whether a file starts with two bytes indicative of a Windows executable file, and if anywhere within a file there are certain string patters - indicative patterns of the Lumma Stealer malware. The Yara Rule condition only proves that a certain type of string was found within file's contents.

[^6]: **Lumma Stealer** is an infostealer malware as a service program developed for Microsoft Windows.

[^7]: What is Subject Alternative Name (SAN)? An HTTPS certificate establishes a cryptographic binding between a public key and one or more domain names, with the binding authenticated by a certificate authority (CA). The **Subject Alternative Name (SAN)** extension specifies the domain names for which the certificate can be used.

[^8]: The shared certificate is evidence of a possible infrastructure relationship, but does not independently establish that every listed domain is malicious, nor does it establish existence of a malicious campaign.

[^9]: These assumptions do not represent confirmed events, only assumptions of what might have happened based on the available evidence. We do not have definitive confirmation of whether Lumma Stealer was successfully installed and executed on Susan's machine, or whether any credentials were actually stolen.
