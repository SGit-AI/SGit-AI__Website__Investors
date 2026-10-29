# investor.sgit.ai: a brief for a website where investors and founders use our tools, not read about them, with the news, contracts as graphs, deal rooms as vaults and sgit as the case study, sgit.ai

> This is an article brief: one idea and one task, and the direction of travel behind them. We are starting to talk to investors, and the challenge with most of what we build is that it has to be experienced to be understood. So the best way to talk to investors is to have them use it, and the place to do that is a website of its own, investor.sgit.ai, for investors and founders together, angel to Series A. It would carry the news from investor circles, tracked from public sources as a graph; startup contracts, cap tables and term sheets as linked graphs with their versions and caveats; a section for founders on how to talk to an investor and what comes next; the funding models from open source to proprietary; deal rooms as vaults, and keys for investors as a demonstration of PKI; RiskMandate's due diligence and de-risking at work; and sgit itself as the case study, its strategy and thinking published as it happens. It would also put back in front of people work that got lost: the GenAI cybersecurity startup evaluation framework I published in March, seven criteria and a meta-criterion scored to forty, which is the first piece of the maturity model I had in mind. Like the PHP newsroom, it would be run by a small team of agents on a schedule, built from the first commit to sgit.ai's rules for a new repository, with CI owning the version. And then I would show it to investors and ask: is this useful, and what would help?

*Source: <https://newsroom.sgit.ai/articles/investor-sgit-ai.html> · sgit.ai v0.7.87 · this file is generated from the same content as the page, so the two cannot drift. Every page on this site has a `.md` twin; internal links below point at them.*

---

[Home](../index.md) / [Articles](index.md) / investor.sgit.ai: a brief for a website where investors and founders use our tools, not read about them, with the news, contracts as graphs, deal rooms as vaults and sgit as the case study

# investor.sgit.ai: a brief for a website where investors and founders use our tools, not read about them, with the news, contracts as graphs, deal rooms as vaults and sgit as the case study

By [Dinis Cruz](https://sgit.ai/about/index.md) · 2026-10-29 · [article v1.0.0](versions/investor-sgit-ai.md) · [newsroom v0.13.130](https://newsroom.sgit.ai/admin/versions.html) · investorsfoundersstartupsbriefvaultspkiriskmandatesgitfundingarticle

***Abstract:** This is an article brief: one idea and one task, and the direction of travel behind them. We are starting to talk to investors, and the challenge with most of what we build is that it has to be experienced to be understood. So the best way to talk to investors is to have them use it, and the place to do that is a website of its own, investor.sgit.ai, for investors and founders together, angel to Series A. It would carry the news from investor circles, tracked from public sources as a graph; startup contracts, cap tables and term sheets as linked graphs with their versions and caveats; a section for founders on how to talk to an investor and what comes next; the funding models from open source to proprietary; deal rooms as vaults, and keys for investors as a demonstration of PKI; RiskMandate's due diligence and de-risking at work; and sgit itself as the case study, its strategy and thinking published as it happens. It would also put back in front of people work that got lost: the GenAI cybersecurity startup evaluation framework I published in March, seven criteria and a meta-criterion scored to forty, which is the first piece of the maturity model I had in mind. Like the PHP newsroom, it would be run by a small team of agents on a schedule, built from the first commit to sgit.ai's rules for a new repository, with CI owning the version. And then I would show it to investors and ask: is this useful, and what would help?*

What investor.sgit.ai would hold, for investors and founders, angel to Series A. A proposal.

## In short

- **This is an article brief.** One idea, one task, and the direction of travel behind them.
- **What we build has to be experienced to be understood.** So investors should use it, not read about it.
- **A website for investors and founders together.** investor.sgit.ai, angel to Series A, running on the tools it describes.
- **Eight sections.** The news, contracts as graphs, founders, an evaluation framework, deal rooms as vaults, keys for investors, sgit as the case study, RiskMandate at work.
- **Work that got lost comes back.** The GenAI cybersecurity startup evaluation framework of March 2026, the first piece of a maturity model.
- **Run by a small team of agents.** On a schedule, like the PHP newsroom's.
- **Built to the house rules from the first commit.** A brief in full, a reality file, CI owning the version, a gate, behaviour policies.
- **Then ask investors.** Is this useful, and what would help?

## Why a website, and why for investors

We are going to start talking to investors, and the challenge is one I keep running into: a lot of what we build needs to be experienced to be understood. A vault that the host cannot read, a read key that works from any static page, an agent with its own key that another agent can send a secret to, a behaviour policy that reads as an insurance policy: each sounds abstract until you open it. So I think the best way to talk to investors is to have them use our own technology, on the problems they actually have.

The pieces of the puzzle exist. This newsroom has the articles and the vaults; [where to invest in sgit](where-to-invest-in-sgit.md) put the investor deck in a vault; [legal on demand for startups](legal-on-demand-for-startups.md) built a founder's desk, an investor's desk and a deal room as vaults; the [insuring agents series](insuring-agents-the-whole-story.md) has a calculator anyone can open. What is missing is one place, for investors and founders, where those pieces are the website.

## What it would hold

For now I would merge investors and startups into one site, because most of what helps one helps the other.

1. **The news.** What is going on in investor circles, with the focus on angel and Series A, the early funding. All of it from public sources, tracked as a semantic graph so the dots connect: who invested in whom, which funds move together, which terms are spreading.
2. **Contracts as graphs.** Startup contracts, cap tables and term sheets, shown as documents that hyperlink to each other, with their versions and their caveats. A clause in a term sheet links to the article in the shareholders' agreement it changes, and to the articles on this site that argue about it, such as [sell, don't issue](sell-dont-issue.md) and [the exit is when you sell control](the-exit-is-when-you-sell-control.md).
3. **For founders.** How a founder talks to an investor, what the next steps are, what services are available, and what we can help with, so that a founder's life gets easier. [Start a company](start-a-company.md) and [the controllable founder](the-controllable-founder.md) are the beginning.
4. **The funding models, all of them.** From the open-source model I use, through open core, to fully proprietary, with what each gives the founder and the investor; [open source so you keep it](open-source-so-you-keep-it.md) and [a small slice sets the price](a-small-slice-sets-the-price.md) already cover parts.
5. **An evaluation framework for security startups,** below.
6. **Deal rooms as vaults.** How information moves between an investor and a startup, and all the overhead around it. Vaults suit this well, especially connected to an agent: give a deal room its own workspace, email and team accounts, and keep everything in its vault, where it is managed and protected.
7. **Keys for investors.** A key pair for an investor who wants one, as a demonstration of how public and private keys work, and of how agents can send each other secrets, as [agents have an identity now](agents-have-an-identity-now.md) describes.
8. **sgit as the case study, and RiskMandate at work.** I did this before for The Cyber Boardroom, in a repository where I published strategy, marketing and thinking as it happened. The same for sgit: why sgit, why now, why invest in it, the follow-up to [where to invest in sgit](where-to-invest-in-sgit.md). Not the amount being raised, for now, but everything else, captured as it evolves. Beside it, RiskMandate and vaults solving problems founders and investors have: analysing startups, gathering material and research, market analysis, due diligence and de-risking, with the vaults that show them running.

## Work that got lost: the evaluation framework

In March I published a framework for evaluating GenAI cybersecurity startups, and it is a good example of the kind of thing we publish that gets lost. It is on [notebook-lm.sgit.ai](https://notebook-lm.sgit.ai/), as an infographic, a slide deck and its source. I had remembered it as a maturity model; it is a scored framework, which is the first piece of one.

The GenAI cybersecurity startup evaluation framework: seven criteria and a meta-criterion, scored to 40.

Its thesis is that "many GenAI cybersecurity startups are solving the wrong problem, or solving the right problem in a way that doesn't survive the next model improvement." It scores seven criteria from 1 to 5, structural against temporary, unit value, inline risk, business context, model survivability, open source and deployment sovereignty, and a meta-criterion on the architecture: models inline as the execution engine, or agentic development with a deterministic runtime. The total, out of 40, falls in a band from "35-40: Rare" to "8-13: Avoid". For investors, it names business context and model survivability as "the strongest predictors of long-term value".

On investor.sgit.ai it would be something to push and to map: applied to real startups, in public, with the evidence for each score in a vault, and grown into a maturity model with levels, which it does not have yet. It leaves team, traction and financials out by design, and the site should say so.

## Run by agents, fed by the newsroom

The site would be agentic, with an agent schedule, like [the PHP newsroom](https://php.oct.2026.newsroom.sgit.ai/), which runs with two people and nineteen agents and roles. It need not be that large, but it needs the same workflow: a conductor that hands out the work, a journalist that writes, a researcher that reads the sources, security and observability, each with its own key, published with its role, and an append lane for messages and requests.

I am in two minds about one thing: who makes the news feeds. The newsroom already runs the workflow, its wires, a public vault per wire that agents write and pages read. So one option is that the newsroom runs an investor wire and investor.sgit.ai consumes it; the other is that the site's own team does it. My inclination is the first, because it shows the point of vaults: one team writes, another site reads, and the vault is the contract between them. Reading data from the other newsrooms' vaults is a good demonstration of sgit in itself.

## Built to the house rules from the first commit

New agents tend to miss the guidance on how to start a new repository, so the brief should say it plainly. sgit.ai's [guidance for every repository](https://sgit.ai/docs/guidance/repositories.md) sets the start: the brief published in full, a reality file, where "a feature that is not in the reality file does not exist", a corrections file, a gate that fails the build, tests against real things, a review folder, roles and a board as files, `.md` twins and an `llms.txt`, and "Read keys may be published; vault keys never." The agents run under a behaviour policy.

The latest rule matters most for a site several agents will push to: CI owns the version. The pipeline picks every number, the last one on `dev` and the middle one on `main`, and no agent ever works out the next number itself, because that causes conflicts; [CI owns the version](ci-owns-the-version.md) explains why. And the site should point to the sites that hold the house standards: [coding.sgit.ai](https://coding.sgit.ai/) for the code, [nfrs.sgit.ai](https://nfrs.sgit.ai/) for the non-functional requirements, and [ux.sgit.ai](https://ux.sgit.ai/), which measures the user experience across the sgit.ai sites.

## Then ask investors

My angle is simple. Once a first version runs, I would like to email and reach out to a lot of investors and ask: what do you think of this? Do you find it useful? What would help? The answers decide what the site becomes, and every answer goes on the record, like everything else here.

## What this does not claim

- **None of it is built.** This is a brief; the site, its team and its sections are proposals.
- **The evaluation framework is not a maturity model.** It scores; the levels are still to design, and it does not cover team, traction or financials.
- **The news section needs care with sources and names.** Public sources only, dated and linked, and no private person named.
- **The Cyber Boardroom repository is described from memory.** Its link is to be added.
- **The amount being raised for sgit is not published.** By choice, for now.

If you invest at angel or Series A and would tell us what would help, write to [agent@riskmandate.ai](mailto:agent@riskmandate.ai).

## Where this comes from

Two voice memos of mine on 28 October 2026, kept word for word in this site's repository under `admin/notes/2026-10-28__investor-sgit-ai/`, written by this site's agent in the voice of this site. The argument and the editorial responsibility are mine. The evaluation framework, the PHP newsroom's team and sgit.ai's guidance for a new repository were read on 29 October 2026 by a research agent of this site, from their own pages: [notebook-lm.sgit.ai](https://notebook-lm.sgit.ai/) (the framework's source, v1.0, March 2026), [the PHP newsroom](https://php.oct.2026.newsroom.sgit.ai/) and [sgit.ai's repository guidance](https://sgit.ai/docs/guidance/repositories.md). The build brief for the agent that would make the site is `admin/notes/2026-10-29__brief__investor-sgit-ai.md` in this site's repository.

## Threads

Startups & strategyVaults & method[This article as a graph →](graphs.md#investor-sgit-ai)

### Builds on

- [Where to invest in sgit: the tool, a hub for vaults, or open core, with the history of developer platforms, the evidence of use, three business plans, and the investor deck as a vault](where-to-invest-in-sgit.md) Where investment in sgit should go, from the history of developer platforms, with the deck as a vault.
- [Legal on demand for startups: agent teams that do the reading, lawyers who sign, and a meter instead of a retainer, with three vaults that show the founder's desk, the investor's desk and the deal room](legal-on-demand-for-startups.md) Legal services that scale: agent teams do the reading, lawyers sign, a meter instead of a retainer, and three vaults with real signatures.
- [Insuring agents, the whole story: five articles and three vaults on one idea, that an agent's behaviour policy can be read as an insurance policy, priced row by row and backed by capital](insuring-agents-the-whole-story.md) The five articles on insuring agents in one place, and the three vaults where the ideas run: the simulation, the calculator and AIUC-1.
- [Sell, don't issue: a funding model for founders who have already won, where the investor buys the founder's shares, the founder lends the company what it needs, and open source keeps everyone honest](sell-dont-issue.md) For founders who have already won: the investor buys the founder's shares, the founder lends the company what it needs, and open source keeps everyone honest.
- [The exit is when you sell control: why a founder should leave the day someone else is calling the shots, and why to negotiate that day at the start, the Mourinho clause](the-exit-is-when-you-sell-control.md) A founder's exit is the day someone else buys control, which can come long before the shares go. Leave then, and agree the terms at the start.
- [Start a company: the UK, where it takes an afternoon, Portugal, where I learned the hard way, and Lithuania, where I would like to go next](start-a-company.md) Start a company once there is revenue: the UK in an afternoon, Portugal's monthly accountant learned the hard way, and Lithuania's e-residency next.
- [The controllable founder: why investors pick one founder over another who looks just as good, and what record labels taught us about who the commodity is](the-controllable-founder.md) Why investors pick one founder over another who looks just as good: coachability, contracts that move control, and who the commodity is.
- [Open source what you build, even while you are employed: nobody copies it, and it is the only way you get to keep using it](open-source-so-you-keep-it.md) Nobody copies your open source ideas; the real advantage is that you keep using your own work from job to job, and a rough public history protects you.
- [A small slice sets the price: what the 2026 mega-listings actually sold, how much of each company changed hands, and what founders should take from it](a-small-slice-sets-the-price.md) The 2026 mega-listings priced trillion-dollar companies by selling a few per cent of them. What was sold, what it raised, and the founder's lesson.
- [Agents have an identity now: a key pair made in every session, published with its role, so any agent can seal a secret to it, and the piece the cloud providers could add](agents-have-an-identity-now.md) A key pair made in every agent session, published with its role in a repository, so any agent can seal a secret to it; what the clouds could add.
- [CI owns the version: the release scheme I wrote for OSBot-Utils in 2023, now on every site we run, and the technical debt that showed us why](ci-owns-the-version.md) The pipeline, not whoever pushes, picks the release number: a 2023 scheme now on every site we run.

[All articles](index.md) · [All graphs](graphs.md)

Article No. 322 · [start a reading list with it](https://newsroom.sgit.ai/for/make.html#r=322)

**Posting this article on LinkedIn?** The cover is [investor-sgit-ai.jpg](banners/investor-sgit-ai.jpg) (1920×1080, title and key ideas on it). Upload it as the article cover, paste the title, then select and copy the body from this page.

**Want the next issue by email.** One issue a week or so: what was published, what it adds up to, and what is worth your time. [Subscribe to the SGit Newsroom →](../subscribe/index.md)

[← All articles](index.md)


---

*[Site index for agents](../llms.txt) · [HTML version](https://newsroom.sgit.ai/articles/investor-sgit-ai.html)*
