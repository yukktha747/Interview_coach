# Model Context Protocol (MCP)

## Q1: What is MCP?
MCP is a protocol for connecting AI applications to external tools and data sources through a standardized interface. It helps models interact with capabilities without every application inventing a completely different integration pattern.

**Rubric:** Should explain standardized tool/data integration.

---

## Q2: Why is MCP useful?
It can make tool integrations reusable across compatible AI clients and servers. Instead of tightly coupling every model application to every tool, MCP provides a common protocol layer.

**Rubric:** Should connect MCP to interoperability and reduced integration coupling.

---

## Q3: What can an MCP server expose?
An MCP server can expose capabilities such as tools, resources, and prompts depending on the implementation.

**Rubric:** Should understand that MCP is broader than a single function call.

---

## Q4: What is an MCP tool?
An MCP tool represents an action that an AI application can invoke, such as querying a service, running an operation, or retrieving information.

**Rubric:** Should distinguish an action from static context.

---

## Q5: What security concerns matter?
Tool permissions, authentication, authorization, input validation, secret handling, and preventing an untrusted model-generated request from performing unintended actions are critical.

**Rubric:** Should mention least privilege and validation.
