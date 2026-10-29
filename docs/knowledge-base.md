# Fjord Trips · Knowledge base settings (Module 13)

These are the settings used in the Foundry portal (**Knowledge**). Nothing in the app code changes: the app calls `trip-agent` by name, and the agent uses the knowledge base.

| Setting | Value |
|---|---|
| Search resource | `fjordtrips-search` (Foundry IQ / Azure AI Search), resource group `rg-fjordtrips`, Sweden Central, pricing tier **Basic** (billed per hour: delete it when you finish the course) |
| Knowledge base | `fjord-brochure` |
| Description | Official Fjord Trips brochure 2027 |
| Chat completions model | `gpt-5-mini` |
| Retrieval reasoning effort | Low |
| Output mode | Answer synthesis |
| Answer instructions | Answer only from the brochure. Always include prices exactly as written. |
| Retrieval instructions | Search the brochure for trips, prices, dates and policies. |
| Knowledge source | Upload files: `data/brochure.pdf`, source name `brochure-2027`, default embedding model |
| Access | The `fjordtrips` project's managed identity has the **Search Data Index Reader** role on `fjordtrips-search` |
| Agent | Attached to `trip-agent` with **Use in an agent** |

Test questions:
- How much is the Northern Lights Week, and what's the cancellation policy?
- Is breakfast included on the Bergen City Break?
- Do you offer a trip to Iceland? (expected: the brochure doesn't include one)
