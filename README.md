# DevFlow: The Autonomous AI Engineering Squad

## 1. The Pitch: Why I Built This
In the modern enterprise, software maintenance is a productivity killer. Critical bugs often get buried in Jira backlogs while developers are distracted by low-priority tasks. As a solo developer, I wanted to multiply my output by creating a virtual engineering team.

I didn't want to build another chatbot that simply "explains" code. I built a worker that fixes it.

**DevFlow** is an autonomous multi-agent system that acts as a "AI Engineering Squad." It connects real business requirements (Atlassian Jira) to actual code implementation (GitHub). It doesn't just guess; it uses **Test-Driven Development (TDD)** to verify its own work, keeping the Jira ticket updated with status comments at every stage of the repair process.

## 2. The Solution: A Multi-Agent Architecture
My solution leverages the power of **Google Gemini 2.5** to orchestrate a sequential multi-agent workflow. Unlike standard coding assistants, DevFlow is aware of "Business Priority" and maintains a paper trail in Jira.

The system consists of three distinct agents orchestrated by a Root Manager:

*   **DevOps_Manager_Agent (The Orchestrator):** The root agent that initializes the session, manages memory, and directs the workflow between the sub-agents.
*   **Sprint_Lead_Agent (The Gatekeeper):**
    *   **Role:** Connects to Live Jira.
    *   **Intelligence:** Scans the backlog for Project 'Sales-Dashboard', filters out noise, and identifies the highest priority ticket (e.g., SCRUM-1) based on severity.
    *   **Action:** Assigns the ticket, moves status to "In Progress," and posts an "Investigation Started" comment to notify stakeholders.
*   **Dev_Expert_Agent (The Builder):**
    *   **Role:** Connects to GitHub and the local execution environment.
    *   **Intelligence:** Follows a strict TDD Loop (Clone → Reproduce via Test → Refactor → Verify → Commit → Update Jira).

## 3. Technical Implementation: Key Course Concepts Applied
I demonstrated mastery of the Agentic AI curriculum by applying the following key concepts:

### A. Sequential Multi-Agent System & State Management
I implemented a hierarchical architecture where the `DevOps_Manager_Agent` maintains the state. The Jira Ticket ID of business critical task is programmatically extracted from the Sprint Lead's output and passed as context to the Developer. I utilized `InMemorySessionService` to maintain conversation history and context across the workflow.

### B. Enterprise Deployment (FastAPI & Streamlit)
DevFlow is designed as a scalable microservice, not just a notebook script.
*   **Backend:** The Agent Logic is exposed via **FastAPI**, creating a decoupled REST endpoint (`/api/chat`) that creates agent sessions and handles requests asynchronously.
*   **Frontend:** A "Command Center" UI built with **Streamlit** consumes this API. It provides a professional, immersive dashboard for issuing commands to the squad and receiving structured responses from the agents.

### C. Safety & Governance Layer (The Sentinel)
To address the "Confused Deputy Problem" (where an AI with high-level GitHub permissions is tricked by a malicious user), I implemented a strict **Security Middleware** before the agent execution.
*   **Input Guardrails:** A regex-based validator checks for prompt injection attacks (e.g., "Ignore instructions," "Delete Repo," "rm -rf").
*   **Outcome:** If a malicious command is detected, the API blocks the request immediately, ensuring the agent never receives the dangerous instruction.

### D. Extensive Custom Tooling (Real-World Integration)
Rather than relying on mocks, I built a comprehensive suite of **Custom Python Tools** that give the agents full autonomy over the development lifecycle.

**1. Sprint Lead Tools (Jira Management):**
*   `search_tickets`: Uses JQL (Jira Query Language) to filter the project & business priority.
*   `read_ticket`: Extracts the full description and acceptance criteria to understand the business context.
*   `update_ticket_status`: Moves tickets through the workflow (To Do → In Progress → Done).
*   `comment_on_ticket`: Posts real-time updates to stakeholders so humans know the AI is working.

**2. Dev Expert Tools (Full Stack Execution):**
*   **Repository Control:**
    *   `clone_repository`: Securely authenticates and clones the target repo.
    *   `list_repo_files` & `read_repo_file`: Allows the agent to explore the codebase structure and read source files.
    *   `push_changes_to_github`: Commits the final fix and pushes to the remote branch.
*   **Code & Test Execution:**
    *   `create_or_update_file`: The core "writing" tool used to create reproduction scripts and apply fixes.
    *   `run_pytest`: The critical feedback loop. Allows the agent to run tests, capture `stdout`/`stderr`, and self-correct if the test fails.
*   **Cross-Functional Access:**
    *   The Dev Agent also has access to `read_ticket` and `update_ticket_status` to close the loop once the code is merged.

## 4. The "Self-Healing" TDD Loop (Innovation)
The most innovative feature of DevFlow is its adherence to **Test-Driven Development (TDD)**. In the demo, the agent:
1.  Read the bug report about "Revenue Under-reporting".
2.  Autonomously wrote a new unit test asserting the correct logic.
3.  Ran the test -> **FAILED** (Red).
4.  Modified the source code.
5.  Ran the test -> **PASSED** (Green).

This proves the agent isn't just generating text; it is understanding logic and verifying reality before pushing code.

## 5. Challenges & Future Roadmap
**Challenges (The Pivot):**
I initially attempted to implement the **Model Context Protocol (MCP)** for the GitHub integration to leverage standardized agent connectivity. However, I encountered persistent environment compatibility issues within the runtime. With time constraints looming, I made a strategic decision to pivot to a native Python Git integration. This approach proved to be highly robust and efficient, offering the agents granular control over file operations and commit history without the overhead of the full MCP stack.

**Future Improvements:**
*   **Human-in-the-Loop:** Adding a reviewer approval gate before the final git push.
*   **Parallel Agents:** Implementing a "QA Agent" that runs in parallel to write test cases while the Developer analyzes the code.

## 6. Conclusion
DevFlow represents the future of solo development—where AI doesn't just assist, but actively collaborates, triages, tests, and solves problems, allowing humans to focus on architecture rather than bug fixes.
