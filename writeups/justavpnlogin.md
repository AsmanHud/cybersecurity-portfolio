# TryHackMe: Just a VPN Login

Platform: TryHackMe.

Room Link: https://tryhackme.com/room/justavpnlogin

Just a VPN Login is a SOC investigation scenario challenge on TryHackMe. This document serves as my write-up for this challenge. Answer values for the questions from the room are excluded.

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

This already raises suspicion {WIP: continue this sentence}

And the final piece of the puzzle - the latest file communication log that was flagged as malicious by 32 out of 76 vendors. TryDetectThis suggests it is a Windows executable with a highly suspicious name "1039ee9692206d53de177c647f073892.virus".

{WIP: continue the write-up}

[^1]: We do not have access to the actual SOC dashboard in this challenge, all of the initial details are gathered from the scenario introduction text.

[^2]: TryDetectThis is a threat intelligence database to check the reputation and other details of IP addresses, domains, and file hashes.

[^3]: When a threat intelligence platform assigns a **VPN tag** to an IP address, it generally means the platform has identified that IP as being associated with VPN infrastructure. More specifically, it often means the IP address is used as a VPN exit IP address.

[^4]: It is also worth clarifying the two mentions of the word "VPN" so far. The first refers to our company's VPN that employees log into for work. The second refers to the VPN tag assigned to the source IP address by TryDetectThis. The VPN infrastructure that the source IP address is potentially associated with has (almost certainly) nothing to do with our company's VPN infrastructure.
