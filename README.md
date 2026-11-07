# Proofline agent skills

This repository is the published distribution of Proofline's coding agent skills, Claude Code plugin, Gemini CLI extension, and Antigravity plugin. These integrations let a coding agent review changes with Proofline, follow a repository's review guidance, and run Proofline setup.

The skills hold instructions and configuration only, and they treat finding text, guidance, and setup conversation text as untrusted data. Proofline's server authorizes every call they make. No skill grants access of its own, publishes, confirms setup, or records a validation.

## Install with the Proofline CLI

Claude Code, Codex, and other skill-based agents reach Proofline through the Proofline CLI's MCP bridge, `proofline mcp`.

Install the CLI on macOS or Linux and sign in:

```sh
curl -fsSL https://proofline.sh/cli | sh
proofline login --scope reviews:read --scope findings:read --scope reviews:request --scope guidance:read
```

The CLI keeps its credential in the operating system keychain. The plugin stores no token.

To run setup, an organization administrator also adds the `setup:write` permission. They must approve it in a browser where they signed in to Proofline within the last 24 hours:

```sh
proofline login --scope reviews:read --scope findings:read --scope reviews:request --scope guidance:read --scope setup:write
```

### Claude Code

Add this repository as a plugin marketplace and install the plugin:

```text
/plugin marketplace add prooflinedev/skills
/plugin install proofline@proofline
```

Restart Claude Code or reload its plugins. The plugin starts `proofline mcp` against `https://proofline.sh`, or against `PROOFLINE_BASE_URL` when it is set. Claude Code asks before each tool call that writes, such as a setup answer.

### Codex and other agents

Connect the agent to Proofline first:

```sh
proofline agent install codex
```

The CLI also configures Cursor, Gemini CLI, and Kiro. Then copy the skills into the agent's skill directory. For Codex:

```sh
git clone https://github.com/prooflinedev/skills.git
mkdir -p ~/.codex/skills
cp -R skills/plugins/proofline/skills/* ~/.codex/skills/
```

The `allowed-tools` lines in the skills apply to Claude Code only. Other agents ask for tool approval in their own way.

## Install with the hosted MCP server

The Gemini CLI extension and Antigravity plugin connect directly to Proofline's hosted MCP server at `https://proofline.sh/mcp` through OAuth. They need no Proofline CLI, copied token, or client secret. Both integrations add the hosted tools only and do not install the Claude Code skills or local-review command.

During browser authentication, choose an organization and the permissions needed for your task. Setup requires an organization administrator and a recent browser sign-in. Cloud access and configuration changes still require separate browser approval in Proofline.

### Gemini CLI extension

Install the extension from this repository:

```sh
gemini extensions install https://github.com/prooflinedev/skills
```

Restart Gemini CLI, then run `/mcp auth proofline` and approve access in your browser.

An existing `proofline` server in Gemini CLI settings takes precedence over the extension. Use `/mcp list` to check which connection is active.

### Antigravity plugin

Install the plugin, then open Antigravity:

```sh
agy plugin install https://github.com/prooflinedev/skills
agy
```

Open `/mcp` and authenticate `proofline_proofline` in your browser.

Antigravity asks before MCP calls. An authenticated server does not by itself approve tool execution. In headless runs, grant only the tools your task needs through Antigravity's per-tool permissions.

## Skills

- `proofline-review`: reviews the checkout's local changes before a push and presents findings by severity. When local review is unavailable, it reads the findings of the newest review of `HEAD`. In Claude Code, it also runs as `/proofline:review`.
- `proofline-guidance`: reads the repository's review guidance before a large edit.
- `proofline-fix-findings`: fixes a pull request's open findings, checks each fix locally with `proofline review --verify`, and after the push asks Proofline to re-verify them. It reports a finding fixed only when Proofline's re-verification says so, and it stops when Proofline refuses a request at its cap.
- `proofline-onboarding`: sets up Proofline for an organization. It reads setup status and blockers, asks Proofline's setup questions with the agent's own question tool, and sends the answers. It uses the same instructions as the setup assistant in the Proofline console.

## Contributing

The skill bundles and host manifests in this distribution are generated. We welcome pull requests for the hand-written files: this README, the instructions in `plugins/proofline/commands/review.md`, and repository maintenance files under `.github/`.

Report defects or suggest workflow changes in [issues](https://github.com/prooflinedev/skills/issues). Changes to a command's permissions or a generated skill also start with an issue.

## Documentation

- [Coding agents](https://proofline.sh/docs/coding-agents/)
- [Set up Proofline from a coding agent](https://proofline.sh/help/agent-setup/)

## License

Apache-2.0. See [LICENSE](LICENSE).
