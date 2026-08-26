#!/usr/bin/env node
/** Read stdin, canonicalize, write canonical bytes to stdout. Does not change canonicalize.mjs. */
import { canonicalize } from "../canonicalize.mjs";
import { readFileSync } from "node:fs";

const mode = process.argv[2];
const forceJson = mode === "json" ? true : mode === "text" ? false : null;
const raw = readFileSync(0);
const out = canonicalize(raw, null, forceJson);
process.stdout.write(out);
