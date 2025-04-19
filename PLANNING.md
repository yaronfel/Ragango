# PLANNING.md - Agno Multi-Agent Prompt Generation System

## 🎯 Project Vision
Create an AI agent orchestration system that transforms general user requests into detailed, production-ready prompts through collaborative work of specialized AI agents.

## 🏗️ Architecture Overview

### System Components
1. **Orchestrator (Agno Core)** - Central coordinator managing agent interactions, memory, and workflow
2. **Agent Framework** - Interface defining agent capabilities, communication protocols, and state management
3. **Knowledge Base** - Internal database of best practices, templates, and technical information
4. **Tool Integration Layer** - API connections to external tools (WebSearch, DBQuery)
5. **Memory Management System** - Shared context preservation across agent interactions
6. **Output Formatter** - Standardizes final prompt deliverables

### Agent Team Structure
- **Team Lead** - Coordinates workflow, clarifies goals, delegates tasks
- **Internet Researcher** - Gathers external information via WebSearch
- **Info Tagger & Structurer** - Organizes raw data into logical categories
- **PRD Writer** - Transforms structured information into product requirements
- **Final Prompt Crafter** - Produces the final, polished prompt artifact

## 🛠️ Tech Stack & Tools

### Core Technologies
- **Language Model**: Foundation for all agents (utilizing specialized system prompts)
- **Memory System**: Persistent storage of conversation history and artifacts
- **Knowledge Retrieval**: Database of domain knowledge, templates, and best practices

### External Tools
- **WebSearch**: Real-time internet information retrieval
- **DBQuery**: Internal knowledge base access
- **Markdown Renderer**: Format final output as structured markdown

## 🔄 Workflow Process
1. **Input Processing** - Parse user request and identify core project elements
2. **Research Phase** - Gather relevant information from internet and internal sources
3. **Information Organization** - Structure and categorize gathered information
4. **Requirement Development** - Create product requirement draft based on structured info
5. **Prompt Synthesis** - Convert all previous outputs into comprehensive final prompt
6. **Delivery** - Format and return the completed prompt to the user

## 📏 Constraints & Guardrails
- Each agent must operate within its defined role and responsibilities
- Maintain professional, collaborative tone in all inter-agent communications
- Ensure final prompt contains all required sections for production readiness
- Validate that output addresses the user's original intent fully
- Provide proper attribution for external information sources

## 🔍 Evaluation Criteria
- **Comprehensiveness**: Covers all aspects needed for implementation
- **Clarity**: Provides unambiguous direction
- **Actionability**: Ready for direct use by an implementing system
- **Relevance**: Addresses the specific user need
- **Structure**: Well-organized and follows consistent format

## 📈 Future Expansion Possibilities
- Add specialized agents for specific domains (e.g., E-commerce Expert, SaaS Specialist)
- Implement feedback loop to improve prompts based on implementation results
- Create template library of successful prompts for similar requests
- Develop visualization tools for inter-agent communication flows