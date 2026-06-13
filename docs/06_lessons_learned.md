# Lessons Learned

This is the most important file in the documentation system.

Purpose:

Transform product thinking into reusable lessons.

This file is the source of truth for:

```text
Raw Thinking
↓
Lessons Learned
↓
Build In Public
↓
LinkedIn
Blog
Case Studies
Interview Stories
```

The founder should only need to maintain this file.

`docs/05_build_in_public.md` is generated from this file by:

```bash
python3 scripts/process_lessons.py
```

## Lesson Template

```text
---
Date:

Original Assumption:

New Insight:

Evidence:

Why It Matters:

Product Decision:

LinkedIn Angle:

---
```

## Lessons

---
Date:

2026-06-13

Original Assumption:

AI is the product.

New Insight:

AI is not the product. AI is the tool. The product is business value for salon owners.

Evidence:

Founder observations and early product thinking showed that salon owners care more about customer flow, revenue, promotions, and saving time than the AI system itself.

Why It Matters:

The owner does not care whether the system is technically impressive. She cares whether it helps her get more customers, understand her business, save time, and make better decisions.

Product Decision:

Do not sell AI. Sell business outcomes.

LinkedIn Angle:

Customers do not buy AI. Customers buy outcomes.

---
Date:

2026-06-13

Original Assumption:

The first product should be an AI knowledge base.

New Insight:

The first pain point is not knowledge retrieval. The first pain point is daily business recording and structured data collection.

Evidence:

Customer discovery and founder observations suggest that small salon owners first need help turning daily business activity into usable data.

Why It Matters:

Without daily data, the system cannot produce useful reports, advice, or marketing recommendations.

Product Decision:

Build Business Recorder Agent first.

LinkedIn Angle:

Before building AI agents, understand what the user actually does every day.

---
Date:

2026-06-13

Original Assumption:

Small salon owners need dashboards and CRM.

New Insight:

They often do not want to learn software. They want to speak naturally and get useful outputs.

Evidence:

Target users prefer WeChat and voice communication, and do not have a strong habit of using Excel or structured CRM systems.

Why It Matters:

For this user, a powerful dashboard can still fail if it requires a new habit. Conversation fits the way the owner already works through WeChat and voice messages.

Product Decision:

Use a chat-first and voice-first interaction model.

LinkedIn Angle:

For non-technical users, the best interface may not be a dashboard. It may be a conversation.

---
Date:

2026-06-13

Original Assumption:

More features make the product better.

New Insight:

The MVP should focus on one real salon and one daily workflow.

Evidence:

The product is being built for one real salon first, where the most important workflow is daily recording.

Why It Matters:

The first version needs to prove that one real owner can use it in daily operations. Extra features can hide whether the core behavior actually works.

Product Decision:

Start with one salon, one workflow, and one agent.

LinkedIn Angle:

The first version of an AI product should not be impressive. It should be usable.

---
Date:

2026-06-13

Original Assumption:

Beauty salons need an AI knowledge base.

New Insight:

Salon owners do not care about AI knowledge bases. They care about customers, revenue, promotions, and saving time.

Evidence:

Founder discussions and industry observations.

Why It Matters:

Technology is not the product. Business outcomes are the product.

Product Decision:

Do not prioritize RAG. Prioritize Business Recorder Agent.

LinkedIn Angle:

Customers do not buy AI. Customers buy outcomes.

---
Date:

2026-06-13

Original Assumption:

The product should start with advanced AI features.

New Insight:

The product should start with the user's daily behavior.

Evidence:

Owners record customers, revenue, and business performance every day. They do not query knowledge bases every day.

Why It Matters:

The product should fit an existing habit before asking the user to adopt a new workflow.

Product Decision:

Build Voice Input -> Structured Data -> Daily Report before everything else.

LinkedIn Angle:

Build around habits, not technology.

---
Date:

2026-06-13

Original Assumption:

Salon owners should learn digital tools.

New Insight:

Salon owners do not want to learn software.

Evidence:

Excel and CRM adoption is extremely low. Many owners do not even have a habit of structured data recording.

Why It Matters:

If the product requires the owner to become a software user first, the product will likely fail before it creates value.

Product Decision:

Use chat-first interaction and voice-first interaction instead of traditional dashboards.

LinkedIn Angle:

The best interface may be a conversation.

---
Date:

2026-06-13

Original Assumption:

AI architecture should come first.

New Insight:

Customer discovery should come first.

Evidence:

Real user discussions created more product clarity than any technical research.

Why It Matters:

Architecture should serve the user's real workflow, not the builder's excitement about technical design.

Product Decision:

Customer Discovery -> Product Design -> Architecture.

LinkedIn Angle:

Customer discovery before architecture.

---
Date:

2026-06-13

Original Assumption:

I originally thought I was building an AI knowledge base for beauty salons. Most of my attention was on RAG, LangGraph, agents, and knowledge retrieval.

New Insight:

Real salon owners do not care about AI. They care about customers, revenue, promotions, and business growth.

Evidence:

Founder discussions and product thinking created the first major pivot: from Beauty Industry AI Knowledge Base to 老板娘经营助手.

Why It Matters:

This was the first major product pivot. AI is not the product. AI is the tool. The product is business value.

Product Decision:

Phase 1 should focus on the Business Recorder Agent: Voice/Text Input -> Structured Data -> Database -> Daily Report.

LinkedIn Angle:

AI is not the product. AI is the tool. The product is business value.

---
