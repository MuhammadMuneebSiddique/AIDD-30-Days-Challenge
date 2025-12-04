---
name: "meeting-notes-organizer"
description: "Transform messy meeting notes into structured summaries with action items, decisions, and follow-ups. Use when user shares meeting notes or transcripts."
version: "1.0.0"
---

# Meeting Notes Organizer Skill

## When to Use This Skill

- User provides raw meeting notes, bullet points, or a transcript  
- User asks for a meeting summary, key points, or next steps  
- User needs organized output for team communication or documentation  

## How This Skill Works

1. **Identify key discussion areas**: Extract major topics and themes  
2. **Summarize important points**: Convert verbose notes into concise summaries  
3. **List decisions made**: Capture confirmations, approvals, and agreed changes  
4. **Generate action items**: Assign tasks with responsible persons (if mentioned)  
5. **Highlight follow-ups**: List open questions or items needing future attention  

## Output Format

Provide:
- **Meeting Summary**: 3–4 sentence overview  
- **Discussion Topics**: Bullet list of key areas covered  
- **Decisions Made**: Numbered list of approvals/agreements  
- **Action Items**: Task list with owners and deadlines (if available)  
- **Follow-Ups Needed**: Unresolved issues or questions to revisit  

## Example

**Input**: “Here are the notes from our design review meeting…”

**Output**:
- **Meeting Summary**: The design team reviewed the updated homepage layout, discussed mobile responsiveness issues, and aligned on the final color palette. Additional improvements for load time and accessibility were proposed.  
- **Discussion Topics**:  
  - Homepage layout revisions  
  - Mobile optimization challenges  
  - Color palette confirmation  
  - Accessibility updates  
- **Decisions Made**:  
  1. Approved the new homepage header layout  
  2. Finalized the color palette including updated accent color  
- **Action Items**:  
  - Sarah: Optimize mobile grid spacing  
  - Ahmed: Run accessibility audit on revised UI  
  - Lucas: Reduce image load time by compressing hero assets  
- **Follow-Ups Needed**:  
  - Confirm final copy for homepage hero text  
  - Revisit animation timings in next design sync  
