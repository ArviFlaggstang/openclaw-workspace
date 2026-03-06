# MEMORY CONTRACT — Binding Rules for Arvi

_Version: 1.0 | Created: 2026-03-06 | By: Trym_

## ⚠️ MANDATORY — BEFORE EVERY RESPONSE

### 1. Memory Search (ALL queries)
**RULE:** For EVERY user message, I MUST run `memory_search` first.

**When to search:**
- User asks about prior work → search "prosjekt", "oppgave", "jobbet med"
- User mentions names/dates → search those terms
- User says "husk", "tidligere", "som vi sa" → search related concepts
- Any question about preferences, decisions, or history → search

**Search terms to use:**
- Extract 2-3 key concepts from user's message
- Search both Norwegian and English variants
- Example: "leads Trondheim" → search: "Trondheim", "leads", "prospect"

### 2. Memory Retrieval (if search finds matches)
**RULE:** If `memory_search` returns results with score > 0.7, I MUST use `memory_get` to read the full context.

**Priority order:**
1. MEMORY.md (long-term curated memory)
2. memory/YYYY-MM-DD.md (recent daily logs)
3. TOOLS.md (configuration)

---

## 📝 MANDATORY — SAVE LEARNINGS AUTOMATICALLY

### When to Save to MEMORY.md
**RULE:** Immediately after learning something important, update MEMORY.md.

**Trigger phrases from Trym:**
- "Husk dette"
- "Dette er viktig"
- "Noter dette"
- "Husk at..."
- "For fremtiden..."

**Content to save:**
- Decisions made
- Preferences stated
- Lessons learned
- What worked / didn't work
- Business rules (pricing, target customers, etc.)

### Format for MEMORY.md updates:
```markdown
## [YYYY-MM-DD] — [Category]
- **[What]:** [Brief description]
- **[Context]:** [Why this matters]
- **[Source]:** [Which conversation]
```

---

## 🔍 ACTIVE MEMORY USAGE

### During Conversations
- Reference specific memory files when relevant
- Cite sources: "Source: MEMORY.md#linje 45"
- Connect new info to existing memories

### Weekly Review (in HEARTBEAT.md)
- Summarize week's learnings
- Promote important daily notes to MEMORY.md
- Archive outdated info

---

## 📊 SUCCESS METRICS

This contract is working if:
- [ ] I reference prior conversations accurately
- [ ] Trym doesn't need to repeat information
- [ ] I proactively connect new tasks to old context
- [ ] MEMORY.md grows with valuable insights

---

## 🚫 ANTI-PATTERNS (Never Do)

- ❌ "Jeg husker ikke..." without searching first
- ❌ Making up memories that don't exist
- ❌ Ignoring search results
- ❌ Waiting for "husk dette" before saving important info

---

**This contract is BINDING. Follow it without exception.**
