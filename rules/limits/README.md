# Limit tables

One YAML per base grade (`S355J2.yaml` covers `S355J2+N`, `S355J2+AR`, ...).
Only numeric limit values, never copied text from standards (copyright).

`verified: false` = values entered from secondary sources, must be checked against a
licensed copy of the standard (university access) or a customer spec before eval runs.

Format:
```yaml
grade: S355J2
standard: EN 10025-2
verified: false
thickness_range_mm: [3, 16]   # band these limits apply to
chemistry:                    # % by mass, ladle analysis
  C: {max: 0.20}
mechanical:
  ReH: {min: 355}             # MPa
  Rm: {min: 470, max: 630}    # MPa
  A: {min: 22}                # %
  KV: {min: 27}               # J, test temperature in `kv_temp_c`
```
