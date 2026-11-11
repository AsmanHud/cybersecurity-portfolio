# TryHackMe: Just a VPN Login

Platform: TryHackMe.

Room Link: https://tryhackme.com/room/justavpnlogin

Just a VPN Login is a SOC investigation scenario challenge on TryHackMe. This document serves as my write-up for this challenge. Answer values for the questions from the room are excluded.

## Introduction and Scenario

**PART 1: "Unusual Login"**

In this challenge, we act as an SOC analyst on shift. We are greeted by an internal alert on the SOC dashboard titled:

`Unusual VPN login of susan.martin@probablyfine.thm from 37[.]19[.]201[.]132 (Singapore).`

> We do not have access to the SOC dashboard in this challenge, the details are provided within the introduction.

Aside from the alert title, the SOC handover notes contain the following information: "Susan from Marketing is in Singapore, attending a security vendor conference."

Our first objective is to verify the IP mentioned in the alert title using the provided threat intel platform "TryDetectThis". We will need to gather more information and determine the threat level.

> TryDetectThis is a threat intelligence database to check the reputation and other details of IP addresses, domains, and file hashes.

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

The first part starts with only the internal alert (of which we only get the alert title). My initial thought is that the login was flagged as unusual because Singapore is not a usual location for Susan to log in. Furthermore, the SOC handover note tells us that Susan is attending a conference in Singapore, so the login appers to be legitimate at first.

However, as SOC analysts, we never operate on presumptions - only on facts. Therefore, we must verify the login using TryDetectThis.

The second part of the introduction gives away the main conclusion of the first part of this scenario - after our verification, we will come to realise that this login IP looks more suspicious than we initially thought. We will inform our teammates about our findings, and they will reach out to Susan to confirm whether she logged in or not.

In the following investigation process, I will act out this hypothetical timeline as the analyst. I will first conduct the IP address analysis and prepare the initial findings for my teammates. Essentially, the findings should clearly communicate the need for further investigation, including reaching out to Susan. Then Susan will be contacted, and we will continue our investigation with the new information revealed.

## Threat Intelligence Investigation
