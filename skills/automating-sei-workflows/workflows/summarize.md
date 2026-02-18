# Summarize Process Workflow

Steps for AI-powered summarization of SEI process PDFs.

## Prerequisites
- Extracted PDF (run `extract-pdf` first)
- LLM API access configured

## Steps
1. Extract text from PDF
2. Send text to LLM with prompt focused on 8° BBM relevance
3. Return structured summary (relevant/not relevant, key points, action items)

> **TODO:** Flesh out with PDF parsing library choice and LLM prompt template.
