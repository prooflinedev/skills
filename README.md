# Proofline agent skills

Skills and a Claude Code plugin that let a coding agent review changes with
Proofline, follow a repository's review guidance and run Proofline setup.
The skills hold instructions and configuration only. Proofline's server
authorizes every call they make, so a skill grants no access of its own.

This repository is generated from Proofline's source and syncs itself from
proofline.sh every hour. Report problems at
<https://github.com/prooflinedev/skills/issues>; changes made here directly are
replaced by the next sync.

## Skills

- `proofline-review`: reviews the checkout's local changes before a push and
  presents findings by severity. When local review is unavailable, it reads the
  findings of the newest review of `HEAD`. In Claude Code it also runs as
  `/proofline:review`.
- `proofline-guidance`: reads the repository's review guidance before a large
  edit.
- `proofline-fix-findings`: fixes a pull request's open findings, checks each fix
  locally with `proofline review --verify`, and after the push asks Proofline to
  re-verify them. It reports a finding fixed only when Proofline's re-verification
  says so, and stops when Proofline refuses a request at its cap.
- `proofline-onboarding`: sets up Proofline for an organization. It reads setup
  status and blockers, asks Proofline's setup questions with the agent's own
  question tool, and sends the answers. It uses the same instructions as the setup
  assistant in the Proofline console.

The skills treat finding text, guidance and setup conversation text as untrusted
data. None of them grants access, publishes, confirms setup or records a
validation.

## Before you start

The skills reach Proofline through the Proofline CLI's MCP bridge, `proofline mcp`.
Install the CLI on macOS or Linux and sign in:

```sh
curl -fsSL https://proofline.sh/cli | sh
proofline login --scope reviews:read --scope findings:read --scope reviews:request --scope guidance:read
```

The CLI keeps its credential in the operating system keychain. The plugin stores
no token.

To run setup, an organization administrator also adds the `setup:write`
permission, approved in a browser where they signed in to Proofline within the
last 24 hours:

```sh
proofline login --scope reviews:read --scope findings:read --scope reviews:request --scope guidance:read --scope setup:write
```

## Claude Code

Add this repository as a plugin marketplace and install the plugin:

```text
/plugin marketplace add prooflinedev/skills
/plugin install proofline@proofline
```

Restart Claude Code or reload its plugins. The plugin starts `proofline mcp`
against `https://proofline.sh`, or against `PROOFLINE_BASE_URL` when it is set.
Claude Code asks before each tool call that writes, such as a setup answer.

## Codex and other agents

Connect the agent to Proofline first:

```sh
proofline agent install codex
```

The CLI also configures Cursor, Gemini CLI and Kiro. Then copy the skills into the
agent's skill directory. For Codex:

```sh
git clone https://github.com/prooflinedev/skills.git
mkdir -p ~/.codex/skills
cp -R skills/plugins/proofline/skills/* ~/.codex/skills/
```

The `allowed-tools` lines in the skills apply to Claude Code only; other agents
ask for tool approval in their own way.

## Documentation

- [Coding agents](https://proofline.sh/docs/coding-agents/)
- [Set up Proofline from a coding agent](https://proofline.sh/help/agent-setup/)

## License

Apache-2.0. See [LICENSE](LICENSE).
