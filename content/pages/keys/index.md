---
title: Keys for investors: public key cryptography you can hold
description: A key pair for an investor who wants one, as a demonstration of how public and private keys work, and of how agents send each other secrets.
status: proposed
order: 6
short: Keys for investors
---
# Keys for investors

A key pair for an investor who wants one: a demonstration of how public and private keys work, by using them.

## The proposal

- **Make a key pair in the browser.** The private key stays with you; the public key is what you publish.
- **Receive a secret sealed to you.** A founder, or an agent, seals a document to your public key; only your private key opens it. No password is sent anywhere.
- **See the same thing agents do.** In [agents have an identity now](https://newsroom.sgit.ai/articles/agents-have-an-identity-now.html), every agent session makes a key pair and publishes the public half with its role, so any agent can seal a secret to it. The investor's key is the same idea, held by a person.

## Why it is here

Public key cryptography sounds abstract until you have used it once. A deal room where documents are sealed to each investor's key is the practical form; this is the first step towards it.

## What this does not claim

- **Nothing on this page runs yet.** It is a proposal from [the brief](/about/brief.html). When it is built, it will say which algorithms it uses and where the keys are stored.
