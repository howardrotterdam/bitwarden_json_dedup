# Bitwarden JSON export deduplicator

Repeated or failed import (from other password manager) exported data may leave
many duplicated entries in the password vault. This script is to remove
duplicated entries from unencrypted JSON export of Bitwarden password vault.

Most of the code were [created by](claude.md) free version of [Anthropic Claude 3.7
Sonnet](https://claude.ai/). This demonstrates how AI code generator can help in
daily work of a programmer by providing handy tools effortlessly.

Answers of major AI engines:

- [Antropic Claude](claude.md)
- [Deepseek](deepseek.md)
- [OpenAI ChatGPT](chatgpt.md)
- [Microsoft CoPilot](copilot.md)
- [xAI Grok](grok.md)
- [Mistra Le Chat](mistra.md)
- [Google Gemini](gemini.md)

Hopefully major [Bitwarden client apps](#bitwarden-client-apps) will provide
such deduplicate function.

## TODO

1. Add sample data of "Identity" type.
2. Add test cases.
3. Provide diff output for verification.

## References

### Similar projects

- [Bitwarden Deduplicator](https://github.com/peterbenoit/Bitwarden-Deduplicator)

- [bitwarden-dedupe](https://github.com/roelentless/bitwarden-dedupe)

### Bitwarden client apps

- [Bitwarden Client Applications](https://github.com/bitwarden/clients)
- [Goldwarden](https://github.com/quexten/goldwarden)
- [Keyguard](https://github.com/AChep/keyguard-app)
