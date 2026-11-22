# Docker-first Project Rule

**Status:** Active. Applies to all runnable projects in this repository, including new projects and projects updated later.

## Required behavior

- The default way to run or test a project is **Docker**. Host prerequisites should normally be Docker only.
- Provide a project-scoped `Dockerfile` with all runtime dependencies and a clear, reproducible build.
- Put a copy-ready `docker run` command near the top of each project's `<short-name>/README.md`. Include required port, file mount, and environment options.
- Use `docker run --rm` for single-container tools and `docker compose` only for genuinely multi-container applications.
- Run tests and development commands inside the image; do not require host `python`, `pip`, `venv`, `npm`, `java`, or other project runtimes.
- Prefer a **published versioned prebuilt image** for one-command `docker run`. If it is not published, document `docker build` followed by `docker run` and do not claim one-command availability.
- Keep containers non-root where possible. Expose only necessary ports, default web UIs to `127.0.0.1`, avoid privileged flags and mounting the Docker socket, and do not bake secrets into images.
- For tools needing cloud or Kubernetes access, use explicit read-only scoped credentials and mounts, with a clear security warning. No production changes by default.
- Preserve the project's language-specific source, dependency declarations, and tests for maintainability. Docker is the execution boundary, not a reason to hide source code.
- Documentation-only and architecture-only projects do not need an artificial container.

## Standard Docker workflow

~~~bash
# From repository root. Rebuild when dependencies or code change.
docker build -t <project>:local path/to/<project>

# Default execution: replace port and arguments to suit the project.
docker run --rm -p 127.0.0.1:<host-port>:<container-port> <project>:local
~~~

For SmartLog, see [the complete quickstart](../ai-engineering/smartlog/README.md).

## Acceptance check for any runnable project

A reviewer must be able to build, run and test the project with **Docker only** on the host. The README must not lead with host-language installation instructions.
