# Android Dojo Toolkit

**A safety-first Android diagnostic, recovery, firmware, partition, and image workbench for learning, repair, and responsible device experimentation.**

> **Respect the device. Study the system. Repair with evidence.**

Android Dojo Toolkit is the workbench for [Android Dojo](https://github.com/mythologyprospector-hub/android-dojo): a unified toolkit for people who want to understand Android deeply without treating a real phone as disposable laboratory equipment.

This is **not another ADB/Fastboot wrapper**.

It is intended to become a serious, instructor-like diagnostic and repair environment that can move from ordinary Android debugging all the way down to partitions, boot images, super partitions, firmware artifacts, bootloader/download modes, and vendor-specific low-level protocols—while putting safety, evidence, and explanation ahead of execution.

---

## Why This Exists

A lot of Android tooling follows the same basic pattern:

```text
find a command
find some firmware
run the command
hope the firmware is right
flash it
pray
repeat
```

That is a poor way to learn.

It is also a remarkably effective way to turn an educational experiment into a dead phone.

Android Dojo Toolkit exists to change that relationship.

The goal is not to make dangerous operations impossible. The goal is to make **blind operations impossible**.

Before the toolkit writes something important, it should know what the device is, what the artifact is, why the operation is appropriate, what can go wrong, how to recover, and how to verify the result.

The software should behave less like a command launcher and more like a knowledgeable instructor standing beside the student.

---

## The Core Idea

The toolkit follows a simple progression:

```text
DISCOVER
   ↓
IDENTIFY
   ↓
INSPECT
   ↓
DIAGNOSE
   ↓
EXPLAIN
   ↓
BACKUP
   ↓
PLAN
   ↓
DRY RUN
   ↓
VERIFY
   ↓
EXECUTE
   ↓
VERIFY AGAIN
   ↓
REPORT
```

The important word is **before**.

A destructive operation should be the end of an evidence-driven process, not the beginning of one.

---

## What This Should Become

Android Dojo Toolkit is envisioned as a unified workbench capable of handling the layers of Android repair and investigation that are normally scattered across dozens of utilities, scripts, vendor tools, forum posts, and undocumented workflows.

### Device discovery and diagnosis

- Identify connected devices and transports.
- Determine exact model and variant where possible.
- Identify SoC, architecture, Android generation, build information, and boot state.
- Detect ADB, Fastboot, recovery, bootloader, download, and other supported modes.
- Inspect available capabilities before presenting operations.
- Collect logs and diagnostic evidence.
- Produce a device dossier and diagnostic report.

### Partitions and storage

- Inspect partition tables and layouts.
- Understand A/B slots and boot-critical partitions.
- Inspect logical partitions inside dynamic/super partitions.
- Work with sparse images.
- Identify filesystem types and relevant metadata.
- Compare expected and observed partition information.
- Back up and restore where the device and transport safely permit it.

### Boot image workbench

Boot images should be a first-class subsystem, not an afterthought.

The toolkit should eventually support safe workflows around:

- boot images
- vendor boot images
- init/ramdisk contents
- device trees and DTBO
- kernel artifacts
- vbmeta and AVB metadata
- unpacking and inspection
- rebuilding
- signing/verification workflows where legitimately supported
- image comparison
- provenance and hashing
- preflight compatibility checks

### Super partition workbench

Dynamic partitions deserve the same treatment.

The toolkit should provide an understandable model of:

- `super`
- logical partitions
- groups
- extents
- metadata
- sparse representations
- extraction
- inspection
- reconstruction
- validation

The objective is to make the structure understandable before anything is changed.

### Firmware

Firmware handling should be evidence-driven rather than filename-driven.

The toolkit should be able to reason about artifacts such as:

- complete firmware packages
- OTA payloads
- partition images
- boot-critical images
- vendor/system/product artifacts
- vendor-specific package formats
- hashes and metadata
- firmware/build relationships

A file named `boot.img` is not automatically the right `boot.img`.

### Low-level device work

The project is intended to provide a common architecture for documented and responsibly implemented low-level workflows, including vendor/platform-specific mechanisms where appropriate.

Areas of interest include, among others:

- MediaTek
- Qualcomm
- Rockchip
- Allwinner/sunxi
- Samsung download/firmware workflows
- USB device modes
- bootloader protocols
- recovery protocols
- partition access
- device-tree and platform artifacts

Existing projects and utilities are valuable prior art. The toolkit should learn from them, integrate proven techniques where licensing and safety permit, and normalize them behind a coherent device model rather than becoming a collection of unrelated scripts.

---

## Safety Is Architecture

Safety is not a warning printed above a shell command.

Every operation that can affect a device should be able to describe itself before execution.

Conceptually:

```text
Operation
├── target
├── prerequisites
├── evidence
├── compatibility requirements
├── risk level
├── affected artifacts
├── reversible?
├── backup requirements
├── dry-run capability
├── verification procedure
├── recovery procedure
└── execution
```

### Hard principles

**Never guess device identity.**

If the toolkit cannot establish what it is talking to, it should not perform a device-changing operation.

**Read before write.**

Inspection, discovery, and evidence collection should be the normal starting point.

**Verify before flash.**

Device identity, artifact identity, format, architecture, partition expectations, firmware generation, and other applicable compatibility information should be checked before writing.

**Back up before destructive operations.**

Where technically possible, establish a recovery path before modifying anything important.

**Explain before execute.**

The user should understand what will happen, what could go wrong, and how recovery works.

**Prefer reversible operations.**

If something can be inspected, extracted, staged, compared, or simulated before writing it, do that first.

**Fail closed on dangerous ambiguity.**

A safety check that cannot establish compatibility should stop the operation rather than turn uncertainty into a confirmation dialog.

**Verify after writing.**

Successful transmission is not the same thing as successful repair.

**Keep an audit trail.**

Important operations should record what was attempted, what evidence supported it, what artifacts were involved, and what the result was.

---

## Risk Is Not One Thing

The toolkit should distinguish at least three broad classes of work:

### Read-only

Inspection and evidence collection with no intended device mutation.

Examples:

- identify device
- inspect partitions
- collect logs
- inspect an image
- calculate hashes
- parse metadata
- generate a report

### Reversible or recoverable

Operations that can be safely undone or restored when appropriate safeguards exist.

Examples may include:

- creating backups
- extracting artifacts
- controlled configuration changes
- staging an image without writing it

### Destructive / boot-critical

Operations capable of causing data loss, boot failure, or persistent device-state changes.

Examples include:

- erasing partitions
- flashing boot-critical images
- changing partition layouts
- unlocking or changing bootloader state
- modifying AVB-related artifacts
- writing vendor-specific firmware

These operations require substantially stronger preflight checks and explicit user authorization.

Some situations should not offer a normal **Proceed** path at all.

---

## The Toolkit Must Be Honest

There will be devices we cannot safely identify.

There will be protocols we do not understand.

There will be firmware we cannot verify.

There will be repairs that cannot be performed without vendor-specific knowledge or hardware.

The correct response is:

> **I don't know yet.**

Not:

> **This command probably works.**

Honest failure is a feature.

---

## No Exploitation Toolkit

This project is intended for legitimate diagnostics, education, repair, recovery, research, and device ownership workflows.

It is **not** intended to provide:

- exploitation frameworks
- credential theft
- unauthorized access
- covert persistence
- destructive malware
- bypasses intended to defeat authorization or security controls
- unauthorized extraction of another person's private data
- instructions for compromising devices that the operator is not authorized to work on

Low-level Android knowledge is not inherently malicious. Understanding boot chains, partitions, protocols, firmware formats, and device internals is necessary for legitimate repair and education.

The boundary is **what the capability is for and how it is used**.

---

## Designed for Students

Android Dojo Toolkit should be useful to someone who has never worked below the Android settings screen and still remain powerful enough for experienced tinkerers.

A beginner should be able to ask:

> **What am I looking at?**

and receive an explanation.

An experienced user should be able to ask:

> **What does the toolkit know about this device?**

and receive evidence rather than a vague answer.

The same underlying model should serve both.

### Explain mode

Operations should be able to explain:

- what they are doing
- why the operation was proposed
- what evidence supports it
- what assumptions are being made
- what could fail
- what recovery options exist
- what the student should learn from the operation

The toolkit should teach without requiring the user to gamble a phone to discover the lesson.

---

## Android Dojo + Android Dojo Toolkit

[Android Dojo](https://github.com/mythologyprospector-hub/android-dojo) is the classroom.

**Android Dojo Toolkit is the workbench.**

The two projects should reinforce one another without becoming the same project.

The Dojo explains concepts such as:

- Android boot architecture
- partitions
- ADB and Fastboot
- recovery
- boot images
- dynamic partitions
- AVB
- kernels
- firmware
- troubleshooting

The toolkit lets the student safely observe those concepts on real devices and real artifacts.

Eventually, a toolkit diagnostic or safety refusal may be able to point a learner toward the relevant lesson.

---

## Architecture Direction

The project is intended to grow around a canonical device model rather than a pile of commands.

A future high-level architecture is expected to include areas such as:

```text
android-dojo-toolkit/
├── core/          # device model, capabilities, operations, safety
├── discovery/     # device identification and evidence collection
├── transport/     # USB, ADB, Fastboot, recovery, vendor transports
├── protocols/     # platform/vendor-specific implementations
├── images/        # boot, sparse, super, AVB, filesystem artifacts
├── firmware/      # packages, payloads, provenance, verification
├── partitions/    # partition maps and logical partition handling
├── diagnostics/   # logs, health, boot failures, evidence
├── repair/        # guarded repair operations
├── verification/  # preflight and post-operation verification
├── reporting/     # device dossiers, reports, audit records
├── cli/           # human-facing command interface
└── tests/         # safety, compatibility, parser, and integration tests
```

This is a direction, not a promise that the initial implementation will use exactly this tree.

The architecture will be established deliberately as the project develops.

---

## One Device Model

The central concept is the **device dossier**.

It should eventually provide one coherent representation of everything the toolkit knows about a device:

```text
Device Dossier
├── identity
│   ├── manufacturer
│   ├── model
│   ├── variant
│   ├── serial / identifiers
│   └── product information
├── platform
│   ├── SoC
│   ├── architecture
│   └── platform family
├── software
│   ├── Android version
│   ├── build fingerprint
│   ├── firmware generation
│   └── security state
├── boot
│   ├── current mode
│   ├── bootloader state
│   ├── active slot
│   └── AVB information
├── storage
│   ├── physical partitions
│   ├── logical partitions
│   ├── super metadata
│   └── filesystem information
├── transport
│   ├── USB
│   ├── ADB
│   ├── Fastboot
│   └── vendor-specific modes
├── capabilities
├── evidence
├── known artifacts
├── risk state
└── recovery options
```

The purpose is to stop every subsystem from independently making its own assumptions about the same phone.

**One device. One model. One evidence trail.**

---

## Integration Philosophy

The project should not reinvent good tools merely because they already exist.

Existing open-source utilities and documented techniques may be used, integrated, adapted, or wrapped when their licenses, technical constraints, and project safety requirements permit.

Likely areas of integration include tooling for:

- ADB / Fastboot
- Android Verified Boot
- dynamic partitions
- boot image formats
- sparse images
- OTA/payload formats
- filesystem images
- MediaTek devices
- Qualcomm devices
- Rockchip devices
- Allwinner/sunxi devices
- Samsung firmware
- device-tree artifacts
- firmware metadata

The important architectural rule is:

> **Vendor-specific complexity belongs behind a common capability model.**

The user should not have to understand seventeen unrelated command-line programs just to answer the question, “What is wrong with my phone?”

---

## Communications and Organs Compatibility

Where this toolkit participates in the broader Organs architecture, it should use the established communication model rather than creating another competing bus.

The compatibility target includes:

- the shared Organ HTTP surface
- Registry-based service discovery
- correlation IDs
- the established Communications BUS
- shared error conventions
- telemetry that remains separate from safety/risk decisions
- explicit executive approval for operations requiring it

The toolkit's internal modules should remain understandable and independently testable; Organs integration should provide the communication boundary rather than dictate every internal implementation detail.

---

## Development Principles

### Safety before convenience

A few extra seconds of verification are preferable to an unrecoverable mistake.

### Evidence before interpretation

Collect what the device actually says before deciding what it means.

### Explicit over magical

The toolkit should expose important assumptions instead of hiding them.

### Reproducible over clever

A repair procedure should be explainable and repeatable.

### Small trusted core

Safety-critical decisions should live in a small, well-tested core rather than being scattered throughout vendor plugins.

### Plugins for platform diversity

Device and vendor differences should be isolated behind capability/provider boundaries where practical.

### Test the guardrails

Safety behavior is functionality. It needs tests just as much as parsers and transports do.

### Never make the phone the test fixture

Whenever possible, protocol parsing, image manipulation, compatibility checks, and safety logic should be testable without a physical device.

---

## Project Status

**Early architecture / foundation phase.**

The repository is intentionally starting small.

The first goal is not to collect every Android tool ever written. The first goal is to establish a trustworthy spine:

1. canonical device model
2. evidence model
3. capability model
4. operation model
5. safety/preflight engine
6. transport abstraction
7. verification model
8. reporting/audit trail
9. test harness
10. integrations built on top of that foundation

A large toolbox without a coherent safety model is just a larger pile of commands.

---

## License

MIT License.

See [`LICENSE`](LICENSE) for the full license text.

---

## Disclaimer

Android devices differ substantially by manufacturer, model, region, carrier, SoC, firmware generation, bootloader configuration, and hardware revision.

No software can guarantee recovery of every device or every failure state.

This project aims to reduce avoidable mistakes through identification, verification, backups, explanations, guarded execution, and honest reporting. Users remain responsible for ensuring they are authorized to operate on the devices and data involved.

---

## The Standard

A student should be able to hand this toolkit an unfamiliar Android device and ask:

> **“What is this, what condition is it in, what can I safely do with it, and why?”**

The toolkit's job is to answer those questions **before** asking the student to press the button.

**Respect the device. Study the system. Repair with evidence.**
